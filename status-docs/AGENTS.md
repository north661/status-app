# status-docs

Feature specifications for the [Status](https://status.app) desktop and mobile application.

## Purpose

These specs define how app features should behave. They serve as:
- A regression testing reference for QA
- A feature behaviour reference for developers and designers
- A source of truth for AI-driven test generation and bug triage

## Structure

- `specs/{area}/{feature}.md` — Feature specs (the core content)
- `templates/spec-template.md` — Template for new specs (copy to create)
- `coverage.md` — Tracks which features have specs
- `guide.md` — How to read, write, and use specs
- `SUMMARY.md` — GitBook navigation structure

## Spec format

Each spec is a Markdown file with YAML frontmatter. Scenarios use a structured
format with explicitly labelled fields:

- **Priority**: Critical / High / Medium / Low
- **Platforms**: Which platforms the scenario applies to
- **Preconditions**: What must be true before the scenario
- **Action**: What the user does (user intent, not UI clicks)
- **Expected**: Verifiable outcomes (concrete, not vague)

Scenario IDs follow: `SC-{CODE}-{NUM}` for scenarios, `EC-{CODE}-{NUM}` for
edge cases. The `{CODE}` comes from the spec's `code` field in frontmatter.
IDs are permanent — never renumber, never reuse deleted IDs.

## Creating a spec

1. Copy `templates/spec-template.md` to `specs/{area}/{feature}.md`
2. Fill all required frontmatter fields (id, code, title, area, keywords, platforms, risk, status, app_version)
3. Write a 2-3 sentence summary
4. Add requirements using RFC 2119 language (SHALL, SHOULD, MAY)
5. Write scenarios using the structured format (Priority, Platforms, Preconditions, Action, Expected)
6. Add edge cases, platform differences, and regression notes where applicable
7. Check against quality rules in `.cursor/rules/spec-quality.mdc`

## Updating a spec

When feature behaviour changes in a new release:
1. Update the affected scenarios
2. Bump the `app_version` field in frontmatter
3. Add an entry to the Changelog section at the bottom of the file

## Generating tests from a spec

Each scenario maps to one test function. Read:
- `Preconditions` → test fixtures and setup
- `Action` → test body
- `Expected` → assertions
- `automation` frontmatter field → paths to existing test files for code style reference

For desktop tests: follow patterns in `test/e2e/` (pytest + Squish)
For mobile tests: follow patterns in `test/e2e_appium/` (pytest + Appium)

## Triaging bugs against specs

1. Search specs by `keywords` frontmatter field matching the bug's affected area
2. Find the scenario describing expected behaviour
3. Check the platform coverage matrix for platform-specific behaviour
4. Check regression notes for known fragile areas
5. Reference the scenario ID (e.g., "Defect against SC-CHAN-02") in the bug report
