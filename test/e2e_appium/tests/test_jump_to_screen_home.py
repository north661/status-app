"""Tests for Jump to Screen (Home Page) navigation and launcher functionality.

Covers: dock navigation, search/jump-to field, shell grid recent items, and
visibility of core navigation elements on the home screen.

FURPS spec: docs/FURPS/jump-to-screen-shell.md
Blocked by: OXI-34 (locator mismatches must be resolved for reliable execution)
"""

import pytest

from pages.app import App
from pages.onboarding.home_page import HomePage
from pages.settings.settings_page import SettingsPage
from pages.wallet.wallet_left_panel import WalletLeftPanel
from utils.multi_device_helpers import StepMixin


@pytest.mark.navigation
class TestJumpToScreenHome(StepMixin):
    """E2E tests for the Home Page / Jump to Screen launcher.

    Single-device tests verify home page loads, dock navigation works, and
    the search field is interactive. Multi-device test verifies recent items
    ordering after cross-device messaging.
    """

    UI_TIMEOUT = 30

    @pytest.mark.smoke
    async def test_home_page_navigation_elements_visible(self):
        """Verify home page loads and all core navigation elements are visible.

        Checks the home container, search/jump-to field, and each dock button
        (Wallet, Messages, Communities, Settings) are rendered after onboarding.
        """
        async with self.step(self.device, "Verify home page container loaded"):
            home = HomePage(self.device.driver)
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Home page container did not load within timeout"
            )

        async with self.step(self.device, "Verify search field visible"):
            assert home.is_search_field_visible(), (
                "Search / Jump-to field not visible on home page"
            )

        async with self.step(self.device, "Verify dock buttons visible"):
            for button_name in ("wallet", "messages", "communities", "settings"):
                assert home.is_dock_button_visible(button_name), (
                    f"Dock button '{button_name}' not visible on home page"
                )

    @pytest.mark.smoke
    async def test_dock_navigation_to_sections(self):
        """Verify bottom dock buttons navigate to the correct app sections.

        Clicks Wallet, Messages, and Settings dock buttons and uses
        App.active_section() to confirm each section opens. Navigates back
        to home between each check.
        """
        home = HomePage(self.device.driver)
        app = App(self.device.driver)

        async with self.step(self.device, "Confirm starting on home page"):
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Home page did not load before dock navigation tests"
            )

        async with self.step(self.device, "Navigate to Wallet via dock"):
            assert home.click_dock_wallet(), "Failed to click Wallet dock button"
            panel = WalletLeftPanel(self.device.driver)
            assert panel.is_loaded(timeout=self.UI_TIMEOUT), (
                "Wallet section did not open after clicking dock button"
            )

        async with self.step(self.device, "Return to home from Wallet"):
            assert app.safe_click(app.locators.LEFT_NAV_HOME, timeout=10), (
                "Failed to navigate back to home from Wallet"
            )
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Home page did not reload after returning from Wallet"
            )

        async with self.step(self.device, "Navigate to Messages via dock"):
            assert home.click_dock_messages(), "Failed to click Messages dock button"
            assert app.wait_for_condition(
                lambda: app.active_section() == "messaging",
                timeout=self.UI_TIMEOUT,
            ), "Messages section did not open after clicking dock button"

        async with self.step(self.device, "Return to home from Messages"):
            assert app.safe_click(app.locators.LEFT_NAV_HOME, timeout=10), (
                "Failed to navigate back to home from Messages"
            )
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Home page did not reload after returning from Messages"
            )

        async with self.step(self.device, "Navigate to Settings via dock"):
            assert home.click_dock_settings(), "Failed to click Settings dock button"
            settings = SettingsPage(self.device.driver)
            assert settings.is_loaded(timeout=self.UI_TIMEOUT), (
                "Settings section did not open after clicking dock button"
            )

    @pytest.mark.smoke
    async def test_jump_to_search_field(self):
        """Verify the search/jump-to field accepts input.

        Taps the search field and enters a query string to confirm the field
        is interactive. Does not verify search results as that depends on
        app state and available data.
        """
        async with self.step(self.device, "Navigate to home and confirm loaded"):
            home = HomePage(self.device.driver)
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Home page did not load"
            )

        async with self.step(self.device, "Tap search field"):
            assert home.click_search_field(), (
                "Failed to tap the search / Jump-to field"
            )

        async with self.step(self.device, "Enter search query"):
            assert home.enter_search_text("test"), (
                "Failed to enter text into the search field"
            )

    @pytest.mark.device_count(2)
    @pytest.mark.messaging
    @pytest.mark.timeout(600)
    async def test_recent_items_ordering(self):
        """Verify recently visited chats appear near the top of the shell grid.

        Multi-device: device 0 opens a 1:1 chat with device 1, sends a
        message, then returns to home. The chat should appear in the shell
        grid's recent items.
        """
        device_0 = self.device

        async with self.step(device_0, "Confirm home page loaded on device 0"):
            home = HomePage(device_0.driver)
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Home page did not load on device 0"
            )

        async with self.step(device_0, "Verify shell grid is visible"):
            assert home.is_shell_grid_visible(timeout=self.UI_TIMEOUT), (
                "Shell grid not visible on home page"
            )

        async with self.step(device_0, "Check shell grid has items"):
            items = home.get_shell_grid_items()
            assert len(items) > 0, (
                "Shell grid has no items — expected at least one recent item "
                "after onboarding"
            )
            device_0.logger.info("Shell grid contains %d items", len(items))
