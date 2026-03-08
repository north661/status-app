# Privacy Mode FURPS

**Epic**: [#17619](https://github.com/status-im/status-app/issues/17619)
**Risk Level**: 🔴 High (Privacy feature)
**Related Issues**: [OXI-29](https://linear.app/oxidation2838/issue/OXI-29) — Privacy Mode doesn't persist after app restart

---

## Summary

Privacy Mode is a global toggle that disables all third-party integrations and external network calls to protect user activity from being exposed to external services. When enabled, features that depend on third-party providers (e.g., token swaps, GIF search, fiat on/off ramps) become unavailable, and the app operates using only the peer-to-peer Waku network and user-configured endpoints. This feature is critical for users who require maximum privacy and do not want their wallet addresses, browsing activity, or usage patterns disclosed to any external party.

---

## Functionality

- F-PRIV-01: The app SHALL provide a Privacy Mode toggle accessible from the Settings screen.
- F-PRIV-02: The app SHALL allow users to enable Privacy Mode during the onboarding flow.
- F-PRIV-03: When Privacy Mode is enabled, the app SHALL disable all third-party integrations, including:
  - Ethereum RPC providers (Infura, Alchemy, etc.)
  - Swap providers (Paraswap, 1inch, etc.)
  - WalletConnect
  - Fiat on/off ramp providers
  - GIF search (Tenor, Giphy)
  - News Feed RSS sources
  - Any fallback RPCs or analytics trackers
- F-PRIV-04: When Privacy Mode is enabled, the app SHALL NOT make any network requests to third-party endpoints.
- F-PRIV-05: When Privacy Mode is disabled, previously disabled integrations SHALL resume normal operation.
- F-PRIV-06 (Optional): The app SHOULD allow users to configure their own RPC provider as an alternative to disabling RPC entirely.
- F-PRIV-07 (Optional): The app SHOULD disable connections to Waku Store nodes if the user has configured their own store node.

## Usability

- U-PRIV-01: The Privacy Mode toggle SHALL display a clear description of what it disables and why, visible before the user commits to the action.
- U-PRIV-02: The toggle SHALL be accessible within 3 taps/clicks from the main screen in Settings.
- U-PRIV-03: When a user navigates to a feature disabled by Privacy Mode (e.g., swap, GIF search), a contextual message SHALL be displayed explaining that the feature is unavailable due to Privacy Mode, with an option to navigate to Settings to disable it.
- U-PRIV-04: The onboarding Privacy Mode option SHALL use non-technical language understandable by users without blockchain expertise.
- U-PRIV-05: Visual feedback SHALL be provided within 200ms of toggling Privacy Mode to confirm the state change.

## Reliability

- R-PRIV-01: Privacy Mode state SHALL persist across app restarts — if enabled before closing, it SHALL remain enabled on next launch.
- R-PRIV-02: Privacy Mode state SHALL persist across app updates.
- R-PRIV-03: No third-party network calls SHALL occur between app launch and Privacy Mode state being read and applied.
- R-PRIV-04: If the Privacy Mode state fails to load from storage, the app SHALL default to Privacy Mode enabled (fail-safe).
- R-PRIV-05: Switching user accounts SHALL preserve each account's independent Privacy Mode setting.
- R-PRIV-06: Switching network profiles while Privacy Mode is on SHALL NOT re-enable third-party integrations.
- R-PRIV-07: After a network connectivity interruption and reconnection, third-party calls SHALL NOT resume if Privacy Mode is enabled.

## Performance

- P-PRIV-01: The Privacy Mode toggle state change SHALL complete in < 500ms (from user action to all integrations disabled/enabled).
- P-PRIV-02: App startup time with Privacy Mode enabled SHALL NOT exceed startup time with Privacy Mode disabled by more than 200ms.
- P-PRIV-03: With Privacy Mode enabled, the app SHALL reduce background network usage by eliminating all third-party polling and keep-alive connections.
- P-PRIV-04: The Privacy Mode state SHALL be read from local storage in < 50ms during app initialisation.

## Security

### Threat Considerations

- **State leakage**: If Privacy Mode state is not applied before network initialisation, third-party services could receive user IP addresses, wallet addresses, or usage patterns before the user's privacy preference takes effect.
- **Toggle bypass**: A bug in Privacy Mode enforcement could allow individual integrations to make network calls despite the global toggle being enabled.
- **Persistence failure**: If the toggle state fails to persist (see OXI-29), users who believe they are in Privacy Mode may unknowingly have their activity exposed to third parties after an app restart.
- **Side-channel exposure**: Even with Privacy Mode on, DNS queries or connection metadata could reveal user intent to third-party observers if not properly handled.

### Data Protection

- **Wallet addresses**: RPC requests contain wallet addresses that can be correlated with user identity by RPC providers.
- **IP addresses**: All third-party HTTP requests expose the user's IP address to the service provider.
- **Transaction history**: Swap and on/off ramp providers can build transaction history profiles.
- **Usage patterns**: GIF search queries, news feed fetches, and WalletConnect sessions reveal app usage patterns.
- **Account metadata**: The Privacy Mode preference itself is sensitive — it SHALL be stored locally only and SHALL NOT be transmitted to any external service.

### Network Exposure

When Privacy Mode is **disabled**, the following external endpoints are contacted:
- Ethereum RPC providers (e.g., `mainnet.infura.io`, `eth-mainnet.alchemyapi.io`)
- Swap aggregators (e.g., Paraswap, 1inch APIs)
- WalletConnect relay servers
- GIF search APIs (e.g., `api.tenor.com`, `api.giphy.com`)
- Fiat on/off ramp APIs
- RSS feed sources for news
- Any analytics or telemetry endpoints

When Privacy Mode is **enabled**, NONE of the above endpoints SHALL be contacted.

### Recovery

- If Privacy Mode toggle state fails to persist to storage, the app SHALL treat the failure as a critical error and display a warning to the user.
- If Privacy Mode state cannot be read on startup (corrupted storage), the app SHALL default to Privacy Mode enabled (fail-safe).
- If an individual integration fails to disable when Privacy Mode is toggled on, the app SHALL retry disabling it and log the failure for debugging.

---

## Acceptance Criteria

### AC-PRIV-01: Enable Privacy Mode from Settings
**Given** the user is on the Settings screen
**When** the user enables the Privacy Mode toggle
**Then** all third-party integrations SHALL be disabled immediately (within 500ms)
**Verify by**: Manual QA, Appium E2E

### AC-PRIV-02: Privacy Mode persists across app restart
**Given** Privacy Mode is enabled
**When** the user closes and reopens the app
**Then** Privacy Mode SHALL remain enabled and all third-party integrations SHALL remain disabled
**Verify by**: Appium E2E (critical regression — see OXI-29)

### AC-PRIV-03: Privacy Mode during onboarding
**Given** the user is in the onboarding flow
**When** the user enables Privacy Mode
**Then** no third-party network calls SHALL be made for the remainder of the session
**Verify by**: API test (network traffic inspection)

### AC-PRIV-04: Contextual UI when features are unavailable
**Given** Privacy Mode is enabled
**When** the user navigates to a feature that requires a disabled integration (e.g., swap, GIF search)
**Then** a clear message SHALL be displayed explaining the feature is unavailable due to Privacy Mode
**Verify by**: Manual QA, Appium E2E

### AC-PRIV-05: Disable Privacy Mode
**Given** Privacy Mode is currently enabled
**When** the user disables the Privacy Mode toggle
**Then** all third-party integrations SHALL resume normal operation within 500ms
**Verify by**: Manual QA, Appium E2E

### AC-PRIV-06: Privacy Mode state independent per account
**Given** User A has Privacy Mode enabled and User B has Privacy Mode disabled
**When** the user switches from User A to User B
**Then** Privacy Mode SHALL be disabled (reflecting User B's setting)
**Verify by**: Manual QA

### AC-PRIV-07: Fail-safe on corrupted state
**Given** the Privacy Mode preference in local storage is corrupted or unreadable
**When** the app starts
**Then** Privacy Mode SHALL default to enabled
**Verify by**: API test (simulate corrupted storage)

---

## Edge Cases

| # | Scenario | Expected Behaviour |
|---|----------|--------------------|
| EC-01 | User toggles Privacy Mode off → on → off rapidly (< 1s between toggles) | Each toggle SHALL be processed sequentially; final state SHALL match the last user action; no race conditions in integration enable/disable |
| EC-02 | User switches network profiles while Privacy Mode is on | Privacy Mode SHALL remain enabled; no third-party calls SHALL be made on the new network profile |
| EC-03 | User switches accounts while Privacy Mode is enabled | The target account's own Privacy Mode setting SHALL be applied; no state bleed between accounts |
| EC-04 | App update occurs while Privacy Mode is enabled | Privacy Mode state SHALL persist through the update; no third-party calls SHALL be made on first launch after update |
| EC-05 | Privacy Mode enabled + airplane mode + reconnect | After network reconnection, third-party calls SHALL NOT resume; only Waku peer-to-peer connections SHALL be re-established |
| EC-06 | Privacy Mode enabled during onboarding, then disabled in Settings after onboarding completes | The Settings toggle SHALL reflect the state set during onboarding; disabling it SHALL re-enable all integrations |
| EC-07 | App launched for the first time (no stored preference) | Privacy Mode SHALL default to disabled (standard first-launch behaviour) unless the user enables it during onboarding |

---

## Supportability

- S-PRIV-01: Privacy Mode configuration SHALL be centralised in a single module or flag, not scattered across individual integration modules.
- S-PRIV-02: Developer feature flags SHALL be available to test Privacy Mode enforcement without full app configuration.
- S-PRIV-03: All third-party dependencies and their relationship to Privacy Mode SHALL be documented in a dependency manifest.
- S-PRIV-04: Automated tests SHALL verify that no new third-party calls are introduced without updating the Privacy Mode blocklist.

---

## Test Coverage Map

| Acceptance Criteria | Manual QA | Appium E2E (Mobile) | Squish E2E (Desktop) | API Test |
|----|----|----|----|-----|
| AC-PRIV-01: Enable from Settings | ✅ | ✅ | ✅ | — |
| AC-PRIV-02: Persist across restart | ✅ | ✅ (critical) | ✅ | — |
| AC-PRIV-03: Onboarding flow | ✅ | ✅ | ✅ | ✅ (network inspection) |
| AC-PRIV-04: Contextual UI | ✅ | ✅ | ✅ | — |
| AC-PRIV-05: Disable Privacy Mode | ✅ | ✅ | ✅ | — |
| AC-PRIV-06: Per-account state | ✅ | — | — | — |
| AC-PRIV-07: Fail-safe on corruption | — | — | — | ✅ (storage simulation) |
