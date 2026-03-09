# Activity Center Revamp — FURPS

**Epic**: Activity Center Revamp (Release 2.38)
**Risk Level**: 🟡 Medium (Messaging / Communities)

## Summary

The Activity Center is a centralised notification hub that aggregates all user-facing events — contact requests, community invites, mentions, replies, reactions, ownership transfers, and device-pairing alerts — into a single filterable panel. The revamp introduces a redesigned card-based UI with grouped notification categories, inline accept/decline actions, read/unread management, and an updated empty-state experience.

## Functionality

- **F-AC-01**: Display notifications of all supported types: contact requests, community invitations, community membership requests, community kicked/banned/unbanned, mentions, replies, new 1:1 chats, new private group chats, contact verification, contact removed, owner token received, ownership received/lost/failed/declined, share accounts, community token received, new installation received/created, and news messages.
- **F-AC-02**: Allow the user to filter notifications by group category (All, Mentions, Replies, Contact Requests, Community, Membership, System).
- **F-AC-03**: Allow the user to filter notifications by read state: All, Unread, or Read.
- **F-AC-04**: Mark an individual notification as read.
- **F-AC-05**: Mark an individual notification as unread.
- **F-AC-06**: Mark all notifications as read in a single action via the "Mark all as read" button.
- **F-AC-07**: Accept a contact request directly from the Activity Center notification card.
- **F-AC-08**: Decline (dismiss) a contact request directly from the Activity Center notification card.
- **F-AC-09**: Accept a community invitation directly from the Activity Center notification card.
- **F-AC-10**: Decline (dismiss) a community invitation directly from the Activity Center notification card.
- **F-AC-11**: Accept a community membership request (admin view) directly from the Activity Center.
- **F-AC-12**: Decline a community membership request (admin view) directly from the Activity Center.
- **F-AC-13**: Accept an unknown group chat invitation directly from the Activity Center.
- **F-AC-14**: Navigate to the originating chat, community, or message when a notification card is clicked (switch-to action).
- **F-AC-15**: Display an unread notification badge count on the Activity Center icon in the navigation sidebar.
- **F-AC-16**: Order notifications chronologically, most recent first.
- **F-AC-17**: Support pagination / incremental loading of notifications when the list exceeds the initial fetch size.
- **F-AC-18**: Display notification metadata: sender avatar, sender display name, community/channel badge, timestamp, and message preview where applicable.
- **F-AC-19**: Enable or sync a new paired installation directly from a new-device notification.
- **F-AC-20**: Hide read notifications when the "Hide read notifications" toggle is active.
- **F-AC-21**: Close the Activity Center panel via the close button.

## Usability

- **U-AC-01**: The user SHALL be able to accept or decline a contact request, community invitation, or membership request within the Activity Center without navigating to another screen (maximum 2 clicks from the notification card).
- **U-AC-02**: Unread notifications SHALL be visually distinct from read notifications through a differentiated card background or indicator.
- **U-AC-03**: When the notification list is empty for the active filter, a descriptive empty-state message and illustration SHALL be displayed.
- **U-AC-04**: Each notification card SHALL display a contextual avatar (user profile image, community logo, or system icon) to aid quick visual identification.
- **U-AC-05**: The group filter tabs SHALL indicate the active selection with a highlighted state.
- **U-AC-06**: Notification cards SHALL display a hover state providing access to context actions (mark read/unread, more options) on desktop.
- **U-AC-07**: The Activity Center panel SHALL open and close without a full-screen transition — it SHALL appear as a floating side panel overlaying the current view.

## Reliability

