"""
MainPage — Page Object cho cửa sổ FormMainEliteRF của PC17.

Đây là facade mỏng: mỗi method delegate xuống panel tương ứng.
Logic thực tế nằm trong pages/panels/:
    - SystemPanel       — kết nối / ngắt kết nối
    - DetailPanel       — Temperature, Serial Number
    - VnaPanel          — Measurement, Stimulus, Markers
    - SpectrumPanel     — Analysis Mode, Sweep Settings, Zero-span Setting
    - AttenuatorPanel   — (chưa implement)
    - SignalPanel       — RF1 output, Trigger Output
    - PowerPanel        — Sensor Setting, Chart Setting, Control Measurement
    - OscilloscopePanel — DSO Setting, DDS Setting
"""
from __future__ import annotations

from core.app_controller import AppController
from pages.base_page import BasePage
from pages.panels import (
    AttenuatorPanel,
    DetailPanel,
    OscilloscopePanel,
    PowerPanel,
    SignalPanel,
    SpectrumPanel,
    SystemPanel,
    VnaPanel,
)


class MainPage(BasePage):
    """Facade cho FormMainEliteRF — compose các panel con."""

    def __init__(self, controller: AppController):
        super().__init__(controller)
        self.system       = SystemPanel(controller)
        self.detail       = DetailPanel(controller)
        self.vna          = VnaPanel(controller)
        self.spectrum     = SpectrumPanel(controller)
        self.attenuator   = AttenuatorPanel(controller)
        self.signal       = SignalPanel(controller)
        self.power        = PowerPanel(controller)
        self.oscilloscope = OscilloscopePanel(controller)

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

    # ── Power panel ───────────────────────────────────────────────────────────

    def ensure_power_panel_open(self) -> None:
        self.power.ensure_power_panel_open()

    def open_sensor_setting(self) -> None:
        self.power.open_sensor_setting()

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
        return self.power.set_sensor_setting_params(
            averages=averages,
            correction_db=correction_db,
            disp_res=disp_res,
            duty_cycle_pct=duty_cycle_pct,
            frequency_hz=frequency_hz,
            frequency_unit=frequency_unit,
            interval_ms=interval_ms,
            pulse_top_power=pulse_top_power,
            pulse_width=pulse_width,
            signal_peak_noise=signal_peak_noise,
            signal_power=signal_power,
            trace_delay=trace_delay,
            trace_size=trace_size,
            trace_time=trace_time,
            units=units,
        )

    def toggle_power_correction(self) -> None:
        self.power.toggle_correction()

    def toggle_power_duty_cycle(self) -> None:
        self.power.toggle_duty_cycle()

    def set_power_frequency(self, value: str, unit: str = "") -> None:
        self.power.set_frequency(value, unit)

    def set_power_averages(self, value: str) -> None:
        self.power.set_averages(value)

    def set_power_units(self, unit: str) -> None:
        self.power.set_units(unit)

    def read_signal_power(self) -> str:
        return self.power.read_signal_power()

    def open_chart_setting(self) -> None:
        self.power.open_chart_setting()

    def set_chart_setting_params(
        self,
        time_span: str = "",
        max_dbm: str = "",
        dbm_per_div: str = "",
    ) -> list:
        return self.power.set_chart_setting_params(
            time_span=time_span,
            max_dbm=max_dbm,
            dbm_per_div=dbm_per_div,
        )

    def click_pause_scrolling(self) -> None:
        self.power.click_pause_scrolling()

    def click_auto_scroll(self) -> None:
        self.power.click_auto_scroll()

    def open_control_measurement(self) -> None:
        self.power.open_control_measurement()

    def click_start_measurement(self) -> None:
        self.power.click_start_measurement()

    def click_stop_measurement(self) -> None:
        self.power.click_stop_measurement()

    # ── Oscilloscope panel ────────────────────────────────────────────────────

    def ensure_oscilloscope_panel_open(self) -> None:
        self.oscilloscope.ensure_oscilloscope_panel_open()

    def open_dso_setting(self) -> None:
        self.oscilloscope.open_dso_setting()

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
        return self.oscilloscope.set_dso_params(
            time_div=time_div,
            channel=channel,
            channel_on=channel_on,
            probe=probe,
            voltage_div=voltage_div,
            coupling=coupling,
            trigger_mode=trigger_mode,
            trigger_sweep=trigger_sweep,
        )

    def select_oscilloscope_channel(self, channel: str) -> None:
        self.oscilloscope.select_channel(channel)

    def set_oscilloscope_channel_enabled(self, enabled: bool) -> None:
        self.oscilloscope.set_channel_enabled(enabled)

    def set_time_div(self, value: str) -> None:
        self.oscilloscope.set_time_div(value)

    def set_voltage_div(self, value: str) -> None:
        self.oscilloscope.set_voltage_div(value)

    def set_oscilloscope_coupling(self, value: str) -> None:
        self.oscilloscope.set_coupling(value)

    def set_trigger_mode(self, mode: str) -> None:
        self.oscilloscope.set_trigger_mode(mode)

    def set_trigger_sweep(self, sweep: str) -> None:
        self.oscilloscope.set_trigger_sweep(sweep)

    def oscilloscope_cancel(self) -> None:
        self.oscilloscope.click_cancel()

    def open_dds_setting(self) -> None:
        self.oscilloscope.open_dds_setting()

    def set_dds_params(
        self,
        signal_type: str = "",
        frequency_hz: str = "",
        amplitude_v: str = "",
        offset_v: str = "",
    ) -> list:
        return self.oscilloscope.set_dds_params(
            signal_type=signal_type,
            frequency_hz=frequency_hz,
            amplitude_v=amplitude_v,
            offset_v=offset_v,
        )

    def toggle_dds_signal_on(self) -> None:
        self.oscilloscope.toggle_signal_on()

    def click_dds_sync(self) -> None:
        self.oscilloscope.click_sync()
