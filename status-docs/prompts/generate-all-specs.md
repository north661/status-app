# Spec Generation Prompts

Run each prompt as a Cursor background agent with access to both the
`status-app` and `status-docs` repositories.

Each prompt is scoped to one feature area. Run them one at a time, review
the output, then move to the next area.

Before running, ensure:
- `status-docs/templates/spec-template.md` exists (the master template)
- `status-docs/.cursor/rules/spec-creation.mdc` exists (extraction rules)
- `status-docs/.cursor/rules/spec-quality.mdc` exists (quality rules)

After each run, review the generated specs, then update `SUMMARY.md` and
`coverage.md` to reflect the new content.

---

## 1. Communities

```
You are generating feature specs for the Status app. Read the spec template
at status-docs/templates/spec-template.md and the creation rules at
status-docs/.cursor/rules/spec-creation.mdc and the quality rules at
status-docs/.cursor/rules/spec-quality.mdc. Follow them precisely.

Also read the existing spec at status-docs/specs/communities/community-channels.md
as an example of the expected output quality and format.

Generate specs for the Communities area by reading these source files:

QML (read for UI actions, validation, role visibility, flow structure):
- ui/app/AppLayouts/Communities/popups/CreateCommunityPopup.qml
- ui/app/AppLayouts/Communities/popups/CreateCategoryPopup.qml
- ui/app/AppLayouts/Communities/popups/KickBanPopup.qml
- ui/app/AppLayouts/Communities/popups/TokenPermissionsPopup.qml
- ui/app/AppLayouts/Communities/popups/TransferOwnershipPopup.qml
- ui/app/AppLayouts/Communities/views/CommunityColumnView.qml
- ui/app/AppLayouts/Communities/views/CommunitySettingsView.qml
- ui/app/AppLayouts/Communities/views/PermissionsView.qml
- ui/app/AppLayouts/Communities/views/JoinCommunityView.qml
- ui/app/AppLayouts/Communities/views/MintedTokensView.qml
- ui/app/AppLayouts/stores/Messaging/Community/CommunityRootStore.qml
- ui/app/AppLayouts/stores/Messaging/Community/CommunityAccessStore.qml
- ui/app/AppLayouts/stores/Messaging/Community/PermissionsStore.qml
- ui/app/AppLayouts/Communities/stores/CommunitiesStore.qml

Nim (read for action/event model, business logic, state transitions):
- src/app/modules/main/communities/io_interface.nim
- src/app/modules/main/communities/module.nim
- src/app/modules/main/communities/controller.nim
- src/app/modules/shared_models/section_item.nim
- src/app/modules/shared_models/member_model.nim

Tests (read for verified scenarios, assertions, known issues):
- test/e2e/tests/communities/test_communities_screens_overview.py
- test/e2e/tests/communities/test_join_leave_status_community.py
- test/e2e/tests/communities/test_communities_kick_ban.py
- test/e2e/tests/communities/test_communities_limit_to_5_permissions.py
- test/e2e/tests/communities/test_communities_send_accept_decline_request_from_profile.py

FURPS (read for requirements and constraints):
- docs/FURPS/communities.md

Do NOT regenerate community-channels.md — it already exists.

Generate these spec files in status-docs/specs/communities/:

1. community-overview.md (code: COMOV) — Creating a community, editing
   community details (name, description, logo, banner, colour, tags, intro/
   outro messages), community settings (pin messages, manual/auto accept)
2. community-roles.md (code: ROLE) — Owner, Token Master, Admin, Member
   role model. What each role can and cannot do.
3. community-permissions.md (code: PERM) — Token-gated permissions, permission
   types (become member, become admin, view channel, view and post), creating/
   editing/deleting permissions, the 5-permission limit
4. community-categories.md (code: CAT) — Creating, editing, deleting
   categories, assigning channels to categories, reordering
5. community-membership.md (code: MEM) — Joining, leaving, spectating,
   request to join flow, accept/decline requests, kick, ban, member list
6. community-tokens.md (code: CTOK) — Minting community tokens, airdrops,
   token management (if enough detail in the source)

For each spec:
- Extract validation rules from QML (field lengths, regexes, error messages)
- Extract actions and outcomes from Nim io_interface method names
- Extract verified scenarios from test code (map with step() to Action, assertions to Expected)
- Note any skipped tests as gaps in Regression Notes
- Include requirements from the FURPS doc using RFC 2119 language
- Flag any contradictions between QML and Nim as potential issues in Regression Notes
```

---

## 2. Wallet