- **R-AC-01**: New notifications SHALL appear in the Activity Center within 5 seconds of receipt without requiring the user to manually refresh.
- **R-AC-02**: Notification ordering SHALL remain consistent: no duplicate entries, no out-of-order insertions after real-time updates.
- **R-AC-03**: When a notification references deleted content (e.g., a message in a community the user has left), the notification card SHALL still render with a fallback state indicating the content is no longer available.
- **R-AC-04**: Mark-as-read state SHALL propagate to all paired devices within 30 seconds via the sync protocol.
- **R-AC-05**: Accept/decline actions SHALL be idempotent — repeated invocations for the same notification SHALL NOT produce errors or duplicate side effects.
- **R-AC-06**: If the backend returns an error for an accept/decline action, the notification card SHALL revert to its prior state and display visible feedback indicating the action failed.
- **R-AC-07**: Dismissed or accepted notifications SHALL be removed from the unread list immediately on the local device.
- **R-AC-08**: The Activity Center SHALL recover gracefully from a network interruption: notifications fetched before the interruption SHALL remain visible, and new notifications SHALL load once connectivity is restored.

## Performance

- **P-AC-01**: The Activity Center panel SHALL open and display the first page of notifications in < 500 ms on a device meeting minimum hardware requirements.
- **P-AC-02**: Rendering a notification list of 100 items SHALL complete in < 1 second with no visible frame drops (> 30 FPS throughout scroll).
- **P-AC-03**: Real-time notification update latency (from Waku message receipt to UI display) SHALL be < 3 seconds.
- **P-AC-04**: Switching between group filter tabs SHALL update the displayed list in < 300 ms.
- **P-AC-05**: The "Mark all as read" action SHALL complete (local UI update) in < 500 ms regardless of notification count.
- **P-AC-06**: Incremental loading (pagination) SHALL fetch and render the next page in < 1 second.

## Security

- **S-AC-01**: Contact request notifications SHALL display the sender's verified public chat key so the user can confirm the requester's identity before accepting.
- **S-AC-02**: Community invitation notifications SHALL display the community name, logo, and member count sourced from the authenticated community description signed by the community owner.
- **S-AC-03**: Accept/decline RPC calls SHALL be authenticated through the user's session — no unauthenticated actor SHALL be able to accept or dismiss notifications on behalf of the user.
- **S-AC-04**: Notification content (message previews, sender names) SHALL be decrypted locally; no plaintext notification content SHALL be transmitted to or stored on third-party servers.

### Threat Considerations

- A malicious actor could craft spoofed community invitations; the UI must display cryptographically verified community metadata.
- Mass notification spam (e.g., thousands of contact requests) could be used as a denial-of-service vector against the Activity Center UI.

### Data Protection

- Notifications contain sender public keys, message content previews, and community identifiers — all classified as user-private data.
- Notification state (read/unread, accepted/dismissed) is synced between paired devices via the Waku sync protocol.

## Acceptance Criteria

### AC-AC-01: View unread notifications
**Given** the user has 5 unread notifications (2 contact requests, 2 mentions, 1 community invite)
**When** the user opens the Activity Center
**Then** all 5 notifications are displayed in chronological order (most recent first), each with distinct unread visual treatment
**Verify by**: Manual QA, Appium E2E

### AC-AC-02: Filter by notification group
**Given** the user has notifications across multiple categories
**When** the user selects the "Mentions" group tab
**Then** only mention-type notifications are displayed; all other types are hidden
**Verify by**: Manual QA, Appium E2E

### AC-AC-03: Mark individual notification as read
**Given** the user has an unread mention notification
**When** the user triggers the "mark as read" action on that notification
**Then** the notification's visual treatment changes to the read state, and the badge count decreases by 1
**Verify by**: Manual QA, Appium E2E

### AC-AC-04: Mark all as read
**Given** the user has 10 unread notifications
**When** the user clicks "Mark all as read"
**Then** all notifications transition to the read state within < 500 ms, and the badge count resets to 0
**Verify by**: Manual QA, Appium E2E

### AC-AC-05: Accept contact request from Activity Center
**Given** the user has a pending contact request notification from User B
**When** the user clicks "Accept" on the notification card
**Then** User B is added to the user's contacts, the notification is marked as accepted, and User B appears in the contacts list
**Verify by**: Manual QA (multi-device), Appium E2E (multi-device)

### AC-AC-06: Decline contact request from Activity Center
**Given** the user has a pending contact request notification from User B
**When** the user clicks "Decline" on the notification card
**Then** the contact request is dismissed, the notification is removed from the unread list, and User B is NOT added to contacts
**Verify by**: Manual QA, Appium E2E

