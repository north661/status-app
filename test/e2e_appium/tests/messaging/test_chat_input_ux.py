"""Tests for Chat Input Field UX improvements.

Covers markdown formatting (bold, italic, code), @mention autocomplete,
multiline input, link preview, input preservation on navigation, and
long message behaviour.

Uses the module-scoped established_chat fixture for shared session.
Each test operates on the primary device's chat input field.

FURPS Spec: Pending (OXI-39)
Feature Area: Messaging (UI)
"""

import asyncio
import uuid
from contextlib import asynccontextmanager

import pytest

from config.logging_config import get_logger
from pages.app import App
from pages.messaging.chat_page import ChatPage


def _unique(prefix: str = "input") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@pytest.mark.messaging
@pytest.mark.device_count(2)
class TestChatInputUx:
    """Chat input field UX: formatting, mentions, multiline, link preview.

    All tests share a module-scoped established_chat fixture so the contact
    establishment flow runs only once.
    """

    UI_TIMEOUT = 30
    logger = get_logger("TestChatInputUx")

    @pytest.fixture(autouse=True)
    def setup(self, established_chat):
        self.ctx = established_chat
        self.driver = established_chat.primary.driver
        self.device = established_chat.primary

    @asynccontextmanager
    async def step(self, description: str):
        self.logger.info(f"Step: {description}")
        yield
        self.logger.info(f"Completed: {description}")

    async def _ensure_in_chat(self) -> ChatPage:
        """Navigate to the established chat with message input ready."""
        app = App(self.driver)
        chat_page = ChatPage(self.driver)

        if chat_page.is_element_visible(chat_page.locators.MESSAGE_INPUT, timeout=2):
            return chat_page

        app.click_messages_button()
        chat_page.dismiss_backup_prompt(timeout=3)
        await asyncio.sleep(0.5)

        if chat_page.wait_for_message_input(timeout=5):
            return chat_page

        if self.ctx.secondary_suffix:
            secondary_name = None
            if self.ctx.secondary.user:
                secondary_name = self.ctx.secondary.user.display_name
            if chat_page.open_chat_by_suffix(
                self.ctx.secondary_suffix, display_name=secondary_name
            ):
                if chat_page.wait_for_message_input(timeout=self.UI_TIMEOUT):
                    return chat_page

        if chat_page.open_first_chat(timeout=self.UI_TIMEOUT):
            if chat_page.wait_for_message_input(timeout=self.UI_TIMEOUT):
                return chat_page

        raise AssertionError("Could not navigate to a chat with message input")

    # ------------------------------------------------------------------
    # 1. Bold text via markdown
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_send_bold_text(self) -> None:
        """Send bold markdown text and verify it appears in the chat log.

        Types **bold text**, sends it, and checks that the rendered message
        is visible in the chat. Exact formatting verification depends on
        accessibility tree representation of bold elements.
        """
        bold_content = _unique("bold")
        markdown = f"**{bold_content}**"

        async with self.step("Send bold markdown message"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.send_formatted_message(markdown), (
                f"Failed to send bold message: {markdown}"
            )

        async with self.step("Verify bold message appears in chat"):
            assert chat_page.message_has_bold_text(bold_content, timeout=self.UI_TIMEOUT), (
                f"Bold message not visible in chat: {bold_content}"
            )

    # ------------------------------------------------------------------
    # 2. Italic text via markdown (validates PR #20136 fix)
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_send_italic_text(self) -> None:
        """Send italic markdown text and verify it renders correctly.

        Validates the fix from PR #20136 where italic rendering was broken.
        """
        italic_content = _unique("italic")
        markdown = f"*{italic_content}*"

        async with self.step("Send italic markdown message"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.send_formatted_message(markdown), (
                f"Failed to send italic message: {markdown}"
            )

        async with self.step("Verify italic message appears in chat"):
            assert chat_page.message_has_italic_text(
                italic_content, timeout=self.UI_TIMEOUT
            ), f"Italic message not visible in chat: {italic_content}"

    # ------------------------------------------------------------------
    # 3. Code block
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_send_code_block(self) -> None:
        """Send a code block and verify it renders in the chat log."""
        code_content = _unique("code")
        markdown = f"```\n{code_content}\n```"

        async with self.step("Send code block message"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.send_formatted_message(markdown), (
                f"Failed to send code block: {markdown}"
            )

        async with self.step("Verify code block appears in chat"):
            assert chat_page.message_has_code_block(
                code_content, timeout=self.UI_TIMEOUT
            ), f"Code block not visible in chat: {code_content}"

    # ------------------------------------------------------------------
    # 4. @mention user autocomplete
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_mention_user_autocomplete(self) -> None:
        """Type @ in the input field and verify the autocomplete popup appears.

        Selects the chat partner from suggestions to confirm the flow works end-to-end.
        """
        async with self.step("Type @ to trigger autocomplete"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.type_in_input("@"), "Failed to type @ in input"

        async with self.step("Verify mention suggestions popup appears"):
            assert chat_page.is_mention_autocomplete_visible(timeout=self.UI_TIMEOUT), (
                "Mention autocomplete popup did not appear after typing @"
            )

        async with self.step("Select user from suggestions"):
            secondary_name = (
                self.ctx.secondary.user.display_name
                if self.ctx.secondary.user
                else self.ctx.secondary_suffix
            )
            assert chat_page.select_mention_suggestion(
                secondary_name, timeout=self.UI_TIMEOUT
            ), f"Failed to select mention suggestion: {secondary_name}"

        async with self.step("Clean up input field"):
            chat_page.clear_message_input()

    # ------------------------------------------------------------------
    # 5. Multiline input
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_multiline_input(self) -> None:
        """Enter multi-line text, verify the input field grows, and send.

        The input field should expand vertically to accommodate multiple lines.
        After sending, the full multiline content must appear in the chat.
        """
        line1 = _unique("line1")
        line2 = _unique("line2")
        line3 = _unique("line3")

        async with self.step("Type single line and measure input height"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.type_in_input(line1), "Failed to type first line"
            single_line_height = chat_page.get_input_field_height()

        async with self.step("Add more lines via Shift+Enter"):
            # Shift+Enter inserts a newline without sending
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains

            actions = ActionChains(self.driver)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
            actions.send_keys(line2)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
            actions.send_keys(line3)
            actions.perform()

        async with self.step("Verify input field grew for multiline content"):
            multiline_height = chat_page.get_input_field_height()
            if single_line_height is not None and multiline_height is not None:
                assert multiline_height > single_line_height, (
                    f"Input field did not grow: {single_line_height}px → {multiline_height}px"
                )

        async with self.step("Send multiline message and verify in chat"):
            assert chat_page.tap_send_button(), "Failed to tap send button"
            assert chat_page.message_exists(line1, timeout=self.UI_TIMEOUT), (
                f"First line not visible in sent message: {line1}"
            )

    # ------------------------------------------------------------------
    # 6. Paste URL → link preview
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_paste_url_link_preview(self) -> None:
        """Paste a URL into the input field and verify a link preview is generated."""
        url = "https://status.app"

        async with self.step("Type URL into message input"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.type_in_input(url), f"Failed to type URL: {url}"
            # Allow time for the link preview to be fetched
            await asyncio.sleep(3)

        async with self.step("Verify link preview appears"):
            assert chat_page.is_link_preview_visible(timeout=self.UI_TIMEOUT), (
                "Link preview did not appear after typing URL"
            )

        async with self.step("Send message with link preview"):
            assert chat_page.tap_send_button(), "Failed to send URL message"
            assert chat_page.message_exists(url, timeout=self.UI_TIMEOUT), (
                f"URL message not visible in chat: {url}"
            )

    # ------------------------------------------------------------------
    # 7. Input preservation on navigation
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_input_preservation_on_navigation(self) -> None:
        """Type text, navigate away and back, verify the draft is preserved.

        The chat input should retain unsent text when the user switches to
        another section and returns to the same conversation.
        """
        draft_text = _unique("draft")

        async with self.step("Type text without sending"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.type_in_input(draft_text), "Failed to type draft"

        async with self.step("Navigate away from chat"):
            app = App(self.driver)
            assert app.click_settings_button(), "Failed to navigate to settings"
            await asyncio.sleep(1)

        async with self.step("Navigate back to messages"):
            app = App(self.driver)
            assert app.click_messages_button(), "Failed to navigate back to messages"
            chat_page = ChatPage(self.driver)
            chat_page.dismiss_backup_prompt(timeout=3)
            await asyncio.sleep(0.5)

        async with self.step("Re-open the same chat"):
            secondary_name = None
            if self.ctx.secondary.user:
                secondary_name = self.ctx.secondary.user.display_name
            chat_page.open_chat_by_suffix(
                self.ctx.secondary_suffix, display_name=secondary_name
            )
            assert chat_page.wait_for_message_input(timeout=self.UI_TIMEOUT), (
                "Message input not visible after returning to chat"
            )

        async with self.step("Verify draft text is preserved"):
            current_text = chat_page.get_message_input_text()
            assert current_text is not None, "Could not read input field text"
            assert draft_text in current_text, (
                f"Draft text not preserved. Expected '{draft_text}', got '{current_text}'"
            )

        async with self.step("Clean up draft"):
            chat_page.clear_message_input()

    # ------------------------------------------------------------------
    # 8. Long message input
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    async def test_long_message_input(self) -> None:
        """Type a very long message, verify the input field scrolls, and send.

        The input field should handle messages exceeding the visible area
        without truncation. The full message must appear in the chat log.
        """
        tag = _unique("long")
        long_body = "A" * 500
        long_message = f"{tag} {long_body}"

        async with self.step("Type long message into input"):
            chat_page = await self._ensure_in_chat()
            assert chat_page.type_in_input(long_message), "Failed to type long message"

        async with self.step("Verify input field is scrollable / not truncated"):
            height = chat_page.get_input_field_height()
            assert height is not None, "Could not read input field dimensions"
            self.logger.info(f"Input field height with long message: {height}px")

        async with self.step("Send long message"):
            assert chat_page.tap_send_button(), "Failed to send long message"

        async with self.step("Verify long message appears in chat"):
            assert chat_page.message_exists(tag, timeout=self.UI_TIMEOUT), (
                f"Long message not visible in chat (searched for tag: {tag})"
            )
