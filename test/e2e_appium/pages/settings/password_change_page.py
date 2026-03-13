import time
from typing import Optional

from ..base_page import BasePage
from locators.settings.password_change_locators import PasswordChangeLocators
from .change_password_modal import ChangePasswordModal

_BROWSERSTACK_INTER_KEY_DELAY = 80


class PasswordChangePage(BasePage):
    """Page object for the Settings → Change Password screen."""

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
        """Fill all password fields, submit, and return the confirmation modal.

        Retries the entire form fill if the submit button does not become
        enabled (which indicates a password mismatch from dropped keystrokes).
        """
        if not self.is_loaded(timeout=10):
            self.logger.error("Password change page did not load")
            return None

        max_form_attempts = 2
        for form_attempt in range(1, max_form_attempts + 1):
            if not self._fill_all_password_fields(current_password, new_password):
                if form_attempt < max_form_attempts:
                    self._clear_all_fields()
                    continue
                return None

            self._dismiss_keyboard_for_submit()

            if self._wait_for_submit_button_enabled(timeout=15):
                break

            self.logger.warning(
                "Submit button not enabled after filling fields (attempt %s/%s); "
                "passwords may not match due to dropped keystrokes",
                form_attempt, max_form_attempts,
            )
            if form_attempt < max_form_attempts:
                self._clear_all_fields()
            else:
                self.logger.error(
                    "Submit button never became enabled after %s form attempts",
                    max_form_attempts,
                )
                return None

        return self._click_and_wait_for_modal(max_attempts=3)

    def _fill_all_password_fields(
        self, current_password: str, new_password: str,
    ) -> bool:
        """Fill all three password fields without dismissing the keyboard between them.

        Hiding the keyboard between fields is counterproductive on Qt/BrowserStack:
        it often fails (HTTP 500), wastes time on retries, and can disrupt focus.
        Clicking the next field naturally transfers keyboard focus.
        """
        fields = [
            (self.locators.CURRENT_PASSWORD_INPUT, current_password, "current password"),
            (self.locators.NEW_PASSWORD_INPUT, new_password, "new password"),
            (self.locators.CONFIRM_PASSWORD_INPUT, new_password, "confirm password"),
        ]

        for locator, password, field_name in fields:
            self.scroll_to_element(locator, max_swipes=2, timeout=3)
            if not self.qt_safe_input(
                locator, password, verify=False,
                inter_key_delay=_BROWSERSTACK_INTER_KEY_DELAY,
            ):
                self.logger.error("Failed to populate %s field", field_name)
                return False
            time.sleep(0.3)

        return True

    def _clear_all_fields(self) -> None:
        """Clear all password fields before a form-fill retry."""
        for locator in [
            self.locators.CURRENT_PASSWORD_INPUT,
            self.locators.NEW_PASSWORD_INPUT,
            self.locators.CONFIRM_PASSWORD_INPUT,
        ]:
            self._clear_input_field(locator, timeout=3)
        time.sleep(0.3)

    def _dismiss_keyboard_for_submit(self) -> None:
        """Dismiss the keyboard and scroll the submit button into view.

        Always scrolls to the button regardless of hide_keyboard() outcome,
        because the keyboard animation needs time to finish even on success.
        """
        if not self.hide_keyboard():
            try:
                size = self.driver.get_window_size()
                self.gestures.tap(
                    int(size["width"] * 0.5), int(size["height"] * 0.15),
                )
            except Exception:
                pass

        time.sleep(0.5)
        self.scroll_to_element(
            self.locators.CHANGE_PASSWORD_BUTTON, max_swipes=2, timeout=3,
        )

    def _wait_for_submit_button_enabled(self, timeout: int = 15) -> bool:
        """Wait for the change-password submit button to become enabled.

        If the button isn't enabled after the initial wait, scroll to it and
        retry once -- the button may be off-screen behind the keyboard.
        """
        if self.wait_for_element_enabled(
            self.locators.CHANGE_PASSWORD_BUTTON, timeout=timeout,
        ):
            return True

        self.scroll_to_element(
            self.locators.CHANGE_PASSWORD_BUTTON, max_swipes=2, timeout=3,
        )
        return self.wait_for_element_enabled(
            self.locators.CHANGE_PASSWORD_BUTTON, timeout=5,
        )

    def _click_and_wait_for_modal(
        self, max_attempts: int = 3,
    ) -> Optional[ChangePasswordModal]:
        """Click the submit button and wait for the confirmation modal.

        Retries the click if the modal doesn't appear, which can happen when
        the click is intercepted by a closing keyboard or the QML button
        doesn't receive the event.  Falls back to a gesture tap when the
        regular Selenium click fails to trigger the QML handler.
        """
        modal = ChangePasswordModal(self.driver)

        for attempt in range(1, max_attempts + 1):
            if not self._is_element_enabled(
                self.locators.CHANGE_PASSWORD_BUTTON, timeout=3,
            ):
                self.logger.warning(
                    "Submit button not enabled before click attempt %s", attempt,
                )
                time.sleep(1.0)
                continue

            clicked = False
            try:
                self.safe_click(self.locators.CHANGE_PASSWORD_BUTTON, timeout=5)
                clicked = True
            except Exception as e:
                self.logger.warning(
                    "safe_click failed on attempt %s: %s", attempt, e,
                )

            if not clicked:
                button = self.find_element_safe(
                    self.locators.CHANGE_PASSWORD_BUTTON, timeout=3,
                )
                if button:
                    clicked = self.gestures.element_center_tap(button)

            if clicked and modal.is_displayed(timeout=20):
                return modal

            if attempt < max_attempts:
                self.logger.warning(
                    "Modal not visible after click attempt %s; retrying", attempt,
                )
                time.sleep(1.0)

        self.logger.error(
            "Change password modal did not appear after %s attempts", max_attempts,
        )
        return None