### AC-AC-07: Accept community invitation
**Given** the user has a community invitation notification for Community X
**When** the user clicks "Accept" on the notification card
**Then** the user is added as a member of Community X, and navigating to Communities shows Community X in the joined list
**Verify by**: Manual QA (multi-device), Appium E2E

### AC-AC-08: Navigate to source from notification
**Given** the user has a mention notification from Channel #general in Community X
**When** the user clicks the notification card body
**Then** the app navigates to Channel #general in Community X, scrolled to the mentioned message
**Verify by**: Manual QA, Appium E2E

### AC-AC-09: Real-time notification arrival
**Given** the Activity Center is open
**When** another user sends a new contact request to the current user
**Then** the new notification appears at the top of the list within 5 seconds without manual refresh
**Verify by**: Manual QA (multi-device)

### AC-AC-10: Badge count accuracy
**Given** the user has N unread notifications
**When** the user views the navigation sidebar
**Then** the Activity Center icon displays a badge with count N
**Verify by**: Manual QA, Appium E2E

### AC-AC-11: Empty state display
**Given** the user has no notifications (or no notifications matching the active filter)
**When** the Activity Center is open
**Then** an empty-state message and illustration are displayed
**Verify by**: Manual QA, Appium E2E

### AC-AC-12: Hide read notifications
**Given** the user has both read and unread notifications
**When** the user enables "Hide read notifications"
**Then** only unread notifications are displayed in the list
**Verify by**: Manual QA, Appium E2E

### AC-AC-13: Notification for left community
**Given** the user previously received a mention notification from Community X
**When** the user has since left Community X and opens the Activity Center
**Then** the notification renders with a fallback state indicating the community/content is no longer accessible
**Verify by**: Manual QA

## Edge Cases

| ID | Scenario | Expected Behaviour |
|----|----------|--------------------|
| EC-AC-01 | 1000+ unread notifications | Pagination loads incrementally; the panel remains responsive (> 30 FPS) with no UI freeze. Badge shows "999+" or the actual count. |
| EC-AC-02 | Notification for a message in a community the user has since left | The notification card renders with a fallback state; tapping it does NOT navigate to the community (or shows an informational message). |
| EC-AC-03 | Simultaneous accept/decline of the same contact request from two paired devices | Only one action succeeds; the second device receives a sync update reflecting the winning action. No error is shown to either device. |
| EC-AC-04 | Activity Center opened while new notifications arrive in real-time | New notifications are prepended to the list without disrupting the user's scroll position or selection. |
| EC-AC-05 | Rapid toggling between group filter tabs | Each tab switch cancels the prior filter and displays the correct subset; no stale data from a previous filter is shown. |
| EC-AC-06 | Network disconnection during accept/decline action | The action is retried or the notification reverts to its prior state with an error indication. |
| EC-AC-07 | Notification from a blocked contact | The notification SHALL NOT appear in the Activity Center. |
| EC-AC-08 | All notifications marked as read, then "Hide read" enabled | The list shows the empty state. |

## Suggested Test Coverage

### Manual QA
- AC-AC-01 through AC-AC-13 (all acceptance criteria)
- All edge cases (EC-AC-01 through EC-AC-08)
- Multi-device sync scenarios (AC-AC-05, AC-AC-09, EC-AC-03)

### Appium E2E (mobile)
- Open Activity Center and verify notification list renders (AC-AC-01)
- Filter by group tab and verify correct filtering (AC-AC-02)
- Mark as read / mark all as read (AC-AC-03, AC-AC-04)
- Accept/decline contact request (AC-AC-05, AC-AC-06)
- Badge count verification (AC-AC-10)
- Empty state (AC-AC-11)
- Hide read notifications toggle (AC-AC-12)

### Squish E2E (desktop)
- Existing tests cover: accept contact request from Activity Center (`test_block_unblock_user.py`, `test_messaging_group_chat.py`)
- Extend to cover: group filtering, mark all as read, community invitation accept/decline, navigate-to-source
