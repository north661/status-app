from typing import Any

from appium.webdriver.webdriver import WebDriver

from config.logging_config import get_logger
from core.models import TestUser
from fixtures.onboarding_fixture import OnboardingConfig, OnboardingFlow, OnboardingFlowError
from utils.exceptions import SessionManagementError


class DeviceState:
    """Internal state tracking for a device context."""

    def __init__(self):
        self.user: TestUser | None = None
        self._custom_state: dict[str, Any] = {}


class DeviceContext:

    __test__ = False

    def __init__(self, driver: WebDriver, device_id: str, device_config: dict[str, Any] | None = None):
        self.driver = driver
        self.device_id = device_id
        self.device_config = device_config or {}
        self._state = DeviceState()
        self.logger = get_logger(f"device_{device_id}")

    @property
    def user(self) -> TestUser | None:
        return self._state.user

    @user.setter
    def user(self, value: TestUser):
        self._state.user = value
        self.logger.debug("User state updated: %s", value.display_name if value else None)

    async def onboard_user(
        self,
        config: OnboardingConfig | None = None,
        display_name: str | None = None,
        password: str | None = None,
    ) -> TestUser:
        import asyncio

        self.logger.info("Starting user onboarding on device %s", self.device_id)

        if config is None:
            config = OnboardingConfig()

        if display_name:
            config.custom_display_name = display_name

        if password:
            config.custom_password = password

        def _onboard():
            try:
                flow = OnboardingFlow(self.driver, config, self.logger)
                result = flow.execute_complete_flow()

                if not result.get("success", False):
                    raise SessionManagementError(
                        f"Onboarding failed on device {self.device_id}: {result.get('error', 'Unknown error')}"
                    )

                user_data = result.get("user_data", {})
                if not user_data:
                    raise SessionManagementError(
                        f"Onboarding completed but no user data returned on device {self.device_id}"
                    )

                test_user = TestUser.from_onboarding_result(user_data, config)

                self.user = test_user
                self.logger.info(
                    "User onboarded successfully on device %s: %s",
                    self.device_id,
                    test_user.display_name,
                )

                return test_user

            except OnboardingFlowError as e:
                self.logger.error(
                    "OnboardingFlowError on device %s: %s",
                    self.device_id,
                    e,
                )
                raise SessionManagementError(
                    f"Failed to onboard user on device {self.device_id}: {e}"
                ) from e

            except Exception as e:
                self.logger.error(
                    "Unexpected error during onboarding on device %s: %s",
                    self.device_id,
                    e,
                )
                raise SessionManagementError(
                    f"Unexpected error during onboarding on device {self.device_id}: {e}"
                ) from e

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _onboard)

    def get_state(self, key: str, default: Any = None) -> Any:
        return self._state._custom_state.get(key, default)

    def set_state(self, key: str, value: Any) -> None:
        self._state._custom_state[key] = value
        self.logger.debug("State updated: %s = %s", key, value)

    def clear_state(self) -> None:
        self._state._custom_state.clear()
        self.logger.debug("Custom state cleared")

    def capture_profile_link(self) -> str | None:
        """Capture the user's profile link.

        On Android mobile the "Copy link to profile" action
        (``userStatusCopyLinkAction``) is permanently disabled in QML
        (``enabled: !SQUtils.Utils.isMobile``).  This method opens the
        profile popup and taps the mobile-only "Invite contacts" action
        to reach the ShareProfileDialog which contains the link.

        Returns the captured link if successful, otherwise None.
        """
        from pages.app import App
        from pages.settings.share_profile_dialog import ShareProfileDialog
        self.logger.info("Capturing profile link for device %s", self.device_id)

        main_app = App(self.driver)

        # Open the profile popup via the nav-bar profile button.
        # Use the App.open_profile_menu() method which handles
        # _ensure_main_nav_visible() correctly for both landscape and
        # portrait modes.
        if not main_app.open_profile_menu():
            self.logger.error("Failed to open profile menu")
            return None

        # On mobile Android, "Invite contacts" (userStatusShareProfileAction)
        # is the enabled action.  Skip the desktop-only "Copy link to
        # profile" (userStatusCopyLinkAction, disabled on mobile) to
        # avoid wasting ~20s per device.
        INVITE_ACTION = (
            "xpath",
            "//*[contains(@resource-id,'userStatusShareProfileAction')]",
        )
        if not main_app.is_element_visible(INVITE_ACTION, timeout=10):
            self.logger.error("Invite contacts action not visible in profile menu")
            main_app.dump_page_source("invite_action_not_visible")
            # Dismiss the profile popup before returning
            try:
                self.driver.back()
            except Exception:
                pass
            return None

        try:
            main_app.safe_click(INVITE_ACTION, timeout=5)
        except Exception as exc:
            self.logger.error("Failed to click Invite contacts: %s", exc)
            try:
                self.driver.back()
            except Exception:
                pass
            return None

        dialog = ShareProfileDialog(self.driver)
        if not dialog.is_displayed(timeout=10):
            self.logger.error("ShareProfileDialog did not appear after invite tap")
            try:
                self.driver.back()
            except Exception:
                pass
            return None

        profile_link = dialog.get_profile_link()

        # Dismiss: ShareProfileDialog + profile popup = 2 overlays
        for _ in range(2):
            try:
                self.driver.back()
            except Exception:
                pass

        # Re-activate app in case driver.back() exited it on BrowserStack
        main_app.app_lifecycle.activate_app()

        if not profile_link:
            self.logger.error("ShareProfileDialog did not contain a profile link")
            return None

        self.logger.info("Profile link captured: %s", profile_link)
        self.set_state("profile_link", profile_link)

        if self.user:
            self.user.profile_link = profile_link

        return profile_link

    def _capture_via_settings(self, app) -> str | None:
        """Capture profile link via the mobile 'Invite contacts' flow.

        On Android the profile menu exposes "Invite contacts" instead of
        "Copy link to profile".  Tapping it opens the ShareProfileDialog
        which contains the link.

        This method ensures all overlays it opens (profile popup and
        ShareProfileDialog) are dismissed before returning, so the caller
        gets a clean navigation state.
        """
        from locators.app_locators import AppLocators
        from pages.settings.share_profile_dialog import ShareProfileDialog

        locators = AppLocators()
        overlays_to_dismiss = 0

        INVITE_ACTION = ("xpath", "//*[contains(@resource-id,'userStatusShareProfileAction')]")

        try:
            invite_visible = app.is_element_visible(INVITE_ACTION, timeout=2)
            if invite_visible:
                # Profile popup already open from a previous attempt.
                overlays_to_dismiss = 1
            else:
                try:
                    app._ensure_main_nav_visible()
                    app.safe_click(locators.PROFILE_NAV_BUTTON, timeout=5)
                    overlays_to_dismiss = 1
                except Exception as exc:
                    self.logger.error("Failed to open profile menu for invite path: %s", exc)
                    return None
                invite_visible = app.is_element_visible(INVITE_ACTION, timeout=15)

            if not invite_visible:
                self.logger.error("Invite contacts action not visible in profile menu")
                app.dump_page_source("invite_action_not_visible")
                return None

            try:
                app.safe_click(INVITE_ACTION, timeout=5)
            except Exception as exc:
                self.logger.error("Failed to click Invite contacts: %s", exc)
                return None

            dialog = ShareProfileDialog(self.driver)
            if not dialog.is_displayed(timeout=10):
                self.logger.error("ShareProfileDialog did not appear after invite tap")
                return None

            # ShareProfileDialog sits on top of the profile popup — two layers.
            overlays_to_dismiss = 2

            link = dialog.get_profile_link()
            if not link:
                self.logger.error("ShareProfileDialog did not contain a profile link")
                return None

            return link
        finally:
            for i in range(overlays_to_dismiss):
                try:
                    self.driver.back()
                except Exception:
                    self.logger.debug(
                        "driver.back() #%d suppressed during overlay cleanup", i + 1
                    )

