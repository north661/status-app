---
id: community-channels
code: CHAN
title: Community Channels
area: communities
keywords: [channel, create, edit, delete, rename, community, category, emoji, description]
platforms: [desktop, ios, android]
risk: medium
status: active
app_version: "2.32"
refs:
  epic: ""
  figma: ""
automation:
  desktop: "test/e2e/tests/communities/test_communities_channels.py"
  mobile: ""
---

# Community Channels

## Summary

Channels organise messages within a community by topic. Community owners and
admins can create, edit, and delete channels. Channels can be assigned to
categories, given custom names, descriptions, emoji, and colours. Members can
view and post in channels according to their permissions.

## Requirements

- Every community SHALL have a default "General" channel created automatically
- Channel names SHALL be unique within a community
- Channel names SHALL support Unicode characters including emoji
- Only users with the Owner, Token Master, or Admin role SHALL be able to
  create, edit, or delete channels
- Members without the appropriate role SHALL NOT see create, edit, or delete
  controls for channels
- Users without read permission on a channel MUST NOT be able to read messages
  in that channel (encryption SHALL be used)
- Channel list updates SHOULD propagate to all community members within
  10 minutes (per Community Description update interval)
- Channel operations (create, edit, delete) SHOULD complete within 5 seconds
  on desktop and 10 seconds on mobile

## Scenarios

### SC-CHAN-01: Admin creates a new channel

- **Priority**: Critical
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
  - Community exists with default General channel
- **Action**: Create a new channel named "announcements" with description
  "Official updates" and a custom emoji
- **Expected**:
  - "announcements" appears in the uncategorised channel list
  - The new channel is automatically opened
  - Channel name, description, and emoji are visible in channel info
  - The General channel remains in the list

### SC-CHAN-02: Admin edits a channel

- **Priority**: High
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
  - Community exists with a channel named "announcements"
- **Action**: Edit the channel — change name to "official-announcements",
  update description, change emoji
- **Expected**:
  - Channel list shows the updated name "official-announcements"
  - Channel toolbar/header displays the updated name and description
  - Updated emoji is visible
  - Existing messages in the channel are preserved

### SC-CHAN-03: Admin deletes a channel

- **Priority**: High
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
  - Community exists with at least two channels (General + one other)
- **Action**: Delete the non-General channel
- **Expected**:
  - The deleted channel is removed from the channel list
  - Channel count decreases by one
  - The community view remains functional

### SC-CHAN-04: Admin deletes all channels

- **Priority**: Medium
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
  - Community exists with channels
- **Action**: Delete all channels including General
- **Expected**:
  - Channel list is empty
  - Community view handles the empty state without errors

### SC-CHAN-05: Default General channel exists on community creation

- **Priority**: Critical
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in user
- **Action**: Create a new community
- **Expected**:
  - A "General" channel is automatically present
  - General channel has description "General channel for the community"
  - General channel is open by default

### SC-CHAN-06: Member cannot create channels

- **Priority**: Critical
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as a community member (not owner, token master, or admin)
  - Member of a community
- **Action**: Attempt to find channel creation controls
- **Expected**:
  - Create channel/category button is not visible
  - Add channel button is not visible
  - No channel creation option exists in any accessible menu

### SC-CHAN-07: Member cannot edit or delete channels

- **Priority**: Critical
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as a community member (not owner, token master, or admin)
  - Member of a community with at least one channel
- **Action**: Attempt to find edit/delete controls for a channel via context
  menu and toolbar options
- **Expected**:
  - Right-click/long-press context menu does not show Edit or Delete options
  - Toolbar more-options menu does not show Edit or Delete options

### SC-CHAN-08: Non-member cannot see hidden channel

- **Priority**: High
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Two users: owner and member
  - Community exists with both users as members
  - Owner creates a channel with a token-gated view permission and
    "hide if permissions not met" enabled
  - Member does not hold the required token
- **Action**: Member views the community channel list
- **Expected**:
  - The token-gated hidden channel is not visible in the member's channel list
  - The channel is visible in the owner's channel list

### SC-CHAN-09: Member can view and post in unrestricted channel

- **Priority**: High
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Two users: owner and member
  - Community exists with both users as members
  - An unrestricted channel exists (no token-gated permissions)
- **Action**: Owner sends a message in the channel. Member opens the same
  channel, reads the message, and sends a reply.
- **Expected**:
  - Member can see the owner's message
  - Member can send a message in the channel
  - Owner can see the member's reply

## Edge Cases

### EC-CHAN-01: Channel name at maximum length

- **Priority**: Medium
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
- **Action**: Create a channel with a name at the maximum character limit
- **Expected**:
  - Channel is created successfully if within the limit
  - Input is rejected or truncated with a visible indication if exceeding
    the limit

### EC-CHAN-02: Channel name with special characters

- **Priority**: Medium
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
- **Action**: Create a channel with a name containing emoji, Unicode
  characters, mixed scripts, or special punctuation
- **Expected**:
  - Channel is created with the name preserved correctly
  - Channel name renders correctly in the channel list and header

### EC-CHAN-03: Duplicate channel name

- **Priority**: Medium
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
  - A channel named "announcements" already exists
- **Action**: Attempt to create another channel named "announcements"
- **Expected**:
  - Creation is rejected with a clear validation message indicating the
    name is already in use

### EC-CHAN-04: Rapid sequential channel operations

- **Priority**: Low
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
- **Action**: Create a channel, immediately rename it, then immediately
  delete it
- **Expected**:
  - Each operation completes without errors
  - Final state is consistent (channel is deleted)

### EC-CHAN-05: Channel operations on slow/lossy network

- **Priority**: Medium
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Signed in as community owner
  - Network is throttled or experiencing packet loss
- **Action**: Create a channel
- **Expected**:
  - Operation eventually completes or fails with a clear error message
  - No partial/corrupt state in the channel list

## Platform Differences

| Behaviour | Desktop | iOS | Android | Notes |
|-----------|---------|-----|---------|-------|
| Channel creation access | Bottom menu + right-click context menu | Bottom menu | Bottom menu | Desktop has additional right-click option |
| Channel edit access | Right-click context menu + toolbar more-options | Long-press context menu + toolbar | Long-press context menu + toolbar | |
| Channel delete confirmation | Dialog prompt | Dialog prompt | Dialog prompt | Confirm across all platforms |

## Regression Notes

- RN-CHAN-01: The existing desktop test (`test_create_edit_remove_community_channel`)
  covers create, edit, and delete as a single test flow. Historically coupled —
  if create breaks, edit and delete are untestable in that run.
- RN-CHAN-02: Multi-user channel tests (hidden channels, view-and-post) are
  currently skipped in desktop e2e (`@pytest.mark.skip`) due to test data issues.
  These scenarios (SC-CHAN-08, SC-CHAN-09) lack automated coverage.
- RN-CHAN-03: Channel emoji rendering in the toolbar has had assertion issues —
  the test checks for `'👍 '` (with trailing space), suggesting potential
  whitespace handling inconsistency.

## Changelog

| Version | Change |
|---------|--------|
| 2.32 | Initial spec — extracted from FURPS requirements and existing desktop e2e tests |
