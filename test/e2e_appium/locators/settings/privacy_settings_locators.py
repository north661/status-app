from ..base_locators import BaseLocators


class PrivacySettingsLocators(BaseLocators):
    """Locators for the Privacy Mode settings screen.

    QML source: ui/app/AppLayouts/Profile/views/PrivacyView.qml (assumed)
    """

    PRIVACY_MENU_ITEM = BaseLocators.text_contains("Privacy")
    THIRD_PARTY_TOGGLE = BaseLocators.text_contains("Third-party")
    ENABLE_PRIVACY_MODE_BUTTON = BaseLocators.text_contains("Enable Privacy Mode")
    DISABLE_PRIVACY_MODE_BUTTON = BaseLocators.text_contains("Disable Privacy Mode")
    PRIVACY_MODE_ENABLED_LABEL = BaseLocators.text_contains("Privacy Mode is enabled")
    THIRD_PARTY_SWITCH = BaseLocators.resource_id_contains("thirdPartySwitch")
