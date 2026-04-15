# Black Testing Framework

pytest automation framework cho Windows app (PC17 + S2VNA) + USB Serial device.

---

## Cấu trúc dự án

```
black-testing-framework/
├── config/
│   ├── loader.py            # Pydantic models + get_settings()
│   └── settings.yaml        # Cấu hình chính (app, serial, relay, report)
├── core/
│   ├── app_controller.py    # pywinauto wrapper (click, type, screenshot...)
│   ├── relay_controller.py  # USB relay board (CH340 protocol)
│   ├── serial_device.py     # pyserial wrapper (send/recv/query)
│   └── testcase_decorator.py# @testcase decorator + @tag docstring parser
├── pages/
│   ├── base_page.py         # BasePage — delegate xuống AppController
│   ├── main_page.py         # PC17 FormMainEliteRF (connect + detail)
│   ├── s2vna_page.py        # S2VNA simulator page
│   └── setup_page.py        # SetupPage — helper setup session
├── tests/
│   ├── attenuator/          # TC-0001, TC-0002 (real HW)
│   ├── demo/                # Mock fixtures, không cần HW
│   └── vna/
│       ├── conftest.py      # Fixture s2vna_ctrl, s2vna_page
│       └── test_puc_2_1_vna_power.py
├── utils/
│   ├── logger.py            # get_logger() — console + file handler
│   └── report_excel.py      # ExcelReporter + TestResult
├── conftest.py              # Root fixtures + pytest hooks
├── pytest.ini               # markers, addopts, logging
├── Jenkinsfile              # CI/CD pipeline
└── README_CICD_SETUP.md     # Hướng dẫn cài Jenkins + Task Scheduler
```

---

## Quick Start

```bash
# Cài dependencies
pip install -r requirements.txt

# Chạy demo (không cần hardware)
pytest tests/demo/ -v

# Chạy VNA tests
pytest tests/vna/ -v

# Chạy theo marker
pytest -m "functional and hw_depend"
pytest -m "not hw_depend"

# Chạy 1 test case cụ thể
pytest tests/vna/ -k "test_vna_puc_2_1_0001" -v

# Override COM port
set SERIAL_PORT=COM5 && pytest tests/
```

---

## Fixtures

Khai báo trong `conftest.py` (root) và `tests/vna/conftest.py`:

| Fixture | Scope | Mô tả |
|---------|-------|-------|
| `app_ctrl` | session | AppController cho PC17 — tự launch nếu chưa chạy |
| `main_page` | session | MainPage — tự chạy `setup_connection()` một lần |
| `device` | session | SerialDevice — mở COM port DUT |
| `relay` | session | RelayController — disabled by default |
| `s2vna_ctrl` | session | AppController cho S2VNA (chỉ trong `tests/vna/`) |
| `s2vna_page` | session | S2VnaPage (chỉ trong `tests/vna/`) |

---

## Viết test case mới

```python
from core import testcase
from pages.main_page import MainPage

@testcase
def test_feature_tc_XXXX(main_page: MainPage):
    """
    @test_id: test_feature_tc_XXXX
    @brief: Mô tả ngắn (1 dòng)
    @details: Chi tiết test case

    @pre:- Điều kiện tiên quyết 1
         - Điều kiện tiên quyết 2

    @test_procedure:
        [code]
            - Bước 1: làm gì đó
            - Bước 2: kiểm tra gì đó
        [!code]

    @pass_criteria:- Kết quả mong đợi

    @test_level: software
    @test_type: functional
    @execution_type: automatic
    @hw_depend: yes
    """
    main_page.click_detail()
    temperature = main_page.get_temperature()
    assert temperature not in [None, "", ":"], f"Invalid: {temperature!r}"
```

**Giá trị hợp lệ cho các tag:**

| Tag | Giá trị |
|-----|---------|
| `@test_level` | `system` `integration` `unit` `software` |
| `@test_type` | `functional` `regression` `smoke` |
| `@execution_type` | `automatic` `semi_automatic` `manual` |
| `@hw_depend` | `yes` / `no` |

---

## Pages

### `MainPage` — PC17 FormMainEliteRF

```python
# Setup (tự động qua fixture)
main_page.setup_connection()   # Tools → RF Test Set → System → Connect → Connected

# Trạng thái kết nối
main_page.is_connected() -> bool
main_page.click_disconnect()

# Detail panel
main_page.click_detail()
main_page.get_temperature()    -> str   # text sau label "Temperature"
main_page.get_serial_number()  -> str   # text sau label "Serial Number"

# Attenuator (nếu có)
main_page.turn_on_attenuator()
main_page.turn_off_attenuator()
main_page.get_attenuator_status() -> str
main_page.is_attenuator_on()      -> bool
```

### `S2VnaPage` — S2VNA Simulator

```python
s2vna_page.click_connect()
s2vna_page.is_connected() -> bool
s2vna_page.power_on()
s2vna_page.power_off()
s2vna_page.is_powered_on() -> bool
s2vna_page.set_freq_start("1000000")
s2vna_page.set_freq_stop("3000000000")
s2vna_page.click_sweep()
```

---

## Cấu hình (`config/settings.yaml`)

```yaml
app:
  name: "FormMainEliteRF"
  exe_path: "C:/PC17/PC17.exe"
  backend: "uia"

s2vna:
  name: "S2VNA"
  exe_path: "C:/VNA/S2VNA/S2VNA.exe"
  backend: "uia"
  startup_wait: 3

serial:
  default_port: "COM3"    # override: set SERIAL_PORT=COM5
  baudrate: 115200

relay:
  enabled: false          # bật khi có phần cứng relay
```

**Override bằng env var:**
```bash
set SERIAL_PORT=COM5
set APP_EXE_PATH=C:\MyApp\PC17.exe
set S2VNA_EXE_PATH=C:\VNA\S2VNA\S2VNA.exe
```

---

## Reports

Sau khi chạy, kết quả tại:

```
reports/
├── html/report.html          # HTML report (mở trình duyệt)
├── excel/test_results.xlsx   # Excel: PASS=xanh, FAIL=đỏ, SKIP=vàng
├── junit.xml                 # JUnit XML cho Jenkins
├── logs/
│   ├── framework.log
│   └── pytest.log
└── screenshots/              # Tự chụp khi test FAIL
```

---

## Tìm element identifier

```python
from pywinauto import Application

# PC17
app = Application(backend="uia").connect(title_re=".*FormMainEliteRF.*")
app.top_window().print_control_identifiers(depth=5)

# S2VNA
app = Application(backend="uia").connect(title_re=".*S2VNA.*")
app.top_window().print_control_identifiers(depth=5)
```

---

## CI/CD

Xem hướng dẫn đầy đủ tại [README_CICD_SETUP.md](README_CICD_SETUP.md).

Tóm tắt nhanh:
- Jenkins chạy qua **Task Scheduler** (không phải service) để có interactive session
- Apps (S2VNA, PC17) được launch bởi Task Scheduler trước khi pytest chạy
- Trigger: `http://localhost:8080/job/PC17-Tests` → **Build with Parameters**
