# Activity Center Revamp — FURPS

**Risk Level**: 🟡 Medium (Messaging / Communities)
**Release Target**: 2.38 (mid-March 2026)

## Summary

The Activity Center is the unified notification hub in Status, aggregating contact requests, community invites, membership requests, mentions, replies, ownership transfers, device pairing events, news messages, and more. This revamp restructures the Activity Center as a full section layout (replacing the previous popup) with category-based filtering, read/unread management, infinite-scroll pagination, and inline actions for accepting, declining, or navigating to source content.

## Functionality

### F-AC-01: Notification types

The Activity Center SHALL display notifications for each of the following types:

| ID | Type | QML Component |
|----|------|---------------|
| F-AC-01a | Contact Request (incoming) | `ActivityNotificationContactRequest` |
| F-AC-01b | Contact Removed | `ActivityNotificationContactRemoved` |
| F-AC-01c | Mention (in channel or DM) | `ActivityNotificationMention` |
| F-AC-01d | Reply (to user's message) | `ActivityNotificationReply` |
| F-AC-01e | Community Invitation | `ActivityNotificationCommunityInvitation` |
| F-AC-01f | Community Join Request | `ActivityNotificationCommunityRequest` |
| F-AC-01g | Community Membership Request | `ActivityNotificationCommunityMembershipRequest` |
| F-AC-01h | Community Kicked | `ActivityNotificationCommunityKicked` |
| F-AC-01i | Community Banned / Unbanned | `ActivityNotificationCommunityBanUnban` |
| F-AC-01j | Community Token Received | `ActivityNotificationCommunityTokenReceived` |
| F-AC-01k | Ownership Transfer (received/lost/failed/declined) | `ActivityNotificationTransferOwnership` |
| F-AC-01l | Share Accounts (community address sharing) | `ActivityNotificationCommunityShareAddresses` |
| F-AC-01m | New Device Detected / Created | `ActivityNotificationNewDevice` |
| F-AC-01n | New Keypair from Paired Device | `ActivityNotificationNewKeypairFromPairedDevice` |
| F-AC-01o | Group Chat Invitation (unknown group) | `ActivityNotificationUnknownGroupChatInvitation` |
| F-AC-01p | News Message (RSS-based Status News) | `ActivityNotificationNewsMessage` |

### F-AC-02: Category filtering

The Activity Center SHALL support filtering notifications by category group via a top bar (`ActivityCenterPopupTopBarPanel`):

| Group | Enum | Visibility condition |
|-------|------|---------------------|
| All | `ActivityCenterGroup.All` | Always visible |
| Mentions | `ActivityCenterGroup.Mentions` | `mentionsCount > 0` |
| Replies | `ActivityCenterGroup.Replies` | `repliesCount > 0` |
| Contact Requests | `ActivityCenterGroup.ContactRequests` | `contactRequestsCount > 0` |
| Membership | `ActivityCenterGroup.Membership` | `membershipCount > 0` |
| Admin | `ActivityCenterGroup.Admin` | `adminCount > 0` |
| News Message | `ActivityCenterGroup.NewsMessage` | Always visible when News enabled |

### F-AC-03: Read / unread management

- F-AC-03a: The user SHALL be able to mark a single notification as read.
- F-AC-03b: The user SHALL be able to mark a single notification as unread.
- F-AC-03c: The user SHALL be able to mark all notifications as read via the "Mark all as Read" button (`objectName: markAllReadButton`). This button SHALL be disabled when `unreadNotificationsCount == 0`.
- F-AC-03d: The user SHALL be able to toggle between showing all notifications and showing only unread notifications via the hide/show button (`objectName: hideReadNotificationsButton`).

### F-AC-04: Inline actions

- F-AC-04a: Contact requests SHALL present Accept, Decline, and Block actions directly within the notification card.
- F-AC-04b: Community membership requests SHALL present Accept and Decline actions directly within the notification card.
- F-AC-04c: Group chat invitations SHALL present Accept and Dismiss actions.
- F-AC-04d: Mentions and replies SHALL allow the user to navigate to the source message via `switchTo(sectionId, chatId, messageId)`.
- F-AC-04e: Community invitations SHALL allow the user to navigate to the community via `setActiveCommunity(communityId)`.
- F-AC-04f: News messages SHALL provide a "Read More" action that opens the `NewsMessagePopup`.
- F-AC-04g: Device pairing notifications SHALL provide a "More Details" action opening the pair/sync dialog.
- F-AC-04h: Share Accounts notifications SHALL open the community share addresses popup.

### F-AC-05: Badge count

- F-AC-05a: The Activity Center navigation button SHALL display the count of unseen notifications.
- F-AC-05b: The badge SHALL update in real time when new notifications arrive or existing ones are marked as read/seen.

### F-AC-06: Chronological ordering

Notifications SHALL be displayed in reverse chronological order (newest first) within the `StatusListView`.

### F-AC-07: Pagination / infinite scroll

- F-AC-07a: The notification list SHALL load additional notifications when the user scrolls to within the threshold of the bottom of the list.
- F-AC-07b: Loading SHALL be debounced at 100 ms intervals via `Backpressure.oneInTimeQueued`.

### F-AC-08: Mark as seen on exit

When the Activity Center view loses focus or the user navigates away, all currently displayed notifications SHALL be marked as seen via `markAsSeenActivityCenterNotifications()`.

### F-AC-09: News settings integration

- F-AC-09a: When RSS is disabled in Privacy & Security settings, the News category SHALL display an "Enable RSS" prompt instead of the notification list.
- F-AC-09b: When Status News notifications are disabled in Notification settings, the News category SHALL display an "Enable Status News notifications" prompt.
- F-AC-09c: When no news notifications exist (or all are read in unread-only mode), an appropriate empty state message SHALL be shown.

## Usability

### U-AC-01: Quick actions without context switch

Users SHALL be able to accept, decline, block, or dismiss notifications without navigating away from the Activity Center.

### U-AC-02: Visual distinction between read and unread

- U-AC-02a: Unread notifications SHALL have a visually distinct appearance from read notifications (background colour, indicator, or badge).
- U-AC-02b: The distinction SHALL be immediately visible without requiring user interaction.

### U-AC-03: Empty state messaging

- U-AC-03a: When no notifications exist, the Activity Center SHALL display: "Your notifications will appear here".
- U-AC-03b: When filtering to unread-only and all notifications are read, the Activity Center SHALL display: "You're all caught up".

### U-AC-04: Navigation to source content

- U-AC-04a: Tapping/clicking a mention or reply notification SHALL navigate the user directly to the source message in the correct chat/channel.
- U-AC-04b: Tapping/clicking a community notification SHALL navigate the user to the relevant community.

### U-AC-05: Profile access

All notification types that reference a contact SHALL provide access to the sender's profile popup via the notification avatar or header.

## Reliability

### R-AC-01: Notification ordering consistency

Notifications SHALL maintain consistent reverse-chronological ordering across app restarts and after network reconnections.

### R-AC-02: Real-time updates

- R-AC-02a: New notifications SHALL appear in the list without requiring manual refresh or page reload.
- R-AC-02b: Badge count SHALL update within 5 seconds of a new notification being received from the backend.

### R-AC-03: State sync across devices

When a notification is marked as read on one device, it SHALL be marked as read on all paired devices within 60 seconds, provided both devices are online.

### R-AC-04: Handling of notifications for deleted content

- R-AC-04a: If a community referenced by a notification has been deleted or the user has left it, the notification SHALL still render without crashing, using fallback data (empty community name, default colour).
- R-AC-04b: If a chat or message referenced by a mention/reply no longer exists, the navigation action SHALL fail gracefully (no crash, optional toast or silent no-op).

### R-AC-05: Concurrent action safety

If the user accepts a contact request or community invitation from the Activity Center while the same request is being processed on another device, the app SHALL not crash or produce duplicate accept/decline operations. The final state SHALL be deterministic.

### R-AC-06: Pagination resilience

If new notifications arrive while the user is scrolling through paginated results, the list SHALL not jump, duplicate items, or lose the user's scroll position.

## Performance

### P-AC-01: Activity Center open time

The Activity Center section SHALL be fully interactive within **1.5 seconds** of the user tapping the navigation button, measured from tap to first notification rendered.

### P-AC-02: Notification list render time

A list of **100 notifications** SHALL render completely within **2 seconds** on a device meeting minimum hardware requirements.

### P-AC-03: Pagination fetch latency

Loading the next page of notifications (triggered by scroll threshold) SHALL complete within **1 second** on a stable network connection (> 1 Mbps).

### P-AC-04: Real-time update latency

A new notification generated by the backend SHALL appear in an open Activity Center within **3 seconds** of being emitted.

### P-AC-05: Mark all as read latency

The "Mark all as read" action SHALL complete (UI updated, badge cleared) within **2 seconds** for up to 500 unread notifications.

### P-AC-06: Memory usage

The Activity Center SHALL not increase app memory usage by more than **50 MB** when displaying 500 notifications with loaded avatars and community images.

## Security

### S-AC-01: Contact request validation

- S-AC-01a: Contact request notifications SHALL only be displayed for requests originating from valid Waku messages signed by the sender's public key.
- S-AC-01b: Accept/decline actions SHALL be authenticated against the current user's identity before being sent to the backend.

### S-AC-02: Community invite authenticity

- S-AC-02a: Community invitation notifications SHALL only be displayed when the invitation can be verified against the community's public key or the inviting member's identity.
- S-AC-02b: Accepting a community invitation SHALL validate that the community still exists and the invitation has not been revoked.

### S-AC-03: Notification content sanitisation

Notification content (message previews, community names, contact display names) SHALL be sanitised to prevent injection of executable content or UI spoofing.

## Acceptance Criteria

### AC-AC-01: View all notification types
**Given** the user has received at least one notification of each type (contact request, mention, reply, community invitation, membership request, community kicked, news message)
**When** the user opens the Activity Center
**Then** each notification type is displayed with the correct visual layout and action buttons
**Verify by**: Manual QA — generate each notification type via multi-device setup

### AC-AC-02: Filter by category
**Given** the user has notifications in the Mentions and Contact Requests categories
**When** the user selects the "Mentions" filter tab
**Then** only mention notifications are displayed, and selecting "All" shows all types again
**Verify by**: Manual QA + Appium E2E

### AC-AC-03: Mark single notification as read
**Given** the user has an unread notification
**When** the user marks it as read (via context action)
**Then** the notification visually transitions to the read state and `unreadNotificationsCount` decreases by 1
**Verify by**: Appium E2E

### AC-AC-04: Mark all as read
**Given** the user has 10 unread notifications
**When** the user taps the "Mark all as Read" button
**Then** all notifications transition to read state, the badge count becomes 0, and the button becomes disabled
**Verify by**: Appium E2E

### AC-AC-05: Toggle unread-only view
**Given** the user has 5 read and 3 unread notifications
**When** the user taps the hide-read-notifications button
**Then** only 3 unread notifications are shown; tapping again shows all 8
**Verify by**: Appium E2E

### AC-AC-06: Accept contact request from Activity Center
**Given** User B has sent a contact request to User A
**When** User A opens Activity Center and taps "Accept" on the contact request notification
**Then** User B appears in User A's contacts list, and the notification action buttons are replaced with accepted state
**Verify by**: Manual QA + Appium E2E (multi-device)

### AC-AC-07: Decline contact request from Activity Center
**Given** User B has sent a contact request to User A
**When** User A opens Activity Center and taps "Decline" on the contact request notification
**Then** the contact request is dismissed, and User B does not appear in User A's contacts
**Verify by**: Manual QA + Appium E2E (multi-device)

### AC-AC-08: Navigate to mention source
**Given** the user has a mention notification referencing a message in community channel #general
**When** the user taps the mention notification
**Then** the app navigates to #general and scrolls to the mentioned message
**Verify by**: Manual QA

### AC-AC-09: Infinite scroll pagination
**Given** the user has 150 notifications and the initial page loads 50
**When** the user scrolls to the bottom of the list
**Then** the next batch of notifications loads seamlessly without duplicates or gaps
**Verify by**: Manual QA + Appium E2E (with seeded data)

### AC-AC-10: Badge count accuracy
**Given** the user has 7 unseen notifications
**When** the Activity Center is closed
**Then** the navigation button displays a badge with count 7; after opening and closing the Activity Center, the badge reflects the seen state
**Verify by**: Appium E2E

### AC-AC-11: News message settings integration
**Given** RSS is disabled in Privacy & Security settings
**When** the user selects the News category in Activity Center
**Then** the "Enable RSS" prompt is displayed instead of the notification list
**Verify by**: Manual QA

### AC-AC-12: Empty state display
**Given** the user has no notifications
**When** the user opens the Activity Center
**Then** the message "Your notifications will appear here" is displayed
**Verify by**: Manual QA + Appium E2E

## Edge Cases

### EC-AC-01: 1000+ unread notifications
**Scenario**: User accumulates 1000+ unread notifications while offline.
**Expected**: Activity Center opens within P-AC-01 threshold. Pagination loads incrementally. Badge displays count (or "999+" if capped). "Mark all as read" completes within 5 seconds.

### EC-AC-02: Notification for a left community
**Scenario**: User receives a mention notification in a community, then leaves that community before opening Activity Center.
**Expected**: The notification renders with fallback data (empty community name/image). Tapping it does not crash the app. Navigation action is a no-op or shows a toast.

### EC-AC-03: Simultaneous accept/decline from multiple devices
**Scenario**: User A opens Activity Center on Device 1 and Device 2 simultaneously. User taps "Accept" on Device 1 and "Decline" on Device 2 for the same contact request.
**Expected**: One action wins (first-write-wins or last-write-wins). The final state is consistent on both devices. No duplicate contact entries or orphaned requests.

### EC-AC-04: New notifications while Activity Center is open
**Scenario**: User has Activity Center open and a new mention notification arrives.
**Expected**: The new notification appears at the top of the list without disrupting scroll position or causing a full list reload.

### EC-AC-05: Rapid filter switching
**Scenario**: User rapidly switches between All, Mentions, Replies, and Contact Requests filter tabs within 1 second.
**Expected**: The list updates correctly for the final selected filter. No stale data from intermediate filter states is displayed.

### EC-AC-06: Notification for deleted message
**Scenario**: A reply notification references a message that has since been deleted by its author.
**Expected**: The notification still renders (with a placeholder or "Message deleted" indicator). Navigation action fails gracefully.

### EC-AC-07: Network disconnection during accept action
**Scenario**: User taps "Accept" on a community membership request while the network drops.
**Expected**: The action is queued or retried. The UI shows a pending/loading state rather than silently failing. If retry fails, the notification reverts to its actionable state.

### EC-AC-08: Activity Center opened during initial sync
**Scenario**: User opens Activity Center immediately after login while the app is still syncing historical notifications.
**Expected**: Already-loaded notifications display immediately. New notifications appear incrementally as sync completes. No blank screen or loading spinner for more than 3 seconds.

### EC-AC-09: Owner token received for unknown community
**Scenario**: An ownership transfer notification arrives for a community ID that the local database does not yet have metadata for.
**Expected**: The notification renders with fallback styling. Once community metadata is fetched, the notification updates to show the community name and colour.

## Test Coverage Matrix

| Acceptance Criteria | Manual QA | Appium E2E | Squish Desktop | API Test |
|---|---|---|---|---|
| AC-AC-01 (all types) | ✅ | — | ✅ (partial, contact requests) | — |
| AC-AC-02 (filter) | ✅ | ✅ (planned) | — | — |
| AC-AC-03 (mark read) | ✅ | ✅ (planned) | — | — |
| AC-AC-04 (mark all read) | ✅ | ✅ (planned) | — | — |
| AC-AC-05 (toggle unread) | ✅ | ✅ (planned) | — | — |
| AC-AC-06 (accept contact) | ✅ | ✅ (planned, multi-device) | ✅ (existing) | — |
| AC-AC-07 (decline contact) | ✅ | ✅ (planned, multi-device) | ✅ (existing) | — |
| AC-AC-08 (navigate mention) | ✅ | — | — | — |
| AC-AC-09 (pagination) | ✅ | ✅ (planned) | — | — |
| AC-AC-10 (badge count) | ✅ | ✅ (planned) | — | — |
| AC-AC-11 (news settings) | ✅ | — | — | — |
| AC-AC-12 (empty state) | ✅ | ✅ (planned) | — | — |

## Existing Test Infrastructure

### Desktop E2E (Squish) — Partial coverage

- **Page object**: `test/e2e/gui/components/activity_center.py` — `ActivityCenter`, `ContactRequest` classes with `accept_contact_request`, `find_contact_request_in_list`
- **Locators**: `test/e2e/gui/objects_map/activity_center_names.py` — `activityCenterLeftPanel`, `activityCenterListView`, `activityCenterContactRequest`, accept/decline/more buttons
- **Tests**: `test/e2e/tests/settings/settings_messaging/test_block_unblock_user.py`, `test/e2e/tests/crtitical_tests_prs/test_messaging_group_chat.py` — both use Activity Center for contact request acceptance

### Appium E2E — No coverage

No Activity Center page objects, locators, or tests exist in `test/e2e_appium/`.

**Reusable adjacent infrastructure**:
- `test/e2e_appium/pages/messaging/` — `ChatPage`, `CreateChatPage`, `MessageContextMenuPage`
- `test/e2e_appium/pages/settings/contacts_page.py` — `ContactsSettingsPage` with contact request handling
- `test/e2e_appium/locators/messaging/` — chat, message context menu locators
- `test/e2e_appium/locators/settings/contacts_locators.py` — contact tab, pending tab, accept button
- `test/e2e_appium/tests/messaging/conftest.py` — `established_chat` fixture for multi-device contact setup

### QML objectNames already in place

| objectName | Element | File |
|---|---|---|
| `activityCenterLeftPanel` | Left panel layout | `ActivityCenterLayout.qml` |
| `markAllReadButton` | Mark all read button | `ActivityCenterLayout.qml` |
| `hideReadNotificationsButton` | Toggle read/unread filter | `ActivityCenterLayout.qml` |
| `activityCenterGroupButton` | Category filter buttons | `ActivityCenterTypes.qml` / Top bar |
| `acceptBtn` | Accept contact request | `ContactRequestCta.qml` |
| `declineBtn` | Decline contact request | `ContactRequestCta.qml` |
| `moreBtn` | More options on contact request | `ContactRequestCta.qml` |

### Missing objectNames (needed for Appium automation)

- Individual notification cards (no `objectName` on delegate loaders)
- Notification type indicators within cards
- Badge count element on navigation button
- News "Read More" button
- Pair/sync dialog buttons
- Community action buttons (accept/decline membership)
