# Flaky Test Stabilization Plan — E2E Gate Tests (BrowserStack)

## Context

Workflow **E2E Gate Tests (BrowserStack)** run #23062475340 was executed 5 times on the same commit (`2df51d6`). Results:

| Attempt | Status  | Duration |
|---------|---------|----------|
| 1       | FAILURE | 11m 38s  |
| 2       | SUCCESS | 21m 22s  |
| 3       | SUCCESS | 13m 32s  |
| 4       | FAILURE | 14m 46s  |
| 5       | SUCCESS | 20m 25s  |

**Pass rate: 60%** (3/5). The wide duration variance (11m–21m) suggests BrowserStack infrastructure instability contributes significantly.

---

## Test Classification

### Stable (1 test)

| Test | File | Confidence |
|------|------|------------|
| `test_import_and_reimport_seed` | `test_onboarding_import_seed.py` | High — single device, deterministic flow, no heavy crypto mid-test, no `@flaky` marker |

### Known Flaky (2 tests — explicitly marked `@pytest.mark.flaky`)

| Test | File | Reruns | Root Cause |
|------|------|--------|------------|
| `test_change_password_and_login` | `test_settings_password_change_password.py` | 2 | Re-encryption blocks Android UI thread ~80s → HTTP 500 / Appium timeout |
| `test_add_and_delete_generated_account` | `test_wallet_accounts_basic.py` | 1 | Key derivation blocks accessibility tree ~60s; BrowserStack queue flakes |

### Suspected Flaky (5 tests — class-level `@flaky(reruns=1)`)

| Test | File | Primary Risk |
|------|------|-------------|
| `test_context_menu_own_message_actions` | `test_message_context_menu.py` | Long-press race with `chatLogView.moving` |
| `test_add_reaction_to_message` | `test_message_context_menu.py` | Long-press race + reaction tap timing |
| `test_copy_message_action` | `test_message_context_menu.py` | Long-press race |
| `test_reply_to_message` | `test_message_context_menu.py` | Long-press race + reply mode detection timing |
| `test_verify_reaction_on_message` | `test_message_context_menu.py` | Multi-device reaction sync over Waku — highest flakiness risk |

---

## Root Causes

### 1. BrowserStack Infrastructure Instability
- HTTP 500 errors during Appium commands
- Connection drops (`RemoteDisconnected`, `ConnectionReset`)
- Queue wait times causing session start delays
- **Evidence:** Duration variance of 11m–21m across identical runs; `_is_connection_error()` in `messaging/conftest.py` explicitly handles these

### 2. CPU-Heavy Operations Blocking Android Accessibility Tree
- Password re-encryption: ~80s UI thread block
- Key derivation (account creation): ~60s accessibility tree freeze
- During these periods, Appium cannot find elements → `NoSuchElementException` / timeout
- **Affected tests:** `test_change_password_and_login`, `test_add_and_delete_generated_account`

### 3. Long-Press Gesture Race Condition (QML)
- `onPressAndHold` in `MessageView.qml` silently ignores gestures while `chatLogView.moving == true`
- After navigation or message send, the chat view may still be decelerating
- No explicit "view settled" wait exists before long-press attempts
- **Affected tests:** All 5 `TestMessageContextMenu` tests

### 4. Multi-Device Sync Timing
- Waku message/reaction propagation between two BrowserStack devices is non-deterministic
- `test_verify_reaction_on_message` waits for reaction sync with a fixed 30s `UI_TIMEOUT`
- Network conditions on BrowserStack are variable
- **Affected tests:** `test_verify_reaction_on_message`

### 5. Module-Scoped Fixture Cascade Failure
- `established_chat` fixture establishes contact between 2 devices (180s timeout)
- If this fails, all 5 messaging tests fail together — amplifying a single infra flake into 5 failures
- The fixture already retries once, but a second failure is still possible

---

## Stabilization Plan

### Phase 1: Quick Wins (Low Risk, High Impact)

#### 1.1 Add scroll-settled wait before long-press gestures
**File:** `test/e2e_appium/pages/messaging/message_context_menu_page.py`
**Change:** In `long_press_message()`, wait for scroll deceleration before performing the gesture. Poll for the message element position stability (same coordinates in two consecutive checks ~300ms apart) before issuing the long-press.
**Impact:** Fixes root cause #3 for all 5 messaging tests.

#### 1.2 Increase `reruns` for `test_add_and_delete_generated_account`
**File:** `test/e2e_appium/tests/test_wallet_accounts_basic.py`
**Change:** Bump `@pytest.mark.flaky(reruns=1)` → `reruns=2` to match the password change test's retry budget.
**Impact:** Reduces infra-caused failures for this test.

#### 1.3 Increase `UI_TIMEOUT` for multi-device reaction sync
**File:** `test/e2e_appium/tests/messaging/test_message_context_menu.py`
**Change:** In `test_verify_reaction_on_message`, use a dedicated `SYNC_TIMEOUT = 60` (instead of `UI_TIMEOUT = 30`) for the secondary device reaction check.
**Impact:** Gives Waku more time to propagate between BrowserStack devices.

