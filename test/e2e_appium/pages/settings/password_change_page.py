import time
from typing import Optional

from ..base_page import BasePage
from locators.settings.password_change_locators import PasswordChangeLocators
from .change_password_modal import ChangePasswordModal


class PasswordChangePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PasswordChangeLocators()

    def is_loaded(self, timeout: Optional[int] = 10) -> bool:
        if not self.is_element_visible(
            self.locators.CURRENT_PASSWORD_CONTAINER, timeout=timeout
        ):
            return False
        return self.is_element_visible(
            self.locators.CURRENT_PASSWORD_INPUT, timeout=timeout
        )

    def change_password(
        self, current_password: str, new_password: str
    ) -> Optional[ChangePasswordModal]:
        if not self.is_loaded(timeout=10):
            self.logger.error("Password change page did not load")
            return None

        if not self.qt_safe_input(self.locators.CURRENT_PASSWORD_INPUT, current_password, verify=False):
            self.logger.error("Failed to populate current password field")
            return None
        self.hide_keyboard()

        if not self.qt_safe_input(self.locators.NEW_PASSWORD_INPUT, new_password, verify=False):
            self.logger.error("Failed to populate new password field")
            return None
        self.hide_keyboard()

        if not self.qt_safe_input(self.locators.CONFIRM_PASSWORD_INPUT, new_password, verify=False):
            self.logger.error("Failed to populate confirm password field")
            return None

        self._dismiss_keyboard_for_submit()

        if not self._wait_for_submit_button_enabled(timeout=15):
            self.logger.error("Change password button did not become enabled")
            return None

        return self._click_and_wait_for_modal(max_attempts=2)

    def _dismiss_keyboard_for_submit(self) -> None:
        """Aggressively dismiss the keyboard so the submit button is reachable."""
        if self.hide_keyboard():
            return

        # Keyboard couldn't be hidden via standard API; tap outside the fields
        # to defocus and dismiss it, then scroll the button into view.
        try:
            size = self.driver.get_window_size()
            self.gestures.tap(int(size["width"] * 0.5), int(size["height"] * 0.15))
            time.sleep(0.5)
        except Exception:
            pass

        self.scroll_to_element(self.locators.CHANGE_PASSWORD_BUTTON, max_swipes=2, timeout=3)

    def _wait_for_submit_button_enabled(self, timeout: int = 15) -> bool:
        """Wait for the change-password submit button to become enabled.

        If the button isn't enabled after the initial wait, scroll to it and
        retry once -- the button may be off-screen behind the keyboard.
        """
        if self.wait_for_element_enabled(self.locators.CHANGE_PASSWORD_BUTTON, timeout=timeout):
            return True

        self.scroll_to_element(self.locators.CHANGE_PASSWORD_BUTTON, max_swipes=2, timeout=3)
        return self.wait_for_element_enabled(self.locators.CHANGE_PASSWORD_BUTTON, timeout=5)

    def _click_and_wait_for_modal(self, max_attempts: int = 2) -> Optional[ChangePasswordModal]:
        """Click the submit button and wait for the confirmation modal.

        Retries the click if the modal doesn't appear on the first attempt,
        which can happen when the click is intercepted by a closing keyboard.
        """
        modal = ChangePasswordModal(self.driver)

        for attempt in range(1, max_attempts + 1):
            try:
                self.safe_click(self.locators.CHANGE_PASSWORD_BUTTON, timeout=5)
            except Exception as e:
                self.logger.error("Failed to click change password button: %s", e)
                if attempt < max_attempts:
                    time.sleep(1.0)
                    continue
                return None

            if modal.is_displayed(timeout=20):
                return modal

            if attempt < max_attempts:
                self.logger.warning(
                    "Modal not visible after click attempt %s; retrying", attempt
                )
                time.sleep(1.0)

        self.logger.error("Change password modal did not appear after clicking button")
        return None