```
You are generating feature specs for the Status app. Read the spec template
at status-docs/templates/spec-template.md and the creation rules at
status-docs/.cursor/rules/spec-creation.mdc and the quality rules at
status-docs/.cursor/rules/spec-quality.mdc. Follow them precisely.

Read the existing spec at status-docs/specs/communities/community-channels.md
as an example of expected output quality and format.

Generate specs for the Wallet area by reading these source files:

QML:
- ui/app/AppLayouts/Wallet/WalletLayout.qml
- ui/app/AppLayouts/Wallet/popups/simpleSend/SimpleSendModal.qml
- ui/app/AppLayouts/Wallet/popups/SendSignModal.qml
- ui/app/AppLayouts/Wallet/popups/swap/SwapModal.qml
- ui/app/AppLayouts/Wallet/popups/BuyCryptoModal.qml (if exists)
- ui/app/AppLayouts/Wallet/views/AssetsDetailView.qml (or similar)
- ui/app/AppLayouts/Wallet/views/CollectiblesView.qml (or similar)
- ui/app/AppLayouts/Wallet/views/SavedAddressesView.qml (or similar)
- ui/app/AppLayouts/Wallet/stores/RootStore.qml
- ui/app/AppLayouts/Wallet/stores/SwapStore.qml (if exists)
- ui/app/AppLayouts/Wallet/stores/BuyCryptoStore.qml (if exists)

Nim:
- src/app/modules/main/wallet_section/io_interface.nim
- src/app/modules/main/wallet_section/module.nim
- src/app/modules/main/wallet_section/send/io_interface.nim (or send_new/)
- src/app/modules/main/wallet_section/assets/io_interface.nim
- src/app/modules/main/wallet_section/all_collectibles/io_interface.nim
- src/app/modules/main/wallet_section/saved_addresses/io_interface.nim
- src/app/modules/main/wallet_section/accounts/io_interface.nim
- src/app/modules/main/wallet_section/networks/io_interface.nim
- src/app/modules/main/wallet_section/buy_sell_crypto/io_interface.nim

Tests:
- test/e2e/tests/wallet_main_screen/ (all files)
- test/e2e/tests/transactions_tests/ (all files)
- test/e2e_appium/tests/test_wallet_accounts_basic.py
- test/e2e_appium/tests/test_wallet_account_from_settings.py
- test/e2e_appium/tests/test_saved_addresses.py

Generate these spec files in status-docs/specs/wallet/:

1. wallet-overview.md (code: WALOV) — Wallet main screen, viewing balances,
   assets list, account overview
2. wallet-accounts.md (code: WACC) — Creating accounts (generated, seed phrase,
   private key, Keycard, watch-only), editing, removing, reordering accounts
3. wallet-send.md (code: SEND) — Sending ETH and ERC-20 tokens, recipient
   selection, amount entry, network selection, fee estimation, transaction
   signing, confirmation
4. wallet-collectibles.md (code: COLL) — Viewing collectibles/NFTs, details,
   sending NFTs
5. wallet-saved-addresses.md (code: SADR) — Adding, editing, removing saved
   addresses, using saved addresses in send flow
6. wallet-swap.md (code: SWAP) — Token swap flow, provider selection, approval,
   execution (if enough detail in the source)
7. wallet-buy.md (code: BUY) — Buy crypto flow, provider selection,
   on-ramp integration (if enough detail in the source)

For each spec, follow the same extraction approach as described in
spec-creation.mdc. This is a high-security area — include a Security
section in Requirements covering transaction signing, private key handling,
and fund safety.
```

---

## 3. Messaging

```
You are generating feature specs for the Status app. Read the spec template
at status-docs/templates/spec-template.md and the creation rules at
status-docs/.cursor/rules/spec-creation.mdc and the quality rules at
status-docs/.cursor/rules/spec-quality.mdc. Follow them precisely.

Read the existing spec at status-docs/specs/communities/community-channels.md
as an example of expected output quality and format.

Generate specs for the Messaging area by reading these source files:

QML:
- ui/app/AppLayouts/Chat/ChatLayout.qml
- ui/app/AppLayouts/Chat/views/ChatColumnView.qml
- ui/app/AppLayouts/Chat/views/CreateChatView.qml
- ui/app/AppLayouts/Chat/stores/RootStore.qml
- ui/app/AppLayouts/Chat/stores/MessageStore.qml
- ui/app/AppLayouts/Chat/panels/ (all files)
- ui/imports/shared/views/chat/ChatContextMenuView.qml
- ui/imports/shared/views/chat/ (other relevant files)
- ui/app/AppLayouts/Chat/popups/PinnedMessagesPopup.qml
- ui/app/AppLayouts/Chat/popups/PaymentRequestModal.qml (if exists)

Nim:
- src/app/modules/main/chat_section/io_interface.nim
- src/app/modules/main/chat_section/module.nim
- src/app/modules/main/chat_section/chat_content/io_interface.nim
- src/app/modules/main/chat_section/chat_content/messages/io_interface.nim
- src/app/modules/main/chat_section/chat_content/input_area/io_interface.nim
- src/app/modules/main/chat_section/chat_content/users/io_interface.nim
- src/app/modules/main/stickers/io_interface.nim
- src/app/modules/main/gifs/io_interface.nim

Tests:
- test/e2e/tests/crtitical_tests_prs/ (chat-related files)
- test/e2e_appium/tests/messaging/ (all files)

Generate these spec files in status-docs/specs/messaging/:

1. one-to-one-chat.md (code: DM) — Starting a 1:1 chat, sending text
   messages, receiving messages, message status indicators, message history
2. group-chat.md (code: GRP) — Creating group chats, adding/removing members,
   admin controls, group info
3. message-actions.md (code: MACT) — Replying, editing, deleting messages,
   pinning, reactions, context menu actions, mark as read
4. message-types.md (code: MTYP) — Text, images, stickers, GIFs, links,
   link previews, payment requests (if applicable)
```

