---
id: feature-name
code: FEAT
title: Feature Name
area: area-name
keywords: [keyword1, keyword2, keyword3]
platforms: [desktop, ios, android]
risk: medium
status: draft
app_version: "0.0.0"
refs:
  epic: ""
  figma: ""
automation:
  desktop: ""
  mobile: ""
---

# Feature Name

## Summary

<!-- 2-3 sentences: what this feature does and why it exists. -->

## Requirements

<!-- Constraints and non-functional requirements using RFC 2119 language.
     These absorb relevant FURPS criteria (performance, reliability, security).
     Delete this section if there are no non-functional requirements. -->

- The feature SHALL ...
- The feature SHOULD ...
- The feature MAY ...

## Scenarios

<!-- Each scenario is one testable behaviour. Use the structured format below.
     IDs are permanent: never renumber, never reuse deleted IDs.
     New scenarios always get the next available number. -->

### SC-FEAT-01: Scenario title

- **Priority**: Critical | High | Medium | Low
- **Platforms**: Desktop, iOS, Android
- **Preconditions**:
  - Precondition one
  - Precondition two
- **Action**: What the user does (describe intent, not UI clicks)
- **Expected**:
  - Verifiable outcome one
  - Verifiable outcome two

### SC-FEAT-02: Another scenario title

- **Priority**:
- **Platforms**:
- **Preconditions**:
  -
- **Action**:
- **Expected**:
  -

## Edge Cases

<!-- Boundary conditions, error states, unusual inputs.
     Same format as scenarios but with EC- prefix. -->

### EC-FEAT-01: Edge case title

- **Priority**:
- **Platforms**:
- **Preconditions**:
  -
- **Action**:
- **Expected**:
  -

## Platform Differences

<!-- Only include if behaviour varies across platforms.
     Delete this section if behaviour is identical everywhere. -->

| Behaviour | Desktop | iOS | Android | Notes |
|-----------|---------|-----|---------|-------|
|           |         |     |         |       |

## Regression Notes

<!-- Tribal knowledge: things that have broken before, historically fragile areas,
     non-obvious interactions. Delete this section if there's nothing to note yet. -->

## Changelog

| Version | Change |
|---------|--------|
| 0.0.0   | Initial draft |
