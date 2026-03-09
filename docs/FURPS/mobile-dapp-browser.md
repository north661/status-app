# Mobile DApp Browser FURPS ([#19535](https://github.com/status-im/status-app/issues/19535))

**Desktop DApp Browser Spec**: [dapp-browser.md](dapp-browser.md)
**Risk Level**: 🔴 High (transaction signing, wallet integration)
**Release Target**: 2.38

---

## Summary

The Mobile DApp Browser enables users on iOS and Android to browse and interact with decentralised applications (DApps) from within the Status app. Unlike the desktop variant which uses an embedded QtWebEngine browser, the mobile implementation SHALL use the platform's native browser (iOS Safari WebView / Android WebView) or delegate to the system browser, with wallet connectivity provided via WalletConnect or a native bridge for transaction signing and message signing.

---

## Functionality

- **F-MDB-001**: The app SHALL launch a DApp URL in a mobile browser context (in-app WebView or system browser) when a user taps a DApp link from chat, the home page, or the browser section.
- **F-MDB-002**: The app SHALL support wallet connection to DApps via WalletConnect v2 protocol, including session proposal, approval, and rejection flows.
- **F-MDB-003**: The app SHALL support wallet connection to DApps via a native bridge (StatusConnect / BrowserConnect) when using an in-app WebView, injecting an EIP-1193-compliant `window.ethereum` provider.
- **F-MDB-004**: The app SHALL present transaction signing requests to the user with a modal overlay showing: recipient address, value, gas estimate, and network name.
- **F-MDB-005**: The app SHALL present message signing requests (personal_sign, eth_signTypedData) to the user with a modal showing the message content.
- **F-MDB-006**: The app SHALL support Sign-In with Ethereum (SIWE) flows initiated by DApps.
- **F-MDB-007**: The app SHALL handle `status-app://` deep links containing WalletConnect URIs (`/wc?uri=...`) by initiating a WalletConnect pairing session.
- **F-MDB-008**: The app SHALL handle deep links from external browsers or other apps to return the user to the Status app after a DApp interaction.
- **F-MDB-009**: The app SHALL maintain a list of active DApp sessions, displaying connected DApps with their name, icon, and connected chain(s).
- **F-MDB-010**: The app SHALL allow the user to disconnect from a DApp session from the active sessions list.
- **F-MDB-011**: The app SHALL allow the user to select which wallet account and which network chain(s) to use when connecting to a DApp.
- **F-MDB-012**: The app SHALL handle DApp links shared in chat messages by opening the DApp browser when the link is tapped.

---

## Usability

- **U-MDB-001**: Transaction and message signing prompts SHALL be displayed as full-width bottom sheets occupying at least 60% of the screen height, ensuring all critical information (amount, recipient, network) is visible without scrolling on devices with screen width ≥ 320dp.
- **U-MDB-002**: The DApp connection approval modal SHALL present the DApp name, icon, requested permissions, and account/chain selectors within a single scrollable view.
- **U-MDB-003**: Navigation from the Status app to the DApp browser and back SHALL require no more than 2 taps (e.g., tap DApp link → browser opens; tap back/home → return to Status).
- **U-MDB-004**: On Android, the system back button and swipe-back gesture SHALL navigate back within the DApp browser context. When at the first page, the gesture SHALL return the user to the Status app.
- **U-MDB-005**: On iOS, the swipe-from-left-edge gesture SHALL navigate back within the DApp browser context, consistent with iOS navigation conventions.
- **U-MDB-006**: Active WalletConnect sessions SHALL be accessible from the wallet section in no more than 2 taps from the wallet home screen.
- **U-MDB-007**: When a signing request arrives while the app is in the foreground, the signing modal SHALL appear within 1 second of receipt.

---

## Reliability

- **R-MDB-001**: WalletConnect sessions SHALL persist across app backgrounding and foregrounding. A session active before backgrounding SHALL remain active when the app returns to the foreground.
- **R-MDB-002**: WalletConnect sessions SHALL persist across app process kills, provided the session has not expired. On next app launch, previously active sessions SHALL be restored from local storage.
- **R-MDB-003**: If a transaction signing request fails (user rejection, network error, or timeout), the app SHALL display an error message specifying the failure reason and SHALL NOT submit the transaction.
- **R-MDB-004**: If network connectivity is lost during a DApp interaction, the app SHALL display a connectivity warning within 5 seconds and SHALL NOT silently fail any pending signing request.
- **R-MDB-005**: If the app is backgrounded during a signing flow, the signing request SHALL remain pending for at least 5 minutes. A local notification SHALL be sent reminding the user of the pending request.
- **R-MDB-006**: If a DApp requests an unsupported chain, the app SHALL display an error stating the chain is not supported and SHALL NOT connect.
- **R-MDB-007**: If the wallet is locked (password/biometric required) when a signing request arrives, the app SHALL prompt for authentication before displaying the signing details.
- **R-MDB-008**: WalletConnect session expiry SHALL be handled gracefully; when a session expires, the app SHALL remove it from the active sessions list and notify the user.

