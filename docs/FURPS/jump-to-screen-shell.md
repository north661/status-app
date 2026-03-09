# Jump to Screen (Home Page) FURPS

**Epic**: [#17971](https://github.com/status-im/status-app/issues/17971)
**Figma**: N/A — refer to epic for design references
**Risk Level**: Standard (Navigation / UI)

## Summary

The Jump to Screen feature provides a unified home page launcher that lets users quickly navigate to communities, chats, accounts, and dApps through a tile grid and search bar. Recent items are displayed with live metadata such as unread counts and timestamps, and a bottom dock provides persistent access to the app's main sections.

## Functionality

- F-JTS-001: The home page SHALL display a grid of recent items representing communities, chats, accounts, and dApps.
- F-JTS-002: Each tile SHALL display live metadata including unread count, media preview, and last-activity timestamp.
- F-JTS-003: Grid items SHALL be ordered by most recent interaction, with the most recent item first.
- F-JTS-004: When a grid item is selected, it SHALL move to the top position in the grid upon returning to the home page.
- F-JTS-005: The bottom dock SHALL display navigation buttons for Wallet, Messages, Communities, and Settings.
- F-JTS-006: Items SHALL be pinnable and unpinnable from the bottom dock.
- F-JTS-007: A search/filter input field SHALL be available at the top of the home page with placeholder text "Jump to...".
- F-JTS-008: The search field SHALL filter grid items to match the user's query as they type.

## Usability

- U-JTS-001: The grid layout SHALL use consistent tile sizing and spacing for visual clarity.
- U-JTS-002: Each tile SHALL display an identifiable icon or avatar alongside a text label.
- U-JTS-003: Tiles with unread activity SHALL display a visible badge indicator.
- U-JTS-004: Hover states SHALL provide visual feedback on interactive tiles (desktop).
- U-JTS-005: The search field SHALL be reachable within 1 tap/click from the home page.
- U-JTS-006: Dock buttons SHALL use recognisable icons with text labels for each section.

## Reliability

- R-JTS-001: Tile metadata (unread status, timestamps) SHALL update within 5 seconds of the underlying data changing, or upon page refresh.
- R-JTS-002: The home page SHALL remain responsive during rapid section switching (5+ transitions within 3 seconds).
- R-JTS-003: Tiles with missing or malformed data SHALL display a default thumbnail and fallback title instead of crashing or showing blank content.
- R-JTS-004: If network connectivity is lost during metadata refresh, the home page SHALL display the last cached data and SHALL NOT show an error state unless the user explicitly refreshes.
- R-JTS-005: The search field SHALL handle empty queries by displaying the full unfiltered grid.

## Performance

- P-JTS-001: The home page grid SHALL render all visible tiles within 500 ms of navigation to the home page.
- P-JTS-002: Animations during grid transitions SHALL maintain a frame rate above 30 FPS.
- P-JTS-003: Frame drops SHALL NOT exceed 3 consecutive dropped frames during tile transitions or dock interactions.
- P-JTS-004: Navigation from a tile tap to the target screen (chat, community, etc.) SHALL complete within 300 ms.
- P-JTS-005: With 50 tiles loaded, memory usage attributed to the home page SHALL NOT exceed 150 MB.
- P-JTS-006: CPU usage during idle state on the home page (no user interaction) SHALL NOT exceed 5% of a single core.
- P-JTS-007: Search field filtering SHALL display updated results within 200 ms of the last keystroke.

## Supportability

- S-JTS-001: The grid component SHALL be modular, allowing addition or removal of content types (e.g., NFTs, media, tokens) without modifying the core grid layout.
- S-JTS-002: All interactive UI elements SHALL have QML `objectName` or accessibility identifiers for automated test targeting.
- S-JTS-003: The home page SHALL be testable with mock data sources (storybook or equivalent).

## Acceptance Criteria

### AC-JTS-001: Home grid loads with recent items
**Given** a user has completed onboarding and has prior activity
**When** the Home Page is displayed
**Then** the grid shows recent items ordered by most recent interaction
**Verify by**: Appium E2E — `test_home_page_navigation_elements_visible`

### AC-JTS-002: Navigation dock buttons work
**Given** the Home Page is loaded
**When** the user taps a dock button (Wallet / Messages / Communities / Settings)
**Then** the corresponding section opens within 300 ms
**Verify by**: Appium E2E — `test_dock_navigation_to_sections`

### AC-JTS-003: Search/Jump field filters results
**Given** the Home Page is loaded
**When** the user types in the search field
**Then** results are filtered to match the query within 200 ms of the last keystroke
**Verify by**: Appium E2E — `test_jump_to_search_field`

### AC-JTS-004: Grid item reordering on interaction
**Given** the Home Page is loaded with multiple grid items
**When** the user opens a grid item and returns to the Home Page
**Then** the opened item appears at the top of the grid
**Verify by**: Appium E2E — `test_recent_items_ordering`

### AC-JTS-005: Pin and unpin dock items
**Given** the Home Page is loaded
**When** the user pins an item to the dock
**Then** the item appears in the dock and persists across app restarts
**Verify by**: Manual QA — `test_dock_pin_unpin_persistence`

### AC-JTS-006: Tile metadata displays correctly
**Given** a user has unread messages in a chat
**When** the Home Page is displayed
**Then** the chat tile shows an unread badge and the correct last-activity timestamp
**Verify by**: Appium E2E — `test_tile_metadata_display`

## Edge Cases

| ID | Scenario | Expected Behaviour |
|----|----------|-------------------|
| EC-JTS-001 | New user with no prior activity (empty state) | Home page SHALL display an onboarding prompt or empty state placeholder instead of a blank grid |
| EC-JTS-002 | Maximum tiles in grid (100+ items) | Grid SHALL remain scrollable and render within 1000 ms; no items SHALL be silently dropped |
| EC-JTS-003 | Search with no matching results | Search SHALL display a "No results" message; the grid SHALL NOT show stale results |
| EC-JTS-004 | Network disconnection during metadata refresh | Home page SHALL display cached data; no error dialog SHALL appear unless the user manually refreshes |
| EC-JTS-005 | Rapid switching between dock sections (5+ within 3 s) | App SHALL NOT crash, freeze, or show corrupted UI; each section SHALL load correctly |
| EC-JTS-006 | Special characters in search query | Search SHALL handle Unicode, emoji, and special characters without crashing; results SHALL match if applicable |
| EC-JTS-007 | Very long item title in grid tile | Title SHALL be truncated with an ellipsis; tile layout SHALL NOT break |
| EC-JTS-008 | App backgrounded and resumed on home page | Home page SHALL refresh metadata on resume without full reload |

## Suggested Test Coverage

| Acceptance Criteria | Manual QA | Appium E2E | Squish E2E |
|--------------------|-----------|-----------:|------------|
| AC-JTS-001 | Visual grid inspection | `test_home_page_navigation_elements_visible` | `test_home_grid_loads` |
| AC-JTS-002 | Tap each dock button | `test_dock_navigation_to_sections` | Existing dock tests in `test_communities_channels.py` |
| AC-JTS-003 | Type queries, verify filter | `test_jump_to_search_field` | `HomeScreen.search()` coverage |
| AC-JTS-004 | Open item, verify reorder | `test_recent_items_ordering` | `click_grid_item_by_title` + verify order |
| AC-JTS-005 | Pin/unpin + restart | `test_dock_pin_unpin_persistence` | — |
| AC-JTS-006 | Send message, check badge | `test_tile_metadata_display` | — |
