# Requirements for Chat Input Field UX Improvements — FURPS

- **Epic**: Chat Input Field UX Improvements (Release 2.38)
- **Related PRs**: #20136 (italics fix, regression of #19812)
- **Figma**: TBD — link to be added when designs are available
- **Risk Level**: Medium (Messaging feature area)

## Summary

The chat input field is the primary interface through which users compose and send messages in 1:1 and group chats. This spec covers text formatting operations (bold, italic, code, strikethrough), @mention autocomplete, emoji picker integration, link preview generation, multi-line input behaviour, file/image attachment initiation, and reply-to-message context. PR #20136 confirms active changes to the italic formatting path, making this area a regression risk for the 2.38 release.

## Functionality

### F-INPUT-001: Plain Text Entry

The chat input field SHALL accept plain text entry of any Unicode character, including emoji, CJK characters, and RTL scripts.

### F-INPUT-002: Multi-line Input

The chat input field SHALL support multi-line text entry. The field SHALL expand vertically to accommodate up to 5 visible lines of text before becoming scrollable.

### F-INPUT-003: Send Message

The user SHALL be able to send the composed message by pressing the Send button or pressing the Enter/Return key. The input field SHALL be cleared after a successful send.

### F-FMT-001: Bold Formatting

The user SHALL be able to apply bold formatting by wrapping selected text or typed text with `**` delimiters. Bold-formatted text SHALL render with increased font weight in the chat log.

### F-FMT-002: Italic Formatting

The user SHALL be able to apply italic formatting by wrapping selected text or typed text with `*` delimiters. Italic-formatted text SHALL render with italic font style in the chat log.

### F-FMT-003: Code Formatting

The user SHALL be able to apply inline code formatting by wrapping text with single backtick (`` ` ``) delimiters. Code-formatted text SHALL render in a monospace font with a distinct background.

### F-FMT-004: Strikethrough Formatting

The user SHALL be able to apply strikethrough formatting by wrapping text with `~~` delimiters. Strikethrough text SHALL render with a horizontal line through the centre of the text.

### F-FMT-005: Code Block Formatting

The user SHALL be able to create multi-line code blocks by wrapping text with triple backtick (` ``` `) delimiters. Code blocks SHALL render in a monospace font with a distinct background container.

### F-FMT-006: Combined Formatting

The user SHALL be able to nest formatting operations (e.g., bold within italic: `***text***`). The rendered output SHALL reflect all applied formatting styles simultaneously.

### F-MENTION-001: @Mention Trigger

Typing the `@` character in the input field SHALL trigger an autocomplete suggestions list showing members of the current chat or community channel.

### F-MENTION-002: @Mention Autocomplete

The autocomplete list SHALL filter results in real time as the user types additional characters after `@`. The list SHALL match against display names.

### F-MENTION-003: @Mention Selection

Selecting an entry from the autocomplete list SHALL insert the user's display name as a mention token in the input field. The mention token SHALL be visually distinct from plain text.

### F-MENTION-004: @Mention Notification

When a message containing an @mention is sent, the mentioned user SHALL receive a notification (push or in-app) indicating they were mentioned.

### F-EMOJI-001: Emoji Picker Access

The user SHALL be able to open the emoji picker via the emoji button adjacent to the input field. The picker SHALL display categorised emoji with a search function.

### F-EMOJI-002: Emoji Search

The emoji picker SHALL provide a search field that filters emojis by shortname (e.g., "thumbsup") as the user types. Results SHALL update with each keystroke.

### F-EMOJI-003: Emoji Insertion

Selecting an emoji from the picker SHALL insert it at the current cursor position in the input field. The picker SHALL close after selection.

### F-LINK-001: Link Preview Generation

When a URL is pasted or typed into the input field, a link preview (title, description, thumbnail) SHALL be generated and displayed below or above the input field before sending.

### F-LINK-002: Link Preview Dismiss

The user SHALL be able to dismiss a generated link preview before sending the message. Dismissing the preview SHALL NOT remove the URL text from the input field.

### F-ATTACH-001: Image Attachment

The user SHALL be able to initiate an image attachment via the command menu button. Selecting "Add Image" SHALL open the device's file/image picker.

### F-ATTACH-002: File Attachment

The user SHALL be able to attach files through the command menu. Attached files SHALL display a preview or icon in the input area before sending.

### F-REPLY-001: Reply Mode Activation

When a user selects "Reply" from the message context menu, the input field SHALL enter reply mode. A reply preview bar SHALL appear above the input field showing the original message content and author.

### F-REPLY-002: Reply Mode Cancellation

The user SHALL be able to cancel reply mode by tapping the close button on the reply preview bar. Cancelling reply mode SHALL NOT clear any text already typed in the input field.

### F-REPLY-003: Reply Message Display

A sent reply SHALL display with a visual reply indicator (reply corner) linking it to the original message in the chat log.

## Usability

### U-INPUT-001: Typing Responsiveness

Characters typed into the input field SHALL appear within 50 ms of the keystroke. There SHALL be no perceptible lag during rapid typing (> 5 characters per second).

