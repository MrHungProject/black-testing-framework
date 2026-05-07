# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Windows GUI automation testing framework for PC17 (RF Test Set) + S2VNA (Vector Network Analyzer). Uses **pytest + pywinauto** with a Page Object Model (POM) pattern. Tests interact with real Windows applications (PC17, S2VNA, Spike) via UIA accessibility tree.

## Common Commands

```bash
# Run all tests
pytest tests/ -v

# Run a single module
pytest tests/vna/ -v
pytest tests/spectrumanalyzer/ -v

# Run a single test case
pytest tests/vna/test_puc_2_1_vna_power.py -k "0007" -v --tb=short -s

# Run by marker
pytest -m "automatic and hw_depend" -v
pytest -m "not hw_depend" -v

# Override COM port
set SERIAL_PORT=COM5 && pytest tests/
```

## Architecture

### Layer Stack
```
Test files (tests/)
    └── MainPage facade (pages/main_page.py)
           └── Panel objects (pages/panels/*.py)
                  └── BasePage (pages/base_page.py)
                         └── AppController (core/app_controller.py)
                                └── pywinauto (UIA backend)
```

### AppController (`core/app_controller.py`)
Central pywinauto wrapper. Key interaction methods:
- `click_by_text(text)` — scan `_main_window.descendants()`, click matching control
- `select_from_desktop_popup(text)` — scan ALL desktop windows (for dropdown popups that open at Desktop level, e.g. Trace selector, Calibrate menu)
- `click_in_any_window(text)` — same as above but skips `is_enabled()` check (for list items/menu items)
- `set_field_by_label(label, value)` — find label → find nearest Edit → Ctrl+A → set_edit_text → Enter
- `build_cache()` / `invalidate_cache()` — batch multiple `descendants()` scans into one (critical for performance; `descendants()` costs ~3.5s per call)
- `wait_for_text(text, timeout)` — polls `_main_window.descendants()` until text appears

### Panel Objects (`pages/panels/`)
Each panel manages one UI section. All inherit `BasePage` and take an `AppController`.

| Panel | Key feature |
|---|---|
| `SystemPanel` | Per-device connect/disconnect (must be on Connect panel for `is_device_connected()` to work) |
| `VnaPanel` | Measurement/Stimulus/Markers/Calibration tabs; floating `FormDetailVNACalibration` uses `auto_id` navigation |
| `SpectrumPanel` | Analysis Mode radio buttons (click right of label by offset px); toggle-safe `open_sweep_settings()` |
| `SignalPanel` | RF1 output + Trigger output; `check_validation_errors()` after Apply |
| `DetailPanel` | Read-only Temperature + Serial Number |

### MainPage (`pages/main_page.py`)
Thin facade — every method delegates to a panel. Add a delegation here whenever a new panel method is created.

## Test Structure & Conventions

### Naming
- File: `test_puc_{module}_{sequence}_{feature}.py` → e.g. `test_puc_2_1_vna_power.py`
- Class: `TestVnaPuc21`, `TestSpectrumPuc43ZeroSpan`
- Method: `test_vna_puc_2_1_0001` (zero-padded 4-digit sequence)
- `@test_id` in docstring must match method name exactly

### `@testcase` Decorator
Every test method must use this decorator. It parses the structured docstring and applies pytest marks automatically (`@test_level`, `@test_type`, `@execution_type`, `hw_depend`). Tests with `@execution_type: manual` are auto-skipped unless `-m manual` is passed.

```python
@testcase
def test_vna_puc_2_1_0001(self, main_page: MainPage):
    """
    @test_id: test_vna_puc_2_1_0001
    @brief: One-line summary
    @execution_type: automatic
    @hw_depend: yes
    """
```

### Class-level `_ensure_connected` Fixture (standard pattern)
Every test class uses an `autouse=True` fixture to guarantee device connection before each TC. Check `is_device_connected()` first — only navigate to Connect panel if needed (avoids unnecessary panel switching):

```python
@pytest.fixture(autouse=True)
def _ensure_connected(self, main_page: MainPage):
    if main_page.is_device_connected(self._DEVICE_LABEL):
        return  # already connected, skip navigation
    main_page.open_connect_panel()
    if not main_page.is_device_connected(self._DEVICE_LABEL):
        main_page.connect_device(self._DEVICE_LABEL)
        time.sleep(3)
```

### Fixture Scopes
- **Session**: `s2vna_ctrl`, `app_ctrl`, `main_page` — launched once, shared across all tests
- **Function**: `_ensure_connected` (autouse per-class) — runs before each test method
- S2VNA must launch **before** PC17 (dependency declared via fixture parameter)

## Critical Patterns

### UI Element Identification (priority order)
1. `auto_id` (most reliable) — use `child_window(auto_id="...")` for known forms
2. `click_by_text()` for controls in `_main_window.descendants()`
3. `select_from_desktop_popup()` for dropdowns that open outside the main window
4. `click_in_any_window()` when `is_enabled()` returns False for valid targets (e.g. list items)

### Toggle-Safe Navigation
Several nav items (SPECTRUM panel, Sweep Settings, VNA card) toggle open/closed. Pattern:
```python
if not self._ctrl.wait_for_text("ExpectedChild", timeout=5):
    # click again to re-open (toggle closed by first click)
    self._ctrl.click_by_text("NavItem", retries=5)
    self._ctrl.wait_for_text("ExpectedChild", timeout=5)
```

### VNA Calibration Flow
`FormDetailVNACalibration` is a child window of FormMainEliteRF (not a Desktop popup):
- Click "Calibrate" via `auto_id="selectCustomTypeButton1"` on `FormDetailVNACalibration`
- After selecting "2-Port SOLT Cal", wizard `FormDetailVNACalibration2Port` appears
- 7 calibration buttons: `btnOpen`, `btnShort`, `btnLoad`, `btnOpen2`, `btnShort2`, `btnLoad2`, `btnThru`
- Apply = `btnSave`, Cancel = `btnCancel`

### Performance
- `descendants()` costs ~3.5s — always use `build_cache()` before multiple `set_field_by_label()` calls, then `invalidate_cache()` after
- Replace `time.sleep(N)` with `wait_for_text(text, timeout=N)` wherever possible
- `click_by_text()` retry sleep is 0.3s; `wait_for_text()` polls every 0.2s

### Validation Errors
After clicking Apply on any form, check `check_validation_errors()` (defined in `BasePage`). Returns `list[str]` of error messages. Log warning if non-empty, assert empty if test requires clean input.

## Configuration

`config/settings.yaml` is the primary config. Override via env vars:
- `SERIAL_PORT` — COM port for serial device
- `APP_EXE_PATH` — PC17 exe path
- `S2VNA_EXE_PATH` — S2VNA exe path

Key settings: `app.action_delay` (global click delay, currently 0.1s), `app.connect_timeout`.

## Reports

Auto-generated on session end:
- `reports/excel/[suite]_report.xlsx` — color-coded pass/fail with metadata
- `reports/html/report.html` — pytest-html
- `reports/junit.xml` — for Jenkins
- `reports/logs/framework.log` — full framework log
- `reports/screenshots/` — auto-captured per test

`TEST_SUITE` env var controls Excel report naming/grouping.
