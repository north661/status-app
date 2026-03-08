"""Tests for Privacy Mode settings toggle."""

import time

import pytest

from pages.app import App
from pages.settings.settings_page import SettingsPage


@pytest.mark.settings
@pytest.mark.device_count(1)
class TestPrivacyMode:

    UI_TIMEOUT = 30

    @pytest.fixture(autouse=True)
    def setup(self, onboarding):
        self.driver = onboarding.driver
        self.app = App(self.driver)

    async def test_enable_privacy_mode(self):
        self.app.click_settings_button()
        settings = SettingsPage(self.driver)
        settings.driver.find_element("xpath", "//*[contains(@text,'Privacy')]").click()
        time.sleep(2)
        settings.driver.find_element("xpath", "//*[contains(@text,'Third-party')]").click()
        time.sleep(3)
        confirm_btn = settings.driver.find_element("xpath", "//*[contains(@text,'Enable Privacy Mode')]")
        confirm_btn.click()
        time.sleep(2)
        assert settings.driver.find_element("xpath", "//*[contains(@text,'Privacy Mode is enabled')]")

    async def test_disable_privacy_mode(self):
        self.app.click_settings_button()
        settings = SettingsPage(self.driver)
        settings.driver.find_element("xpath", "//*[contains(@text,'Privacy')]").click()
        time.sleep(2)
        third_party = settings.driver.find_element("xpath", "//*[contains(@text,'Third-party')]")
        third_party.click()
        time.sleep(3)
        disable_btn = settings.driver.find_element("xpath", "//*[contains(@text,'Disable Privacy Mode')]")
        disable_btn.click()
        time.sleep(2)
        switch = settings.driver.find_element("xpath", "//*[contains(@resource-id,'thirdPartySwitch')]")
        assert switch.get_attribute("checked") == "true"

    async def test_privacy_mode_persists_after_restart(self):
        self.app.click_settings_button()
        settings = SettingsPage(self.driver)
        settings.driver.find_element("xpath", "//*[contains(@text,'Privacy')]").click()
        time.sleep(2)
        settings.driver.find_element("xpath", "//*[contains(@text,'Third-party')]").click()
        time.sleep(3)
        settings.driver.find_element("xpath", "//*[contains(@text,'Enable Privacy Mode')]").click()
        time.sleep(2)
        self.driver.terminate_app("im.status.ethereum")
        time.sleep(5)
        self.driver.activate_app("im.status.ethereum")
        time.sleep(10)
        self.app.click_settings_button()
        settings.driver.find_element("xpath", "//*[contains(@text,'Privacy')]").click()
        time.sleep(2)
        switch = settings.driver.find_element("xpath", "//*[contains(@resource-id,'thirdPartySwitch')]")
        assert switch.get_attribute("checked") == "false"