---

## 4. Onboarding

```
You are generating feature specs for the Status app. Read the spec template
at status-docs/templates/spec-template.md and the creation rules at
status-docs/.cursor/rules/spec-creation.mdc and the quality rules at
status-docs/.cursor/rules/spec-quality.mdc. Follow them precisely.

Read the existing spec at status-docs/specs/communities/community-channels.md
as an example of expected output quality and format.

Generate specs for the Onboarding area by reading these source files:

QML:
- ui/app/AppLayouts/Onboarding/ (all flow files, page files, store files)
  Key files to prioritise: any *Flow.qml, *Page.qml, *Store.qml files

Nim:
- src/app/modules/onboarding/io_interface.nim
- src/app/modules/onboarding/module.nim
- src/app/modules/onboarding/controller.nim
- src/app/modules/shared_modules/keycard_popup/io_interface.nim

Tests:
- test/e2e/tests/onboarding/ (all files)
- test/e2e/tests/crtitical_tests_prs/ (onboarding-related files)
- test/e2e_appium/tests/test_onboarding_import_seed.py
- test/e2e_appium/tests/test_backup_recovery_phrase.py

Generate these spec files in status-docs/specs/onboarding/:

1. create-account.md (code: SIGNUP) — New user sign-up flow: generate keys,
   set display name, set password, create profile
2. login.md (code: LOGIN) — Password login, biometric login (mobile),
   session management
3. seed-phrase.md (code: SEED) — Backup seed phrase, import from seed phrase,
   seed phrase validation, negative cases
4. keycard-onboarding.md (code: KCON) — Create profile with Keycard, import
   to Keycard, Keycard login (if enough detail)
5. sync-new-device.md (code: SYNC) — Syncing to a new device, device pairing

This is a high-security area — include Security sections covering seed phrase
handling, key generation, password strength, and data protection.
```

---

## 5. Settings

```
You are generating feature specs for the Status app. Read the spec template
at status-docs/templates/spec-template.md and the creation rules at
status-docs/.cursor/rules/spec-creation.mdc and the quality rules at
status-docs/.cursor/rules/spec-quality.mdc. Follow them precisely.

Read the existing spec at status-docs/specs/communities/community-channels.md
as an example of expected output quality and format.

Generate specs for the Settings area by reading these source files:

QML:
- ui/app/AppLayouts/Profile/ProfileLayout.qml
- ui/app/AppLayouts/Profile/views/ (all view files — AboutView, AppearanceView,
  ContactsView, LanguageView, NotificationsView, PrivacyAndSecurityView,
  SyncingView, ChangePasswordView, etc.)
- ui/app/AppLayouts/Profile/stores/ (all store files)
- ui/app/AppLayouts/Profile/popups/ (all popup files)

Nim:
- src/app/modules/main/profile_section/io_interface.nim
- src/app/modules/main/profile_section/profile/io_interface.nim
- src/app/modules/main/profile_section/contacts/io_interface.nim
- src/app/modules/main/profile_section/privacy/io_interface.nim
- src/app/modules/main/profile_section/notifications/io_interface.nim
- src/app/modules/main/profile_section/sync/io_interface.nim
- src/app/modules/main/profile_section/devices/io_interface.nim
- src/app/modules/main/profile_section/ens_usernames/io_interface.nim
- src/app/modules/main/profile_section/keycard/io_interface.nim

Tests:
- test/e2e/tests/settings/ (all subdirectories)
- test/e2e/tests/crtitical_tests_prs/ (settings-related files)
- test/e2e_appium/tests/test_settings_password_change_password.py

FURPS:
- docs/FURPS/privacy-mode.md

Generate these spec files in status-docs/specs/settings/:

1. profile-settings.md (code: PROF) — Edit display name, bio, profile
   picture, social links, share profile
2. contacts.md (code: CONT) — Add contact, remove contact, block/unblock,
   contact requests, contact list
3. privacy-and-security.md (code: PRIV) — Privacy mode, who can see status,
   message permissions, privacy settings
4. notifications.md (code: NOTIF) — Notification settings, mute options,
   notification types
5. password-and-keycard.md (code: AUTH) — Change password, Keycard management
   (unlock, factory reset, setup), biometric settings
6. network-and-fleet.md (code: NET) — Network settings, fleet selection,
   RPC configuration (if enough detail)
7. ens-usernames.md (code: ENS) — Register ENS name, set as primary, release
   ENS name
8. sync-and-devices.md (code: SYNCD) — Device syncing, paired devices,
   sync settings
```

