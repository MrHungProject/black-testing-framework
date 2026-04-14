# Black Testing Framework

pytest-based automation framework for Windows app + USB device testing.

## Quick Start

```bash
pip install -r requirements.txt
pytest                                      # run all
pytest tests/attenuator/                   # run one module
pytest -m "functional and hw_depend"       # run by marker
pytest -m "not hw_depend"                  # skip hardware tests
```

## Cấu trúc

```
├── config/           # settings.yaml → typed config
├── core/
│   ├── testcase_decorator.py   ← parse @tag docstring + apply pytest marks
│   ├── app_controller.py       ← pywinauto wrapper (click, type, screenshot)
│   ├── serial_device.py        ← USB Serial (COM port)
│   └── relay_controller.py     ← Power relay (enable in settings.yaml)
├── pages/            # Page Object Model cho từng màn hình của app
├── tests/            # Test files — mỗi folder = 1 module/feature
├── utils/
│   ├── logger.py
│   └── report_excel.py
└── conftest.py       # Fixtures + hooks → tự generate Excel report
```

## Viết test case mới

```python
from core import testcase
from pages.main_page import MainPage

@testcase
def test_feature_tc_XXXX(main_page: MainPage, device):
    """
    @test_id: test_feature_tc_XXXX
    @brief: Mô tả ngắn
    @details: Chi tiết

    @pre:- Điều kiện trước khi chạy

    @test_procedure:
        [code]
            - Bước 1
            - Bước 2
        [!code]

    @pass_criteria:- Kết quả mong đợi

    @test_level: system
    @test_type: functional
    @execution_type: semi-automatic
    @hw_depend: yes
    """
    # === CODE AUTOMATION ===
    main_page.click("SomeButton")
    assert ...
```

## Tìm element identifier của app

```python
from pywinauto import Application
app = Application(backend="uia").connect(title_re=".*PC17.*")
app.top_window().print_control_identifiers(depth=5)
```

## Reports

- HTML: `reports/html/report.html`
- Excel: `reports/excel/test_results.xlsx`
- Log:   `reports/logs/`
- Screenshots on fail: `reports/screenshots/`

## Config

Chỉnh sửa `config/settings.yaml` cho:
- Tên app / exe path
- COM port / baudrate
- Relay (bật khi có phần cứng)
- TestRail integration
