"""Tests for Privacy Mode settings toggle."""

import pytest

from pages.app import App
from pages.settings.settings_page import SettingsPage


@pytest.mark.settings
@pytest.mark.device_count(1)
class TestPrivacyMode:

    UI_TIMEOUT = 30

    @pytest.fixture(autouse=True)
    def setup(self, onboarding):
        self.driver = onboarding.driver
        self.app = App(self.driver)

    def _open_privacy_settings(self):
        """Navigate to Settings > Privacy and return the privacy page object."""
        self.app.click_settings_button()
        settings = SettingsPage(self.driver)
        privacy = settings.open_privacy_settings()
        assert privacy is not None, "Failed to open Privacy settings"
        return privacy

    async def test_enable_privacy_mode(self):
        """Verify that privacy mode can be enabled via the third-party toggle."""
        privacy = self._open_privacy_settings()
        assert privacy.enable_privacy_mode(timeout=self.UI_TIMEOUT), (
            "Failed to enable privacy mode"
        )
        assert privacy.is_privacy_mode_enabled(timeout=self.UI_TIMEOUT), (
            "Privacy Mode enabled label not visible after enabling"
        )

    async def test_disable_privacy_mode(self):
        """Verify that privacy mode can be disabled after being enabled."""
        privacy = self._open_privacy_settings()

        assert privacy.enable_privacy_mode(timeout=self.UI_TIMEOUT), (
            "Failed to enable privacy mode (prerequisite for disable test)"
        )
        assert privacy.is_privacy_mode_enabled(timeout=self.UI_TIMEOUT), (
            "Privacy Mode not confirmed enabled before attempting disable"
        )

        assert privacy.disable_privacy_mode(timeout=self.UI_TIMEOUT), (
            "Failed to disable privacy mode"
        )
        assert privacy.is_third_party_switch_checked(), (
            "Third-party switch should be checked after disabling privacy mode"
        )

    async def test_privacy_mode_persists_after_restart(self):
        """Verify that privacy mode state survives an app restart."""
        privacy = self._open_privacy_settings()
        assert privacy.enable_privacy_mode(timeout=self.UI_TIMEOUT), (
            "Failed to enable privacy mode before restart"
        )
        assert privacy.is_privacy_mode_enabled(timeout=self.UI_TIMEOUT), (
            "Privacy Mode not confirmed enabled before restart"
        )

        assert self.app.restart_app(), "App restart failed"

        privacy_after = self._open_privacy_settings()
        assert not privacy_after.is_third_party_switch_checked(), (
            "Third-party switch should remain unchecked after restart"
        )
