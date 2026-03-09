# Status App Feature Specs

Feature specifications for the [Status](https://status.app) decentralised messenger, crypto wallet, and community platform.

## What is this?

This repository contains **feature specs** — documents that define how each feature of the Status app should behave. Each spec covers a single feature or user flow with:

- **Requirements** — what the feature must do, with measurable criteria
- **Scenarios** — concrete, testable descriptions of behaviour
- **Edge cases** — boundary conditions and error handling
- **Platform differences** — where desktop, iOS, and Android diverge

## Who is this for?

- **QA** — use specs as a regression testing reference and to verify expected behaviour
- **Developers** — use specs to understand intended behaviour before and during implementation
- **Designers** — use specs to check that designs align with documented requirements

## How to use

- **Browse**: visit the [GitBook site](https://north661.gitbook.io/status-docs) (once configured)
- **Search**: use GitBook search or grep the markdown files directly
- **Contribute**: see [guide.md](guide.md) for how to write and update specs

## Spec areas

| Area | Description |
|------|-------------|
| [Communities](specs/communities/) | Community creation, channels, permissions, roles, categories |
| [Wallet](specs/wallet/) | Accounts, transactions, saved addresses, token management |
| [Messaging](specs/messaging/) | 1:1 chat, group chat, message types, reactions |
| [Onboarding](specs/onboarding/) | Sign up, login, seed phrase, key generation |
| [Settings](specs/settings/) | Profile, contacts, notifications, privacy, network |

## Repository layout

```
specs/              Feature specs organised by area
templates/          Spec template (copy to create new specs)
coverage.md         Feature coverage tracker
guide.md            How to read, write, and use specs
SUMMARY.md          GitBook navigation
AGENTS.md           AI agent operating manual
.cursor/rules/      Quality rules for AI-assisted spec writing
```

## Related repositories

- [status-app](https://github.com/status-im/status-app) — the application source code
- [status-go](https://github.com/status-im/status-go) — the Go backend
- Desktop e2e tests: `status-app/test/e2e/`
- Mobile e2e tests: `status-app/test/e2e_appium/`
