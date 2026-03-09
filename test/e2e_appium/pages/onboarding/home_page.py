from ..base_page import BasePage
from locators.onboarding.home_locators import HomeLocators


class HomePage(BasePage):
    """Home page (Jump to Screen launcher) with dock navigation and shell grid."""

    _DOCK_BUTTON_MAP = {
        "wallet": "WALLET_BUTTON",
        "messages": "MESSAGES_BUTTON",
        "communities": "COMMUNITIES_BUTTON",
        "market": "MARKET_BUTTON",
        "settings": "SETTINGS_BUTTON",
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = HomeLocators()

    def is_home_loaded(self) -> bool:
        return self.is_element_visible(self.locators.HOME_CONTAINER)

    def wait_for_home_load(self, timeout: int = 30) -> bool:
        return self.is_element_visible(self.locators.HOME_CONTAINER, timeout=timeout)

    def is_search_field_visible(self) -> bool:
        return self.is_element_visible(self.locators.SEARCH_FIELD)

    def click_dock_settings(self) -> bool:
        return self.safe_click(self.locators.SETTINGS_BUTTON)

    def click_dock_wallet(self) -> bool:
        return self.safe_click(self.locators.WALLET_BUTTON)

    def click_dock_messages(self) -> bool:
        return self.safe_click(self.locators.MESSAGES_BUTTON)

    def click_dock_communities(self) -> bool:
        return self.safe_click(self.locators.COMMUNITIES_BUTTON)

    def is_dock_button_visible(self, button_name: str, timeout: int = 5) -> bool:
        """Check if a dock button is visible by name (wallet, messages, communities, market, settings)."""
        attr = self._DOCK_BUTTON_MAP.get(button_name.lower())
        if attr is None:
            self.logger.error("Unknown dock button name: '%s'", button_name)
            return False
        locator = getattr(self.locators, attr)
        return self.is_element_visible(locator, timeout=timeout)

    def is_shell_grid_visible(self, timeout: int = 5) -> bool:
        return self.is_element_visible(self.locators.SHELL_GRID, timeout=timeout)

    def get_shell_grid_items(self, timeout: int = 10) -> list:
        """Return child elements of the shell grid for recent items verification."""
        grid = self.find_element_safe(self.locators.SHELL_GRID, timeout=timeout)
        if grid is None:
            self.logger.error("Shell grid not found")
            return []
        try:
            children = grid.find_elements("xpath", "./*")
            return children
        except Exception as exc:
            self.logger.error("Failed to get shell grid children: %s", exc)
            return []

    def click_search_field(self) -> bool:
        return self.safe_click(self.locators.SEARCH_FIELD)

    def enter_search_text(self, query: str) -> bool:
        """Tap the search field and enter a query."""
        if not self.click_search_field():
            self.logger.error("Failed to tap search field")
            return False
        return self.qt_safe_input(self.locators.SEARCH_FIELD, query)

    def click_profile_button(self) -> bool:
        return self.safe_click(self.locators.PROFILE_BUTTON)
