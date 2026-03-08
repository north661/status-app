# Privacy Mode FURPS ([#17619](https://github.com/status-im/status-app/issues/17619))

## Functionality
- Implement a **Privacy Mode toggle** to disable all third-party integrations globally.
- Allow users to activate Privacy Mode during onboarding or from app settings at any time.
- Ensure deactivation of all identified services:
  - Ethereum RPC providers
  - Swap providers
  - WalletConnect
  - On/off ramps
  - Gif search
  - News Feed (if it still uses RSS)
  - Any fallback RPCs or trackers
- Optional: disable connection to Waku Store nodes if a way for users to configure one themselves is availble
- Optional: Enable users to setup their own RPC provider
- Prevent network traffic to third-party endpoints when Privacy Mode is enabled.

## Usability
- Display clear information about what Privacy Mode disables and why.
- Integrate the toggle seamlessly in both onboarding and settings UI.
- Show contextual UI messages when features are unavailable due to Privacy Mode.
- Avoid overwhelming users with technical details; keep the interaction simple and confidence-boosting.

## Reliability
- Guarantee strict enforcement: no third-party calls occur when Privacy Mode is on.
- Ensure that Privacy Mode settings persist across sessions and updates.
- Avoid state leakage or edge cases where a previously enabled service might resume.
- Cover edge cases (e.g., user switching networks or profiles while Privacy Mode is on).

## Performance
- Reduce overhead by not initializing or pinging unnecessary third-party services.
- Ensure smooth transition when toggling Privacy Mode on/off without app restarts.

## Supportability
- Centralize Privacy Mode configuration in a single flag or module.
- Provide developer hooks or feature flags to test and enforce privacy constraints.
- Document all third-party dependencies and their relation to Privacy Mode.
- Add automated tests and runtime checks to prevent future regressions or silent violations.

## Acceptance Criteria

### AC-PM-001: Toggle disables third-party calls
**Given** the user is on the Privacy & Security settings screen
**When** they enable Privacy Mode via the third-party services toggle
**Then** no network requests are made to third-party domains (coingecko, infura, walletconnect, etc.)
**Verify by**: Network traffic capture during a 2-minute session with Privacy Mode on

### AC-PM-002: User sees confirmation before enabling
**Given** the user taps the third-party services toggle
**When** the confirmation popup appears
**Then** it clearly explains what will be disabled and allows cancel
**Verify by**: UI inspection of popup content

### AC-PM-003: Persistence across app restart
**Given** Privacy Mode is enabled
**When** the user force-closes and reopens the app
**Then** Privacy Mode remains enabled and no third-party calls are made during startup
**Verify by**: Appium E2E test checking toggle state after restart

### AC-PM-004: Contextual messages on disabled features
**Given** Privacy Mode is enabled
**When** the user navigates to Swap, WalletConnect, or GIF search
**Then** a message explains the feature is unavailable due to Privacy Mode
**Verify by**: UI inspection of each affected screen

## Edge Cases
- User switches network while Privacy Mode is on → Privacy Mode remains on
- App update while Privacy Mode is enabled → Privacy Mode remains enabled
- User has pending WalletConnect session when enabling → Session is terminated
- User enables during onboarding → All third-party services start disabled
