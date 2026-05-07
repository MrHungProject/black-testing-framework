"""
MainPage — Page Object cho cửa sổ FormMainEliteRF của PC17.

Đây là facade mỏng: mỗi method delegate xuống panel tương ứng.
Logic thực tế nằm trong pages/panels/:
    - SystemPanel   — kết nối / ngắt kết nối
    - DetailPanel   — Temperature, Serial Number
    - VnaPanel        — Measurement, Stimulus, Markers
    - SpectrumPanel   — connect/disconnect, Analysis Mode, Sweep Settings, Zero-span Setting
    - AttenuatorPanel — (chưa implement)
    - SignalPanel     — RF1 output, Trigger Output
"""
from __future__ import annotations

from core.app_controller import AppController
from pages.base_page import BasePage
from pages.panels import (
    AttenuatorPanel,
    DetailPanel,
    SignalPanel,
    SpectrumPanel,
    SystemPanel,
    VnaPanel,
)


class MainPage(BasePage):
    """Facade cho FormMainEliteRF — compose các panel con."""

    def __init__(self, controller: AppController):
        super().__init__(controller)
        self.system     = SystemPanel(controller)
        self.detail     = DetailPanel(controller)
        self.vna        = VnaPanel(controller)
        self.spectrum   = SpectrumPanel(controller)
        self.attenuator = AttenuatorPanel(controller)
        self.signal     = SignalPanel(controller)

    # ── System / Connection ───────────────────────────────────────────────────

    def setup_connection(self) -> None:
        self.system.setup_connection()

    def open_connect_panel(self) -> None:
        self.system.open_connect_panel()

    def is_connected(self) -> bool:
        return self.system.is_connected()

    def click_disconnect(self) -> None:
        self.system.click_disconnect()

    def reconnect(self) -> None:
        self.system.reconnect()

    # ── Detail panel ──────────────────────────────────────────────────────────

    def click_detail(self) -> bool:
        return self.detail.click_detail()

    def get_temperature(self) -> str:
        return self.detail.get_temperature()

    def get_serial_number(self) -> str:
        return self.detail.get_serial_number()

    # ── VNA panel ─────────────────────────────────────────────────────────────

    def ensure_vna_open(self) -> None:
        self.vna.ensure_vna_open()

    def open_measurement(self) -> None:
        self.vna.open_measurement()

    def select_s_parameter(self, name: str) -> None:
        self.vna.select_s_parameter(name)

    def click_apply(self) -> None:
        self.vna.click_apply()

    def open_calibration(self) -> None:
        self.vna.open_calibration()

    def click_calibrate(self) -> None:
        self.vna.click_calibrate()

    def click_solt_cal(self) -> None:
        self.vna.click_solt_cal()

    def click_all_calibration_steps(self) -> None:
        self.vna.click_all_calibration_steps()

    def wait_for_calibration_complete(self, timeout: int = 60) -> bool:
        return self.vna.wait_for_calibration_complete(timeout=timeout)

    def apply_calibration(self) -> None:
        self.vna.apply_calibration()

    def open_stimulus(self) -> None:
        self.vna.open_stimulus()

    def set_stimulus_params(
        self,
        start: str = "2GHz",
        stop: str = "6GHz",
        center: str = "9.05GHz",
        span: str = "3GHz",
        points: str = "301",
        if_bw: str = "10kHz",
        power: str = "0",
    ) -> list:
        return self.vna.set_stimulus_params(
            start=start, stop=stop, center=center,
            span=span, points=points, if_bw=if_bw, power=power,
        )

    def open_markers(self) -> None:
        self.vna.open_markers()

    def click_add_marker(self) -> None:
        self.vna.click_add_marker()

    def open_trace_dropdown(self) -> None:
        self.vna.open_trace_dropdown()

    def select_trace(self, value: str = "Trace 2") -> None:
        self.vna.select_trace(value)

    def setup_marker(self) -> None:
        self.vna.setup_marker()

    def extract_traces(self) -> list:
        return self.vna.extract_traces()

    def extract_markers(self) -> list:
        return self.vna.extract_markers()

    # ── Signal panel ──────────────────────────────────────────────────────────

    def ensure_signal_panel_open(self) -> None:
        self.signal.ensure_signal_panel_open()

    def open_rf1_output(self) -> None:
        self.signal.open_rf1_output()

    def set_rf1_params(self, rf1_out: str = "0", power_level: str = "0") -> None:
        self.signal.set_rf1_params(rf1_out=rf1_out, power_level=power_level)

    def open_trigger_output(self) -> None:
        self.signal.open_trigger_output()

    def set_trigger_params(
        self,
        start_freq: str = "",
        stop_freq: str = "",
        step: str = "",
        dwell_time: str = "",
        cycles: str = "",
    ) -> None:
        self.signal.set_trigger_params(
            start_freq=start_freq, stop_freq=stop_freq,
            step=step, dwell_time=dwell_time, cycles=cycles,
        )

    def signal_check_validation_errors(self) -> list:
        return self.signal.check_validation_errors()

    def signal_get_error_near_label(self, label: str) -> str:
        return self.signal.get_error_near_label(label)

    def signal_get_temperature(self) -> str:
        return self.signal.get_temperature()

    # ── System — per-device connection ───────────────────────────────────────

    def connect_device(self, device_label: str) -> bool:
        return self.system.connect_device(device_label)

    def disconnect_device(self, device_label: str) -> bool:
        return self.system.disconnect_device(device_label)

    def is_device_connected(self, device_label: str) -> bool:
        return self.system.is_device_connected(device_label)

    # ── Spectrum panel ────────────────────────────────────────────────────────

    def click_spectrum_panel(self) -> None:
        self.spectrum._click_spectrum_panel()

    def ensure_spectrum_panel_open(self) -> None:
        self.spectrum.ensure_spectrum_panel_open()

    def open_analysis_mode(self) -> None:
        self.spectrum.open_analysis_mode()

    def select_analysis_mode(self, mode: str) -> bool:
        return self.spectrum.select_analysis_mode(mode)

    def open_sweep_settings(self) -> None:
        self.spectrum.open_sweep_settings()

    def open_zerospan_setting(self) -> None:
        self.spectrum.open_zerospan_setting()

    def open_capture_setting(self) -> None:
        self.spectrum.open_capture_setting()

    def set_capture_setting_params(
        self,
        center: str = "",
        step: str = "",
        ref_level: str = "",
        swp_time: str = "",
    ) -> list:
        return self.spectrum.set_capture_setting_params(
            center=center, step=step, ref_level=ref_level, swp_time=swp_time,
        )

    def open_frequency(self) -> None:
        self.spectrum.open_frequency()

    def set_frequency_params(
        self,
        start: str = "",
        stop: str = "",
        step: str = "",
        center: str = "",
        span: str = "",
    ) -> list:
        return self.spectrum.set_frequency_params(
            start=start, stop=stop, step=step, center=center, span=span,
        )

    def open_amplitude(self) -> None:
        self.spectrum.open_amplitude()

    def set_amplitude_params(
        self,
        ref_level: str = "",
        div: str = "",
        gain: str = "",
        atten: str = "",
    ) -> list:
        return self.spectrum.set_amplitude_params(
            ref_level=ref_level, div=div, gain=gain, atten=atten,
        )

    def click_spectrum_preset(self) -> None:
        self.spectrum.click_preset()

    def open_spectrum_markers(self) -> None:
        self.spectrum.open_markers()

    def click_peak_search(self) -> None:
        self.spectrum.click_peak_search()

    def click_next_peak(self) -> None:
        self.spectrum.click_next_peak()

    def remove_all_markers(self) -> None:
        self.spectrum.remove_all_markers()

    def extract_spectrum_markers(self) -> list:
        return self.spectrum.extract_markers()
