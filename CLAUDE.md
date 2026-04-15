# Black Testing Framework — CLAUDE.md

Framework pytest cho automation testing Windows app (pywinauto) + USB Serial device trên Windows.

---

## Cấu trúc dự án

```
black-testing-framework/
├── config/
│   ├── __init__.py          → export get_settings, Settings
│   ├── loader.py            → Pydantic models + get_settings() với lru_cache
│   └── settings.yaml        → config chính (app, serial, relay, report, testrail)
├── core/
│   ├── __init__.py          → export testcase, TestCaseMetadata
│   ├── app_controller.py    → pywinauto wrapper (click, type, screenshot...)
│   ├── relay_controller.py  → USB relay board control (CH340 protocol)
│   ├── serial_device.py     → pyserial wrapper (send/recv/query/auto-detect)
│   └── testcase_decorator.py → @testcase decorator + docstring @tag parser
├── pages/
│   ├── __init__.py          → export BasePage
│   ├── base_page.py         → Page Object base (delegate to AppController)
│   └── main_page.py         → PC17 main window POM (locators + actions)
├── tests/
│   ├── attenuator/
│   │   └── test_tc_0001_turn_on_attenuator.py  → TC-0001 + TC-0002 (real HW)
│   ├── demo/
│   │   ├── conftest.py      → Mock fixtures (không cần HW thật)
│   │   └── test_demo_attenuator.py  → TC-0001~0005 dùng mock
│   └── vna/
│       └── test_puc_2_1_vna_power.py  → VNA power test (TC1 normal + TC2 abnormal)
├── utils/
│   ├── __init__.py          → export get_logger
│   ├── logger.py            → logging factory (console + file handler)
│   └── report_excel.py      → ExcelReporter + TestResult dataclass
├── conftest.py              → Root fixtures (session-scoped) + pytest hooks
├── pytest.ini               → test discovery, markers, logging, addopts
├── requirements.txt         → dependencies
├── Jenkinsfile              → CI/CD pipeline (Windows agent, label: windows-dut)
├── CICD_SETUP.md            → hướng dẫn cài Jenkins
└── README.md                → quick start + cách viết test mới
```

---

## Config (`config/`)

### `config/loader.py`

```python
from config import get_settings

settings = get_settings()  # lru_cache, đọc settings.yaml 1 lần
settings.app.exe_path      # AppConfig
settings.serial.default_port
settings.relay.enabled
settings.report.output_dir
settings.testrail.enabled
```

**Pydantic models:**
- `AppConfig` — name, exe_path, backend ("uia"|"win32"), connect_timeout=15, action_delay=0.3
- `S2VnaConfig` — name, exe_path, backend, connect_timeout, startup_wait=3
- `SerialConfig` — default_port="COM3", baudrate=115200, timeout=2.0, auto_detect=True
- `RelayConfig` — enabled=False, port="COM10", baudrate=9600, channels=4, power_cycle_delay=3.0
- `ReportConfig` — output_dir, html_dir, excel_dir, log_dir, excel_filename, screenshot_on_fail=True
- `TestRailConfig` — enabled=False, url, username, api_key, project_id, suite_id

**Env var overrides (CI/CD):**
- `SERIAL_PORT` → `serial.default_port`
- `APP_EXE_PATH` → `app.exe_path`
- `RELAY_PORT` → `relay.port`
- `S2VNA_EXE_PATH` → `s2vna.exe_path`

---

## Core (`core/`)

### `core/app_controller.py` — `AppController`

Wrapper pywinauto. Nếu pywinauto không install → chạy STUB mode (warning log, không crash).