### U-INPUT-002: Formatting Toolbar Discoverability

Formatting options (bold, italic, code, strikethrough) SHALL be discoverable either through a visible toolbar or through commonly known markdown syntax. If a toolbar is present, it SHALL be accessible within 1 tap from the input field.

### U-INPUT-003: Cursor Positioning After Formatting

After applying a formatting operation (e.g., bold), the cursor SHALL be positioned immediately after the closing delimiter, ready for continued typing.

### U-INPUT-004: Paste Behaviour — Plain Text

Pasting plain text from the clipboard SHALL insert the text at the current cursor position without additional formatting.

### U-INPUT-005: Paste Behaviour — Rich Text

Pasting rich text (e.g., from a web page) SHALL insert only the plain-text content, stripping HTML/RTF formatting.

### U-INPUT-006: Paste Behaviour — Images

Pasting an image from the clipboard SHALL attach the image to the message, displaying a preview in the input area.

### U-INPUT-007: Input Focus Restoration

When the user returns to a chat after navigating away within the app, the input field SHALL retain focus state and any draft text that was previously entered.

## Reliability

### R-INPUT-001: Draft Preservation on Navigation

If the user navigates away from a chat (e.g., switches to another chat or app section) with unsent text in the input field, the draft text SHALL be preserved and restored when the user returns to that chat.

### R-INPUT-002: Formatting Consistency Across Platforms

Bold, italic, code, strikethrough, and code block formatting SHALL render identically on all supported platforms (desktop Linux, desktop macOS, desktop Windows, mobile Android, mobile iOS).

### R-INPUT-003: Input State Recovery After Crash

If the application crashes or is force-closed while the user has unsent text in the input field, the draft text SHOULD be recoverable on next launch (best-effort; loss of up to 30 seconds of typing is acceptable).

### R-INPUT-004: Emoji Picker Stability

The emoji picker SHALL open and close without causing the input field to lose its content or cursor position.

### R-INPUT-005: Mention Autocomplete Resilience

The @mention autocomplete SHALL gracefully handle members with special characters in display names (e.g., emoji, Unicode, parentheses) without crashing or displaying corrupted text.

## Performance

### P-INPUT-001: Keystroke Latency

Each keystroke in the input field SHALL be rendered within 50 ms on devices meeting minimum system requirements.

### P-INPUT-002: Formatting Render Time

Applying a formatting operation (bold, italic, code, strikethrough) SHALL complete and visually update the input field within 100 ms.

### P-INPUT-003: Autocomplete Suggestion Latency

The @mention autocomplete list SHALL display initial results within 200 ms of typing the `@` character. Subsequent filtering SHALL update within 100 ms per keystroke.

### P-INPUT-004: Emoji Picker Load Time

The emoji picker SHALL be fully interactive within 500 ms of the user tapping the emoji button.

### P-INPUT-005: Link Preview Generation Time

Link preview metadata (title, description) SHALL begin rendering within 3 seconds of the URL being recognised in the input field.

### P-INPUT-006: Large Message Handling

The input field SHALL remain responsive (< 100 ms per keystroke) when the message length exceeds 5,000 characters, up to the maximum allowed message length.

## Acceptance Criteria

### AC-INPUT-001: Send plain text message

**Given** the user is in a 1:1 chat with the message input field visible
**When** the user types "Hello, World!" and taps the Send button
**Then** the message "Hello, World!" SHALL appear in the chat log for both sender and recipient
**Verify by**: Appium E2E — `test_messaging_1x1_chat.py` covers basic send/receive flow

### AC-FMT-001: Bold formatting renders correctly

**Given** the user is in a chat with the message input field visible
**When** the user types `**bold text**` and sends the message
**Then** the text "bold text" SHALL render with bold font weight in the chat log
**Verify by**: Manual QA — visual inspection; Appium E2E — verify message content-desc contains "bold text"

### AC-FMT-002: Italic formatting renders correctly

**Given** the user is in a chat with the message input field visible
**When** the user types `*italic text*` and sends the message
**Then** the text "italic text" SHALL render with italic font style in the chat log
**Verify by**: Manual QA — visual inspection of font style; regression test for PR #20136

### AC-FMT-003: Code inline formatting renders correctly

**Given** the user is in a chat with the message input field visible
**When** the user types `` `code snippet` `` and sends the message
**Then** the text "code snippet" SHALL render in a monospace font with a distinct background
**Verify by**: Manual QA — visual inspection

### AC-FMT-004: Strikethrough formatting renders correctly

**Given** the user is in a chat with the message input field visible
**When** the user types `~~strikethrough~~` and sends the message
**Then** the text "strikethrough" SHALL render with a horizontal line through the text
**Verify by**: Manual QA — visual inspection

### AC-FMT-005: Nested bold and italic renders correctly

**Given** the user is in a chat with the message input field visible
**When** the user types `***bold italic***` and sends the message
**Then** the text "bold italic" SHALL render with both bold weight and italic style
**Verify by**: Manual QA — visual inspection

### AC-MENTION-001: @mention autocomplete appears

