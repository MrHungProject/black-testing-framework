"""
Attenuator test suite — Power ON / OFF
"""
import pytest
from core import testcase
from pages.main_page import MainPage
from core.serial_device import SerialDevice


# ════════════════════════════════════════════════════════════════════════════
#  TC-0001 · Turn on Attenuator
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_attenuator_tc_0001(main_page: MainPage, device: SerialDevice):
    """
    @test_id: test_attenuator_tc_0001
    @brief: Turn on Attenuator
    @details: Verify that the Attenuator can be powered on from PC17 UI
              and hardware status is correct

    @pre:- PC17 application is running
         - Attenuator is connected via USB

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
    @execution_type: semi-automatic
    @hw_depend: yes
    """
    # ── Step 1: Turn on Attenuator from UI ───────────────────────────────────
    main_page.turn_on_attenuator()

    # ── Step 2: Verify hardware — measure voltage via serial ─────────────────
    voltage = device.read_voltage("VOLT?\r\n")
    assert voltage > 0, f"Expected voltage > 0V, got {voltage}V"

    # ── Step 3: Verify UI status ──────────────────────────────────────────────
    assert main_page.is_attenuator_on(), (
        f"UI status not updated. Got: {main_page.get_attenuator_status()!r}"
    )


# ════════════════════════════════════════════════════════════════════════════
#  TC-0002 · Turn off Attenuator
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_attenuator_tc_0002(main_page: MainPage, device: SerialDevice):
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
            - Measure supply voltage — should read 0 V
            - Confirm UI status changed to OFF
        [!code]

    @pass_criteria:- Attenuator voltage reads 0 V (or near zero)
                   - UI shows Attenuator is OFF

    @test_level: system
    @test_type: functional
    @execution_type: semi-automatic
    @hw_depend: yes
    """
    # ── Step 1: Turn off Attenuator from UI ──────────────────────────────────
    main_page.turn_off_attenuator()

    # ── Step 2: Verify hardware voltage dropped ───────────────────────────────
    voltage = device.read_voltage("VOLT?\r\n")
    assert voltage < 0.5, f"Expected ~0V after OFF, got {voltage}V"

    # ── Step 3: Verify UI status ──────────────────────────────────────────────
    status = main_page.get_attenuator_status().lower()
    assert "off" in status or "inactive" in status, (
        f"UI should show OFF, got: {status!r}"
    )
