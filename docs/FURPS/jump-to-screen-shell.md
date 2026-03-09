# Jump to Screen (Home Page) FURPS

**Epic**: [#17971](https://github.com/status-im/status-app/issues/17971)
**Risk Level**: Standard
**Feature Area**: Navigation / Home Page

---

## Summary

The Jump to Screen feature provides a unified Home Page launcher that gives users quick access to communities, chats, wallet accounts, and dApps through a searchable tile grid. Items are ordered by most recent interaction and display live metadata such as unread counts, media previews, and timestamps. A bottom navigation dock provides persistent access to main application sections.

---

## Functionality

- F-JTS-001: The Home Page SHALL display a grid of tiles representing communities, chats, wallet accounts, and dApps.
- F-JTS-002: Each tile SHALL display live metadata including unread count, media preview, and last interaction timestamp.
- F-JTS-003: Tiles SHALL be ordered by most recent interaction, with the most recently accessed item at the top.
- F-JTS-004: Selecting a tile SHALL navigate the user to the corresponding content (community, chat, account, or dApp).
- F-JTS-005: When a tile is selected, it SHALL move to the top position in the grid.
- F-JTS-006: A search/filter input field SHALL be available with placeholder text "Jump to a community, chat, account or a dApp...".
- F-JTS-007: Typing in the search field SHALL filter the visible tiles to match the query string.
- F-JTS-008: A bottom navigation dock SHALL display main sections (Wallet, Messages, Communities, Settings) and pinned items.
- F-JTS-009: Users SHALL be able to pin and unpin items from the bottom navigation dock.

## Usability

- U-JTS-001: Tiles SHALL be arranged in a visually clear grid layout.
- U-JTS-002: Each tile SHALL display an icon and label identifying its content type and name.
- U-JTS-003: Unread badges SHALL be visible on tiles with unread content.
- U-JTS-004: The search field SHALL be positioned at the top of the Home Page for immediate discoverability.
- U-JTS-005: Standard interaction patterns (hover highlight, click activation) SHALL be supported on desktop; tap activation on mobile.

## Reliability

- R-JTS-001: Tile metadata (unread status, timestamps) SHALL update within 5 seconds of a change event or upon page refresh.
- R-JTS-002: The Home Page SHALL remain responsive when the user rapidly switches between sections or performs repeated searches.
- R-JTS-003: Tiles with missing or malformed data SHALL display a default thumbnail and fallback title rather than crashing or showing blank entries.
- R-JTS-004: If network connectivity is lost during metadata refresh, the Home Page SHALL display the last known cached data without error dialogs.
- R-JTS-005: The grid SHALL handle 0 items (empty state) and display an appropriate placeholder message.

## Performance

- P-JTS-001: The Home Page grid SHALL render all visible tiles within 500 ms of the page being activated.
- P-JTS-002: Animations during tile transitions SHALL maintain a minimum of 30 FPS.
- P-JTS-003: Frame drops SHALL NOT exceed 3 consecutive dropped frames during page transitions or scrolling.
- P-JTS-004: Navigation from tile selection to the target view SHALL complete within 300 ms.
- P-JTS-005: Search field filtering SHALL return updated results within 200 ms of the last keystroke.
- P-JTS-006: Memory usage for the Home Page SHALL NOT exceed 150 MB with 50 tiles loaded (including media previews).
- P-JTS-007: CPU usage SHALL NOT exceed 15% during idle display of the Home Page with live metadata updates.

## Supportability

- S-JTS-001: The tile grid SHALL be modular to support adding or removing content types (e.g., NFTs, media, tokens) without modifying the core grid component.
- S-JTS-002: Interface components SHALL be testable in isolation via Storybook with mockable data models.

---

## Acceptance Criteria

### AC-JTS-001: Home grid loads with recent items
**Given** a user has completed onboarding and has prior activity
**When** the Home Page is displayed
**Then** the grid shows recent items ordered by most recent interaction
**Verify by**: Manual QA; Squish E2E — `test_add_delete_account_from_settings.py` (verifies grid items)

### AC-JTS-002: Navigation dock buttons work
**Given** the Home Page is loaded
**When** the user taps a dock button (Wallet / Messages / Communities / Settings)
**Then** the corresponding section opens within 300 ms
**Verify by**: Manual QA; Appium E2E — `test_dock_navigation_to_sections` (to be created per OXI-33)

### AC-JTS-003: Search/Jump field filters results
**Given** the Home Page is loaded and tiles are displayed
**When** the user types a query in the search field
**Then** only tiles matching the query are visible, updated within 200 ms of the last keystroke
**Verify by**: QML unit test — `tst_HomePage::test_gridItem_search_and_click`; Appium E2E — `test_jump_to_search_field` (to be created per OXI-33)

### AC-JTS-004: Tile selection navigates to target
**Given** the Home Page grid is displayed with tiles
**When** the user selects a tile (community, chat, wallet account, or dApp)
**Then** the application navigates to the corresponding view and the tile moves to the top of the grid
**Verify by**: QML unit test — `tst_HomePage::test_gridItem_search_and_click`; Manual QA

### AC-JTS-005: Pin and unpin items from dock
**Given** the Home Page is loaded with items in the grid
**When** the user pins an item to the dock
**Then** the item appears in the bottom navigation dock and persists across sessions
**Verify by**: Manual QA; Appium E2E (to be created per OXI-33)

### AC-JTS-006: Empty state for new user
**Given** a user has just completed onboarding with no prior activity
**When** the Home Page is displayed
**Then** a placeholder message is shown indicating no recent items, and the dock remains functional
**Verify by**: Manual QA

---

## Edge Cases

| ID | Condition | Expected Behaviour |
|----|-----------|-------------------|
| EC-JTS-001 | New user with no prior activity (empty grid) | Placeholder message displayed; dock buttons remain functional |
| EC-JTS-002 | Maximum tiles in grid (50+ items) | Grid scrolls; performance stays within P-JTS-001 thresholds |
| EC-JTS-003 | Search query with no matching results | Grid shows empty state with "No results" message; clearing search restores all tiles |
| EC-JTS-004 | Network disconnection during metadata refresh | Last cached data displayed; no error dialogs; metadata refreshes when connectivity returns |
| EC-JTS-005 | Rapid switching between sections via dock | UI remains responsive per R-JTS-002; no duplicate navigation events |
| EC-JTS-006 | Tile with missing thumbnail or malformed metadata | Default thumbnail and fallback title displayed per R-JTS-003 |
| EC-JTS-007 | dApps disabled via feature flag | dApp tiles not shown in grid; other tile types unaffected |
| EC-JTS-008 | Very long tile name or label | Text truncated with ellipsis; tooltip shows full name on hover (desktop) |

---

## Suggested Test Coverage

| Acceptance Criteria | Manual QA | QML Unit Test | Squish E2E (Desktop) | Appium E2E (Mobile) |
|----|----|----|----|-----|
| AC-JTS-001 | Yes | `tst_HomePage::test_basic_geometry` | `test_add_delete_account_from_settings` | To be created (OXI-33) |
| AC-JTS-002 | Yes | — | `test_back_up_recovery_phrase` (partial) | To be created (OXI-33) |
| AC-JTS-003 | Yes | `tst_HomePage::test_gridItem_search_and_click` | — | To be created (OXI-33) |
| AC-JTS-004 | Yes | `tst_HomePage::test_gridItem_search_and_click` | — | To be created (OXI-33) |
| AC-JTS-005 | Yes | — | — | To be created (OXI-33) |
| AC-JTS-006 | Yes | — | — | To be created (OXI-33) |
