"""
DEMO — Attenuator test suite chạy với mock (không cần hardware thật).

Chạy:
    pytest tests/demo/ -v

Sau khi chạy:
    reports/html/report.html      ← mở bằng browser
    reports/excel/test_results.xlsx
"""
import pytest
from core import testcase


# ════════════════════════════════════════════════════════════════════════════
#  TC-0001 · Turn on Attenuator  [PASS expected]
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_attenuator_tc_0001(main_page, device):
    """
    @test_id: test_attenuator_tc_0001
    @brief: Turn on Attenuator
    @details: Verify that the Attenuator can be powered on from PC17 UI
              and hardware status is correct

    @pre:- PC17 application is running
         - Attenuator is connected

    @test_procedure:
        [code]
            - Turn on the Attenuator from PC17 UI
            - Observe LED indicator or measure supply voltage
            - Check status displayed on UI
        [!code]

    @pass_criteria:- Attenuator LED is ON or correct voltage is present
                   - UI shows Attenuator is ON and ready

    @test_level: system
    @test_type: functional
    @execution_type: semi_automatic
    @hw_depend: yes
    """
    # ── Step 1: Bật Attenuator từ UI ─────────────────────────────────────────
    main_page.turn_on_attenuator()

    # ── Step 2: Đọc voltage từ hardware qua serial ───────────────────────────
    voltage = device.read_voltage("VOLT?\r\n")
    assert voltage > 0, f"Expected voltage > 0V, got {voltage}V"

    # ── Step 3: Kiểm tra UI status ────────────────────────────────────────────
    assert main_page.is_attenuator_on(), (
        f"UI chưa update. Hiện tại: {main_page.get_attenuator_status()!r}"
    )


# ════════════════════════════════════════════════════════════════════════════
#  TC-0002 · Turn off Attenuator  [PASS expected]
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_attenuator_tc_0002(main_page, device):
    """
    @test_id: test_attenuator_tc_0002
    @brief: Turn off Attenuator
    @details: Verify that the Attenuator can be powered off from PC17 UI
              and hardware is de-energised

    @pre:- PC17 application is running
         - Attenuator is ON (TC-0001 passed)

    @test_procedure:
        [code]
            - Turn off the Attenuator from PC17 UI
            - Measure supply voltage — should read 0V
            - Confirm UI status changed to OFF
        [!code]

    @pass_criteria:- Attenuator voltage reads ~0V
                   - UI shows Attenuator is OFF

    @test_level: system
    @test_type: functional
    @execution_type: semi_automatic
    @hw_depend: yes
    """
    # ── Step 1: Tắt Attenuator từ UI ─────────────────────────────────────────
    main_page.turn_off_attenuator()

    # ── Step 2: Verify voltage về 0 ──────────────────────────────────────────
    voltage = device.read_voltage("VOLT?\r\n")
    assert voltage < 0.5, f"Expected ~0V after OFF, got {voltage}V"

    # ── Step 3: Verify UI status ──────────────────────────────────────────────
    status = main_page.get_attenuator_status().upper()
    assert status == "OFF", f"UI should show OFF, got: {status!r}"


# ════════════════════════════════════════════════════════════════════════════
#  TC-0003 · Connection status  [PASS expected]
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_attenuator_tc_0003(main_page, device):
    """
    @test_id: test_attenuator_tc_0003
    @brief: Verify device connection status on UI
    @details: After clicking Connect, UI must show Connected status
              and device must respond to ping

    @pre:- PC17 application is running
         - Device plugged in via USB

    @test_procedure:
        [code]
            - Click Connect button on UI
            - Check UI connection label
            - Ping device via serial
        [!code]

    @pass_criteria:- UI shows "Connected"
                   - Device responds OK to ping

    @test_level: system
    @test_type: functional
    @execution_type: automatic
    @hw_depend: yes
    """
    main_page.click_connect()

    assert main_page.is_connected(), (
        f"Connection status wrong: {main_page.get_connection_status()!r}"
    )
    assert device.is_connected(), "Device did not respond to ping"


# ════════════════════════════════════════════════════════════════════════════
#  TC-0004 · Intentional FAIL demo  [FAIL expected — để thấy report đỏ]
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_attenuator_tc_0004_intentional_fail(main_page, device):
    """
    @test_id: test_attenuator_tc_0004
    @brief: Intentional FAIL — demo report màu đỏ
    @details: TC này được tạo để demo report khi test FAIL.
              Không phải bug của framework.

    @pre:- Không có

    @test_procedure:
        [code]
            - Đọc voltage khi Attenuator OFF
            - Assert sai để demo FAIL
        [!code]

    @pass_criteria:- TC này sẽ luôn FAIL (intentional)

    @test_level: system
    @test_type: functional
    @execution_type: automatic
    @hw_depend: no
    """
    voltage = device.read_voltage()
    # Attenuator hiện OFF → voltage = 0, nhưng assert > 5 để demo fail
    assert voltage > 5.0, (
        f"[DEMO FAIL] Voltage {voltage}V không đạt ngưỡng 5V. "
        "TC này cố ý fail để demo màu đỏ trên report."
    )


# ════════════════════════════════════════════════════════════════════════════
#  TC-0005 · Skip demo  [SKIP expected]
# ════════════════════════════════════════════════════════════════════════════

@testcase
@pytest.mark.skip(reason="Hardware relay chưa gắn — sẽ chạy sau")
def test_attenuator_tc_0005_power_cycle(main_page, device):
    """
    @test_id: test_attenuator_tc_0005
    @brief: Power cycle Attenuator via relay
    @details: Dùng relay để cắt nguồn, chờ 3s, bật lại. Verify recovery.

    @pre:- Relay board kết nối COM10
         - relay.enabled: true trong settings.yaml

    @test_procedure:
        [code]
            - Relay OFF CH1 → Attenuator mất điện
            - Chờ 3 giây
            - Relay ON CH1 → Attenuator có điện lại
            - Verify UI recovery
        [!code]

    @pass_criteria:- Attenuator tự recover sau power cycle
                   - UI hiển thị trạng thái đúng

    @test_level: system
    @test_type: regression
    @execution_type: automatic
    @hw_depend: yes
    """
    pass  # sẽ implement khi có relay
