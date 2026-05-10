"""PowerPanel — tương tác với Power Meter panel trong FormMainEliteRF."""
from __future__ import annotations

import time

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class PowerPanel(BasePage):
    """
    Power Meter controls.

    Nav tree:
        Power → Sensor Setting
              → Chart Setting
              → Control Measurement
    """

    # ── Panel open ────────────────────────────────────────────────────────────

    def ensure_power_panel_open(self) -> None:
        """
        @brief  Đảm bảo Power panel đang mở (click "Power" nếu chưa mở).
                Nếu click vô tình đóng panel (toggle), tự click lại để mở.
        @retval None
        """
        if self._ctrl._main_window is None:
            return
        if self._is_power_nav_expanded():
            return
        logger.info("PowerPanel: mở Power card …")
        if not self._ctrl.click_by_text("Power", retries=5):
            raise RuntimeError("PowerPanel: Không click được 'Power'")
        if not self._ctrl.wait_for_text("Sensor Setting", timeout=5):
            logger.warning("PowerPanel: click đã đóng panel, click lại …")
            self._ctrl.click_by_text("Power", retries=5)
            self._ctrl.wait_for_text("Sensor Setting", timeout=5)

    # ── Sensor Setting ────────────────────────────────────────────────────────

    def open_sensor_setting(self) -> None:
        """
        @brief  Click mục "Sensor Setting" trong Power panel
        @retval None
        """
        logger.info("PowerPanel: mở Sensor Setting")
        self.ensure_power_panel_open()
        if not self._ctrl.click_by_text("Sensor Setting", retries=5):
            raise RuntimeError("PowerPanel: Không click được 'Sensor Setting'")
        self._ctrl.wait_for_text("Averages", timeout=5)

    def set_sensor_setting_params(
        self,
        averages: str = "",
        correction_db: str = "",
        disp_res: str = "",
        duty_cycle_pct: str = "",
        frequency_hz: str = "",
        frequency_unit: str = "",
        interval_ms: str = "",
        pulse_top_power: str = "",
        pulse_width: str = "",
        signal_peak_noise: str = "",
        signal_power: str = "",
        trace_delay: str = "",
        trace_size: str = "",
        trace_time: str = "",
        units: str = "",
    ) -> list:
        """
        @brief  Điền các thông số Sensor Setting rồi click Apply
        @param  averages:          Số lần trung bình (1–2000)
        @param  correction_db:     Giá trị Correction (dB)
        @param  disp_res:          Display Resolution dropdown (ví dụ: "Digits_2")
        @param  duty_cycle_pct:    Duty Cycle %
        @param  frequency_hz:      Tần số Frequency — phần số (ví dụ: "100", "1")
        @param  frequency_unit:    Đơn vị tần số dropdown (ví dụ: "G(Hz)", "M(Hz)", "k(Hz)")
        @param  interval_ms:       Interval (ms)
        @param  pulse_top_power:   Pulse top power (dBm)
        @param  pulse_width:       Pulse width (sec)
        @param  signal_peak_noise: Signal peak-to-peak noise (dB)
        @param  signal_power:      Signal Power (dBm)
        @param  trace_delay:       Trace delay (seconds)
        @param  trace_size:        Trace size (points)
        @param  trace_time:        Trace time (seconds)
        @param  units:             Units dropdown ("W" hoặc "dBm")
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"PowerPanel SensorSetting: averages={averages}, correction={correction_db}, "
            f"freq={frequency_hz}{frequency_unit}, units={units}"
        )
        self._ctrl.build_cache()
        try:
            if averages:
                self._ctrl.set_field_by_label("Averages", averages)
            if correction_db:
                self._ctrl.set_field_by_label("Correction (dB)", correction_db)
            if duty_cycle_pct:
                self._ctrl.set_field_by_label("Duty Cycle %", duty_cycle_pct)
            if frequency_hz:
                self._ctrl.set_field_by_label("Frequency (Hz)", frequency_hz)
            if interval_ms:
                self._ctrl.set_field_by_label("Interval (ms)", interval_ms)
            if pulse_top_power:
                self._ctrl.set_field_by_label("Pulse top power (dBm)", pulse_top_power)
            if pulse_width:
                self._ctrl.set_field_by_label("Pulse width (sec)", pulse_width)
            if signal_peak_noise:
                self._ctrl.set_field_by_label("Signal peak-to-peak noise (dB)", signal_peak_noise)
            if signal_power:
                self._ctrl.set_field_by_label("Signal Power (dBm)", signal_power)
            if trace_delay:
                self._ctrl.set_field_by_label("Trace delay (seconds)", trace_delay)
            if trace_size:
                self._ctrl.set_field_by_label("Trace size (points)", trace_size)
            if trace_time:
                self._ctrl.set_field_by_label("Trace time (seconds)", trace_time)
        finally:
            self._ctrl.invalidate_cache()

        if disp_res:
            self._select_dropdown("Disp Res", disp_res)
        if frequency_unit:
            self._select_dropdown("Frequency (Hz)", frequency_unit)
        if units:
            self._select_dropdown("Units", units)

        self._click_apply()
        time.sleep(0.2)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"PowerPanel SensorSetting: validation errors — {errs}")
        else:
            logger.info("PowerPanel SensorSetting: Apply OK")
        return errs

    def toggle_correction(self) -> None:
        """
        @brief  Click toggle On/Off của Correction (dB)
        @retval None
        """
        logger.info("PowerPanel: toggle Correction On/Off")
        if not self._ctrl.click_by_text("Correction (dB)", retries=5):
            raise RuntimeError("PowerPanel: Không tìm thấy toggle Correction")

    def toggle_duty_cycle(self) -> None:
        """
        @brief  Click toggle On/Off của Duty Cycle
        @retval None
        """
        logger.info("PowerPanel: toggle Duty Cycle On/Off")
        if not self._ctrl.click_by_text("Duty Cycle On/Off", retries=5):
            logger.warning("PowerPanel: toggle Duty Cycle On/Off — không tìm thấy text")

    def set_frequency(self, value: str, unit: str = "") -> None:
        """
        @brief  Set Frequency (Hz) và tùy chọn chọn đơn vị từ dropdown
        @param  value: Giá trị số (ví dụ: "100", "1")
        @param  unit:  Đơn vị dropdown (ví dụ: "G(Hz)", "M(Hz)", "k(Hz)", "(Hz)")
        @retval None
        """
        logger.info(f"PowerPanel: set Frequency = {value} {unit}")
        self._ctrl.set_field_by_label("Frequency (Hz)", value)
        if unit:
            self._select_dropdown("Frequency (Hz)", unit)

    def set_averages(self, value: str) -> None:
        """
        @brief  Set field Averages rồi click Apply
        @param  value: Số lần trung bình (ví dụ: "1", "100", "2000")
        @retval None
        """
        logger.info(f"PowerPanel: set Averages = {value}")
        self._ctrl.set_field_by_label("Averages", value)
        self._click_apply()
        time.sleep(0.2)

    def set_units(self, unit: str) -> None:
        """
        @brief  Chọn đơn vị hiển thị từ dropdown rồi click Apply
        @param  unit: "W" hoặc "dBm"
        @retval None
        """
        logger.info(f"PowerPanel: set Units = {unit}")
        self._select_dropdown("Units", unit)
        self._click_apply()
        time.sleep(0.2)

    def read_signal_power(self) -> str:
        """
        @brief  Đọc giá trị Signal Power hiển thị trên Power Meter
        @retval str — giá trị công suất đọc được; chuỗi rỗng nếu không tìm thấy
        """
        return self._ctrl.get_text_after_label("Signal Power (dBm)")

    # ── Chart Setting ─────────────────────────────────────────────────────────

    def open_chart_setting(self) -> None:
        """
        @brief  Click mục "Chart Setting" trong Power panel
        @retval None
        """
        logger.info("PowerPanel: mở Chart Setting")
        self.ensure_power_panel_open()
        if not self._ctrl.click_by_text("Chart Setting", retries=5):
            raise RuntimeError("PowerPanel: Không click được 'Chart Setting'")
        self._ctrl.wait_for_text("Time Span", timeout=5)

    def set_chart_setting_params(
        self,
        time_span: str = "",
        max_dbm: str = "",
        dbm_per_div: str = "",
    ) -> list:
        """
        @brief  Điền các thông số Chart Setting
        @param  time_span:   Time Span dropdown
                             ("1 sec","3 sec","10 sec","30 sec","1 min","3 min",
                              "10 min","30 min","1 hr","3 hr","10 hr")
        @param  max_dbm:     Max dBm text field (ví dụ: "40.000")
        @param  dbm_per_div: dBm/Div dropdown
                             ("0.2","0.5","1.0","2.0","5.0","10.0","15.0")
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"PowerPanel ChartSetting: time_span={time_span}, "
            f"max_dbm={max_dbm}, dbm_per_div={dbm_per_div}"
        )
        if max_dbm:
            self._ctrl.set_field_by_label("Max dBm", max_dbm)
        if time_span:
            self._select_dropdown("Time Span", time_span)
        if dbm_per_div:
            self._select_dropdown("dBm/Div", dbm_per_div)
        time.sleep(0.2)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"PowerPanel ChartSetting: validation errors — {errs}")
        else:
            logger.info("PowerPanel ChartSetting: params set OK")
        return errs

    # ── Control Measurement ───────────────────────────────────────────────────

    def open_control_measurement(self) -> None:
        """
        @brief  Click mục "Control Measurement" trong Power panel
        @retval None
        """
        logger.info("PowerPanel: mở Control Measurement")
        self.ensure_power_panel_open()
        if not self._ctrl.click_by_text("Control Measurement", retries=5):
            raise RuntimeError("PowerPanel: Không click được 'Control Measurement'")
        self._ctrl.wait_for_text("Start", timeout=5)

    def click_start_measurement(self) -> None:
        """
        @brief  Click nút Start để bắt đầu đo công suất
        @retval None
        """
        logger.info("PowerPanel: Start measurement")
        if not self._ctrl.click_by_text("Start", retries=5):
            raise RuntimeError("PowerPanel: Không click được 'Start'")

    def click_stop_measurement(self) -> None:
        """
        @brief  Click nút Stop để dừng đo công suất
        @retval None
        """
        logger.info("PowerPanel: Stop measurement")
        if not self._ctrl.click_by_text("Stop", retries=5):
            raise RuntimeError("PowerPanel: Không click được 'Stop'")

    # ── Apply ─────────────────────────────────────────────────────────────────

    def _click_apply(self) -> None:
        """
        @brief  Click nút Apply trong Power panel
        @retval None
        """
        if not self._ctrl.click_by_text("Apply"):
            raise RuntimeError("PowerPanel: Không click được 'Apply'")

    # ── Private helpers ───────────────────────────────────────────────────────

    def _select_dropdown(self, label: str, value: str) -> None:
        """
        @brief  Tìm ComboBox kế label → click để mở list → chọn item.
                Primary: select_by_label() (cùng cơ chế Gain/Atten trong SpectrumPanel).
                Fallback: click_by_text(label) + click_in_any_window(value) cho custom dropdown.
        @param  label: Text label đứng trên combobox (ví dụ: "Time Span", "dBm/Div")
        @param  value: Item cần chọn trong list (ví dụ: "1 min", "15.0")
        @retval None
        """
        logger.info(f"PowerPanel: dropdown '{label}' → chọn '{value}'")
        if self._ctrl.select_by_label(label, value):
            return
        logger.warning(f"PowerPanel: select_by_label thất bại cho '{label}', thử fallback …")
        if not self._ctrl.click_by_text(label, retries=3):
            raise RuntimeError(f"PowerPanel: Không mở được dropdown '{label}'")
        time.sleep(0.3)
        if not self._ctrl.click_in_any_window(value):
            raise RuntimeError(f"PowerPanel: Không chọn được '{value}' trong dropdown '{label}'")

    def _is_power_nav_expanded(self) -> bool:
        """
        @brief  Kiểm tra Power nav item đang expanded (sub-items hiển thị trong cây)
        @retval bool — True nếu panel đang mở, False nếu đang đóng
        """
        if self._ctrl._main_window is None:
            return False
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip() in ("Sensor Setting", "Chart Setting", "Control Measurement"):
                    return True
            except Exception:
                pass
        return False