```python
ctrl = AppController(app_name="PC17", backend="uia")
ctrl.connect()     # connect to running app (title_re matching)
ctrl.launch()      # start exe_path then connect
ctrl.disconnect()

# Actions
ctrl.click(identifier)          # identifier: str hoặc dict {"auto_id": ..., "control_type": ...}
ctrl.double_click(identifier)
ctrl.type_text(identifier, text)
ctrl.set_value(identifier, value)  # Ctrl+A then type
ctrl.get_text(identifier) -> str
ctrl.wait_for_element(identifier, timeout=10) -> bool
ctrl.is_element_enabled(identifier) -> bool
ctrl.select_combobox(identifier, item)
ctrl.check_checkbox(identifier, state=True)
ctrl.take_screenshot(filename)  # saved to reports/screenshots/
ctrl.print_ui_tree(depth=5)     # debug: tìm element identifiers
```

`_get_element(identifier)` — thử tuần tự: auto_id → title → class_name.

### `core/relay_controller.py` — `RelayController`

Protocol CH340 relay boards: `bytes([0xA0, channel, cmd_byte, checksum])`.

```python
relay = RelayController()
relay.connect()
relay.on(channel=1)        # 1-based
relay.off(channel=1)
relay.all_on()
relay.all_off()
relay.power_cycle(channel=1)  # OFF → sleep(cycle_delay) → ON
relay.disconnect()

# Context manager
with RelayController() as relay:
    relay.power_cycle(1)
```

Nếu `relay.enabled=False` → log info, không kết nối thật.

### `core/serial_device.py` — `SerialDevice`

```python
dev = SerialDevice(port="COM3", baudrate=115200)
dev.open()
dev.send("VOLT?\r\n")       # encode utf-8, returns bytes written
dev.readline() -> str       # strip whitespace
dev.read_all() -> str
dev.query("CMD\r\n", delay=0.1) -> str   # flush + send + sleep + readline
dev.flush()                 # reset_input_buffer + reset_output_buffer
dev.read_voltage("VOLT?\r\n") -> float   # parse float từ response
dev.is_connected(ping="PING\r\n", expected="OK") -> bool
dev.wait_for_response(expected, timeout=5.0, poll=0.2) -> bool
dev.close()

# Static helpers
SerialDevice.list_ports() -> List[str]
SerialDevice.find_port_by_description(keyword) -> Optional[str]
SerialDevice.find_port_by_vid_pid(vid, pid) -> Optional[str]
```

Override `_detect_port()` để auto-detect thiết bị cụ thể.

### `core/testcase_decorator.py` — `@testcase` decorator

Parse docstring `@tag:` format → `TestCaseMetadata` → apply pytest marks.

```python
from core import testcase

@testcase
def test_feature_tc_0001(main_page, device):
    """
    @test_id: test_feature_tc_0001
    @brief: Mô tả ngắn (1 dòng)
    @details: Chi tiết test case

    @pre:- Điều kiện tiên quyết 1
         - Điều kiện tiên quyết 2

    @test_procedure:
        [code]
            - Bước 1: làm gì đó
            - Bước 2: kiểm tra gì đó
        [!code]

    @pass_criteria:- Kết quả mong đợi 1
                   - Kết quả mong đợi 2

    @test_level: system          # system | integration | unit
    @test_type: functional       # functional | regression | smoke
    @execution_type: semi_automatic  # automatic | semi_automatic | manual
    @hw_depend: yes              # yes/true/1 hoặc no/false/0
    """
```

**Marks tự động được apply:**
- `pytest.mark.test_id(meta.test_id)`
- `pytest.mark.<test_level>` (system, integration, unit)
- `pytest.mark.<test_type>` (functional, regression, smoke)
- `pytest.mark.<execution_type>` (automatic, semi_automatic, manual)
- `pytest.mark.hw_depend` (nếu hw_depend=True)

**`TestCaseMetadata` fields:**
`test_id`, `brief`, `details`, `pre: List[str]`, `procedure_steps: List[str]`,
`procedure_raw: str`, `pass_criteria: List[str]`, `test_level`, `test_type`,
`execution_type`, `hw_depend: bool`

---

## Pages (`pages/`)

### `pages/base_page.py` — `BasePage`

