"""
Tests for LambdaTest provider implementation.

Covers provider instantiation, credential validation, capability building,
session status reporting (executor and REST API), configuration loading,
provider registry, device matrix, and template resolution.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.environment import (
    ConfigurationError,
    DeviceConfig,
    EnvironmentConfig,
    ProviderConfig,
)
from core.providers import create_provider
from core.providers.lambdatest import LambdaTestProvider


def _make_env_config(
    *,
    provider_name="lambdatest",
    username="test_user",
    access_key="test_key",
    app_url="lt://APP12345",
    hub_url=None,
    project_name="Status E2E Appium",
    extra_options=None,
    devices=None,
    device_defaults=None,
):
    """Build a minimal EnvironmentConfig for LambdaTest tests."""
    options = {
        "auth": {"username": username, "access_key": access_key},
        "app": {"app_url_template": app_url},
        "project_name": project_name,
    }
    if hub_url:
        options["hub_url"] = hub_url
    if extra_options:
        options.update(extra_options)

    if devices is None:
        devices = {
            "galaxy_tab_s9_android_14": DeviceConfig(
                id="galaxy_tab_s9_android_14",
                display_name="Galaxy Tab S9 - Android 14",
                tags=["android", "tablet", "cloud"],
                capabilities={
                    "platformName": "android",
                    "platformVersion": "14",
                    "deviceName": "Galaxy Tab S9",
                },
            )
        }

    return EnvironmentConfig(
        name="lambdatest",
        description="LambdaTest test config",
        provider=ProviderConfig(name=provider_name, options=options),
        execution={"concurrency": {"max_sessions": 5, "per_device_limit": 2}},
        timeouts={"default": 30},
        logging={"level": "INFO"},
        directories={"reports": "reports"},
        device_defaults=device_defaults or {"capabilities": {"platformName": "android"}},
        devices=devices,
        default_device_id="galaxy_tab_s9_android_14",
    )


class TestLambdaTestProviderInstantiation:
    """Tests for LambdaTestProvider constructor and credential handling."""

    def test_provider_initialises_with_valid_credentials(self):
        """Verify provider initialises correctly with valid credentials."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)

        assert provider.username == "test_user"
        assert provider.access_key == "test_key"
        assert provider.project_name == "Status E2E Appium"

    def test_provider_initialises_with_env_var_credentials(self, monkeypatch):
        """Verify credentials resolve from environment variables."""
        monkeypatch.setenv("LT_USERNAME", "env_user")
        monkeypatch.setenv("LT_ACCESS_KEY", "env_key")

        env_config = _make_env_config(
            username="${LT_USERNAME}", access_key="${LT_ACCESS_KEY}"
        )
        provider = LambdaTestProvider(env_config)

        assert provider.username == "env_user"
        assert provider.access_key == "env_key"

    def test_provider_raises_on_missing_username(self):
        """Verify ConfigurationError raised when username is empty."""
        env_config = _make_env_config(username="", access_key="valid_key")

        with pytest.raises(ConfigurationError, match="LT_USERNAME"):
            LambdaTestProvider(env_config)

    def test_provider_raises_on_missing_access_key(self):
        """Verify ConfigurationError raised when access key is empty."""
        env_config = _make_env_config(username="valid_user", access_key="")

        with pytest.raises(ConfigurationError, match="LT_ACCESS_KEY"):
            LambdaTestProvider(env_config)

    def test_provider_raises_on_both_credentials_missing(self):
        """Verify ConfigurationError raised when both credentials are absent."""
        env_config = _make_env_config(username="", access_key="")

        with pytest.raises(ConfigurationError, match="LambdaTest credentials"):
            LambdaTestProvider(env_config)

    def test_provider_uses_default_hub_url(self):
        """Verify default hub URL is used when not overridden."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)

        assert provider.hub_url == LambdaTestProvider.HUB_URL

    def test_provider_uses_custom_hub_url(self):
        """Verify custom hub URL overrides default."""
        custom_url = "https://custom-hub.example.com/wd/hub"
        env_config = _make_env_config(hub_url=custom_url)
        provider = LambdaTestProvider(env_config)

        assert provider.hub_url == custom_url

    def test_provider_name_property(self):
        """Verify provider name is derived from config."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)

        assert provider.name == "lambdatest"


