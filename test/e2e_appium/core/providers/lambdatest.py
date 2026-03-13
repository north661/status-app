from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests
from appium import webdriver
from appium.options.common import AppiumOptions

from .base import Provider, SessionMetadata
from ..environment import ConfigurationError, DeviceConfig

logger = logging.getLogger(__name__)


class LambdaTestProvider(Provider):
    """Provider implementation using LambdaTest App Automation."""

    HUB_URL = "https://mobile-hub.lambdatest.com/wd/hub"
    API_BASE_URL = "https://mobile-api.lambdatest.com/mobile-automation/api/v1"

    def __init__(self, env_config):
        super().__init__(env_config)
        auth_cfg = env_config.get_provider_option("auth", {})
        self.username = env_config.resolve_template(auth_cfg.get("username", ""))
        self.access_key = env_config.resolve_template(auth_cfg.get("access_key", ""))
        if not self.username or not self.access_key:
            raise ConfigurationError(
                "LambdaTest credentials are required. Set LT_USERNAME "
                "and LT_ACCESS_KEY."
            )
        self.hub_url = env_config.get_provider_option("hub_url", self.HUB_URL)
        project_name_option = env_config.get_provider_option(
            "project_name", "Status E2E Appium"
        )
        if isinstance(project_name_option, str):
            self.project_name = env_config.resolve_template(project_name_option)
        else:
            self.project_name = project_name_option

    def create_driver(
        self,
        device: DeviceConfig,
        metadata: Optional[SessionMetadata] = None,
    ) -> webdriver.Remote:
        metadata = metadata or SessionMetadata()
        capabilities = self.build_capabilities(device, metadata)

        app_cfg = self.env_config.get_provider_option("app", {})
        app_url = self.env_config.resolve_template(
            app_cfg.get("app_url_template", "")
        )
        if app_url:
            capabilities["app"] = app_url

        lt_options = capabilities.setdefault("lt:options", {})
        self._populate_metadata(lt_options, metadata, device)

        options = AppiumOptions()
        options.load_capabilities(capabilities)

        driver = webdriver.Remote(
            command_executor=f"https://{self.username}:{self.access_key}@mobile-hub.lambdatest.com/wd/hub",
            options=options,
        )
        return driver

    def report_session_status(
        self,
        driver: webdriver.Remote,
        status: str,
        reason: Optional[str] = None,
    ) -> None:
        action = "setSessionStatus"
        arguments: Dict[str, str] = {"status": status}
        if reason:
            arguments["reason"] = reason
        command = {"action": action, "arguments": arguments}
        self._send_lambdatest_executor_command(driver, command)

    def report_session_status_via_api(
        self,
        session_id: Optional[str],
        status: str,
        reason: Optional[str] = None,
    ) -> None:
        """Report LambdaTest session status via REST API."""
        if not session_id:
            return

        url = f"{self.API_BASE_URL}/sessions/{session_id}"
        payload: Dict[str, Any] = {"status_ind": status}
        if reason:
            payload["reason"] = reason

        try:
            response = requests.patch(
                url,
                json=payload,
                auth=(self.username, self.access_key),
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.debug(
                "Failed to update LambdaTest session %s via REST API: %s",
                session_id,
                exc,
            )

    def _populate_metadata(
        self,
        lt_options: Dict[str, Any],
        metadata: SessionMetadata,
        device: DeviceConfig,
    ) -> None:
        lt_options.setdefault(
            "project", metadata.project_name or self.project_name
        )

        build_template = self.env_config.get_provider_option(
            "build_name_template", "Status E2E"
        )
        build_name = self.env_config.resolve_template(build_template)
        lt_options.setdefault("build", build_name)

        session_template = self.env_config.get_provider_option(
            "session_name_template", "${TEST_NAME:-Status Test}"
        )
        session_name = self.env_config.resolve_template(session_template)
        lt_options.setdefault("name", session_name)

        lt_options.setdefault("video", True)
        lt_options.setdefault("console", True)
        lt_options.setdefault("network", False)

        defaults = self.env_config.device_defaults.get("capabilities", {})
        merged_caps = device.merged_capabilities(defaults)
        lt_options.setdefault("platformVersion", merged_caps.get("platformVersion"))
        lt_options.setdefault("deviceName", merged_caps.get("deviceName"))

    def _send_lambdatest_executor_command(
        self, driver: Optional[webdriver.Remote], command: Dict[str, Any]
    ) -> None:
        if not driver:
            return
        try:
            import json
            driver.execute_script(
                f"lambdatest_executor: {json.dumps(command)}"
            )
        except Exception:
            return
