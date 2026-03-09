# Mobile DApp Browser FURPS

**Epic**: Mobile DApp Browser (Release 2.38)
**Related Desktop Spec**: [dapp-browser.md](dapp-browser.md) ([#17970](https://github.com/status-im/status-app/issues/17970))
**Risk Level**: 🔴 High (transaction signing, wallet integration)

---

## Summary

The Mobile DApp Browser allows users on iOS and Android to open and interact with decentralised applications (DApps) from within the Status mobile app. The feature uses the platform's native system browser (Safari on iOS, WebView on Android) and integrates with the Status wallet for transaction signing and message signing via WalletConnect or a native bridge. It handles DApp links shared in chat messages and maintains wallet sessions across the mobile app lifecycle.

---

## Functionality

- **F-MDB-01**: The app SHALL launch DApp URLs in the platform's native browser context (iOS Safari View Controller / Android Custom Tab or WebView).
- **F-MDB-02**: The browser SHALL connect to the user's Status wallet via WalletConnect v2 protocol or a native bridge for transaction and message signing.
- **F-MDB-03**: When a DApp requests a transaction signature, the app SHALL present a signing prompt overlay showing the transaction details (recipient, amount, gas estimate, network).
- **F-MDB-04**: When a DApp requests a message signature (personal_sign, eth_signTypedData), the app SHALL present the message content for user review before signing.
- **F-MDB-05**: The user SHALL be able to approve or reject any signing request from the prompt.
- **F-MDB-06**: DApp links shared in chat messages SHALL be tappable and open in the mobile DApp browser context.
- **F-MDB-07**: The app SHALL maintain a WalletConnect session with the DApp across app backgrounding and foregrounding within the same session lifetime.
- **F-MDB-08**: The app SHALL allow the user to disconnect a DApp session explicitly from a session management screen.
- **F-MDB-09**: The app SHALL support switching between accounts and networks when a DApp requests a chain switch (wallet_switchEthereumChain).
- **F-MDB-10**: The browser context SHALL support standard navigation controls: back, forward, reload, and close.

---

## Usability

- **U-MDB-01**: Signing prompts SHALL be displayed as a modal sheet occupying at least 60% of the screen height, ensuring all transaction details are visible without scrolling on devices with screen width ≥ 320pt.
- **U-MDB-02**: The signing prompt SHALL display the DApp name, DApp icon (if available), and the connected account address.
- **U-MDB-03**: Approve and Reject buttons on signing prompts SHALL have a minimum touch target of 44×44pt (iOS) / 48×48dp (Android).
- **U-MDB-04**: Navigating back from the browser to the Status app SHALL use the platform's standard back gesture (swipe-from-left on iOS, system back on Android) or an explicit close button.
- **U-MDB-05**: When a DApp link is tapped in chat, the browser SHALL open within 1 tap — no intermediate confirmation dialog unless the link domain has not been visited before.
- **U-MDB-06**: The connected wallet account and network SHALL be visible in the browser toolbar or header at all times while a DApp session is active.
- **U-MDB-07**: A warning banner SHALL be displayed when the user navigates to a DApp URL that is not on a known-safe list, showing the full domain name.

---

## Reliability

- **R-MDB-01**: If the app is backgrounded for fewer than 5 minutes during an active DApp session, the session SHALL be restored automatically when the app returns to the foreground.
- **R-MDB-02**: If the app is killed by the OS or backgrounded for more than 5 minutes, the WalletConnect session SHALL be re-established on next app launch if the session has not expired on the DApp side.
- **R-MDB-03**: If a transaction signing request fails (network error, insufficient gas, nonce conflict), the app SHALL display an error message specifying the failure reason and allow the user to retry or dismiss.
- **R-MDB-04**: If network connectivity is lost during a DApp interaction, the app SHALL display a connectivity warning within 3 seconds and queue no further signing requests until connectivity is restored.
- **R-MDB-05**: If the wallet is locked (biometrics/password required) when a signing request arrives, the app SHALL prompt the user to unlock before presenting the signing details.
- **R-MDB-06**: If the DApp requests an unsupported chain, the app SHALL display a message stating the chain is not supported and SHALL NOT attempt to sign on a different chain.
- **R-MDB-07**: The browser context SHALL handle DApp JavaScript errors without crashing the host app. Errors SHALL be logged but not shown to the user.

---

## Performance

- **P-MDB-01**: Browser launch time (from user tap to browser content visible) SHALL be < 2 seconds on devices meeting minimum OS requirements (iOS 16+, Android 9+) on a stable Wi-Fi connection.
- **P-MDB-02**: DApp page load time (DOMContentLoaded) SHALL be < 5 seconds for DApps under 5 MB initial payload on a 10 Mbps connection.
- **P-MDB-03**: Signing prompt display time (from DApp request to prompt visible) SHALL be < 1 second.
- **P-MDB-04**: The mobile DApp browser context SHALL not increase the app's resident memory usage by more than 150 MB above baseline.
- **P-MDB-05**: WalletConnect session handshake (pairing to connected state) SHALL complete in < 3 seconds on a stable connection.
- **P-MDB-06**: Closing the browser context SHALL release its allocated memory within 5 seconds, returning to within 20 MB of pre-browser baseline.

---

## Security

### Threat Considerations

- **S-MDB-01**: Phishing DApps may impersonate legitimate DApps to trick users into signing malicious transactions. The app SHALL display the full DApp domain URL in the signing prompt, not just the DApp-provided name.
- **S-MDB-02**: Transaction manipulation — a compromised DApp may alter transaction parameters after the user reviews them. The signing prompt SHALL display the exact transaction data that will be signed, and no modification SHALL occur between user approval and signature submission.
- **S-MDB-03**: The app SHALL implement EIP-712 structured data display for typed data signing requests so users can verify the data being signed.

### Data Protection

- **S-MDB-04**: Private keys SHALL never be exposed to the browser context, WebView, or any DApp JavaScript execution environment.
- **S-MDB-05**: The WalletConnect session key SHALL be stored in the platform's secure storage (iOS Keychain / Android Keystore).
- **S-MDB-06**: The browser context SHALL NOT have access to the app's local database, keystore, or any data beyond what is explicitly shared via the wallet connection protocol.

### Network Exposure

- **S-MDB-07**: The mobile DApp browser SHALL make external network calls only to: (a) the DApp URL requested by the user, (b) WalletConnect relay servers, (c) Ethereum RPC endpoints configured in the user's wallet settings. No other external calls SHALL be made from the browser context.
- **S-MDB-08**: All WalletConnect communication SHALL use encrypted WebSocket connections (wss://).

### Recovery

- **S-MDB-09**: If a signing operation is interrupted (app crash, network loss, user cancel), no partial signature SHALL be transmitted. The transaction SHALL either be fully signed and submitted, or not submitted at all.
- **S-MDB-10**: On app crash during an active DApp session, no sensitive data (private keys, session secrets) SHALL persist in unprotected storage or crash logs.

---

## Acceptance Criteria

### AC-MDB-01: Launch DApp browser from chat link
**Given** a user is in a 1:1 or group chat containing a DApp link (e.g., https://app.uniswap.org)
**When** the user taps the DApp link
**Then** the mobile DApp browser opens and loads the DApp page within 2 seconds
**Verify by**: Manual QA on iOS and Android; Appium E2E test

### AC-MDB-02: Wallet connection prompt
**Given** the mobile DApp browser is open and loaded with a DApp that requests wallet connection
**When** the DApp initiates a WalletConnect session
**Then** a connection prompt is displayed showing the DApp name, URL, and requested permissions, with Approve and Reject options
**Verify by**: Manual QA; Appium E2E test with a test DApp

### AC-MDB-03: Transaction signing approval
**Given** a DApp session is connected and the DApp sends a transaction signing request
**When** the signing prompt appears
**Then** the prompt displays recipient address, amount, gas estimate, network name, and the full DApp domain; the user can approve or reject
**Verify by**: Manual QA with test DApp on testnet; Appium E2E test

### AC-MDB-04: Transaction signing rejection
**Given** a transaction signing prompt is displayed
**When** the user taps Reject
**Then** the transaction is not signed, the DApp receives a rejection response, and the session remains active
**Verify by**: Manual QA; Appium E2E test

### AC-MDB-05: Session persistence across backgrounding
**Given** a DApp session is active and the user backgrounds the app for < 5 minutes
**When** the user returns to the app
**Then** the DApp session is still active and the browser state is preserved
**Verify by**: Manual QA on iOS and Android

### AC-MDB-06: Session recovery after app kill
**Given** a DApp session is active and the OS kills the app
**When** the user relaunches the app and opens the browser
**Then** the WalletConnect session is re-established if it has not expired on the DApp side
**Verify by**: Manual QA

### AC-MDB-07: Unsupported chain request
**Given** a DApp session is active on Ethereum mainnet
**When** the DApp requests switching to a chain not supported by the Status wallet
**Then** the app displays a message stating the chain is not supported and the session remains on the original chain
**Verify by**: Manual QA with test DApp; Appium E2E test

### AC-MDB-08: No internet at browser launch
**Given** the device has no internet connectivity
**When** the user attempts to open a DApp link
**Then** the browser displays a clear "No internet connection" error and provides a retry option
**Verify by**: Manual QA; Appium E2E test

### AC-MDB-09: Wallet locked during signing
**Given** the wallet is locked (requires biometrics or password) and a signing request arrives
**When** the signing prompt is triggered
**Then** the app prompts the user to unlock the wallet first, then displays the signing details upon successful unlock
**Verify by**: Manual QA on iOS (Face ID/Touch ID) and Android (fingerprint/PIN)

### AC-MDB-10: Phishing domain warning
**Given** the user navigates to a DApp URL not on the known-safe list
**When** the page begins loading
**Then** a warning banner is displayed showing the full domain name with an option to proceed or go back
**Verify by**: Manual QA; Appium E2E test

---

## Edge Cases

| ID | Condition | Expected Behaviour |
|----|-----------|-------------------|
| EC-MDB-01 | Browser launched with no internet | Error message displayed with retry option; no crash (AC-MDB-08) |
| EC-MDB-02 | Wallet locked during transaction signing | Unlock prompt shown before signing details (AC-MDB-09) |
| EC-MDB-03 | DApp requests unsupported chain | Informative error; session stays on current chain (AC-MDB-07) |
| EC-MDB-04 | App backgrounded during signing flow | Signing prompt preserved on foreground return; transaction not auto-submitted |
| EC-MDB-05 | DApp sends rapid successive signing requests | Requests are queued; only one signing prompt displayed at a time |
| EC-MDB-06 | User rotates device during signing prompt | Prompt layout adapts; no data loss or dismissal |
| EC-MDB-07 | WalletConnect relay server unreachable | Error displayed within 5 seconds; user can retry connection |
| EC-MDB-08 | DApp sends malformed transaction data | Signing prompt displays raw data with a warning; user can reject |
| EC-MDB-09 | Multiple DApp sessions open simultaneously | Each session managed independently; switching between sessions does not corrupt state |
| EC-MDB-10 | Low memory condition on device | Browser context released gracefully; app remains stable; session can be re-established |

---

## Suggested Test Coverage

| Acceptance Criterion | Manual QA | Appium E2E (mobile) | Squish E2E (desktop) |
|---------------------|-----------|---------------------|---------------------|
| AC-MDB-01: Chat link launch | ✅ iOS + Android | ✅ Planned | N/A (mobile only) |
| AC-MDB-02: Wallet connection | ✅ iOS + Android | ✅ Planned (test DApp) | N/A |
| AC-MDB-03: Tx signing approval | ✅ Testnet | ✅ Planned (mock DApp) | N/A |
| AC-MDB-04: Tx signing rejection | ✅ Testnet | ✅ Planned | N/A |
| AC-MDB-05: Background persistence | ✅ iOS + Android | ⚠️ Limited (platform constraint) | N/A |
| AC-MDB-06: App kill recovery | ✅ iOS + Android | ❌ Not feasible | N/A |
| AC-MDB-07: Unsupported chain | ✅ | ✅ Planned | N/A |
| AC-MDB-08: No internet | ✅ iOS + Android | ✅ Planned | N/A |
| AC-MDB-09: Wallet locked | ✅ iOS + Android | ⚠️ Biometrics mock needed | N/A |
| AC-MDB-10: Phishing warning | ✅ | ✅ Planned | N/A |
