"""OscilloscopePanel — tương tác với Oscilloscope panel trong FormMainEliteRF."""
from __future__ import annotations

import time

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class OscilloscopePanel(BasePage):
    """
    Oscilloscope controls.

    Nav tree:
        Oscilloscope → DSO Setting
                     → DDS Setting
    """

    # ── Panel open ────────────────────────────────────────────────────────────

    def ensure_oscilloscope_panel_open(self) -> None:
        """
        @brief  Đảm bảo Oscilloscope panel đang mở (click nav item bên phải nếu chưa mở).
                Dùng rightmost strategy để tránh click nhầm tiêu đề form bên trái.
        @retval None
        """
        if self._ctrl._main_window is None:
            return
        if self._is_oscilloscope_nav_expanded():
            return
        logger.info("OscilloscopePanel: mở Oscilloscope card …")
        self._click_oscilloscope_nav()
        if not self._ctrl.wait_for_text("DSO Setting", timeout=5):
            logger.warning("OscilloscopePanel: click đã đóng panel, click lại …")
            self._click_oscilloscope_nav()
            self._ctrl.wait_for_text("DSO Setting", timeout=5)

    def _click_oscilloscope_nav(self) -> None:
        """Click nav item 'Oscilloscope' bên phải nhất (tránh hit tiêu đề form cùng tên bên trái)."""
        best = None
        best_left = -1
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip().lower() != "oscilloscope":
                    continue
                rect = ctrl.element_info.rectangle
                if rect.left > best_left:
                    best_left = rect.left
                    best = ctrl
            except Exception:
                pass
        if best is None:
            raise RuntimeError("OscilloscopePanel: Không tìm thấy nav item 'Oscilloscope'")
        best.click_input()
        logger.info("OscilloscopePanel: click nav Oscilloscope (rightmost)")

    # ── DSO Setting ───────────────────────────────────────────────────────────

    def open_dso_setting(self) -> None:
        """
        @brief  Click mục "DSO Setting" trong Oscilloscope panel.
                Bỏ qua nếu form đã mở để tránh toggle đóng panel.
        @retval None
        """
        if self.is_dso_setting_open():
            logger.info("OscilloscopePanel: DSO Setting đã mở, bỏ qua")
            return
        logger.info("OscilloscopePanel: mở DSO Setting")
        self.ensure_oscilloscope_panel_open()
        try:
            self._ctrl._main_window.child_window(title="DSO Setting").click_input()
        except Exception:
            if not self._ctrl.click_by_text("DSO Setting", retries=5):
                raise RuntimeError("OscilloscopePanel: Không click được 'DSO Setting'")
        # Đợi form xuất hiện bằng auto_id thay vì quét descendants
        deadline = time.time() + 5
        while time.time() < deadline:
            if self.is_dso_setting_open():
                return
            time.sleep(0.15)
        raise RuntimeError("OscilloscopePanel: DSO Setting không mở trong 5 giây")

    def set_dso_params(
        self,
        time_div: str = "",
        channel: str = "",
        channel_on: bool | None = None,
        probe: str = "",
        voltage_div: str = "",
        coupling: str = "",
        trigger_mode: str = "",
        trigger_sweep: str = "",
    ) -> list:
        """
        @brief  Cấu hình các thông số DSO Setting rồi click Apply
        @param  time_div:      Time/Div dropdown
                               ("200 ns","500 ns","1.0 us","2.0 us","5.00 us",
                                "10.0 us","20.0 us","50.0 us","100 us","200 us",
                                "500 us","1.0 ms","2.0 ms","5.0 ms","10.0 ms",
                                "20.0 ms","50.0 ms","100 ms","200 ms","500 ms","1.0 s")
        @param  channel:       Channel dropdown ("CH1","CH2","CH3","CH4")
        @param  channel_on:    True = bật kênh (ON/OFF checkbox), False = tắt, None = giữ nguyên
        @param  probe:         Probe dropdown ("X1","X10","X100","X1000")
        @param  voltage_div:   Voltage/Div dropdown
                               ("1.00mV","2.00mV","5.00mV","10.0mV","20.0mV","50.0mV",
                                "100mV","200mV","500mV","1.00V","2.00V","5.00V","10.0V")
        @param  coupling:      Coupling dropdown ("DC","AC","GND")
        @param  trigger_mode:  Trigger Mode dropdown ("Edge","Pulse","Slope","Video","Timeout")
        @param  trigger_sweep: Trigger Sweep dropdown ("Auto","Normal","Single")
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"OscilloscopePanel DSO: time_div={time_div}, channel={channel}, "
            f"probe={probe}, voltage_div={voltage_div}, coupling={coupling}, "
            f"trigger_mode={trigger_mode}, trigger_sweep={trigger_sweep}"
        )
        if channel:
            self._select_dropdown("Channel", channel)
        if channel_on is not None:
            self._set_channel_on_off(channel_on)
        if time_div:
            self._select_dropdown("Time/Div", time_div)
        if probe:
            self._select_dropdown("Probe", probe)
        if voltage_div:
            self._select_dropdown("Voltage/Div", voltage_div)
        if coupling:
            self._select_dropdown("Coupling", coupling)
        if trigger_mode:
            self._select_dropdown("Trigger Mode", trigger_mode)
        if trigger_sweep:
            self._select_dropdown("Trigger Sweep", trigger_sweep)

        self._click_apply()
        errs = self._check_form_validation_errors(self._DSO_FORM)
        if errs:
            logger.warning(f"OscilloscopePanel DSO: validation errors — {errs}")
        else:
            logger.info("OscilloscopePanel DSO: Apply OK")
        return errs

    def select_channel(self, channel: str) -> None:
        """
        @brief  Chọn kênh từ Channel dropdown (không Apply)
        @param  channel: "CH1" | "CH2" | "CH3" | "CH4"
        @retval None
        """
        logger.info(f"OscilloscopePanel: select channel = {channel}")
        self._select_dropdown("Channel", channel)

    def set_channel_enabled(self, enabled: bool) -> None:
        """
        @brief  Bật hoặc tắt kênh đang chọn qua checkbox ON/OFF
        @param  enabled: True = ON, False = OFF
        @retval None
        """
        self._set_channel_on_off(enabled)

    def set_time_div(self, value: str) -> None:
        """
        @brief  Chọn Time/Div từ dropdown rồi click Apply
        @param  value: Giá trị Time/Div (ví dụ: "5.00 us", "1.0 ms", "500 ms")
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Time/Div = {value}")
        self._select_dropdown("Time/Div", value)
        self._click_apply()

    def set_voltage_div(self, value: str) -> None:
        """
        @brief  Chọn Voltage/Div từ dropdown rồi click Apply
        @param  value: Giá trị Voltage/Div (ví dụ: "1.00V", "100mV", "10.0mV")
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Voltage/Div = {value}")
        self._select_dropdown("Voltage/Div", value)
        self._click_apply()

    def set_coupling(self, value: str) -> None:
        """
        @brief  Chọn Coupling từ dropdown rồi click Apply
        @param  value: "DC" | "AC" | "GND"
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Coupling = {value}")
        self._select_dropdown("Coupling", value)
        self._click_apply()

    def set_trigger_mode(self, mode: str) -> None:
        """
        @brief  Chọn Trigger Mode từ dropdown rồi click Apply
        @param  mode: "Edge" | "Pulse" | "Slope" | "Video" | "Timeout"
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Trigger Mode = {mode}")
        self._select_dropdown("Trigger Mode", mode)
        self._click_apply()

    def set_trigger_sweep(self, sweep: str) -> None:
        """
        @brief  Chọn Trigger Sweep từ dropdown rồi click Apply
        @param  sweep: "Auto" | "Normal" | "Single"
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Trigger Sweep = {sweep}")
        self._select_dropdown("Trigger Sweep", sweep)
        self._click_apply()

    def set_dso_params_no_apply(
        self,
        channel: str = "",
        coupling: str = "",
        probe: str = "",
        time_div: str = "",
        voltage_div: str = "",
        trigger_mode: str = "",
        trigger_sweep: str = "",
    ) -> None:
        """
        @brief  Thay đổi các dropdown DSO Setting mà KHÔNG click Apply.
                Dùng để test hành vi Cancel — verify giá trị không được lưu.
        @retval None
        """
        logger.info("OscilloscopePanel DSO: set params NO APPLY")
        if channel:       self._select_dropdown("Channel",       channel)
        if coupling:      self._select_dropdown("Coupling",      coupling)
        if probe:         self._select_dropdown("Probe",         probe)
        if time_div:      self._select_dropdown("Time/Div",      time_div)
        if voltage_div:   self._select_dropdown("Voltage/Div",   voltage_div)
        if trigger_mode:  self._select_dropdown("Trigger Mode",  trigger_mode)
        if trigger_sweep: self._select_dropdown("Trigger Sweep", trigger_sweep)

    def set_dds_params_no_apply(
        self,
        signal_type: str = "",
        frequency_hz: str = "",
        amplitude_v: str = "",
        offset_v: str = "",
    ) -> None:
        """
        @brief  Thay đổi các field DDS Setting mà KHÔNG click Apply.
                Dùng để test hành vi Cancel — verify giá trị không được lưu.
        @retval None
        """
        logger.info("OscilloscopePanel DDS: set params NO APPLY")
        if signal_type:  self._dds_select_signal_type(signal_type)
        if frequency_hz: self._dds_set_field("txtFreq",      frequency_hz)
        if amplitude_v:  self._dds_set_field("txtAmplitude", amplitude_v)
        if offset_v:     self._dds_set_field("txtOffset",    offset_v)

    def click_cancel(self) -> None:
        """
        @brief  Click nút Cancel để huỷ thay đổi trong DSO Setting
        @retval None
        """
        logger.info("OscilloscopePanel: Cancel")
        if not self._ctrl.click_by_text("Cancel", retries=5):
            raise RuntimeError("OscilloscopePanel: Không click được 'Cancel'")

    # ── DDS Setting ───────────────────────────────────────────────────────────

    def open_dds_setting(self) -> None:
        """
        @brief  Click mục "DDS Setting" trong Oscilloscope panel.
                Bỏ qua nếu form đã mở để tránh toggle đóng panel.
        @retval None
        """
        if self.is_dds_setting_open():
            logger.info("OscilloscopePanel: DDS Setting đã mở, bỏ qua")
            return
        logger.info("OscilloscopePanel: mở DDS Setting")
        self.ensure_oscilloscope_panel_open()
        try:
            self._ctrl._main_window.child_window(title="DDS Setting").click_input()
        except Exception:
            if not self._ctrl.click_by_text("DDS Setting", retries=5):
                raise RuntimeError("OscilloscopePanel: Không click được 'DDS Setting'")
        deadline = time.time() + 5
        while time.time() < deadline:
            if self.is_dds_setting_open():
                return
            time.sleep(0.15)
        raise RuntimeError("OscilloscopePanel: DDS Setting không mở trong 5 giây")

    def set_dds_params(
        self,
        signal_type: str = "",
        frequency_hz: str = "",
        amplitude_v: str = "",
        offset_v: str = "",
    ) -> list:
        """
        @brief  Cấu hình các thông số DDS Setting rồi click Apply
        @param  signal_type:  Signal Type dropdown
                              ("Sine","Square","AM/FM","Ramp","Trapezia",
                               "Gaussian","Arbitrary (AWG)","Exponent","DC Voltage")
        @param  frequency_hz: Frequency (Hz) text field (ví dụ: "1000.000")
        @param  amplitude_v:  Amplitude (V) text field (ví dụ: "1.000")
        @param  offset_v:     Offset (V) text field (ví dụ: "0.000")
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"OscilloscopePanel DDS: signal_type={signal_type}, "
            f"frequency={frequency_hz}, amplitude={amplitude_v}, offset={offset_v}"
        )
        if signal_type:
            self._dds_select_signal_type(signal_type)

        if frequency_hz:
            self._dds_set_field("txtFreq", frequency_hz)
        if amplitude_v:
            self._dds_set_field("txtAmplitude", amplitude_v)
        if offset_v:
            self._dds_set_field("txtOffset", offset_v)

        self._click_apply()
        errs = self._check_form_validation_errors(self._DDS_FORM)
        if errs:
            logger.warning(f"OscilloscopePanel DDS: validation errors — {errs}")
        else:
            logger.info("OscilloscopePanel DDS: Apply OK")
        return errs

    def toggle_signal_on(self) -> None:
        """
        @brief  Click checkbox Signal On (auto_id=cbSignal) để bật/tắt tín hiệu DDS
        @retval None
        """
        logger.info("OscilloscopePanel DDS: toggle Signal On")
        form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
        form.child_window(auto_id="cbSignal").click_input()
        time.sleep(0.1)

    def click_sync(self) -> None:
        """
        @brief  Click checkbox Sync (auto_id=cbSync) trong DDS Setting
        @retval None
        """
        logger.info("OscilloscopePanel DDS: Sync")
        form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
        form.child_window(auto_id="cbSync").click_input()
        time.sleep(0.1)

    # ── Apply ─────────────────────────────────────────────────────────────────

    def _click_apply(self) -> None:
        """
        @brief  Click nút Apply trong form DSO hoặc DDS (scoped, nhanh hơn click_by_text).
        @retval None
        """
        for form_id in (self._DSO_FORM, self._DDS_FORM):
            try:
                form = self._ctrl._main_window.child_window(auto_id=form_id)
                if not form.exists():
                    continue
                btn = form.child_window(title="Apply", control_type="Button")
                if btn.exists():
                    btn.click_input()
                    return
            except Exception:
                pass
        # fallback
        if not self._ctrl.click_by_text("Apply"):
            raise RuntimeError("OscilloscopePanel: Không click được 'Apply'")

    def _check_form_validation_errors(self, form_auto_id: str) -> list:
        """Quét chỉ trong form con (nhanh) thay vì toàn bộ main_window.descendants()."""
        _KEYWORDS = ("cannot", "invalid", "out of range")
        errors = []
        try:
            form = self._ctrl._main_window.child_window(auto_id=form_auto_id)
            for ctrl in form.descendants():
                try:
                    t = ctrl.window_text().strip()
                    if t and any(kw in t.lower() for kw in _KEYWORDS):
                        errors.append(t)
                except Exception:
                    pass
        except Exception:
            pass
        return errors

    # ── Private helpers ───────────────────────────────────────────────────────

    # auto_id của form DSO và DDS
    _DSO_FORM     = "FormDetailOscilloscopeDSOSetting"
    _DDS_FORM     = "FormDetailOscilloscopeDDSSetting"
    _DROPDOWN_IDS = {
        "Time/Div":      "cmbTime_Div",
        "Channel":       "cmbCH",
        "Probe":         "cmbProbe",
        "Voltage/Div":   "cmbVotage",
        "Coupling":      "cmbCoupling",
        "Trigger Mode":  "cmbTriggerMode",
        "Trigger Sweep": "cmbTriggerSweep",
    }

    def _select_dropdown(self, label: str, value: str) -> None:
        """
        @brief  Click Pane dropdown (auto_id) → chọn item từ popup xuất hiện.
        @param  label: Key trong _DROPDOWN_IDS (ví dụ: "Time/Div", "Coupling")
        @param  value: Item cần chọn trong popup (ví dụ: "5.00 us", "DC")
        @retval None
        """
        logger.info(f"OscilloscopePanel: dropdown '{label}' → chọn '{value}'")
        auto_id = self._DROPDOWN_IDS.get(label)
        if auto_id is None:
            raise RuntimeError(f"OscilloscopePanel: không có auto_id cho label '{label}'")

        form = self._ctrl._main_window.child_window(auto_id=self._DSO_FORM)
        pane = form.child_window(auto_id=auto_id)

        # Click lblContent (hiển thị giá trị hiện tại) để mở dropdown list.
        # Channel (cmbCH) không có lblContent → click thẳng vào pane.
        try:
            pane.child_window(auto_id="lblContent").click_input()
        except Exception:
            pane.click_input()
        time.sleep(0.3)

        if not self._ctrl.click_in_any_window(value):
            raise RuntimeError(f"OscilloscopePanel: Không chọn được '{value}' trong popup '{label}'")

    def _set_channel_on_off(self, enabled: bool) -> None:
        """
        @brief  Click checkbox ON/OFF bên cạnh Channel dropdown để bật/tắt kênh.
                Scope vào DSO form thay vì quét toàn bộ main_window.
        @param  enabled: True = bật kênh (ON), False = tắt kênh (OFF)
        @retval None
        """
        state = "ON" if enabled else "OFF"
        logger.info(f"OscilloscopePanel: set channel ON/OFF → {state}")
        form = self._ctrl._main_window.child_window(auto_id=self._DSO_FORM)
        for ctrl in form.descendants():
            try:
                if ctrl.window_text().strip() != "ON/OFF":
                    continue
                try:
                    current = ctrl.get_toggle_state()  # 0 = OFF, 1 = ON
                    if (enabled and current == 1) or (not enabled and current == 0):
                        logger.info(f"OscilloscopePanel: ON/OFF đã ở {state}, skip click")
                        return
                except Exception:
                    pass
                ctrl.click_input()
                time.sleep(0.1)
                return
            except Exception:
                pass
        raise RuntimeError("OscilloscopePanel: Không tìm thấy control 'ON/OFF' của Channel")

    def _dds_select_signal_type(self, value: str) -> None:
        """Click cmbSignalType > lblContent → popup → chọn item."""
        logger.info(f"OscilloscopePanel DDS: signal_type → '{value}'")
        form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
        pane = form.child_window(auto_id="cmbSignalType")
        pane.child_window(auto_id="lblContent").click_input()
        time.sleep(0.3)
        if not self._ctrl.click_in_any_window(value):
            raise RuntimeError(f"OscilloscopePanel DDS: Không chọn được Signal Type '{value}'")

    def _dds_set_field(self, auto_id: str, value: str) -> None:
        """Tìm Edit (textBox1) bên trong Pane theo auto_id → xoá → nhập value → Enter."""
        logger.info(f"OscilloscopePanel DDS: set field {auto_id!r} = {value!r}")
        form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
        edit = form.child_window(auto_id=auto_id).child_window(auto_id="textBox1")
        edit.click_input()
        time.sleep(0.1)
        edit.type_keys("^a{BACKSPACE}")
        edit.set_edit_text(str(value))
        edit.type_keys("{ENTER}")

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_dso_dropdown_value(self, label: str) -> str:
        """Read current displayed value of a DSO dropdown (lblContent text)."""
        auto_id = self._DROPDOWN_IDS.get(label)
        if not auto_id:
            return ""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DSO_FORM)
            return form.child_window(auto_id=auto_id).child_window(auto_id="lblContent").window_text().strip()
        except Exception:
            return ""

    def get_channel_on_off_state(self) -> bool:
        """Read current ON/OFF checkbox state — scope to DSO form (nhanh hơn)."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DSO_FORM)
            for ctrl in form.descendants():
                try:
                    if ctrl.window_text().strip() == "ON/OFF":
                        return ctrl.get_toggle_state() == 1
                except Exception:
                    pass
        except Exception:
            pass
        return False

    def is_signal_on_checked(self) -> bool:
        """Return True if the Signal On checkbox (cbSignal) is checked."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
            return form.child_window(auto_id="cbSignal").get_toggle_state() == 1
        except Exception:
            return False

    def is_sync_checked(self) -> bool:
        """Return True if the Sync checkbox (cbSync) is checked."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
            return form.child_window(auto_id="cbSync").get_toggle_state() == 1
        except Exception:
            return False

    def get_dds_field_value(self, field_id: str) -> str:
        """Read current text of a DDS input field (textBox1 inside the pane)."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
            return form.child_window(auto_id=field_id).child_window(auto_id="textBox1").window_text().strip()
        except Exception:
            return ""

    # ── Close helpers ─────────────────────────────────────────────────────────

    def click_apply(self) -> None:
        """Public Apply — delegates to _click_apply."""
        self._click_apply()

    def close_dso_setting(self) -> None:
        """Close DSO Setting form via WM_CLOSE (equivalent to clicking X)."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DSO_FORM)
            form.close()
            time.sleep(0.3)
        except Exception:
            pass

    def close_dds_setting(self) -> None:
        """Close DDS Setting form via WM_CLOSE."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
            form.close()
            time.sleep(0.3)
        except Exception:
            pass

    def is_dso_setting_open(self) -> bool:
        """Return True if the DSO Setting form is currently visible."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DSO_FORM)
            return form.exists() and form.is_visible()
        except Exception:
            return False

    def is_dds_setting_open(self) -> bool:
        """Return True if the DDS Setting form is currently visible."""
        try:
            form = self._ctrl._main_window.child_window(auto_id=self._DDS_FORM)
            return form.exists() and form.is_visible()
        except Exception:
            return False

    def _is_oscilloscope_nav_expanded(self) -> bool:
        """
        @brief  Kiểm tra Oscilloscope nav item đang expanded.
                Dùng child_window(title=) thay vì quét toàn bộ descendants() — nhanh hơn.
        @retval bool — True nếu panel đang mở, False nếu đang đóng
        """
        if self._ctrl._main_window is None:
            return False
        try:
            return self._ctrl._main_window.child_window(title="DSO Setting").exists()
        except Exception:
            return False
