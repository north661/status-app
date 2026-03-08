"""Page object for Privacy Mode settings."""

from typing import Optional

from ..base_page import BasePage
from locators.settings.privacy_settings_locators import PrivacySettingsLocators


class PrivacySettingsPage(BasePage):
    """Interactions for the Privacy section in Settings."""

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PrivacySettingsLocators()

    def is_loaded(self, timeout: Optional[int] = 10) -> bool:
        return self.is_element_visible(self.locators.THIRD_PARTY_TOGGLE, timeout=timeout)

    def click_third_party_toggle(self, timeout: Optional[int] = None) -> bool:
        return self.safe_click(self.locators.THIRD_PARTY_TOGGLE, timeout=timeout)

    def confirm_enable_privacy_mode(self, timeout: Optional[int] = 10) -> bool:
        if not self.is_element_visible(self.locators.ENABLE_PRIVACY_MODE_BUTTON, timeout=timeout):
            self.logger.error("Enable Privacy Mode button not visible")
            return False
        return self.safe_click(self.locators.ENABLE_PRIVACY_MODE_BUTTON)

    def confirm_disable_privacy_mode(self, timeout: Optional[int] = 10) -> bool:
        if not self.is_element_visible(self.locators.DISABLE_PRIVACY_MODE_BUTTON, timeout=timeout):
            self.logger.error("Disable Privacy Mode button not visible")
            return False
        return self.safe_click(self.locators.DISABLE_PRIVACY_MODE_BUTTON)

    def is_privacy_mode_enabled(self, timeout: Optional[int] = 10) -> bool:
        return self.is_element_visible(self.locators.PRIVACY_MODE_ENABLED_LABEL, timeout=timeout)

    def is_third_party_switch_checked(self, timeout: Optional[int] = 5) -> bool:
        return self._is_element_checked(self.locators.THIRD_PARTY_SWITCH, timeout=timeout)

    def enable_privacy_mode(self, timeout: Optional[int] = 10) -> bool:
        """Toggle third-party services off and confirm the Enable Privacy Mode popup."""
        if not self.click_third_party_toggle(timeout=timeout):
            return False
        return self.confirm_enable_privacy_mode(timeout=timeout)

    def disable_privacy_mode(self, timeout: Optional[int] = 10) -> bool:
        """Toggle third-party services on and confirm the Disable Privacy Mode popup."""
        if not self.click_third_party_toggle(timeout=timeout):
            return False
        return self.confirm_disable_privacy_mode(timeout=timeout)
