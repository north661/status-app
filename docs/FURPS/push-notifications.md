# Push Notifications FURPS

**Epic**: Push Notifications — Release 2.38 (mid-March)
**Figma**: TBD
**Risk Level**: 🟡 Medium (notification content may contain private message previews; token delivery and registration)

---

## Summary

Push notifications allow Status App users to receive timely alerts for new messages, mentions, and activity across 1-to-1 chats, group chats, and communities — even when the app is in the background or killed. The feature relies on platform-specific delivery services (APNs for iOS, FCM for Android) while preserving the app's privacy-centric design by allowing users to control what notification content is exposed to third-party services.

---

## Functionality

| ID | Requirement |
|----|-------------|
| PN-F-01 | The app SHALL deliver push notifications for new messages in 1-to-1 chats, group chats, and community channels. |
| PN-F-02 | The app SHALL register with the platform push notification service (APNs on iOS, FCM on Android) on first launch after login and store the resulting push token locally. |
| PN-F-03 | The app SHALL provide per-channel-type notification settings allowing users to enable or disable notifications for 1-to-1 chats, group chats, and community channels independently. |
| PN-F-04 | The app SHALL provide a notification content preview toggle: when enabled, notifications display sender name and message excerpt; when disabled, notifications display a generic "New message" text only. |
| PN-F-05 | Tapping a push notification SHALL deep-link the user to the specific chat or community channel that generated the notification. |
| PN-F-06 | The app SHALL maintain an accurate badge count reflecting the total number of unread conversations with pending notifications. |
| PN-F-07 | The app SHALL support per-conversation and per-community-channel mute, suppressing notifications for the muted item for a user-selected duration (1 hour, 8 hours, 1 day, 1 week, or until unmuted). |
| PN-F-08 | The app SHALL support a global Do Not Disturb mode that suppresses all push notifications while active. |
| PN-F-09 | The app SHALL transmit the push token to the Status push notification server over an authenticated, encrypted channel. |
| PN-F-10 | When a user logs out or switches accounts, the app SHALL unregister the push token from the notification server for the previous account. |

---

## Usability

| ID | Requirement |
|----|-------------|
| PN-U-01 | Notification preference settings SHALL be accessible from Settings > Notifications within 2 taps from the home screen. |
| PN-U-02 | Each notification toggle SHALL provide immediate visual feedback (switch state change) within 200 ms of user interaction. |
| PN-U-03 | When the user disables notifications at the OS level, the app SHALL display an in-app banner with a direct link to the OS notification settings. |
| PN-U-04 | Notifications from the same conversation SHALL be grouped (stacked) on both iOS and Android, showing the conversation name as the group title and the count of unread messages. |
| PN-U-05 | Notification grouping SHALL collapse to a single summary notification when more than 5 notifications from the same conversation are pending. |
| PN-U-06 | The mute duration picker SHALL present the options (1 hour, 8 hours, 1 day, 1 week, Until unmuted) in a bottom sheet or popover accessible from the conversation context menu. |

---

## Reliability

| ID | Requirement |
|----|-------------|
| PN-R-01 | When a push token expires or is revoked by the platform, the app SHALL automatically request a new token and re-register with the notification server within 60 seconds of detecting the invalidation. |
| PN-R-02 | When the device transitions between network types (Wi-Fi ↔ cellular) or recovers from airplane mode, the app SHALL verify push token validity and re-register if necessary within 30 seconds of connectivity restoration. |
| PN-R-03 | If the Status push notification server is unreachable, the app SHALL retry token registration using exponential backoff (initial delay 5 s, max delay 5 min, max retries 10) and log each failure. |
| PN-R-04 | The app SHALL persist notification preference state locally so that settings survive app restarts, OS updates, and crashes without data loss. |
| PN-R-05 | If a push notification payload cannot be decrypted or parsed, the app SHALL display a fallback notification with the text "New activity in Status" rather than silently dropping it. |

---

## Performance