class TestLambdaTestCapabilityBuilding:
    """Tests for build_capabilities() producing correct LambdaTest capabilities."""

    def test_capabilities_include_device_fields(self):
        """Verify merged capabilities include device platformName, version, and name."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        device = env_config.get_device()

        caps = provider.build_capabilities(device)

        assert caps["platformName"] == "android"
        assert caps["platformVersion"] == "14"
        assert caps["deviceName"] == "Galaxy Tab S9"

    def test_capabilities_include_defaults(self):
        """Verify device defaults merge into capabilities."""
        env_config = _make_env_config(
            device_defaults={
                "capabilities": {
                    "platformName": "android",
                    "automationName": "UiAutomator2",
                    "newCommandTimeout": 300,
                }
            }
        )
        provider = LambdaTestProvider(env_config)
        device = env_config.get_device()

        caps = provider.build_capabilities(device)

        assert caps.get("automationName") == "UiAutomator2"
        assert caps.get("newCommandTimeout") == 300

    def test_provider_overrides_applied(self):
        """Verify provider-specific overrides from device config are merged."""
        devices = {
            "test_device": DeviceConfig(
                id="test_device",
                capabilities={
                    "platformName": "android",
                    "platformVersion": "14",
                    "deviceName": "Pixel 8",
                },
                provider_overrides={
                    "lambdatest": {"newCommandTimeout": 600}
                },
            )
        }
        env_config = _make_env_config(devices=devices)
        env_config.default_device_id = "test_device"
        provider = LambdaTestProvider(env_config)
        device = env_config.get_device()

        caps = provider.build_capabilities(device)

        assert caps["newCommandTimeout"] == 600


class TestLambdaTestSessionStatusReporting:
    """Tests for report_session_status() executor commands."""

    def test_report_session_status_sends_executor_command(self):
        """Verify report_session_status sends correct lambdatest_executor script."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_driver = MagicMock()

        provider.report_session_status(mock_driver, "passed", "All tests passed")

        mock_driver.execute_script.assert_called_once()
        call_arg = mock_driver.execute_script.call_args[0][0]
        assert call_arg.startswith("lambdatest_executor: ")
        payload = json.loads(call_arg.replace("lambdatest_executor: ", ""))
        assert payload["action"] == "setSessionStatus"
        assert payload["arguments"]["status"] == "passed"
        assert payload["arguments"]["reason"] == "All tests passed"

    def test_report_session_status_without_reason(self):
        """Verify report_session_status works without a reason."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_driver = MagicMock()

        provider.report_session_status(mock_driver, "failed")

        call_arg = mock_driver.execute_script.call_args[0][0]
        payload = json.loads(call_arg.replace("lambdatest_executor: ", ""))
        assert payload["arguments"]["status"] == "failed"
        assert "reason" not in payload["arguments"]

    def test_report_session_status_handles_none_driver(self):
        """Verify report_session_status silently returns for None driver."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)

        # Should not raise
        provider.report_session_status(None, "passed")

    def test_report_session_status_swallows_exceptions(self):
        """Verify executor errors are silently swallowed."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_driver = MagicMock()
        mock_driver.execute_script.side_effect = Exception("Connection lost")

        # Should not raise
        provider.report_session_status(mock_driver, "failed")


class TestLambdaTestAPIStatusReporting:
    """Tests for report_session_status_via_api() REST endpoint calls."""

    @patch("core.providers.lambdatest.requests.patch")
    def test_api_reporting_calls_correct_endpoint(self, mock_patch):
        """Verify REST API call uses correct URL and payload."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_patch.return_value = MagicMock(status_code=200)

        provider.report_session_status_via_api("session_123", "passed", "OK")

        mock_patch.assert_called_once()
        call_kwargs = mock_patch.call_args
        assert "sessions/session_123" in call_kwargs[1].get("url", call_kwargs[0][0] if call_kwargs[0] else "")

        url = call_kwargs[0][0] if call_kwargs[0] else call_kwargs[1]["url"]
        assert url == f"{LambdaTestProvider.API_BASE_URL}/sessions/session_123"

    @patch("core.providers.lambdatest.requests.patch")
    def test_api_reporting_sends_correct_payload(self, mock_patch):
        """Verify REST API sends status_ind and reason in payload."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_patch.return_value = MagicMock(status_code=200)

        provider.report_session_status_via_api("sess_abc", "failed", "Assertion error")

        call_kwargs = mock_patch.call_args[1]
        assert call_kwargs["json"]["status_ind"] == "failed"
        assert call_kwargs["json"]["reason"] == "Assertion error"

    @patch("core.providers.lambdatest.requests.patch")
    def test_api_reporting_uses_basic_auth(self, mock_patch):
        """Verify REST API call authenticates with username/access_key."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_patch.return_value = MagicMock(status_code=200)

        provider.report_session_status_via_api("sess_abc", "passed")

        call_kwargs = mock_patch.call_args[1]
        assert call_kwargs["auth"] == ("test_user", "test_key")

    @patch("core.providers.lambdatest.requests.patch")
    def test_api_reporting_without_reason(self, mock_patch):
        """Verify reason field is omitted from payload when not provided."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_patch.return_value = MagicMock(status_code=200)

        provider.report_session_status_via_api("sess_abc", "passed")

        payload = mock_patch.call_args[1]["json"]
        assert "reason" not in payload

    def test_api_reporting_skips_none_session_id(self):
        """Verify REST API call is skipped when session_id is None."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)

        with patch("core.providers.lambdatest.requests.patch") as mock_patch:
            provider.report_session_status_via_api(None, "passed")
            mock_patch.assert_not_called()

    @patch("core.providers.lambdatest.requests.patch")
    def test_api_reporting_handles_network_error(self, mock_patch):
        """Verify network errors in REST API are logged but not raised."""
        import requests as req

        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_patch.side_effect = req.RequestException("Network error")

        # Should not raise
        provider.report_session_status_via_api("sess_abc", "failed")