---

## Performance

- **P-MDB-001**: The DApp browser (WebView or system browser) SHALL launch and display first contentful paint within 3 seconds on a device with ≥ 3 GB RAM on a stable Wi-Fi connection.
- **P-MDB-002**: A WalletConnect pairing request initiated via deep link SHALL present the session proposal modal within 2 seconds of link activation.
- **P-MDB-003**: Transaction signing modal SHALL render within 500 ms of the signing request being received from the DApp.
- **P-MDB-004**: The mobile DApp browser process (WebView) SHALL not consume more than 150 MB of additional RAM beyond the base app memory footprint.
- **P-MDB-005**: Switching between the Status app and the DApp browser (app-to-browser-to-app) SHALL complete within 1 second per transition.
- **P-MDB-006**: The active DApp sessions list SHALL load and display within 500 ms of navigation.

---

## Security

### Threat Considerations

- **S-MDB-T01**: Phishing DApps may impersonate legitimate DApps to trick users into signing malicious transactions. The app SHALL display the DApp URL prominently in all signing prompts, and the URL SHALL NOT be truncatable or hideable by the DApp.
- **S-MDB-T02**: Transaction manipulation — a compromised DApp may alter transaction parameters after user review. The app SHALL sign only the exact parameters displayed to the user; no mutation of transaction data SHALL occur between display and signing.
- **S-MDB-T03**: Session hijacking — WalletConnect session keys SHALL be stored in platform-secure storage (iOS Keychain / Android Keystore) and SHALL NOT be accessible to other apps.

### Data Protection

- **S-MDB-D01**: Private keys SHALL never be exposed to the browser context (WebView or system browser). All signing operations SHALL occur within the Status app's secure enclave / wallet module.
- **S-MDB-D02**: The EIP-1193 provider injected into the WebView SHALL NOT expose account private keys, seed phrases, or signing keys through any JavaScript API.
- **S-MDB-D03**: WalletConnect session data stored locally SHALL be encrypted at rest using the app's data protection mechanisms.

### Network Exposure

- **S-MDB-N01**: The mobile DApp browser SHALL make external network calls only to: (a) the DApp URL loaded by the user, (b) WalletConnect relay servers (relay.walletconnect.com), and (c) Ethereum RPC endpoints configured in the app.
- **S-MDB-N02**: When Privacy Mode is enabled, WalletConnect connections and DApp browser functionality SHALL be disabled, consistent with [privacy-mode.md](privacy-mode.md).

### Recovery

- **S-MDB-R01**: If a signing operation is interrupted (app crash, network drop), no partial transaction SHALL be broadcast. The user SHALL be able to retry or cancel on recovery.
- **S-MDB-R02**: If a WalletConnect session becomes corrupted, the app SHALL allow the user to force-disconnect and re-pair.

---

## Acceptance Criteria

### AC-MDB-001: Launch DApp from chat link
**Given** the user has an active wallet account and is viewing a chat message containing a DApp URL
**When** the user taps the DApp URL
**Then** the DApp browser opens displaying the DApp's content, and the browser address bar shows the tapped URL
**Verify by**: Manual QA on iOS and Android; Appium E2E test

### AC-MDB-002: WalletConnect pairing via deep link
**Given** the user has the Status app installed and a DApp presents a WalletConnect QR code / deep link
**When** the user activates the `status-app://.../wc?uri=<wc_uri>` deep link
**Then** the Status app opens, displays the session proposal modal with the DApp name, icon, and requested permissions within 2 seconds
**Verify by**: Manual QA; Appium E2E test with deep link intent

### AC-MDB-003: Approve WalletConnect session
**Given** the session proposal modal is displayed with account and chain selectors
**When** the user selects an account and chain(s) and taps "Connect"
**Then** the DApp session is established, the DApp appears in the active sessions list, and the DApp receives the connected accounts
**Verify by**: Manual QA; Appium E2E test

### AC-MDB-004: Transaction signing on mobile
**Given** a DApp sends a transaction signing request via an active session
**When** the signing modal appears
**Then** the modal displays the recipient address, value, gas estimate, network name, and DApp URL; the user can approve or reject; approved transactions are submitted to the network; rejected transactions return an error to the DApp
**Verify by**: Manual QA with test DApp; Appium E2E test

### AC-MDB-005: Session persistence across backgrounding
**Given** the user has an active WalletConnect session and backgrounds the app
**When** the user returns to the app within the session TTL
**Then** the session remains active and the DApp can still send requests
**Verify by**: Manual QA; Appium E2E test (background app → foreground → verify session)

