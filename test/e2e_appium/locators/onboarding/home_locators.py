from ..base_locators import BaseLocators


class HomeLocators(BaseLocators):
    """Locators for the Jump to Screen / Home Page.

    QML source: ui/app/AppLayouts/Shell/HomePage.qml
    Note: SHELL_GRID uses 'shellGrid' but QML may use 'homeGrid' — verify
    against dump_page_source() output on real device (tracked in OXI-34).
    """

    MAIN_LAYOUT = BaseLocators.xpath("//*[contains(@resource-id, 'StatusMainLayout')]")
    HOME_CONTAINER = BaseLocators.xpath("//*[contains(@resource-id, 'homeContainer')]")

    WALLET_BUTTON = BaseLocators.accessibility_id("Wallet")
    MESSAGES_BUTTON = BaseLocators.accessibility_id("Messages")
    COMMUNITIES_BUTTON = BaseLocators.accessibility_id("Communities Portal")
    MARKET_BUTTON = BaseLocators.accessibility_id("Market")
    SETTINGS_BUTTON = BaseLocators.accessibility_id("Settings")

    DOCK_BUTTONS = {
        "Wallet": WALLET_BUTTON,
        "Messages": MESSAGES_BUTTON,
        "Communities": COMMUNITIES_BUTTON,
        "Market": MARKET_BUTTON,
        "Settings": SETTINGS_BUTTON,
    }

    SEARCH_FIELD = BaseLocators.accessibility_id(
        "Jump to a community, chat, account or a dApp..."
    )
    SHELL_GRID = BaseLocators.xpath("//*[contains(@resource-id, 'shellGrid')]")
    SHELL_GRID_FALLBACK = BaseLocators.xpath("//*[contains(@resource-id, 'homeGrid')]")
    SHELL_GRID_ITEM = BaseLocators.xpath(
        "//*[contains(@resource-id, 'shellGrid') or contains(@resource-id, 'homeGrid')]//*[@clickable='true']"
    )
    PROFILE_BUTTON = BaseLocators.xpath("//*[contains(@resource-id, 'ProfileButton')]")