class TestLambdaTestConfigurationLoading:
    """Tests for YAML configuration loading and merging."""

    def test_lambdatest_yaml_loads_and_merges(self):
        """Verify lambdatest.yaml loads and merges with base.yaml."""
        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)

        assert "lambdatest" in mgr.list_available_environments()

    def test_lambdatest_yaml_merges_base_timeouts(self, monkeypatch):
        """Verify base.yaml timeouts are inherited by lambdatest config."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "key")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        assert config.timeouts.get("default") == 30
        assert config.timeouts.get("element_wait") == 30

    def test_lambdatest_provider_name_is_correct(self, monkeypatch):
        """Verify loaded config has provider name 'lambdatest'."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "key")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        assert config.provider.name == "lambdatest"


class TestLambdaTestProviderRegistry:
    """Tests for provider factory returning correct provider type."""

    def test_create_provider_returns_lambdatest(self):
        """Verify create_provider() returns LambdaTestProvider for lambdatest env."""
        env_config = _make_env_config()
        provider = create_provider(env_config)

        assert isinstance(provider, LambdaTestProvider)

    def test_create_provider_error_for_unknown(self):
        """Verify create_provider() raises for unregistered provider names."""
        env_config = _make_env_config(provider_name="unknown_cloud")

        with pytest.raises(ConfigurationError, match="not registered"):
            create_provider(env_config)


