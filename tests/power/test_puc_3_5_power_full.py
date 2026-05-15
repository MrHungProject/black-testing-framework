"""
Power Panel — Sensor Setting full end-to-end test — PUC_3.5
"""

import time

from core import testcase
from pages.main_page import MainPage


class TestPowerPuc35SensorSettingFull:
    """PUC_3.5 — Sensor Setting full end-to-end trong 1 test case."""

    @testcase
    def test_power_puc_3_5_sensor_0001(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_5_sensor_0001
        @brief: Thao tác toàn bộ Sensor Setting — tất cả các field và toggle

        @details: 1 test case duy nhất đi qua toàn bộ chức năng Sensor Setting:
                  (1) Mở Sensor Setting, verify Averages hiển thị
                  (2) Set Averages, Correction, Frequency
                  (3) Set Interval, Pulse top power, Pulse width
                  (4) Set Signal peak-to-peak noise, Signal Power
                  (5) Set Trace delay, Trace size, Trace time
                  (6) Chọn Unit: dBm → W
                  (7) Averages: 1 → 100 → 2000
                  (8) Toggle Correction On/Off x2
                  (9) Toggle Duty Cycle On/Off x2
                  (10) Set nhiều trường cùng lúc → Apply

        @pre:- PC17 đã Connected
             - Power panel chưa mở

        @test_procedure:
            [code]
                Bước 1: Mở Sensor Setting, verify Averages hiển thị
                Bước 2: set_sensor_setting_params(averages, correction_db, frequency_hz)
                Bước 3: set_sensor_setting_params(interval_ms, pulse_top_power, pulse_width)
                Bước 4: set_sensor_setting_params(signal_peak_noise, signal_power)
                Bước 5: set_sensor_setting_params(trace_delay, trace_size, trace_time)
                Bước 6: set_sensor_setting_params(units="dBm") → units="W"
                Bước 7: set_power_averages("1") → "100" → "2000"
                Bước 8: toggle_power_correction() x2
                Bước 9: toggle_power_duty_cycle() x2
                Bước 10: set_sensor_setting_params(nhiều trường) → Apply
            [!code]

        @pass_criteria:- Không có validation error ở bất kỳ bước nào
                       - Không có exception trong suốt quá trình

        @test_level: software
        @test_type: fat
        @execution_type: automatic
        @hw_depend: yes
        """
        errors = []

        # ── Bước 1: Mở Sensor Setting ─────────────────────────────────────────
        main_page.open_sensor_setting()
        assert main_page.has_text("Averages"), "Bước 1: 'Averages' không xuất hiện"

        # ── Bước 2: Averages, Correction, Frequency ───────────────────────────
        errs = main_page.set_sensor_setting_params(
            averages="10",
            correction_db="0.5",
            frequency_hz="1000000000",
        )
        if errs:
            errors.append(f"Bước 2: {errs}")

        # ── Bước 3: Interval, Pulse top power, Pulse width ────────────────────
        errs = main_page.set_sensor_setting_params(
            interval_ms="100",
            pulse_top_power="10.0",
            pulse_width="0.001",
        )
        if errs:
            errors.append(f"Bước 3: {errs}")

        # ── Bước 4: Signal peak-to-peak noise, Signal Power ───────────────────
        errs = main_page.set_sensor_setting_params(
            signal_peak_noise="0.5",
            signal_power="0.0",
        )
        if errs:
            errors.append(f"Bước 4: {errs}")

        # ── Bước 5: Trace delay, Trace size, Trace time ───────────────────────
        errs = main_page.set_sensor_setting_params(
            trace_delay="0.0",
            trace_size="1000",
            trace_time="1.0",
        )
        if errs:
            errors.append(f"Bước 5: {errs}")

        # ── Bước 6: Unit dropdown dBm → W ─────────────────────────────────────
        for unit in ("dBm", "W"):
            errs = main_page.set_sensor_setting_params(units=unit)
            if errs:
                errors.append(f"Bước 6 (units={unit}): {errs}")

        # ── Bước 7: Averages 1 → 100 → 2000 ──────────────────────────────────
        for avg in ("1", "100", "2000"):
            try:
                main_page.set_power_averages(avg)
            except Exception as e:
                errors.append(f"Bước 7 (averages={avg}): {e}")

        # ── Bước 8: Toggle Correction x2 ──────────────────────────────────────
        for step in range(1, 3):
            try:
                main_page.toggle_power_correction()
                time.sleep(0.2)
            except Exception as e:
                errors.append(f"Bước 8 toggle Correction lần {step}: {e}")

        # ── Bước 9: Toggle Duty Cycle x2 ──────────────────────────────────────
        for step in range(1, 3):
            try:
                main_page.toggle_power_duty_cycle()
                time.sleep(0.2)
            except Exception as e:
                errors.append(f"Bước 9 toggle DutyCycle lần {step}: {e}")

        # ── Bước 10: Cấu hình nhiều trường cùng lúc → Apply ──────────────────
        errs = main_page.set_sensor_setting_params(
            averages="50",
            correction_db="1.0",
            frequency_hz="5000000000",
            interval_ms="200",
            pulse_top_power="5.0",
            pulse_width="0.0005",
            signal_peak_noise="1.0",
            signal_power="10.0",
            trace_delay="0.1",
            trace_size="500",
            trace_time="0.5",
            units="dBm",
        )
        if errs:
            errors.append(f"Bước 10 (full config): {errs}")

        assert not errors, "Sensor Setting full test FAILED:\n" + "\n".join(errors)
