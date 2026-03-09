# Chat Input Field UX Improvements — FURPS

**Epic**: Chat Input Field UX Improvements (Release 2.38)
**Risk Level**: 🟢 Standard (UI-only, Messaging — Medium security)
**Release Target**: 2.38 (mid-March 2026)

## Summary

The chat input field is the primary text composition interface for 1:1 chats, group chats, and community channels. This spec covers inline text formatting (bold, italic, strikethrough, code, blockquote), @mention autocomplete, emoji picker integration, link preview generation, multi-line input, image/file attachments, and reply-to-message context. Recent regressions (e.g. italics broken via `966dc4c86`, regression of #19812) confirm this area is actively changing.

## Functionality

### F-CHAT-INPUT-01: Text Formatting

- The input field SHALL support Markdown-style inline formatting: bold (`**text**`), italic (`*text*`), strikethrough (`~~text~~`), inline code (`` `text` ``), code block (` ```text``` `), and blockquote (`> text`).
- Formatting SHALL be applied by selecting text and choosing a format action, or by using keyboard shortcuts.
- The following keyboard shortcuts SHALL be supported:
  - Bold: `Ctrl+B` (`Cmd+B` on macOS)
  - Italic: `Ctrl+I` (`Cmd+I` on macOS)
  - Strikethrough: `Ctrl+Shift+S`
  - Inline code: `Ctrl+Shift+C`
  - Code block: `Ctrl+Shift+Alt+C`
  - Blockquote: `Ctrl+Shift+Q`
- Applying a format to selected text SHALL wrap that text with the corresponding Markdown syntax characters.
- Applying the same format again to already-formatted selected text SHALL unwrap (remove) the formatting characters.
- Nested formatting SHALL be supported (e.g. bold + italic via `***text***`).
- A syntax highlighter SHALL render formatting previews inline as the user types (bold rendered bold, italic rendered italic, etc.).

### F-CHAT-INPUT-02: Formatting Toolbar

- A formatting toolbar (StatusTextFormatMenu) SHALL be accessible from the input field.
- The toolbar SHALL display actions for: Bold, Italic, Strikethrough, Code, Code Block, and Blockquote.
- Each toolbar action SHALL display its associated keyboard shortcut in a tooltip.

### F-CHAT-INPUT-03: @Mention Autocomplete

- Typing `@` followed by characters SHALL trigger a suggestion panel displaying matching community/chat members.
- The suggestion panel SHALL filter members by preferred display name as the user types.
- An "everyone" mention option SHALL be available when applicable.
- The user SHALL be able to select a mention using keyboard navigation (arrow keys + Enter) or mouse/touch.
- Selecting a mention SHALL insert a styled mention tag into the input field at the cursor position.
- The mention tag SHALL resolve to the user's public key when the message is sent.

### F-CHAT-INPUT-04: Emoji Integration

- An emoji picker button SHALL be present in the input field toolbar.
- Opening the emoji picker SHALL display categorised emoji with a search field.
- Selecting an emoji SHALL insert it at the current cursor position.
- Typing `:` followed by a shortname SHALL trigger inline emoji autocomplete suggestions.
- Selecting from emoji suggestions SHALL replace the shortname text with the emoji.
- ASCII emoji sequences (e.g. `:)`, `:(`) SHALL be converted to their Unicode equivalents on send.
- The emoji picker SHALL be accessible via `Ctrl+E` or `Ctrl+Meta+Space`.

### F-CHAT-INPUT-05: Link Preview

- When a URL is pasted or typed into the input field, a link preview card SHALL be generated below the input.
- The link preview SHALL display at minimum: page title, description snippet, and thumbnail (when available).
- The user SHALL be able to dismiss individual link previews before sending.

### F-CHAT-INPUT-06: Multi-line Input and Text Wrapping

- The input field SHALL support multi-line text entry via `Shift+Enter` or natural text wrapping.
- Pressing `Enter` alone SHALL send the message.
- The input field SHALL expand vertically to accommodate multi-line content, up to a maximum visible height, after which it SHALL scroll.

### F-CHAT-INPUT-07: Image and File Attachments

- The user SHALL be able to attach images via a command menu ("Add image" action) or by pasting from clipboard.
- The user SHALL be able to attach images via drag-and-drop onto the input area.
- Attached images SHALL be validated for: supported file extension, file size limit, and maximum number of images.
- A thumbnail preview of attached images SHALL be displayed in an image area below the input field.
- The user SHALL be able to remove individual attached images before sending.

### F-CHAT-INPUT-08: Reply-to-Message

- When the user initiates a reply, a reply context bar SHALL appear above the input field.
- The reply bar SHALL display: the original sender's username and a preview of the original message content (text, image, or sticker).
- The user SHALL be able to dismiss the reply context via a close button.
- Sending a message while reply context is active SHALL associate the sent message with the replied-to message.

### F-CHAT-INPUT-09: Message Editing

- Pressing the Up arrow key when the input field is empty SHALL load the user's most recent sent message into the input field for editing.
- The edited message SHALL be sent with an `(edited)` indicator visible to all participants.

## Usability

### U-CHAT-INPUT-01: Input Responsiveness
- The input field SHALL accept and render typed characters with < 50ms perceived latency per keystroke.
- There SHALL be no visible frame drops or cursor lag during rapid typing (> 5 characters/second).

### U-CHAT-INPUT-02: Formatting Toolbar Discoverability
- The formatting toolbar SHALL be visually associated with the input field (adjacent or contextual on text selection).
- Each action SHALL have a recognisable icon and an accessible tooltip showing the action name and shortcut.
- On Windows, formatting menu buttons SHALL be sized appropriately (not oversized).

### U-CHAT-INPUT-03: Cursor Positioning After Formatting
- After applying formatting to selected text, the cursor SHALL be positioned immediately after the closing formatting characters.
- After inserting a mention or emoji, the cursor SHALL be positioned immediately after the inserted element with a trailing space.

### U-CHAT-INPUT-04: Paste Behaviour
- Pasting plain text SHALL insert the text at the cursor position.
- Pasting an image from the clipboard SHALL trigger the image attachment flow with validation.
- Pasting a URL SHALL insert the URL text and trigger link preview generation.
- Pasting rich text (e.g. from a web page) SHALL insert only the plain-text content.

### U-CHAT-INPUT-05: Platform Consistency
- Formatting, mention, and emoji features SHALL behave consistently across macOS, Windows, and Linux desktop builds.
- Keyboard shortcuts SHALL use platform-appropriate modifier keys (Cmd on macOS, Ctrl on Windows/Linux).

## Reliability

### R-CHAT-INPUT-01: Text Preservation on Navigation
- If the user navigates away from a chat and returns, any unsent draft text in the input field SHALL be preserved.
- Draft preservation SHALL apply per-chat (each chat retains its own draft independently).

### R-CHAT-INPUT-02: Formatting Consistency
- Markdown formatting applied in the input field SHALL render identically in the sent message bubble for all recipients.
- Formatting SHALL render consistently across macOS, Windows, and Linux.

### R-CHAT-INPUT-03: Input State Recovery
- After an app crash or unexpected restart, the input field SHALL recover to an empty state without errors or rendering artefacts.
- No partial or corrupted formatting characters SHALL persist in the input field after recovery.

### R-CHAT-INPUT-04: Mention Resolution
- Mentions SHALL resolve correctly even if the mentioned user's display name changes between composition and sending.
- Mentioning a user who has left the chat SHALL still render the mention tag (with the last known display name).

### R-CHAT-INPUT-05: Error Handling for Attachments
- If an image fails validation (wrong format, too large, too many), a clear error message SHALL be displayed.
- The error message SHALL specify which validation rule was violated.
- The input field and any valid attachments SHALL remain intact after a validation error.

## Performance

### P-CHAT-INPUT-01: Keystroke Latency
- Each keystroke in the input field SHALL be rendered in < 50ms on supported hardware.
- Syntax highlighting updates SHALL complete within < 100ms of the last keystroke.

### P-CHAT-INPUT-02: Formatting Render Time
- Applying a formatting action (via toolbar or shortcut) SHALL update the input field display within < 100ms.

### P-CHAT-INPUT-03: Autocomplete Latency
- @mention suggestion filtering SHALL update within < 200ms of each additional typed character.
- Emoji shortname suggestions SHALL appear within < 200ms of the `:` trigger.

### P-CHAT-INPUT-04: Link Preview Generation
- Link preview metadata SHALL begin loading within < 500ms of URL detection.
- A loading indicator SHALL be shown while the preview is being fetched.

### P-CHAT-INPUT-05: Image Attachment
- Image validation (format, size, quantity) SHALL complete within < 200ms per image.
- Thumbnail generation for attached images SHALL complete within < 500ms.

## Acceptance Criteria

### AC-CHAT-INPUT-01: Bold Formatting
**Given** a user has text selected in the chat input field
**When** the user presses `Ctrl+B`
**Then** the selected text is wrapped with `**` on each side, and the syntax highlighter renders the text in bold
**Verify by**: Manual QA, Squish E2E

### AC-CHAT-INPUT-02: Italic Formatting
**Given** a user has text selected in the chat input field
**When** the user presses `Ctrl+I`
**Then** the selected text is wrapped with `*` on each side, and the syntax highlighter renders the text in italic
**Verify by**: Manual QA, Squish E2E

### AC-CHAT-INPUT-03: Italic Toggle (Unwrap)
**Given** a user has text selected that is already wrapped with `*` italic markers
**When** the user presses `Ctrl+I`
**Then** the `*` markers are removed and the text returns to normal styling
**Verify by**: Manual QA

### AC-CHAT-INPUT-04: Strikethrough Formatting
**Given** a user has text selected in the chat input field
**When** the user presses `Ctrl+Shift+S`
**Then** the selected text is wrapped with `~~` on each side
**Verify by**: Manual QA

### AC-CHAT-INPUT-05: Inline Code Formatting
**Given** a user has text selected in the chat input field
**When** the user presses `Ctrl+Shift+C`
**Then** the selected text is wrapped with single backticks
**Verify by**: Manual QA

### AC-CHAT-INPUT-06: Code Block Formatting
**Given** a user has text selected in the chat input field
**When** the user presses `Ctrl+Shift+Alt+C`
**Then** the selected text is wrapped with triple backticks on separate lines
**Verify by**: Manual QA

### AC-CHAT-INPUT-07: Blockquote Formatting
**Given** a user has text selected in the chat input field
**When** the user presses `Ctrl+Shift+Q`
**Then** the selected line is prefixed with `> `
**Verify by**: Manual QA

### AC-CHAT-INPUT-08: @Mention Autocomplete
**Given** a user is in a chat with members "Alice" and "Bob"
**When** the user types `@Ali` in the input field
**Then** a suggestion panel appears showing "Alice" as a match, and selecting it inserts a mention tag for Alice
**Verify by**: Manual QA, Squish E2E

### AC-CHAT-INPUT-09: Emoji Picker Insert
**Given** a user has the input field focused
**When** the user opens the emoji picker and selects the "thumbs up" emoji
**Then** the 👍 emoji is inserted at the cursor position in the input field
**Verify by**: Manual QA, Appium E2E

### AC-CHAT-INPUT-10: Inline Emoji Autocomplete
**Given** a user types `:thu` in the input field
**When** the emoji suggestion popup appears with matching emoji
**Then** selecting "thumbsup" from the list replaces `:thu` with the 👍 emoji
**Verify by**: Manual QA

### AC-CHAT-INPUT-11: Image Attachment via Command Menu
**Given** a user clicks the command button and selects "Add image"
**When** the user selects a valid image file from the file dialog
**Then** a thumbnail preview appears in the image area below the input field
**Verify by**: Manual QA

### AC-CHAT-INPUT-12: Image Paste from Clipboard
**Given** a user has an image copied to the system clipboard
**When** the user pastes (`Ctrl+V`) into the input field
**Then** the image is validated and a thumbnail preview appears in the image area
**Verify by**: Manual QA

### AC-CHAT-INPUT-13: Reply Context
**Given** a user initiates a reply to a message from "Alice" saying "Hello"
**When** the reply bar appears above the input field
**Then** the reply bar displays "Alice" and "Hello", and sending a message associates it with the replied-to message
**Verify by**: Manual QA, Appium E2E

### AC-CHAT-INPUT-14: Multi-line Input
**Given** a user is typing in the input field
**When** the user presses `Shift+Enter`
**Then** a new line is inserted without sending the message, and the input field expands vertically
**Verify by**: Manual QA

### AC-CHAT-INPUT-15: Message Edit via Up Arrow
**Given** a user has sent a message and the input field is empty
**When** the user presses the Up arrow key
**Then** the most recent sent message is loaded into the input field for editing
**Verify by**: Manual QA

### AC-CHAT-INPUT-16: Bold + Italic Nested Formatting
**Given** a user types `***bold and italic***` in the input field
**When** the message is sent
**Then** the text renders as both bold and italic in the message bubble
**Verify by**: Manual QA

## Edge Cases

### EC-CHAT-INPUT-01: Very Long Messages
- Messages exceeding 10,000 characters SHALL still be composable and sendable without input field errors or truncation.
- The input field SHALL scroll smoothly for long content.

### EC-CHAT-INPUT-02: Nested Formatting
- Applying bold inside an italic selection (or vice versa) SHALL produce valid nested Markdown (`***text***`).
- Triple-nested formatting (e.g. bold + italic + strikethrough) SHALL degrade gracefully if not fully supported.

### EC-CHAT-INPUT-03: Special Characters in Mentions
- Users with display names containing special characters (e.g. `@`, `*`, backticks, emoji) SHALL be mentionable.
- The mention tag SHALL render correctly regardless of special characters in the display name.

### EC-CHAT-INPUT-04: Copy-Paste of Formatted Text
- Copying a formatted message from the chat log and pasting into the input field SHALL paste only the plain-text Markdown representation.
- No invisible formatting artefacts SHALL be introduced by paste operations.

### EC-CHAT-INPUT-05: Rapid Formatting Toggle
- Rapidly toggling a format (e.g. pressing `Ctrl+B` repeatedly) SHALL not produce orphaned or duplicated formatting characters.

### EC-CHAT-INPUT-06: Empty Selection Formatting
- Applying a formatting action with no text selected SHALL insert the formatting wrapper characters with the cursor positioned between them for immediate typing.

### EC-CHAT-INPUT-07: Concurrent Mention and Emoji Popups
- If the user triggers an @mention suggestion and then immediately types `:` for emoji, the mention popup SHALL close before the emoji popup opens.
- Only one autocomplete popup SHALL be visible at a time.

### EC-CHAT-INPUT-08: Image Attachment Limits
- Attempting to attach more images than the maximum allowed SHALL display an error without discarding previously attached valid images.
- Attempting to attach an image exceeding the file size limit SHALL display a specific error message.

### EC-CHAT-INPUT-09: Link Preview for Invalid URLs
- Pasting a malformed or unreachable URL SHALL not generate a link preview card.
- The input field SHALL remain functional with the pasted text intact.

### EC-CHAT-INPUT-10: Input Field with Keyboard Dismissed (Mobile/Tablet)
- On platforms with soft keyboards, dismissing the keyboard SHALL not clear the input field content.
- Refocusing the input field SHALL restore the keyboard and cursor position.

## Suggested Test Coverage

| Acceptance Criteria | Manual QA | Appium E2E (mobile) | Squish E2E (desktop) |
|---|---|---|---|
| AC-CHAT-INPUT-01 to AC-CHAT-INPUT-07 (Formatting) | Yes | No coverage | Suggested: `tst_ChatInputFormatting` |
| AC-CHAT-INPUT-08 (Mentions) | Yes | No coverage | Existing: `send_message_with_mention` in StatusChatScreen |
| AC-CHAT-INPUT-09 to AC-CHAT-INPUT-10 (Emoji) | Yes | Existing: `test_emoji_and_media.py` | Existing: emoji steps in suite_messaging |
| AC-CHAT-INPUT-11 to AC-CHAT-INPUT-12 (Attachments) | Yes | Partial: `open_image_dialog` exists | No coverage |
| AC-CHAT-INPUT-13 (Reply) | Yes | Existing: reply tests in `test_messaging_1x1_chat.py` | Existing: `reply_to_message_at_index` |
| AC-CHAT-INPUT-14 (Multi-line) | Yes | No coverage | No coverage |
| AC-CHAT-INPUT-15 (Edit) | Yes | Partial: edit in context menu tests | Existing: `edit_message_at_index` |
| AC-CHAT-INPUT-16 (Nested formatting) | Yes | No coverage | No coverage |