| ID | Requirement |
|----|-------------|
| PN-P-01 | A push notification SHALL be delivered to the recipient device within 5 seconds of the message being sent, measured end-to-end under normal network conditions (< 100 ms RTT, > 1 Mbps bandwidth). |
| PN-P-02 | The background notification service SHALL consume less than 2% of battery per hour when the app is in the background and no notifications are being received. |
| PN-P-03 | The background notification listener SHALL consume less than 30 MB of RAM when the app is in the background. |
| PN-P-04 | Push token registration (including server round-trip) SHALL complete within 3 seconds on a stable network connection. |
| PN-P-05 | Deep-linking from a notification tap to the target chat screen SHALL complete within 1.5 seconds, including app cold-start if the app was killed. |

---

## Security

| ID | Requirement |
|----|-------------|
| PN-S-01 | **Data protection**: When notification content preview is disabled (PN-F-04), the notification payload sent to APNs/FCM SHALL NOT contain message body text, sender display name, or any user-generated content. |
| PN-S-02 | **Data protection**: When Privacy Mode is enabled globally, the app SHALL automatically disable notification content previews (equivalent to PN-F-04 disabled) regardless of the user's notification preview setting. |
| PN-S-03 | **Token security**: The push token SHALL be stored in the platform secure storage (iOS Keychain / Android Keystore) and SHALL NOT be written to plain-text logs or shared preferences. |
| PN-S-04 | **Token security**: Push token transmission to the Status notification server SHALL use TLS 1.2 or higher with certificate pinning. |
| PN-S-05 | **Third-party exposure**: The only data sent to APNs/FCM SHALL be the device push token and an opaque encrypted payload; no plaintext message content, chat identifiers, or user identifiers SHALL be included in the push payload metadata visible to Apple or Google. |
| PN-S-06 | **Third-party exposure**: The app's privacy policy and notification settings screen SHALL disclose that Apple (APNs) or Google (FCM) act as intermediaries for push delivery. |

---

## Acceptance Criteria

### AC-PN-01: Basic notification delivery for 1-to-1 chat
**Given** User A and User B are contacts with notifications enabled
**When** User A sends a message to User B and User B's app is in the background
**Then** User B receives a push notification within 5 seconds displaying the sender name and message preview
**Verify by**: Manual QA on physical iOS and Android devices

### AC-PN-02: Notification delivery for group chat
**Given** User A is a member of a group chat with notifications enabled
**When** another member sends a message to the group and User A's app is in the background
**Then** User A receives a push notification showing the group name, sender name, and message preview
**Verify by**: Manual QA on physical iOS and Android devices

### AC-PN-03: Notification delivery for community channel
**Given** User A is a member of a community channel with notifications enabled
**When** another member posts a message in the channel and User A's app is in the background
**Then** User A receives a push notification showing the community name, channel name, and sender
**Verify by**: Manual QA on physical iOS and Android devices

### AC-PN-04: Notification content preview toggle
**Given** User A has notification content preview disabled in Settings > Notifications
**When** User A receives a new message while the app is in the background
**Then** the push notification displays "New message" without revealing sender name or message content
**Verify by**: Manual QA; Appium E2E for settings toggle state

### AC-PN-05: Deep-link from notification to chat
**Given** User A receives a push notification for a 1-to-1 chat message
**When** User A taps the notification
**Then** the app opens (or foregrounds) and navigates directly to the 1-to-1 chat with the new message visible, within 1.5 seconds
**Verify by**: Manual QA on physical devices

### AC-PN-06: Per-conversation mute
**Given** User A has muted a specific conversation for 1 hour
**When** a new message arrives in that conversation within the mute window
**Then** no push notification is delivered for that conversation; other conversations still deliver notifications normally
**Verify by**: Manual QA; Appium E2E for mute settings persistence

### AC-PN-07: Do Not Disturb mode
**Given** User A has enabled Do Not Disturb mode
**When** new messages arrive in any chat
**Then** no push notifications are delivered until Do Not Disturb is disabled
**Verify by**: Manual QA

### AC-PN-08: Badge count accuracy
**Given** User A has 3 unread conversations
**When** User A reads one conversation and a new message arrives in a fourth conversation
**Then** the badge count updates to 3 (2 remaining unread + 1 new)
**Verify by**: Manual QA on physical devices

### AC-PN-09: Privacy Mode interaction
**Given** User A has Privacy Mode enabled globally
**When** User A receives a push notification
**Then** the notification displays "New activity in Status" with no sender, message content, or chat identifier
**Verify by**: Manual QA; verify notification payload does not contain plaintext content

