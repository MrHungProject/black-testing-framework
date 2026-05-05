"""SignalPanel — tương tác với Signal Generator panel trong FormMainEliteRF."""
from __future__ import annotations

import time

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SignalPanel(BasePage):
    """
    Signal Generator controls.

    Luồng tương tác:
        ensure_signal_panel_open() → open_rf1_output() → set_rf1_params()
                                   → open_trigger_output() → set_trigger_params()
    """

    # ── Panel open ────────────────────────────────────────────────────────────

    def ensure_signal_panel_open(self) -> None:
        """
        @brief  Đảm bảo Signal Generator panel đang mở (click "SIGNAL GEN" nếu chưa mở)
        @retval None
        """
        if self._ctrl._main_window is None:
            return
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip() in ("RF1 output", "Trigger Output"):
                    return  # panel đã mở
            except Exception:
                pass
        logger.info("SignalPanel: mở Signal Gen card …")
        if not self._ctrl.click_by_text("SIGNAL GEN", retries=5):
            raise RuntimeError("SignalPanel: Không click được 'SIGNAL GEN'")
        self._ctrl.wait_for_text("RF1 output", timeout=5)

    # ── RF1 Output tab ────────────────────────────────────────────────────────

    def open_rf1_output(self) -> None:
        """
        @brief  Click tab "RF1 output" trong Signal Generator panel
        @retval None
        """
        logger.info("SignalPanel: mở tab RF1 output")
        self.ensure_signal_panel_open()
        if not self._ctrl.click_by_text("RF1 output", retries=5):
            raise RuntimeError("SignalPanel: Không click được 'RF1 output'")
        self._ctrl.wait_for_text("Set RF 1 OUT", timeout=5)

    def set_rf1_params(
        self,
        rf1_out: str = "0",
        power_level: str = "0",
    ) -> list:
        """
        @brief  Điền thông số RF1 output (RF OUT và Power Level) rồi click Apply
        @param  rf1_out: Giá trị Set RF 1 OUT (default: "0")
        @param  power_level: Giá trị Set Power Level (default: "0")
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(f"SignalPanel RF1: rf1_out={rf1_out}, power_level={power_level}")
        self._ctrl.build_cache()
        try:
            self._ctrl.set_field_by_label("Set RF 1 OUT", rf1_out)
            self._ctrl.set_field_by_label("Set Power Level", power_level)
        finally:
            self._ctrl.invalidate_cache()
        self._click_apply()
        time.sleep(0.2)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"SignalPanel RF1: validation errors — {errs}")
        else:
            logger.info("SignalPanel RF1: Apply OK")
        return errs

    # ── Trigger Output tab ────────────────────────────────────────────────────

    def open_trigger_output(self) -> None:
        """
        @brief  Click tab "Trigger Output" trong Signal Generator panel
        @retval None
        """
        logger.info("SignalPanel: mở tab Trigger Output")
        self.ensure_signal_panel_open()
        if not self._ctrl.click_by_text("Trigger Output", retries=5):
            raise RuntimeError("SignalPanel: Không click được 'Trigger Output'")
        self._ctrl.wait_for_text("Dwell Time", timeout=5)

    def set_trigger_params(
        self,
        start_freq: str = "",
        stop_freq: str = "",
        step: str = "",
        dwell_time: str = "",
        cycles: str = "",
    ) -> list:
        """
        @brief  Điền thông số Trigger Output (sweep params) rồi click Apply
        @param  start_freq: Start Frequency
        @param  stop_freq: Stop Frequency
        @param  step: Bước nhảy tần số (Step)
        @param  dwell_time: Thời gian dừng mỗi điểm tần (Dwell Time)
        @param  cycles: Số chu kỳ lặp (Cycles)
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"SignalPanel Trigger: start={start_freq}, stop={stop_freq}, "
            f"step={step}, dwell={dwell_time}, cycles={cycles}"
        )
        if start_freq:
            self._ctrl.set_field_by_label("Start Frequency", start_freq)
        if stop_freq:
            self._ctrl.set_field_by_label("Stop Frequency", stop_freq)
        if step:
            self._ctrl.set_field_by_label("Step", step)
        if dwell_time:
            self._ctrl.set_field_by_label("Dwell Time", dwell_time)
        if cycles:
            self._ctrl.set_field_by_label("Cycles", cycles)
        self._click_apply()
        time.sleep(0.5)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"SignalPanel Trigger: validation errors — {errs}")
        else:
            logger.info("SignalPanel Trigger: Apply OK")
        return errs

    # ── Apply ─────────────────────────────────────────────────────────────────

    def _click_apply(self) -> None:
        """
        @brief  Click nút Apply trong Signal Generator panel
        @retval None
        """
        if not self._ctrl.click_by_text("Apply"):
            raise RuntimeError("SignalPanel: Không click được 'Apply'")

    # ── Temperature ───────────────────────────────────────────────────────────

    def get_temperature(self) -> str:
        """
        @brief  Lấy giá trị nhiệt độ hiển thị của Signal Generator
        @retval str — giá trị nhiệt độ; chuỗi rỗng nếu không tìm thấy
        """
        return self._ctrl.get_text_after_label("Temperature")
