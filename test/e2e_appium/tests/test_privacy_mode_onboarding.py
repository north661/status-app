"""Tests for Privacy Mode integration during onboarding.

Coverage gap: docs/FURPS/privacy-mode.md
- F-PM-02: Activate Privacy Mode during onboarding
- U-PM-01: Clear information about what Privacy Mode disables
- U-PM-02: Toggle integrated in onboarding UI

Related Linear issue: OXI-11
"""

import pytest

from pages.app import App
from pages.onboarding import (
    WelcomePage,
    AnalyticsPage,
    CreateProfilePage,
    SeedPhraseInputPage,
    PasswordPage,
    SplashScreen,
)
from pages.settings.settings_page import SettingsPage
from utils.generators import generate_seed_phrase
from utils.multi_device_helpers import StepMixin


@pytest.mark.onboarding
@pytest.mark.privacy
@pytest.mark.smoke
@pytest.mark.raw_devices
class TestPrivacyModeOnboarding(StepMixin):
    """Privacy Mode activation during onboarding flow.

    Verifies that users can enable Privacy Mode during the initial
    onboarding and that the setting carries through to the full app.
    """

    UI_TIMEOUT = 30

    async def test_enable_privacy_mode_during_onboarding(self) -> None:
        """Enable Privacy Mode at the analytics/privacy step of onboarding.

        FURPS ref: privacy-mode.md — Functionality item 2, Usability items 1-2.

        Flow:
        1. Start onboarding from Welcome screen
        2. At analytics/privacy step, enable Privacy Mode toggle
        3. Verify informational text about what Privacy Mode disables
        4. Complete onboarding (seed import, password)
        5. Navigate to Settings → Privacy
        6. Verify Privacy Mode toggle is enabled
        """
        driver = self.device.driver
        seed_phrase = generate_seed_phrase()
        password = "TestPassword123!"

        async with self.step(self.device, "Complete welcome screen"):
            welcome = WelcomePage(driver)
            assert welcome.is_screen_displayed(timeout=self.UI_TIMEOUT), (
                "Welcome screen should be visible"
            )
            assert welcome.click_create_profile(), "Failed to click Create profile"

        async with self.step(self.device, "Enable Privacy Mode at analytics step"):
            analytics = AnalyticsPage(driver)
            assert analytics.is_screen_displayed(), (
                "Analytics screen should be visible"
            )
            # TODO: Locate and enable Privacy Mode toggle on this screen
            # The toggle may be on this page or a dedicated privacy step
            # assert analytics.enable_privacy_mode(), (
            #     "Failed to enable Privacy Mode during onboarding"
            # )
            pytest.skip(
                "Privacy Mode onboarding toggle not yet available in page objects"
            )
            assert analytics.skip_analytics_sharing(), "Failed to proceed past analytics"

        async with self.step(self.device, "Complete seed phrase import"):
            create = CreateProfilePage(driver)
            assert create.is_screen_displayed(), (
                "Create profile screen should be visible"
            )
            assert create.click_use_recovery_phrase(), (
                "Failed to click Use a recovery phrase"
            )
            seed_page = SeedPhraseInputPage(driver, flow_type="create")
            assert seed_page.is_screen_displayed(), (
                "Seed phrase input should be visible"
            )
            assert seed_page.import_seed_phrase(seed_phrase), (
                "Failed to import seed phrase"
            )

        async with self.step(self.device, "Create password and finish onboarding"):
            password_page = PasswordPage(driver)
            assert password_page.is_screen_displayed(), (
                "Password screen should be visible"
            )
            assert password_page.create_password(password), "Failed to create password"
            splash = SplashScreen(driver)
            assert splash.wait_for_loading_completion(timeout=60), (
                "App did not finish loading"
            )

        async with self.step(self.device, "Verify Privacy Mode enabled in Settings"):
            app = App(driver)
            assert app.click_settings_button(), "Failed to open settings"
            settings_page = SettingsPage(driver)
            assert settings_page.is_loaded(timeout=self.UI_TIMEOUT), (
                "Settings page did not load"
            )
            # TODO: Navigate to privacy settings and verify toggle is ON
            # privacy_settings = settings_page.open_privacy_settings()
            # assert privacy_settings.is_privacy_mode_enabled(), (
            #     "Privacy Mode should be enabled after onboarding opt-in"
            # )