Abstract base. Constructor nhận `AppController`. Delegate tất cả action xuống controller.

```python
class BasePage:
    def __init__(self, controller: AppController): ...
    def click(identifier), double_click, type_text, set_value
    def get_text(identifier) -> str
    def is_enabled(identifier) -> bool
    def wait_for(identifier, timeout=10) -> bool
    def select(identifier, item)
    def screenshot(name)
```

### `pages/main_page.py` — `MainPage(BasePage)`

Page Object cho main window PC17. **Locators là placeholder** — cần thay bằng auto_id thật.

**Locators (dict):**
```python
BTN_ATTENUATOR_ON   = {"auto_id": "btnAttenuatorOn",  "control_type": "Button"}
BTN_ATTENUATOR_OFF  = {"auto_id": "btnAttenuatorOff", "control_type": "Button"}
LBL_ATTENUATOR_STATUS = {"auto_id": "lblAttenuatorStatus"}
CMB_PORT            = {"auto_id": "cmbPort"}
BTN_CONNECT         = {"auto_id": "btnConnect"}
BTN_DISCONNECT      = {"auto_id": "btnDisconnect"}
LBL_CONN_STATUS     = {"auto_id": "lblConnectionStatus"}
LBL_APP_STATUS      = {"auto_id": "lblAppStatus"}
BTN_APPLY           = {"auto_id": "btnApply"}
BTN_RESET           = {"auto_id": "btnReset"}
```

**Actions:**
```python
page.turn_on_attenuator()        page.turn_off_attenuator()
page.get_attenuator_status() -> str
page.is_attenuator_on() -> bool  # "on"|"ready"|"active" in status.lower()
page.select_port(port)
page.click_connect()             page.click_disconnect()
page.get_connection_status() -> str
page.is_connected() -> bool      # "connected" in status.lower()
page.get_app_status() -> str
page.click_apply()               page.click_reset()
```

**Tìm locators thật:**
```python
from pywinauto import Application
app = Application(backend="uia").connect(title_re=".*PC17.*")
app.top_window().print_control_identifiers(depth=5)
```

---

## Root `conftest.py` — Fixtures & Hooks

### Session-scoped fixtures

| Fixture | Type | Mô tả |
|---------|------|--------|
| `s2vna_ctrl` | `AppController` | Launch/connect S2VNA simulator (trước PC17) |
| `app_ctrl` | `AppController` | Launch/connect PC17 (depends on s2vna_ctrl) |
| `main_page` | `MainPage` | Page Object, dùng chung cả session |
| `device` | `SerialDevice` | Mở serial port DUT |
| `relay` | `RelayController` | Relay board (disabled by default) |

### Per-test fixtures

`_log_test_boundaries` (autouse): log START/END + duration cho mỗi test, dùng `meta.test_id` từ `@testcase`.

### Pytest hooks

- `pytest_runtest_makereport` — attach `item` vào report object
- `pytest_runtest_logreport` (call phase only):
  - Screenshot on fail (nếu `screenshot_on_fail=True`) → `reports/screenshots/FAIL_<id>_<ts>.png`
  - Append `TestResult` vào `_session_results`
- `pytest_sessionfinish` → `ExcelReporter().generate(_session_results)`

---

## `utils/`

### `utils/logger.py` — `get_logger(name)`

```python
from utils.logger import get_logger
logger = get_logger(__name__)
```

Tạo logger với 2 handlers: console (stdout) + file (`reports/logs/framework.log`).
`lru_cache` không dùng nhưng kiểm tra `logger.handlers` để tránh duplicate.

### `utils/report_excel.py` — `ExcelReporter`

```python
from utils.report_excel import ExcelReporter, TestResult

result = TestResult(
    test_id="tc_001", brief="...", test_level="system",
    test_type="functional", execution_type="automatic",
    hw_depend=True, outcome="passed", duration="1.23",
    error_message="", nodeid="tests/..."
)

reporter = ExcelReporter(output_path=None)  # dùng config.report
reporter.generate([result])  # tạo 2 sheets: Summary + Test Results
```

