# AGENTS.md

## Cursor Cloud specific instructions

### Scope

This environment is configured for the **E2E Appium test framework** at `test/e2e_appium/`. The main Status Desktop/Mobile build toolchain (Nim, Qt, Go, CMake) is **not** in scope.

### Python environment

- Python 3.11 is installed via the `deadsnakes` PPA (`python3.11`). The CI uses 3.11.9; the VM has 3.11.x.
- A virtualenv lives at `test/e2e_appium/.venv` (created with `python3.11 -m venv`).
- Always activate it before running anything: `source test/e2e_appium/.venv/bin/activate`
- All commands below assume the venv is active.

### Running tests

Tests must be run from inside `test/e2e_appium/` (the `pytest.ini` sets `pythonpath = .`).

```bash
cd test/e2e_appium
source .venv/bin/activate

# Collect tests (dry run)
python -m pytest --collect-only -q

# Run unit-like infrastructure tests (no device/cloud needed)
python -m pytest tests/test_multi_device_infrastructure.py -v --env=local --timeout=30

# Run by marker (requires cloud credentials or local Appium)
python -m pytest -m smoke --env=local -v
```

Device-dependent tests (onboarding, messaging, wallet, etc.) require either:
- **BrowserStack** (default, `--env=browserstack`): `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY` env vars are configured as secrets. Also needs `BROWSERSTACK_APP_ID` (e.g. `bs://...`) pointing to an uploaded APK.
- **LambdaTest** (`--env=lambdatest`, used in CI): `LT_USERNAME` / `LT_ACCESS_KEY` env vars.
- **Local Appium server** (`--env=local`): Appium at `localhost:4723` with an Android emulator and a Status APK (`LOCAL_APP_PATH` env var).

To run device tests against BrowserStack, upload an APK first (via BrowserStack dashboard or API), then:
```bash
export BROWSERSTACK_APP_ID="bs://YOUR_APP_HASH"
python -m pytest -m onboarding --env=browserstack -v
```

### Linting

The cursor rules require all Python code to pass `ruff check .` before committing. `ruff` is installed in the venv.

```bash
cd test/e2e_appium
ruff check .          # lint
ruff check . --fix    # auto-fix import sorting and simple issues
```

Note: the existing codebase has ~19 pre-existing ruff findings (unused imports/variables). These are in the existing code, not introduced by agents.

### Key gotchas

- **Circular import**: Importing `config` directly in a standalone script fails due to a circular import through `core/__init__.py` → `session_manager` → `config`. This does **not** affect pytest because pytest handles module loading via its plugin system. Always use `python -m pytest` to run tests.
- **`--env` flag**: Defaults to `browserstack`. Use `--env=local` for local development. The flag sets `CURRENT_TEST_ENVIRONMENT` internally.
- **Config fallback**: When cloud credentials are missing, the framework logs a warning and falls back to default config. Test collection and unit-like tests still work.
- **Generated reports**: pytest auto-generates XML and HTML reports under `reports/`. These are gitignored.
- **Node.js dependency**: `package.json` in `test/e2e_appium/` is only for the `scripts/commit_status_manager.js` GitHub commit status tool. Not needed for running tests.
- **BrowserStack validation**: `EnvironmentConfig.validate()` for BrowserStack checks for `BROWSERSTACK_APP_ID`. Without it, loading the config with validation will raise `ConfigurationError`. Set a placeholder (`bs://placeholder`) if you only need config/plan API access without launching a session.
- **Standalone scripts**: To import framework modules outside pytest (e.g. in a standalone script), use `sys.path.insert(0, '.')` and import from `core.config_manager` / `core.providers` directly. Do not import from `config` top-level due to the circular import issue.
- **Accessibility tree blocking**: Crypto operations (wallet account creation, password re-encryption) block the Android UI thread for up to 60–80s on BrowserStack, causing all UiAutomator2 commands to return HTTP 500. Use polling loops with 90s deadlines and 1–2s per-probe timeouts. After the blocking ends, the tree may return garbage (dicts instead of WebElements, empty results). **Never treat "element not found" as "element dismissed"** — always require positive confirmation of the expected UI state (e.g. wallet panel visible). Use `wait_for_condition()` instead of single-shot queries. See `e2e-browserstack-gotchas.mdc` for full details.
- **Keyboard hide failures**: `hide_keyboard()` fails on Qt/QML apps on BrowserStack. Treat it as best-effort; never gate logic on its return value. Tap a neutral area and scroll instead. See `PasswordChangePage._dismiss_keyboard_for_submit()`.