### Phase 2: Structural Improvements (Medium Risk, High Impact)

#### 2.1 Add Appium command retry middleware for transient HTTP errors
**File:** New — `test/e2e_appium/utils/appium_retry.py`
**Change:** Wrap the Appium remote driver's `execute()` method with a retry decorator that catches HTTP 500, `RemoteDisconnected`, and `ConnectionReset` errors. Retry up to 2 times with 2s backoff. Apply via a `RetryingDriver` wrapper or monkey-patch in conftest.
**Impact:** Fixes root cause #1 across ALL tests transparently.

#### 2.2 Implement element-stability polling for CPU-heavy operations
**Files:**
- `test/e2e_appium/pages/settings/settings_page.py` (password change flow)
- `test/e2e_appium/pages/wallet/wallet_left_panel.py` (account creation flow)

**Change:** After triggering re-encryption or key derivation, poll for a known post-operation element with exponential backoff (5s, 10s, 20s, 40s) up to the existing timeout budget, instead of a single `is_loaded(timeout=N)` call that may fire Appium commands during the UI freeze.
**Impact:** Fixes root cause #2 — avoids sending Appium commands while the accessibility tree is frozen.

#### 2.3 Decouple messaging tests from shared fixture failure
**File:** `test/e2e_appium/tests/messaging/conftest.py`
**Change:** Add `pytest.importorskip`-style guard: if `established_chat` fixture setup fails after all retries, mark remaining tests as `pytest.skip("Contact setup failed")` instead of `ERROR`. This prevents 5 cascading errors from a single infra flake.
**Impact:** Reduces noise — a fixture setup failure shows as 1 error + 4 skips instead of 5 errors.

### Phase 3: Observability & Prevention (Low Risk, Medium Impact)

#### 3.1 Tag tests with flakiness categories in JUnit XML
**File:** `test/e2e_appium/conftest.py`
**Change:** In `pytest_runtest_makereport`, when a test with `@flaky` marker fails and then passes on rerun, emit a JUnit XML property `<property name="flaky" value="true"/>`. This enables tracking flaky test frequency in CI dashboards.
**Impact:** Enables data-driven decisions about which tests to stabilize next.

#### 3.2 Add CI workflow step to parse and surface flaky reruns
**File:** `.github/workflows/e2e-gate-browserstack.yml`
**Change:** After the test run, add a step that parses `gate-junit.xml` for tests that failed then passed (rerun pattern) and surfaces them in the GitHub Step Summary with a warning icon.
**Impact:** Makes flaky tests immediately visible in PR reviews without digging into logs.

#### 3.3 Add `--reruns 1` as a workflow-level default
**File:** `.github/workflows/e2e-gate-browserstack.yml`
**Change:** In the `Run tests` step, add `--reruns 1 --reruns-delay 5` to the base `PYTEST_CMD` (currently hardcoded to `--reruns 0`). Individual tests with higher rerun counts via `@pytest.mark.flaky` will override this.
**Impact:** Provides a baseline safety net for all gate tests against transient infra flakes.

---

## Investigation Steps (To Gather More Data)

1. **Download artifacts** from all 5 attempts (`gate-results-21`) and diff the JUnit XML files to identify exactly which test(s) failed in attempts 1 and 4.
2. **Check BrowserStack dashboard** for session recordings of failed runs — look for visible UI freezes during re-encryption/key derivation.
3. **Grep BrowserStack session logs** for `RemoteDisconnected` / HTTP 500 to confirm infra-level failures vs. genuine test logic failures.
4. **Run messaging tests in isolation** (just the 5 gate messaging tests) 10 times to measure their individual flake rates independently of the wallet/settings tests.
5. **Instrument `long_press_message()`** with timing logs to confirm the `chatLogView.moving` race condition hypothesis — log the time between navigation and first successful long-press.

---

## Priority Order

| Priority | Item | Effort | Expected Impact |
|----------|------|--------|-----------------|
| P0 | 1.1 Scroll-settled wait | 2h | Stabilizes 5 messaging tests |
| P0 | 2.1 Appium retry middleware | 3h | Reduces all infra flakes |
| P1 | 1.3 Increase sync timeout | 15min | Stabilizes `test_verify_reaction_on_message` |
| P1 | 2.2 Element-stability polling | 2h | Stabilizes 2 wallet/settings tests |
| P1 | 3.3 Workflow-level `--reruns 1` | 15min | Safety net for all tests |
| P2 | 1.2 Bump wallet reruns | 5min | Quick mitigation |
| P2 | 2.3 Fixture cascade guard | 1h | Reduces failure noise |
| P3 | 3.1 Flaky tagging in JUnit | 1h | Observability |
| P3 | 3.2 CI flaky summary | 1h | Observability |
