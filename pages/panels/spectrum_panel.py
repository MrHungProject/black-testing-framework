"""SpectrumPanel — tương tác với Spectrum Analyzer panel trong FormMainEliteRF."""
from __future__ import annotations

import time

import pyautogui

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SpectrumPanel(BasePage):
    """Spectrum Analyzer controls."""

    _RADIO_OFFSET_X = 148   # px lệch phải text label để trúng ô tròn radio

    # ── Panel open ────────────────────────────────────────────────────────────

    def ensure_spectrum_panel_open(self) -> None:
        """
        @brief  Đảm bảo Spectrum panel đang mở (click "SPECTRUM" nếu chưa mở).
                Nếu click vô tình đóng panel (toggle), tự click lại để mở.
        @retval None
        """
        if self._ctrl._main_window is None:
            return
        if self._is_spectrum_nav_expanded():
            return
        logger.info("SpectrumPanel: mở SPECTRUM card …")
        self._click_spectrum_panel()
        if not self._ctrl.wait_for_text("Analysis Mode", timeout=5):
            logger.warning("SpectrumPanel: click đã đóng panel, click lại để mở …")
            self._click_spectrum_panel()
            self._ctrl.wait_for_text("Analysis Mode", timeout=5)

    # ── Analysis Mode ─────────────────────────────────────────────────────────

    def open_analysis_mode(self) -> None:
        """
        @brief  Click mục "Analysis Mode" trong Spectrum panel
        @retval None
        """
        logger.info("SpectrumPanel: mở Analysis Mode")
        self.ensure_spectrum_panel_open()
        if not self._ctrl.click_by_text("Analysis Mode", retries=5):
            raise RuntimeError("SpectrumPanel: Không click được 'Analysis Mode'")
        self._ctrl.wait_for_text("Sweep", timeout=5)

    def select_analysis_mode(self, mode: str) -> bool:
        """
        @brief  Chọn radio button Analysis Mode: "Sweep", "Real-Time" hoặc "Zero-span"
        @param  mode: Tên chế độ cần chọn ("Sweep" | "Real-Time" | "Zero-span")
        @retval bool — True nếu click được, False nếu không tìm thấy
        """
        logger.info(f"SpectrumPanel: select analysis mode = {mode}")
        return self._click_radio_by_text(mode)

    # ── Sweep Settings ────────────────────────────────────────────────────────

    def open_sweep_settings(self) -> None:
        """
        @brief  Click mục "Sweep Settings" trong Spectrum panel
        @retval None
        """
        logger.info("SpectrumPanel: mở Sweep Settings")
        self.ensure_spectrum_panel_open()
        if not self._ctrl.click_by_text("Sweep Settings", retries=5):
            raise RuntimeError("SpectrumPanel: Không click được 'Sweep Settings'")
        if not self._ctrl.wait_for_text("Frequency", timeout=5):
            logger.warning("SpectrumPanel: Sweep Settings bị đóng do toggle, click lại …")
            self._ctrl.click_by_text("Sweep Settings", retries=5)
            self._ctrl.wait_for_text("Frequency", timeout=5)

    # ── Zero-span Setting ─────────────────────────────────────────────────────

    def open_zerospan_setting(self) -> None:
        """
        @brief  Click mục "Zero-span Setting" trong Spectrum panel
        @retval None
        """
        logger.info("SpectrumPanel: mở Zero-span Setting")
        self.ensure_spectrum_panel_open()
        if not self._ctrl.click_by_text("Zero-span Setting", retries=5):
            raise RuntimeError("SpectrumPanel: Không click được 'Zero-span Setting'")
        self._ctrl.wait_for_text("Capture Setting", timeout=5)

    def open_capture_setting(self) -> None:
        """
        @brief  Click mục "Capture Setting" trong Zero-span Setting
        @retval None
        """
        logger.info("SpectrumPanel: mở Capture Setting")
        self.ensure_spectrum_panel_open()
        if not self._ctrl.click_by_text("Capture Setting", retries=5):
            raise RuntimeError("SpectrumPanel: Không click được 'Capture Setting'")
        self._ctrl.wait_for_text("Center", timeout=5)

    def set_capture_setting_params(
        self,
        center: str = "",
        step: str = "",
        ref_level: str = "",
        swp_time: str = "",
    ) -> list:
        """
        @brief  Điền các thông số Capture Setting rồi click Apply
        @param  center:    Center frequency (ví dụ: "1MHz")
        @param  step:      Step frequency (ví dụ: "20MHz")
        @param  ref_level: Ref Level (dBm)
        @param  swp_time:  Sweep Time (ví dụ: "1ms")
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"SpectrumPanel Capture Setting: center={center}, step={step}, "
            f"ref_level={ref_level}, swp_time={swp_time}"
        )
        self._ctrl.build_cache()
        try:
            if center:
                self._ctrl.set_field_by_label("Center", center)
            if step:
                self._ctrl.set_field_by_label("Step", step)
            if ref_level:
                self._ctrl.set_field_by_label("Ref Level", ref_level)
            if swp_time:
                self._ctrl.set_field_by_label("Swp Time", swp_time)
        finally:
            self._ctrl.invalidate_cache()
        self._click_apply()
        time.sleep(0.2)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"SpectrumPanel Capture Setting: validation errors — {errs}")
        else:
            logger.info("SpectrumPanel Capture Setting: Apply OK")
        return errs

    # ── Frequency (Sweep Settings → Frequency) ───────────────────────────────

    def open_frequency(self) -> None:
        """
        @brief  Click mục "Frequency" trong Sweep Settings
        @retval None
        """
        logger.info("SpectrumPanel: mở Frequency")
        self.ensure_spectrum_panel_open()
        if not self._ctrl.click_by_text("Frequency", retries=5):
            raise RuntimeError("SpectrumPanel: Không click được 'Frequency'")
        self._ctrl.wait_for_text("Start Frequency", timeout=5)

    def set_frequency_params(
        self,
        start: str = "",
        stop: str = "",
        step: str = "",
        center: str = "",
        span: str = "",
    ) -> list:
        """
        @brief  Điền các thông số Frequency rồi click Apply
        @param  start:  Start Frequency
        @param  stop:   Stop Frequency
        @param  step:   Step Frequency
        @param  center: Center Frequency
        @param  span:   Span Frequency
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"SpectrumPanel Frequency: start={start}, stop={stop}, step={step}, "
            f"center={center}, span={span}"
        )
        self._ctrl.build_cache()
        try:
            if start:
                self._ctrl.set_field_by_label("Start Frequency", start)
            if stop:
                self._ctrl.set_field_by_label("Stop Frequency", stop)
            if step:
                self._ctrl.set_field_by_label("Step Frequency", step)
            if center:
                self._ctrl.set_field_by_label("Center Frequency", center)
            if span:
                self._ctrl.set_field_by_label("Span Frequency", span)
        finally:
            self._ctrl.invalidate_cache()
        self._click_apply()
        time.sleep(0.2)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"SpectrumPanel Frequency: validation errors — {errs}")
        else:
            logger.info("SpectrumPanel Frequency: Apply OK")
        return errs

    # ── Markers (Sweep Settings → Markers) ───────────────────────────────────

    def click_preset(self) -> None:
        """
        @brief  Click nút Preset để reset Spectrum Analyzer về trạng thái mặc định
        @retval None
        """
        if not self._ctrl.click_by_text("Preset"):
            raise RuntimeError("SpectrumPanel: Không click được 'Preset'")
        logger.info("SpectrumPanel: Preset OK")
        time.sleep(0.5)

    def open_markers(self) -> None:
        """
        @brief  Click mục "Markers" trong Sweep Settings.
                Tự động expand Sweep Settings nếu sub-items đã bị collapse.
        @retval None
        """
        logger.info("SpectrumPanel: mở Markers")
        self.ensure_spectrum_panel_open()
        if not self._ctrl.has_element_with_text("Peak Table"):
            self._ctrl.click_by_text("Sweep Settings", retries=5)
            self._ctrl.wait_for_text("Markers", timeout=5)
        if not self._ctrl.click_by_text("Markers", retries=5):
            raise RuntimeError("SpectrumPanel: Không click được 'Markers'")
        self._ctrl.wait_for_text("Peak Search", timeout=5)

    def click_peak_search(self) -> None:
        """
        @brief  Click nút Peak Search để tìm đỉnh tín hiệu mạnh nhất
        @retval None
        """
        if not self._ctrl.click_by_text("Peak Search"):
            raise RuntimeError("SpectrumPanel: Không click được 'Peak Search'")
        logger.info("SpectrumPanel: Peak Search OK")
        self._ctrl.wait_for_text("Marker 1", timeout=5)

    def click_next_peak(self) -> None:
        """
        @brief  Click nút Next Peak để chuyển sang đỉnh kế tiếp
        @retval None
        """
        if not self._ctrl.click_by_text("Next Peak"):
            raise RuntimeError("SpectrumPanel: Không click được 'Next Peak'")
        logger.info("SpectrumPanel: Next Peak OK")
        time.sleep(0.2)

    def remove_all_markers(self) -> None:
        """
        @brief  Click nút Remove All Markers để xóa toàn bộ marker
        @retval None
        """
        if not self._ctrl.click_by_text("Remove All Markers"):
            raise RuntimeError("SpectrumPanel: Không click được 'Remove All Markers'")
        logger.info("SpectrumPanel: Remove All Markers OK")
        time.sleep(0.2)

    def extract_markers(self) -> list:
        """
        @brief  Đọc dữ liệu marker từ panel Markers (Position + Value)
        @retval list[dict] — danh sách {"name", "position", "value"}, rỗng nếu không tìm thấy
        """
        if self._ctrl._main_window is None:
            return []
        _FREQ_UNITS = ("GHz", "MHz", "kHz", "Hz")
        texts = []
        for ctrl in self._ctrl._main_window.descendants():
            try:
                t = ctrl.window_text().strip()
                if t:
                    texts.append(t)
            except Exception:
                pass

        is_freq  = lambda t: any(u in t for u in _FREQ_UNITS)
        is_power = lambda t: "dB" in t

        values = [t for t in texts if is_freq(t) or is_power(t)]
        markers = []
        i = 0
        while i < len(values) - 1:
            if is_freq(values[i]) and is_power(values[i + 1]):
                markers.append({
                    "name":     f"Marker {len(markers) + 1}",
                    "position": values[i],
                    "value":    values[i + 1],
                })
                i += 2
            else:
                i += 1

        if markers:
            logger.info(f"SpectrumPanel: extract_markers — {len(markers)} marker(s)")
            for m in markers:
                logger.info(f"  {m['name']:10s} | position = {m['position']:>12s} | value = {m['value']}")
        else:
            logger.warning("SpectrumPanel: extract_markers — không tìm thấy marker nào")
        return markers

    # ── Amplitude (Sweep Settings → Amplitude) ───────────────────────────────

    def open_amplitude(self) -> None:
        """
        @brief  Click mục "Amplitude" trong Sweep Settings
        @retval None
        """
        logger.info("SpectrumPanel: mở Amplitude")
        self.ensure_spectrum_panel_open()
        if not self._ctrl.click_by_text("Amplitude", retries=5):
            raise RuntimeError("SpectrumPanel: Không click được 'Amplitude'")
        self._ctrl.wait_for_text("Ref Level", timeout=5)

    def set_amplitude_params(
        self,
        ref_level: str = "",
        div: str = "",
        gain: str = "",
        atten: str = "",
    ) -> list:
        """
        @brief  Điền các thông số Amplitude rồi click Apply
        @param  ref_level: Ref Level (dBm)
        @param  div:       Div (dB)
        @param  gain:      Gain — giá trị dropdown (ví dụ: "Auto Gain")
        @param  atten:     Atten — giá trị dropdown (ví dụ: "Auto Atten")
        @retval list[str] — danh sách lỗi validation nếu có; rỗng nếu OK
        """
        logger.info(
            f"SpectrumPanel Amplitude: ref_level={ref_level}, div={div}, "
            f"gain={gain}, atten={atten}"
        )
        self._ctrl.build_cache()
        try:
            if ref_level:
                self._ctrl.set_field_by_label("Ref Level", ref_level)
            if div:
                self._ctrl.set_field_by_label("Div", div)
            if gain:
                self._ctrl.select_by_label("Gain", gain)
            if atten:
                self._ctrl.select_by_label("Atten", atten)
        finally:
            self._ctrl.invalidate_cache()
        self._click_apply()
        time.sleep(0.2)
        errs = self.check_validation_errors()
        if errs:
            logger.warning(f"SpectrumPanel Amplitude: validation errors — {errs}")
        else:
            logger.info("SpectrumPanel Amplitude: Apply OK")
        return errs

    # ── Apply ─────────────────────────────────────────────────────────────────

    def _click_apply(self) -> None:
        """
        @brief  Click nút Apply trong Spectrum panel
        @retval None
        """
        if not self._ctrl.click_by_text("Apply"):
            raise RuntimeError("SpectrumPanel: Không click được 'Apply'")

    # ── Private helpers ───────────────────────────────────────────────────────

    def _is_spectrum_nav_expanded(self) -> bool:
        """Kiểm tra SPECTRUM nav item đang expanded (sub-items hiển thị trong cây)."""
        if self._ctrl._main_window is None:
            return False
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip() in ("Analysis Mode", "Sweep Settings", "Zero-span Setting"):
                    return True
            except Exception:
                pass
        return False

    def _click_spectrum_panel(self) -> None:
        """
        @brief  Click vào nút SPECTRUM bên phải nhất (tránh hit popup/menu cùng tên)
        @retval None
        """
        if self._ctrl._main_window is None:
            raise RuntimeError("SpectrumPanel: main window chưa sẵn sàng")
        best = None
        best_left = -1
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip().lower() != "spectrum":
                    continue
                rect = ctrl.element_info.rectangle
                if rect.left > best_left:
                    best_left = rect.left
                    best = ctrl
            except Exception:
                pass
        if best is None:
            raise RuntimeError("SpectrumPanel: Không tìm thấy nút SPECTRUM panel")
        best.click_input()
        logger.info("SpectrumPanel: click SPECTRUM panel (rightmost)")

    def _click_radio_by_text(self, text: str) -> bool:
        """
        @brief  Tìm [Text] label theo text, click lệch phải _RADIO_OFFSET_X px để trúng ô tròn radio
        @param  text: Nội dung label của radio button cần click
        @retval bool — True nếu click được, False nếu không tìm thấy
        """
        if self._ctrl._main_window is None:
            return False
        for _ in range(5):
            for ctrl in self._ctrl._main_window.descendants():
                try:
                    if ctrl.window_text().strip().lower() == text.lower() and ctrl.is_enabled():
                        rect = ctrl.element_info.rectangle
                        x = rect.right + self._RADIO_OFFSET_X
                        y = (rect.top + rect.bottom) // 2
                        logger.info(f"SpectrumPanel: click radio '{text}' tại ({x}, {y})")
                        pyautogui.click(x, y)
                        return True
                except Exception:
                    pass
            time.sleep(0.5)
        logger.warning(f"SpectrumPanel: không tìm thấy radio '{text}'")
        return False
