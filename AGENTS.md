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
- **Cloud credentials**: `LT_USERNAME` / `LT_ACCESS_KEY` env vars for LambdaTest, or `BROWSERSTACK_USERNAME` / `BROWSERSTACK_ACCESS_KEY` for BrowserStack.
- **Local Appium server** at `localhost:4723` with an Android emulator and a Status APK (`LOCAL_APP_PATH` env var).

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