### AC-PN-10: Token re-registration on network change
**Given** the device transitions from Wi-Fi to cellular
**When** the app detects the network change
**Then** the app verifies the push token and re-registers with the notification server within 30 seconds if the token is invalid
**Verify by**: API test monitoring token registration requests; manual QA with network switching

---

## Edge Cases

| ID | Scenario | Expected Behaviour |
|----|----------|--------------------|
| PN-E-01 | Notification received while app is in the foreground | In-app toast notification is displayed instead of a system push notification; no duplicate OS notification. |
| PN-E-02 | Notification received after app is force-killed by user | OS delivers the push notification normally via APNs/FCM; tapping it cold-starts the app and deep-links to the chat. |
| PN-E-03 | User has notifications disabled at the OS level | App detects the disabled state and displays an in-app banner directing the user to OS settings; no crash or error. |
| PN-E-04 | Privacy Mode enabled after notification preview was on | Notification content preview is automatically disabled; pending queued notifications are not retroactively modified, but all new notifications use the privacy-safe format. |
| PN-E-05 | Multiple devices registered for the same account | Push notification is delivered to all registered devices; reading the message on one device clears the badge count on all devices within 60 seconds. |
| PN-E-06 | Community @mention vs general channel message | @mention notifications SHALL be delivered even if the user has general channel notifications muted; only a full mute suppresses @mention notifications. |
| PN-E-07 | Push token expires while app is not running | On next app launch, the app detects the expired token, requests a new one, and re-registers before processing any pending messages. |
| PN-E-08 | Notification server returns an error during registration | The app retries with exponential backoff per PN-R-03; the user is not shown an error unless all retries are exhausted, at which point a non-blocking banner is shown. |
| PN-E-09 | User logs out and logs in with a different account | The previous account's push token is unregistered; the new account registers a fresh token; no notifications from the old account are delivered. |
| PN-E-10 | Corrupted or unrecognised notification payload | A fallback notification "New activity in Status" is displayed per PN-R-05; the corruption event is logged for diagnostics. |

---

## Test Coverage Matrix

| Acceptance Criteria | Manual QA | Appium E2E | API Test | Squish (Desktop) |
|---------------------|-----------|------------|----------|-------------------|
| AC-PN-01 (1-to-1 delivery) | ✅ | Planned | — | N/A (mobile-only) |
| AC-PN-02 (Group delivery) | ✅ | Planned | — | N/A |
| AC-PN-03 (Community delivery) | ✅ | Planned | — | N/A |
| AC-PN-04 (Content preview toggle) | ✅ | Planned | — | N/A |
| AC-PN-05 (Deep-link) | ✅ | Planned | — | N/A |
| AC-PN-06 (Per-conversation mute) | ✅ | Planned | — | N/A |
| AC-PN-07 (DND mode) | ✅ | — | — | N/A |
| AC-PN-08 (Badge count) | ✅ | Planned | — | N/A |
| AC-PN-09 (Privacy Mode) | ✅ | Planned | Planned | N/A |
| AC-PN-10 (Token re-registration) | ✅ | — | Planned | N/A |

### Existing Reusable Infrastructure

- `test/e2e_appium/pages/settings/messaging_page.py` — `MessagingSettingsPage` (may extend for notification settings)
- `test/e2e_appium/locators/settings/messaging_locators.py` — messaging settings locators (base for notification locators)
- `test/e2e_appium/pages/settings/settings_page.py` — `SettingsPage.open_messaging_settings()`
- `test/e2e_appium/pages/app.py` — `App.wait_for_toast()`, `App.is_toast_present()` (in-app notification verification)
- `test/e2e_appium/locators/app_locators.py` — `TOAST_MESSAGE`, `ANY_TOAST` locators

### New Infrastructure Needed

- `test/e2e_appium/pages/settings/notifications_page.py` — page object for notification settings screen
- `test/e2e_appium/locators/settings/notification_locators.py` — locators for notification toggles, preview settings, DND
- OS notification interaction helpers (Appium `open_notifications()`, notification element locators)
- Push notification trigger mechanism for E2E tests (second device or API-driven message send)