### AC-MDB-006: Session persistence across app kill
**Given** the user has an active WalletConnect session and force-kills the app
**When** the user relaunches the app
**Then** the previously active session is restored and appears in the active sessions list
**Verify by**: Manual QA (kill app → relaunch → check sessions)

### AC-MDB-007: Disconnect DApp session
**Given** the user has an active DApp session listed in the wallet section
**When** the user taps "Disconnect" on that session
**Then** the session is terminated, removed from the list, and the DApp is notified of disconnection
**Verify by**: Manual QA; Appium E2E test

### AC-MDB-008: Network loss during DApp interaction
**Given** the user is interacting with a DApp and a signing request is pending
**When** network connectivity is lost
**Then** a connectivity warning is displayed within 5 seconds; the pending request is not silently dropped
**Verify by**: Manual QA (toggle airplane mode during signing flow)

### AC-MDB-009: Unsupported chain requested
**Given** a DApp requests connection on a chain not configured in the user's wallet
**When** the session proposal is received
**Then** the app displays an error indicating the chain is not supported and does not establish a connection
**Verify by**: Manual QA with test DApp requesting unsupported chain

### AC-MDB-010: Wallet locked during signing
**Given** the user's wallet requires authentication (password/biometric) and a signing request arrives
**When** the signing modal would normally appear
**Then** the app first prompts for wallet authentication; only after successful auth is the signing modal displayed
**Verify by**: Manual QA (lock wallet → trigger signing request)

### AC-MDB-011: Privacy Mode blocks DApp browser
**Given** Privacy Mode is enabled in settings
**When** the user attempts to open a DApp or initiate a WalletConnect connection
**Then** the app displays a message indicating DApp browser is disabled in Privacy Mode and does not open the browser or initiate the connection
**Verify by**: Manual QA; Appium E2E test

---

## Edge Cases

| ID | Scenario | Expected Behaviour |
|----|----------|--------------------|
| EC-MDB-001 | DApp browser launched with no internet connectivity | App displays "No internet connection" error; does not show a blank or broken page |
| EC-MDB-002 | Wallet locked during transaction signing request | App prompts for authentication before showing signing details (see R-MDB-007) |
| EC-MDB-003 | DApp requests connection on an unsupported chain | App rejects with clear error message (see R-MDB-006) |
| EC-MDB-004 | App backgrounded during active signing flow | Signing request preserved for ≥ 5 minutes; local notification sent (see R-MDB-005) |
| EC-MDB-005 | Multiple DApps request signing simultaneously | App queues requests and presents them sequentially; no request is silently dropped |
| EC-MDB-006 | WalletConnect deep link received while app is not running | App cold-starts, completes initialisation, then presents the session proposal |
| EC-MDB-007 | DApp sends malformed transaction data | App validates transaction fields; displays error for invalid data; does not sign |
| EC-MDB-008 | User rotates device during signing modal | Modal adapts to new orientation; no data loss or dismissal |
| EC-MDB-009 | Low memory condition during WebView browsing | App releases non-critical resources; if WebView is reclaimed by OS, user is notified and can reload |
| EC-MDB-010 | DApp attempts to open popup or redirect to external URL | Popup is blocked or presented with user consent; redirects to non-DApp URLs open in system browser |

---

## Suggested Test Coverage

### Manual QA
- Full DApp browser launch and navigation flow on iOS and Android
- WalletConnect pairing via QR code scan and deep link
- Transaction signing and message signing end-to-end with test DApps (e.g., WalletConnect example DApp)
- Session persistence across background, kill, and network changes
- Privacy Mode enforcement
- Platform-specific gesture navigation (back button, swipe gestures)

### Appium E2E (Mobile)
- `test_dapp_browser_launch_from_chat_link` — AC-MDB-001
- `test_walletconnect_deep_link_pairing` — AC-MDB-002
- `test_walletconnect_session_approve` — AC-MDB-003
- `test_dapp_transaction_signing` — AC-MDB-004
- `test_session_persistence_backgrounding` — AC-MDB-005
- `test_dapp_session_disconnect` — AC-MDB-007
- `test_privacy_mode_blocks_dapp` — AC-MDB-011

### Squish E2E (Desktop) — Not applicable
Desktop DApp browser coverage is tracked in [dapp-browser.md](dapp-browser.md).

### Existing Storybook QML Tests (Component Level)
- `tst_DAppsWorkflow.qml` — DApp session proposal, approval, signing flows
- `tst_WCDAppsProvider.qml` — WalletConnect provider session management
- `tst_BCDAppsProvider.qml` — BrowserConnect provider session management
- `tst_ConnectDAppModal.qml` — Connection modal states and interactions
- `tst_SignRequestPlugin.qml` — Sign request accept/reject flows
- `tst_SiweRequestPlugin.qml` — Sign-In with Ethereum flows