**Sheet "Summary":** Total, PASSED (green), FAILED (red), SKIPPED (yellow), pass rate.
**Sheet "Test Results":** Header màu xanh, mỗi row tô màu theo outcome.

---

## Tests

### `tests/demo/` — Chạy không cần hardware

```bash
pytest tests/demo/ -v
```

**Mock classes trong `tests/demo/conftest.py`:**
- `MockAppController` — state dict: `{"attenuator": "OFF", "connection": "Disconnected"}`
- `MockSerialDevice` — `read_voltage()` trả 3.3V khi `_powered=True`, 0.0 khi False
- `MockMainPage` — `turn_on/off_attenuator()` sync cả ctrl._state và device._powered

**Test cases demo:**
- TC-0001: Turn on Attenuator → PASS
- TC-0002: Turn off Attenuator → PASS
- TC-0003: Connection status → PASS
- TC-0004: Intentional FAIL (demo report đỏ) — assert voltage > 5.0
- TC-0005: Skip (relay chưa có HW)

### `tests/attenuator/` — Real hardware

Dùng fixtures từ root conftest. TC-0001 (ON) + TC-0002 (OFF).

### `tests/vna/` — VNA tests

- `test_vna_puc_2_1_normal` — bật VNA, verify voltage + UI (thân rỗng, cần implement)
- `test_vna_puc_2_1_0001` — bật/tắt 5 lần (thân rỗng, cần implement)

---

## `pytest.ini`

```ini
testpaths = tests
addopts = -v --tb=short --strict-markers
          --html=reports/html/report.html --self-contained-html
          --junitxml=reports/junit.xml
log_cli = true | log_cli_level = INFO
log_file = reports/logs/pytest.log | log_file_level = DEBUG
```

**Markers đã đăng ký:** system, integration, unit, functional, regression, smoke,
semi_automatic, automatic, manual, hw_depend, test_id

---

## Chạy tests

```bash
# Demo (mock, không cần HW)
pytest tests/demo/ -v

# Chạy theo marker
pytest -m "functional and hw_depend"
pytest -m "not hw_depend"
pytest -m smoke

# Specific module
pytest tests/attenuator/
pytest tests/vna/

# Override serial port
SERIAL_PORT=COM5 pytest tests/
```

---

## CI/CD (`Jenkinsfile`)

- Agent label: `windows-dut`
- Parameters: `TEST_SUITE` (demo/vna/all), `COM_PORT` (default COM3), `SKIP_HW_TESTS`
- Trigger: `githubPush()` webhook
- Stages: Checkout → Setup venv (`call .venv\Scripts\activate.bat`) → Prepare dirs → Run Tests
- exitCode < 2 → build SUCCESS (1 = test failures, chỉ fail khi pytest crash ≥ 2)
- Post: `junit`, `archiveArtifacts`, `publishHTML` (HTML Publisher plugin cần cài)

---

## Thêm test case mới

1. Tạo file `tests/<module>/test_<name>.py`
2. Dùng `@testcase` decorator + đầy đủ `@tag` docstring
3. Dùng fixtures: `main_page`, `device`, `relay` (từ root conftest)
4. Thêm locator mới vào `MainPage` nếu cần, hoặc tạo page class mới kế thừa `BasePage`

---

## Dependencies chính

| Package | Mục đích |
|---------|---------|
| pytest>=8.0.0 | test runner |
| pywinauto>=0.6.8 | Windows UI automation |
| pyserial>=3.5 | USB Serial |
| pydantic>=2.6.0 | config validation |
| openpyxl>=3.1.2 | Excel report |
| pytest-html>=4.1.0 | HTML report |
| allure-pytest>=2.13.5 | Allure report |
| PyYAML>=6.0.1 | settings.yaml |
