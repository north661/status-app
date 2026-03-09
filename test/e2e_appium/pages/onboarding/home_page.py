from ..base_page import BasePage
from locators.onboarding.home_locators import HomeLocators


class HomePage(BasePage):
    """Page object for the Jump to Screen / Home Page."""

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = HomeLocators()

    def is_home_loaded(self) -> bool:
        return self.is_element_visible(self.locators.HOME_CONTAINER)

    def wait_for_home_load(self, timeout: int = 30) -> bool:
        return self.is_element_visible(self.locators.HOME_CONTAINER, timeout=timeout)

    def is_search_field_visible(self) -> bool:
        return self.is_element_visible(self.locators.SEARCH_FIELD)

    def is_dock_button_visible(self, button_name: str) -> bool:
        """Check visibility of a named dock button (Wallet, Messages, etc.)."""
        locator = self.locators.DOCK_BUTTONS.get(button_name)
        if locator is None:
            self.logger.error("Unknown dock button: %s", button_name)
            return False
        return self.is_element_visible(locator)

    def click_dock_settings(self) -> bool:
        return self.safe_click(self.locators.SETTINGS_BUTTON)

    def click_dock_wallet(self) -> bool:
        return self.safe_click(self.locators.WALLET_BUTTON)

    def click_dock_messages(self) -> bool:
        return self.safe_click(self.locators.MESSAGES_BUTTON)

    def click_dock_communities(self) -> bool:
        return self.safe_click(self.locators.COMMUNITIES_BUTTON)

    def click_search_field(self) -> bool:
        return self.safe_click(self.locators.SEARCH_FIELD)

    def enter_search_text(self, query: str) -> bool:
        return self.qt_safe_input(self.locators.SEARCH_FIELD, query)

    def click_profile_button(self) -> bool:
        return self.safe_click(self.locators.PROFILE_BUTTON)

    def get_shell_grid_items(self) -> list:
        """Return clickable elements from the shell/home grid.

        Tries the primary SHELL_GRID_ITEM locator; returns empty list on failure.
        """
        try:
            self.is_element_visible(
                self.locators.SHELL_GRID,
                fallback_locators=[self.locators.SHELL_GRID_FALLBACK],
                timeout=10,
            )
            return self.driver.find_elements(*self.locators.SHELL_GRID_ITEM)
        except Exception:
            self.logger.error("Failed to retrieve shell grid items")
            return []
