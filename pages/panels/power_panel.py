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

    _POWER_FORM = "FormDetailPowerConfig"

    # auto_id của từng Pane input trong Sensor Setting
    _FIELD_IDS: dict[str, str] = {
        "averages":          "txtPowerAverages",
        "correction_db":     "txtPowerCorrection",
        "duty_cycle_pct":    "txtPowerDutyCycle",
        "frequency_hz":      "txtPowerFrequency",
        "interval_ms":       "txtPowerInterval",
        "pulse_top_power":   "txtPowerPulseTop",
        "pulse_width":       "txtPowerPulseWidth",
        "signal_peak_noise": "txtPowerSignalPeak",
        "signal_power":      "txtPowerSignalPower",
        "trace_delay":       "txtPowerTraceDelay",
        "trace_size":        "txtPowerTraceSize",
        "trace_time":        "txtPowerTraceTime",
    }

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
        fields = {
            "averages":          averages,
            "correction_db":     correction_db,
            "duty_cycle_pct":    duty_cycle_pct,
            "frequency_hz":      frequency_hz,
            "interval_ms":       interval_ms,
            "pulse_top_power":   pulse_top_power,
            "pulse_width":       pulse_width,
            "signal_peak_noise": signal_peak_noise,
            "signal_power":      signal_power,
            "trace_delay":       trace_delay,
            "trace_size":        trace_size,
            "trace_time":        trace_time,
        }
        for key, value in fields.items():
            if value:
                self._set_field(self._FIELD_IDS[key], value)

        if disp_res:
            self._select_dropdown("Disp Res", disp_res)
        if frequency_unit:
            self._select_dropdown("Frequency (Hz)", frequency_unit)
        if units:
            self._select_dropdown("Unit (W or dBm)", units)

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
        @brief  Click toggle On/Off của Correction (dB) — auto_id: rdoCorrection
        @retval None
        """
        logger.info("PowerPanel: toggle Correction On/Off")
        form = self._ctrl._main_window.child_window(auto_id=self._POWER_FORM)
        form.child_window(auto_id="rdoCorrection").click_input()

    def toggle_duty_cycle(self) -> None:
        """
        @brief  Click toggle On/Off của Duty Cycle — auto_id: radioCustom1
        @retval None
        """
        logger.info("PowerPanel: toggle Duty Cycle On/Off")
        form = self._ctrl._main_window.child_window(auto_id=self._POWER_FORM)
        form.child_window(auto_id="radioCustom1").click_input()

    def set_frequency(self, value: str, unit: str = "") -> None:
        """
        @brief  Set Frequency (Hz) và tùy chọn chọn đơn vị từ dropdown
        @param  value: Giá trị số (ví dụ: "100", "1")
        @param  unit:  Đơn vị dropdown (ví dụ: "G(Hz)", "M(Hz)", "k(Hz)", "(Hz)")
        @retval None
        """
        logger.info(f"PowerPanel: set Frequency = {value} {unit}")
        self._set_field("txtPowerFrequency", value)
        if unit:
            self._select_dropdown("Frequency (Hz)", unit)

    def set_averages(self, value: str) -> None:
        """
        @brief  Set field Averages rồi click Apply
        @param  value: Số lần trung bình (ví dụ: "1", "100", "2000")
        @retval None
        """
        logger.info(f"PowerPanel: set Averages = {value}")
        self._set_field("txtPowerAverages", value)
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

    def _set_field(self, auto_id: str, value: str) -> None:
        """
        @brief  Nhập giá trị vào Pane input field qua auto_id.
                Tự scroll element vào vùng nhìn thấy trước khi click.
        @param  auto_id: auto_id của Pane (ví dụ: "txtPowerAverages")
        @param  value:   Giá trị cần nhập
        @retval None
        """
        form = self._ctrl._main_window.child_window(auto_id=self._POWER_FORM)
        pane = form.child_window(auto_id=auto_id)
        try:
            pane.scroll_into_view()
        except Exception:
            pass
        try:
            tb = pane.child_window(auto_id="textBox1")
        except Exception:
            tb = pane
        tb.click_input()
        tb.type_keys("^a", with_spaces=True)
        tb.set_edit_text(value)
        tb.type_keys("{ENTER}", with_spaces=True)
        logger.debug(f"PowerPanel._set_field: {auto_id} = {value!r}")

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
