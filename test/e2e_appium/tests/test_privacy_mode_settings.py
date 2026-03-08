"""Tests for Privacy Mode settings toggle and persistence.

Coverage gap: docs/FURPS/privacy-mode.md
- F-PM-01: Privacy Mode toggle disables all third-party integrations
- F-PM-02: Toggle accessible from Settings at any time
- R-PM-01: Settings persist across sessions and updates
- R-PM-02: No state leakage after toggling

Related Linear issues: OXI-9, OXI-10
"""

import pytest

from pages.app import App
from pages.settings.settings_page import SettingsPage
from utils.multi_device_helpers import StepMixin


@pytest.mark.privacy
@pytest.mark.smoke
class TestPrivacyModeSettings(StepMixin):
    """Privacy Mode toggle and persistence from Settings.

    Verifies that a user can enable/disable Privacy Mode from Settings
    and that the state persists across app restarts.
    """

    UI_TIMEOUT = 15

    async def test_privacy_mode_toggle_and_persistence(self) -> None:
        """Enable Privacy Mode from Settings, restart, verify persistence.

        FURPS ref: privacy-mode.md — Functionality items 1-2, Reliability items 1-2.

        Flow:
        1. Navigate to Settings
        2. Locate Privacy Mode toggle
        3. Enable Privacy Mode
        4. Verify toggle state is enabled
        5. Restart app
        6. Navigate to Settings
        7. Verify Privacy Mode is still enabled
        8. Disable Privacy Mode
        9. Verify toggle state is disabled
        """
        app = App(self.device.driver)

        async with self.step(self.device, "Navigate to Settings"):
            assert app.click_settings_button(), "Failed to open settings"
            settings_page = SettingsPage(self.device.driver)
            assert settings_page.is_loaded(timeout=self.UI_TIMEOUT), (
                "Settings page did not load"
            )

        async with self.step(self.device, "Open Privacy settings"):
            # TODO: Implement when PrivacySettingsPage page object is available
            # privacy_settings = settings_page.open_privacy_settings(timeout=self.UI_TIMEOUT)
            # assert privacy_settings is not None, "Failed to open privacy settings"
            pytest.skip("Privacy settings page object not yet implemented")

        async with self.step(self.device, "Enable Privacy Mode"):
            # TODO: privacy_settings.enable_privacy_mode()
            # assert privacy_settings.is_privacy_mode_enabled(), (
            #     "Privacy Mode toggle should be ON after enabling"
            # )
            pass

        async with self.step(self.device, "Restart app and verify persistence"):
            # TODO: Restart and re-navigate to verify toggle state persists
            # assert base.restart_app(), "Failed to restart app"
            # Re-navigate to Settings → Privacy
            # assert privacy_settings.is_privacy_mode_enabled(), (
            #     "Privacy Mode should persist after app restart (R-PM-01)"
            # )
            pass

        async with self.step(self.device, "Disable Privacy Mode and verify"):
            # TODO: privacy_settings.disable_privacy_mode()
            # assert not privacy_settings.is_privacy_mode_enabled(), (
            #     "Privacy Mode toggle should be OFF after disabling"
            # )
            pass

    async def test_privacy_mode_disables_third_party_features(self) -> None:
        """Verify third-party features are unavailable when Privacy Mode is ON.

        FURPS ref: privacy-mode.md — Functionality items 3-6.
        Covers: RPC providers, WalletConnect, GIF search, swap providers.

        Flow:
        1. Enable Privacy Mode from Settings
        2. Navigate to Wallet — verify swap/WalletConnect unavailable
        3. Navigate to Chat — verify GIF search unavailable
        4. Verify contextual messages for disabled features
        """
        app = App(self.device.driver)

        async with self.step(self.device, "Enable Privacy Mode"):
            assert app.click_settings_button(), "Failed to open settings"
            # TODO: Enable privacy mode via settings
            pytest.skip("Privacy settings page object not yet implemented")

        async with self.step(self.device, "Verify wallet features disabled"):
            assert app.click_wallet_button(), "Failed to navigate to wallet"
            # TODO: Verify swap provider UI is disabled or shows privacy message
            # TODO: Verify WalletConnect pairing is disabled
            pass

        async with self.step(self.device, "Verify chat features disabled"):
            assert app.click_messages_button(), "Failed to navigate to messages"
            # TODO: Verify GIF search button is hidden or disabled
            # TODO: Verify contextual message shown for disabled features
            pass
