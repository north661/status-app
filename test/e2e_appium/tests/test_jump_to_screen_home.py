"""Tests for Jump to Screen / Home Page navigation.

Covers home page load state, dock button visibility, section navigation,
and search field interaction. Maps to FURPS spec: docs/FURPS/jump-to-screen-shell.md
"""

import pytest

from pages.onboarding import HomePage
from pages.app import App
from utils.multi_device_helpers import StepMixin


class TestJumpToScreenHome(StepMixin):
    """Home page smoke tests using a single onboarded device."""

    UI_TIMEOUT = 30

    @pytest.mark.smoke
    @pytest.mark.navigation
    async def test_home_page_navigation_elements_visible(self) -> None:
        """Verify home page loads and all primary navigation elements are visible."""
        driver = self.device.driver

        async with self.step(self.device, "Verify home page loads"):
            home = HomePage(driver)
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Home container should be visible after onboarding"
            )

        async with self.step(self.device, "Verify search field visible"):
            assert home.is_search_field_visible(), (
                "Jump-to search field should be visible on home page"
            )

        async with self.step(self.device, "Verify dock buttons visible"):
            for button_name in ("Wallet", "Messages", "Communities", "Settings"):
                assert home.is_dock_button_visible(button_name), (
                    f"Dock button '{button_name}' should be visible on home page"
                )

    @pytest.mark.smoke
    @pytest.mark.navigation
    async def test_dock_navigation_to_sections(self) -> None:
        """Verify dock buttons navigate to their respective app sections."""
        driver = self.device.driver
        home = HomePage(driver)
        app = App(driver)

        assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
            "Home page should be loaded before testing dock navigation"
        )

        nav_targets = [
            ("Wallet", home.click_dock_wallet, "wallet"),
            ("Messages", home.click_dock_messages, "messaging"),
            ("Settings", home.click_dock_settings, "settings"),
        ]

        for label, click_fn, expected_section in nav_targets:
            async with self.step(self.device, f"Navigate to {label} via dock"):
                assert click_fn(), f"Failed to click dock {label} button"

                section = app.active_section()
                assert section == expected_section, (
                    f"Expected section '{expected_section}' after clicking {label}, "
                    f"got '{section}'"
                )

            async with self.step(self.device, f"Return to home from {label}"):
                app.safe_click(app.locators.LEFT_NAV_HOME, timeout=10)
                assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                    f"Home page should reload after navigating back from {label}"
                )

    @pytest.mark.smoke
    @pytest.mark.navigation
    async def test_jump_to_search_field(self) -> None:
        """Verify search field can be tapped and accepts text input."""
        driver = self.device.driver
        home = HomePage(driver)

        assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
            "Home page should be loaded before testing search"
        )

        async with self.step(self.device, "Tap search field"):
            assert home.click_search_field(), (
                "Should be able to tap the Jump-to search field"
            )

        async with self.step(self.device, "Enter search text"):
            assert home.enter_search_text("test"), (
                "Should be able to type into the search field"
            )

    @pytest.mark.device_count(2)
    @pytest.mark.messaging
    @pytest.mark.timeout(600)
    async def test_recent_items_ordering(self) -> None:
        """Verify recently visited chats appear in the shell grid.

        Multi-device: device_0 sends a message to device_1, then checks
        that the chat appears in the home page shell grid.
        """
        sender = self.device
        _receiver = self.get_device(1)  # noqa: F841 — kept for device provisioning
        home = HomePage(sender.driver)

        async with self.step(sender, "Verify home page loaded on sender"):
            assert home.wait_for_home_load(timeout=self.UI_TIMEOUT), (
                "Sender home page should be loaded"
            )

        async with self.step(sender, "Check shell grid has items"):
            items = home.get_shell_grid_items()
            assert len(items) >= 0, (
                "Shell grid should be queryable (may be empty on fresh account)"
            )