class TestLambdaTestDeviceMatrix:
    """Tests for device configurations producing valid capabilities."""

    def test_device_matrix_from_yaml(self, monkeypatch):
        """Verify device matrix entries from lambdatest.yaml produce valid configs."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "key")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        assert len(config.devices) >= 1

        for device_id, device in config.devices.items():
            defaults = config.device_defaults.get("capabilities", {})
            merged = device.merged_capabilities(defaults)
            assert "platformName" in merged, f"Device {device_id} missing platformName"
            assert "deviceName" in merged, f"Device {device_id} missing deviceName"

    def test_default_device_is_configured(self, monkeypatch):
        """Verify the default device ID is valid."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "key")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        default_device = config.get_device()
        assert default_device is not None
        assert default_device.id == "galaxy_tab_s9_android_14"


class TestLambdaTestTemplateResolution:
    """Tests for environment variable template resolution in LambdaTest config."""

    def test_lt_username_template_resolves(self, monkeypatch):
        """Verify LT_USERNAME template resolves from env var."""
        monkeypatch.setenv("LT_USERNAME", "resolved_user")
        monkeypatch.setenv("LT_ACCESS_KEY", "resolved_key")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        auth = config.provider.options.get("auth", {})
        username = config.resolve_template(auth.get("username", ""))
        assert username == "resolved_user"

    def test_lt_access_key_template_resolves(self, monkeypatch):
        """Verify LT_ACCESS_KEY template resolves from env var."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "resolved_key")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        auth = config.provider.options.get("auth", {})
        access_key = config.resolve_template(auth.get("access_key", ""))
        assert access_key == "resolved_key"

    def test_app_url_template_resolves(self, monkeypatch):
        """Verify LT_APP_URL template resolves from env var."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "key")
        monkeypatch.setenv("LT_APP_URL", "lt://APP_HASH_123")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        app_cfg = config.provider.options.get("app", {})
        app_url = config.resolve_template(app_cfg.get("app_url_template", ""))
        assert app_url == "lt://APP_HASH_123"

    def test_app_url_defaults_to_empty(self, monkeypatch):
        """Verify app URL defaults to empty when LT_APP_URL is not set."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "key")
        monkeypatch.delenv("LT_APP_URL", raising=False)

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        app_cfg = config.provider.options.get("app", {})
        app_url = config.resolve_template(app_cfg.get("app_url_template", ""))
        assert app_url == ""


class TestLambdaTestEnvironmentValidation:
    """Tests for EnvironmentConfig._validate_lambdatest()."""

    def test_validation_passes_with_credentials(self, monkeypatch):
        """Verify validation passes when LambdaTest credentials are present."""
        monkeypatch.setenv("LT_USERNAME", "user")
        monkeypatch.setenv("LT_ACCESS_KEY", "key")

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)
        config = mgr.load_environment("lambdatest")

        # Should not raise
        assert config.provider.name == "lambdatest"

    def test_validation_fails_without_credentials(self, monkeypatch):
        """Verify validation fails when LambdaTest credentials are missing."""
        monkeypatch.delenv("LT_USERNAME", raising=False)
        monkeypatch.delenv("LT_ACCESS_KEY", raising=False)

        from core.config_manager import ConfigurationManager

        config_dir = Path(__file__).parent.parent / "config"
        mgr = ConfigurationManager(config_dir=config_dir)

        with pytest.raises(ConfigurationError, match="LT_USERNAME"):
            mgr.load_environment("lambdatest")


class TestLambdaTestDriverCleanup:
    """Tests for driver cleanup and lifecycle methods."""

    def test_cleanup_driver_calls_quit(self):
        """Verify cleanup_driver calls driver.quit()."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)
        mock_driver = MagicMock()

        provider.cleanup_driver(mock_driver)

        mock_driver.quit.assert_called_once()

    def test_cleanup_driver_handles_none(self):
        """Verify cleanup_driver handles None driver gracefully."""
        env_config = _make_env_config()
        provider = LambdaTestProvider(env_config)

        # Should not raise
        provider.cleanup_driver(None)
