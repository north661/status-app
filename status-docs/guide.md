# How to Use These Specs

## Reading specs

Each spec covers a single feature or user flow. The structure is consistent:

1. **Frontmatter** (YAML metadata) — machine-readable fields for tooling and AI
2. **Summary** — what the feature does in 2-3 sentences
3. **Requirements** — constraints with measurable criteria (RFC 2119 language)
4. **Scenarios** — concrete, testable behaviours with unique IDs
5. **Edge Cases** — boundary conditions and error handling
6. **Platform Differences** — where desktop/iOS/Android diverge
7. **Regression Notes** — tribal knowledge about fragile areas
8. **Changelog** — version history of behaviour changes

### Understanding scenarios

Each scenario has explicitly labelled fields:

- **Priority**: How important this scenario is for regression testing
  - **Critical** — core functionality, include in smoke tests
  - **High** — important paths, include in standard regression
  - **Medium** — secondary paths, include in full regression
  - **Low** — minor details, test when time permits
- **Platforms**: Which platforms this scenario applies to
- **Preconditions**: What must already be true (maps to test fixtures)
- **Action**: What the user does — described as user intent, not specific UI interactions
- **Expected**: What should happen — concrete, verifiable outcomes

### Understanding IDs

Every scenario and edge case has a permanent ID:

- `SC-{CODE}-{NUM}` — standard scenarios (e.g., SC-CHAN-01)
- `EC-{CODE}-{NUM}` — edge cases (e.g., EC-CHAN-01)

The `{CODE}` comes from the spec file's `code` field in frontmatter. IDs are
permanent identifiers, not ordinals. They are never renumbered and deleted IDs
are never reused. New scenarios always get the next available number regardless
of their position in the document.

These IDs can be referenced in:
- Bug reports: "Defect against SC-CHAN-02"
- Test code: `@pytest.mark.spec("SC-CHAN-01")`
- Discussions: "See SC-PERM-03 for the expected behaviour"

### Understanding requirements language

Specs use [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) keywords:

| Keyword | Meaning |
|---------|---------|
| **SHALL** / **MUST** | Absolute requirement — failure is a defect |
| **SHALL NOT** / **MUST NOT** | Absolute prohibition — occurrence is a defect |
| **SHOULD** | Recommended — deviations need justification |
| **SHOULD NOT** | Discouraged — usage needs justification |
| **MAY** | Optional — acceptable to include or omit |

## Writing specs

### Creating a new spec

1. Copy `templates/spec-template.md` to `specs/{area}/{feature-name}.md`
2. Choose a unique `code` (short uppercase identifier, e.g., CHAN, PERM, WAL).
   Check existing specs to avoid duplicates.
3. Fill in all required frontmatter fields
4. Write the summary, requirements, and scenarios
5. Add edge cases for boundary conditions and error states
6. Add platform differences if behaviour varies across desktop/iOS/Android
7. Update `coverage.md` to reflect the new spec
8. Update `SUMMARY.md` to add the spec to GitBook navigation

### Quality checklist

Before considering a spec complete, verify:

- [ ] Every scenario has all five fields (Priority, Platforms, Preconditions, Action, Expected)
- [ ] Expected outcomes are concrete and verifiable (not "works correctly" or "displays properly")
- [ ] Requirements use RFC 2119 keywords (SHALL/SHOULD/MAY, not "should" or "must" lowercase)
- [ ] Performance requirements include specific thresholds (not "fast" or "responsive")
- [ ] The spec covers at least one edge case
- [ ] Platform differences are documented where behaviour diverges
- [ ] All scenario IDs are unique and follow the `SC-{CODE}-{NUM}` pattern
- [ ] Frontmatter keywords accurately reflect the feature's domain

### Updating an existing spec

When feature behaviour changes in a new release:

1. Update affected scenarios to reflect the new behaviour
2. Add new scenarios if the change introduces new capabilities
3. Bump `app_version` in frontmatter to the release version
4. Add an entry to the Changelog section
5. Update regression notes if the change affects a historically fragile area

### Using AI to write specs

AI can draft specs from various inputs:

- **From a Figma design**: provide the Figma link and ask AI to generate scenarios covering the visible states and interactions
- **From an epic/issue**: provide the issue description and ask AI to generate a spec following the template
- **From existing test code**: point AI at test files and ask it to extract a spec documenting what the tests cover
- **From a FURPS document**: provide the FURPS doc and ask AI to generate detailed scenarios from the requirements

Always review AI-generated specs for:
- Completeness (did it miss edge cases?)
- Accuracy (does this match actual app behaviour?)
- Precision (are the expected outcomes specific enough to test against?)

## Using specs for regression testing

### Building a test run

1. Open `coverage.md` to see which areas have specs
2. For each spec in scope, check the Changelog for recent changes (these need focused testing)
3. Filter scenarios by Priority:
   - **Smoke test**: Critical scenarios only
   - **Standard regression**: Critical + High
   - **Full regression**: All scenarios
4. Use the Platform Differences table to identify platform-specific test paths
5. Reference scenario IDs in test results for traceability

### Triaging a bug

1. Identify the feature area from the bug report
2. Search specs by `keywords` in frontmatter
3. Find the scenario that describes the expected behaviour
4. Compare expected behaviour (from the spec) against actual behaviour (from the bug)
5. Check if the bug matches a documented edge case
6. Check regression notes for historical context
7. Reference the scenario ID in the bug report

## Versioning

- The `main` branch always reflects the current or next release
- When a release ships, the repo is tagged (e.g., `v2.32`)
- To see specs as of a past release, check the corresponding git tag
- The `app_version` field in each spec indicates which release it currently reflects
