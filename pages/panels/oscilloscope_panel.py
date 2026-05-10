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
        @brief  Đảm bảo Oscilloscope panel đang mở (click "Oscilloscope" nếu chưa mở).
                Nếu click vô tình đóng panel (toggle), tự click lại để mở.
        @retval None
        """
        if self._ctrl._main_window is None:
            return
        if self._is_oscilloscope_nav_expanded():
            return
        logger.info("OscilloscopePanel: mở Oscilloscope card …")
        if not self._ctrl.click_by_text("Oscilloscope", retries=5):
            raise RuntimeError("OscilloscopePanel: Không click được 'Oscilloscope'")
        if not self._ctrl.wait_for_text("DSO Setting", timeout=5):
            logger.warning("OscilloscopePanel: click đã đóng panel, click lại …")
            self._ctrl.click_by_text("Oscilloscope", retries=5)
            self._ctrl.wait_for_text("DSO Setting", timeout=5)

    # ── DSO Setting ───────────────────────────────────────────────────────────

    def open_dso_setting(self) -> None:
        """
        @brief  Click mục "DSO Setting" trong Oscilloscope panel
        @retval None
        """
        logger.info("OscilloscopePanel: mở DSO Setting")
        self.ensure_oscilloscope_panel_open()
        if not self._ctrl.click_by_text("DSO Setting", retries=5):
            raise RuntimeError("OscilloscopePanel: Không click được 'DSO Setting'")
        self._ctrl.wait_for_text("Time/Div", timeout=5)

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
        time.sleep(0.2)
        errs = self.check_validation_errors()
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
        time.sleep(0.2)

    def set_voltage_div(self, value: str) -> None:
        """
        @brief  Chọn Voltage/Div từ dropdown rồi click Apply
        @param  value: Giá trị Voltage/Div (ví dụ: "1.00V", "100mV", "10.0mV")
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Voltage/Div = {value}")
        self._select_dropdown("Voltage/Div", value)
        self._click_apply()
        time.sleep(0.2)

    def set_coupling(self, value: str) -> None:
        """
        @brief  Chọn Coupling từ dropdown rồi click Apply
        @param  value: "DC" | "AC" | "GND"
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Coupling = {value}")
        self._select_dropdown("Coupling", value)
        self._click_apply()
        time.sleep(0.2)

    def set_trigger_mode(self, mode: str) -> None:
        """
        @brief  Chọn Trigger Mode từ dropdown rồi click Apply
        @param  mode: "Edge" | "Pulse" | "Slope" | "Video" | "Timeout"
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Trigger Mode = {mode}")
        self._select_dropdown("Trigger Mode", mode)
        self._click_apply()
        time.sleep(0.2)

    def set_trigger_sweep(self, sweep: str) -> None:
        """
        @brief  Chọn Trigger Sweep từ dropdown rồi click Apply
        @param  sweep: "Auto" | "Normal" | "Single"
        @retval None
        """
        logger.info(f"OscilloscopePanel: set Trigger Sweep = {sweep}")
        self._select_dropdown("Trigger Sweep", sweep)
        self._click_apply()
        time.sleep(0.2)

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
        @brief  Click mục "DDS Setting" trong Oscilloscope panel
        @retval None
        """
        logger.info("OscilloscopePanel: mở DDS Setting")
        self.ensure_oscilloscope_panel_open()
        if not self._ctrl.click_by_text("DDS Setting", retries=5):
            raise RuntimeError("OscilloscopePanel: Không click được 'DDS Setting'")
        self._ctrl.wait_for_text("Signal Type", timeout=5)

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
            self._select_dropdown("Signal Type", signal_type)

        self._ctrl.build_cache()
        try:
            if frequency_hz:
                self._ctrl.set_field_by_label("Frequency (Hz)", frequency_hz)
            if amplitude_v:
                self._ctrl.set_field_by_label("Amplitude (V)", amplitude_v)
            if offset_v:
                self._ctrl.set_field_by_label("Offset (V)", offset_v)
        finally:
            self._ctrl.invalidate_cache()

        self._click_apply()
        time.sleep(0.2)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"OscilloscopePanel DDS: validation errors — {errs}")
        else:
            logger.info("OscilloscopePanel DDS: Apply OK")
        return errs

    def toggle_signal_on(self) -> None:
        """
        @brief  Click checkbox Signal On để bật/tắt tín hiệu DDS
        @retval None
        """
        logger.info("OscilloscopePanel DDS: toggle Signal On")
        if not self._ctrl.click_by_text("Signal On", retries=5):
            raise RuntimeError("OscilloscopePanel: Không click được checkbox 'Signal On'")

    def click_sync(self) -> None:
        """
        @brief  Click nút Sync trong DDS Setting
        @retval None
        """
        logger.info("OscilloscopePanel DDS: Sync")
        if not self._ctrl.click_by_text("Sync", retries=5):
            raise RuntimeError("OscilloscopePanel: Không click được nút 'Sync'")

    # ── Apply ─────────────────────────────────────────────────────────────────

    def _click_apply(self) -> None:
        """
        @brief  Click nút Apply trong Oscilloscope panel
        @retval None
        """
        if not self._ctrl.click_by_text("Apply"):
            raise RuntimeError("OscilloscopePanel: Không click được 'Apply'")

    # ── Private helpers ───────────────────────────────────────────────────────

    def _select_dropdown(self, label: str, value: str) -> None:
        """
        @brief  Tìm ComboBox kế label → click để mở list → chọn item.
                Primary: select_by_label(). Fallback: click_by_text(label) + click_in_any_window(value).
        @param  label: Text label đứng trên combobox (ví dụ: "Time/Div", "Coupling")
        @param  value: Item cần chọn (ví dụ: "5.00 us", "DC")
        @retval None
        """
        logger.info(f"OscilloscopePanel: dropdown '{label}' → chọn '{value}'")
        if self._ctrl.select_by_label(label, value):
            return
        logger.warning(f"OscilloscopePanel: select_by_label thất bại cho '{label}', thử fallback …")
        if not self._ctrl.click_by_text(label, retries=3):
            raise RuntimeError(f"OscilloscopePanel: Không mở được dropdown '{label}'")
        time.sleep(0.3)
        if not self._ctrl.click_in_any_window(value):
            raise RuntimeError(f"OscilloscopePanel: Không chọn được '{value}' trong dropdown '{label}'")

    def _set_channel_on_off(self, enabled: bool) -> None:
        """
        @brief  Click checkbox ON/OFF bên cạnh Channel dropdown để bật/tắt kênh.
                Đọc get_toggle_state() trước khi click để tránh toggle ngược.
        @param  enabled: True = bật kênh (ON), False = tắt kênh (OFF)
        @retval None
        """
        state = "ON" if enabled else "OFF"
        logger.info(f"OscilloscopePanel: set channel ON/OFF → {state}")
        if self._ctrl._main_window is None:
            raise RuntimeError("OscilloscopePanel: main window không khả dụng")
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip() != "ON/OFF":
                    continue
                try:
                    current = ctrl.get_toggle_state()  # 0 = OFF, 1 = ON
                    if (enabled and current == 1) or (not enabled and current == 0):
                        logger.info(f"OscilloscopePanel: ON/OFF đã ở {state}, skip click")
                        return
                except Exception:
                    pass  # control không hỗ trợ toggle state — click thẳng
                ctrl.click_input()
                time.sleep(0.1)
                return
            except Exception:
                pass
        raise RuntimeError("OscilloscopePanel: Không tìm thấy control 'ON/OFF' của Channel")

    def _is_oscilloscope_nav_expanded(self) -> bool:
        """
        @brief  Kiểm tra Oscilloscope nav item đang expanded (sub-items hiển thị trong cây)
        @retval bool — True nếu panel đang mở, False nếu đang đóng
        """
        if self._ctrl._main_window is None:
            return False
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip() in ("DSO Setting", "DDS Setting"):
                    return True
            except Exception:
                pass
        return False
