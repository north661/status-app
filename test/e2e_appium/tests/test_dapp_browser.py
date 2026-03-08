"""Tests for DApp Browser navigation and wallet integration.

Coverage gap: docs/FURPS/dapp-browser.md
- Dapp browser opening and navigation
- Wallet integration for signing transactions
- Browser configuration (in-app vs system)
- Wallet interaction prompts and security warnings

Related Linear issue: OXI-12
"""

import pytest

from pages.app import App
from utils.multi_device_helpers import StepMixin


@pytest.mark.dapp_browser
@pytest.mark.smoke
class TestDappBrowserNavigation(StepMixin):
    """DApp Browser navigation and basic interaction.

    Verifies the DApp browser can be opened and navigated,
    with proper UI controls and page loading.
    """

    UI_TIMEOUT = 20

    async def test_open_dapp_browser_and_navigate(self) -> None:
        """Open the DApp browser and navigate to a known DApp.

        FURPS ref: dapp-browser.md — Functionality item 1.

        Flow:
        1. Open DApp browser from main navigation
        2. Verify browser UI loads (address bar, controls)
        3. Navigate to a test DApp URL
        4. Verify page content loads
        5. Verify browser back/forward controls work
        """
        app = App(self.device.driver)  # noqa: F841 — skeleton; will use app once page objects exist

        async with self.step(self.device, "Open DApp browser"):
            # TODO: Implement when DApp browser navigation is available
            # assert app.click_dapp_browser_button(), "Failed to open DApp browser"
            pytest.skip("DApp browser page objects not yet implemented")

        async with self.step(self.device, "Verify browser UI loaded"):
            # TODO: Verify address bar, navigation controls, loading indicator
            pass

        async with self.step(self.device, "Navigate to test DApp"):
            # TODO: Enter URL and verify page loads
            pass

    async def test_browser_configuration_setting(self) -> None:
        """Verify browser preference between in-app and system browser.

        FURPS ref: dapp-browser.md — Functionality item 3.

        Flow:
        1. Navigate to Settings → Browser preferences
        2. Verify default browser option
        3. Switch to system browser
        4. Open a link from chat
        5. Verify system browser is used
        """
        app = App(self.device.driver)

        async with self.step(self.device, "Open browser settings"):
            assert app.click_settings_button(), "Failed to open settings"
            # TODO: Navigate to browser configuration
            pytest.skip("Browser settings page object not yet implemented")


@pytest.mark.dapp_browser
@pytest.mark.wallet
@pytest.mark.critical
class TestDappBrowserWalletConnect(StepMixin):
    """DApp Browser wallet integration and transaction signing.

    Verifies wallet connection, transaction signing prompts,
    and security warnings in the DApp browser context.
    """

    UI_TIMEOUT = 30

    async def test_wallet_connect_in_dapp_browser(self) -> None:
        """Connect wallet to a DApp and verify interaction prompts.

        FURPS ref: dapp-browser.md — Functionality item 2, Usability item 3.

        Flow:
        1. Open DApp browser
        2. Navigate to a DApp that requests wallet connection
        3. Verify wallet connection prompt appears
        4. Approve connection
        5. Verify connection established
        6. Verify wallet interaction prompts display securely
        """
        app = App(self.device.driver)  # noqa: F841 — skeleton; will use app once page objects exist

        async with self.step(self.device, "Open DApp browser and navigate"):
            # TODO: Open browser and navigate to test DApp
            pytest.skip("DApp browser page objects not yet implemented")

        async with self.step(self.device, "Verify wallet connection prompt"):
            # TODO: Trigger wallet connection from DApp
            # Verify prompt shows DApp name, requested permissions
            pass

        async with self.step(self.device, "Approve and verify connection"):
            # TODO: Approve connection, verify established state
            pass

    async def test_untrusted_dapp_warning(self) -> None:
        """Verify warning shown for untrusted or unsupported DApps.

        FURPS ref: dapp-browser.md — Usability item 4.

        Flow:
        1. Open DApp browser
        2. Navigate to unknown/untrusted DApp
        3. Verify warning indicator is displayed
        """
        app = App(self.device.driver)  # noqa: F841 — skeleton; will use app once page objects exist

        async with self.step(self.device, "Navigate to untrusted DApp"):
            # TODO: Navigate to untrusted DApp URL
            pytest.skip("DApp browser page objects not yet implemented")

        async with self.step(self.device, "Verify warning displayed"):
            # TODO: Verify security warning or indicator element
            pass