---

## 6. Browser

```
You are generating feature specs for the Status app. Read the spec template
at status-docs/templates/spec-template.md and the creation rules at
status-docs/.cursor/rules/spec-creation.mdc and the quality rules at
status-docs/.cursor/rules/spec-quality.mdc. Follow them precisely.

Read the existing spec at status-docs/specs/communities/community-channels.md
as an example of expected output quality and format.

Generate specs for the Browser area by reading these source files:

QML:
- ui/app/AppLayouts/Browser/BrowserLayout.qml
- ui/app/AppLayouts/Browser/views/ (all files)
- ui/app/AppLayouts/Browser/stores/ (all files)
- ui/app/AppLayouts/Browser/popups/ (all files)

Nim:
- src/app/modules/main/browser_section/io_interface.nim
- src/app/modules/main/browser_section/module.nim
- src/app/modules/main/browser_section/bookmark/io_interface.nim
- src/app/modules/main/browser_section/dapps/io_interface.nim

FURPS:
- docs/FURPS/dapp-browser.md

Generate these spec files in status-docs/specs/browser/:

1. dapp-browser.md (code: BRW) — Opening DApps, navigation, bookmarks,
   browser settings, wallet connection within browser
2. wallet-connect.md (code: WCON) — WalletConnect integration, DApp
   permissions, transaction signing from DApps, session management
   (if enough detail in the source — check the DApps service QML files)

This is a high-security area — include Security sections covering DApp
permissions, transaction signing prompts, and phishing protection.
```

---

## 7. Activity Center, Market, Home Page (smaller areas)

```
You are generating feature specs for the Status app. Read the spec template
at status-docs/templates/spec-template.md and the creation rules at
status-docs/.cursor/rules/spec-creation.mdc and the quality rules at
status-docs/.cursor/rules/spec-quality.mdc. Follow them precisely.

Read the existing spec at status-docs/specs/communities/community-channels.md
as an example of expected output quality and format.

Generate specs for three smaller feature areas:

ACTIVITY CENTER:
QML:
- ui/app/AppLayouts/ActivityCenter/ActivityCenterLayout.qml
- ui/app/AppLayouts/ActivityCenter/ (all views, popups, panels)
- ui/app/AppLayouts/stores/ActivityCenterStore.qml
Nim:
- src/app/modules/main/activity_center/io_interface.nim
- src/app/modules/main/activity_center/module.nim

Generate: status-docs/specs/activity-center/activity-center.md (code: ACTR)
— Notification types, filtering, marking as read, accepting/declining
requests, notification badges

MARKET:
QML:
- ui/app/AppLayouts/Market/MarketLayout.qml
- ui/app/AppLayouts/Market/ (all files)
Nim:
- src/app/modules/main/market_section/io_interface.nim

Generate: status-docs/specs/market/market.md (code: MKT)
— Market tab, token price data, search, favourites (if applicable)

HOME PAGE / JUMP-TO:
QML:
- ui/app/AppLayouts/HomePage/ (all files)
Nim:
- src/app/modules/main/app_search/io_interface.nim
FURPS:
- docs/FURPS/jump-to-screen-shell.md

Generate: status-docs/specs/home/home-page.md (code: HOME)
— Jump-to launcher, search, recent items, dock/grid layout

Create the necessary subdirectories (activity-center/, market/, home/)
in status-docs/specs/.
```

---

## Post-generation checklist

After all prompts have been run and specs reviewed:

1. Update `status-docs/SUMMARY.md` with all new specs in the navigation
2. Update `status-docs/coverage.md` to reflect the current state of all specs
3. Review all specs for:
   - Unique `code` fields (no duplicates across all specs)
   - Sequential scenario IDs within each spec
   - No vague language (check against spec-quality.mdc flag list)
   - Platform differences documented where relevant
4. Commit and push to status-docs
5. Tag as `v0.1.0` (first draft of all specs)