**Given** the user is in a group chat or 1:1 chat
**When** the user types `@` in the input field
**Then** an autocomplete list of chat members SHALL appear within 200 ms
**Verify by**: Appium E2E — verify autocomplete popup becomes visible

### AC-MENTION-002: @mention filters as user types

**Given** the @mention autocomplete list is visible
**When** the user types additional characters after `@`
**Then** the list SHALL filter to show only members whose display names contain the typed substring
**Verify by**: Appium E2E — verify filtered list count decreases

### AC-EMOJI-001: Emoji picker opens and inserts emoji

**Given** the user is in a chat with the input field focused
**When** the user taps the emoji button, searches for "thumbsup", and selects the first result
**Then** the 👍 emoji SHALL be inserted at the cursor position in the input field
**Verify by**: Appium E2E — `ChatPage.send_emoji_to_chat()` covers this flow

### AC-REPLY-001: Reply mode shows preview and sends reply

**Given** the user is in a chat with at least one message visible
**When** the user long-presses a message and selects "Reply" from the context menu
**Then** a reply preview bar SHALL appear above the input field showing the original message
**And** after typing a reply and sending, the reply SHALL display with a reply corner indicator
**Verify by**: Appium E2E — `test_reply_to_message` covers reply activation; `ChatPage.message_is_reply()` verifies indicator

### AC-ATTACH-001: Image attachment via command menu

**Given** the user is in a chat with the input field visible
**When** the user taps the command button and selects "Add Image"
**Then** the device file/image picker SHALL open
**Verify by**: Appium E2E — `ChatPage.open_image_dialog()` covers this flow

### AC-DRAFT-001: Draft preservation across navigation

**Given** the user has typed "unsent draft" in the input field
**When** the user navigates to Settings and returns to the same chat
**Then** the text "unsent draft" SHALL still be present in the input field
**Verify by**: Appium E2E — new test scenario needed

### AC-LINK-001: Link preview generated for URL

**Given** the user is in a chat with the input field visible
**When** the user pastes `https://status.app` into the input field
**Then** a link preview (title and/or description) SHALL appear within 3 seconds
**Verify by**: Manual QA — visual inspection; Appium E2E — new test scenario needed

## Edge Cases

### EC-001: Very Long Messages (10,000+ Characters)

When a user types a message exceeding 10,000 characters, the input field SHALL remain responsive (< 100 ms per keystroke). The send operation SHALL succeed if the message is within the protocol's maximum message size. If the message exceeds the maximum, the app SHALL display an error message before attempting to send.

### EC-002: Nested and Adjacent Formatting

Messages with nested formatting (`***bold italic***`) and adjacent formatting (`**bold** *italic*`) SHALL render each format correctly without corrupting surrounding text.

### EC-003: Special Characters in @Mentions

Members with display names containing special characters (emoji, parentheses, quotes, Unicode scripts) SHALL appear correctly in the autocomplete list and render correctly as mention tokens.

### EC-004: Copy-Paste of Formatted Text

Copying a formatted message from the chat log and pasting it into the input field SHALL insert the plain-text content (markdown source), not the rendered formatting.

### EC-005: Rapid Send Operations

Sending multiple messages in rapid succession (< 500 ms between sends) SHALL queue messages and deliver them in order without loss.

### EC-006: Input Field with Keyboard Dismissed

When the on-screen keyboard is dismissed (mobile), the input field SHALL remain visible and any typed text SHALL be preserved. Re-tapping the input field SHALL restore the keyboard.

### EC-007: Empty Message Send Attempt

Pressing the Send button with an empty input field (or whitespace only) SHALL NOT send a message. The Send button SHOULD be visually disabled when the input field is empty.

### EC-008: Concurrent Editing and Incoming Messages

Receiving new messages while the user is composing SHALL NOT clear the input field, move the cursor, or alter the draft text.

### EC-009: Formatting Delimiters as Literal Text

The user SHALL be able to send literal asterisks, backticks, and tildes by escaping them or when they do not form valid formatting pairs (e.g., a single `*` not followed by a closing `*`).

## Suggested Test Coverage

| Acceptance Criteria | Manual QA | Appium E2E (Mobile) | Squish E2E (Desktop) |
|---|---|---|---|
| AC-INPUT-001 | ✓ | ✓ (existing: `test_messaging_1x1_chat.py`) | ✓ |
| AC-FMT-001–005 | ✓ (visual) | New: `test_chat_input_formatting.py` | ✓ |
| AC-MENTION-001–002 | ✓ | New: `test_chat_mentions.py` | ✓ |
| AC-EMOJI-001 | ✓ | ✓ (existing: `ChatPage.send_emoji_to_chat`) | ✓ |
| AC-REPLY-001 | ✓ | ✓ (existing: `test_reply_to_message`) | ✓ |
| AC-ATTACH-001 | ✓ | ✓ (existing: `ChatPage.open_image_dialog`) | ✓ |
| AC-DRAFT-001 | ✓ | New: `test_chat_draft_preservation.py` | ✓ |
| AC-LINK-001 | ✓ | New: `test_link_preview.py` | ✓ |
