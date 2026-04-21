"""
SpikePage — Page Object cho Spike.exe (Signal Hound Spectrum Analyzer).

Wrap toàn bộ các action điều khiển Spike qua pywinauto UIA backend.
Pattern: scan descendants() theo text thay vì auto_id (Spike không expose stable auto_id).
"""
from __future__ import annotations

from typing import Optional

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SpikePage(BasePage):
    """Page Object cho cửa sổ Spike.exe của Signal Hound."""

    # ── Popup / startup ───────────────────────────────────────────────────────

    def handle_popup(self, keyword: str = "No Device") -> bool:
        """
        @brief  Dismiss popup khởi động của Spike (ví dụ: 'No Device') bằng phím ENTER
        @param  keyword: Chuỗi cần tìm trong title hoặc descendants để nhận diện popup (default: "No Device")
        @retval bool — True nếu tìm thấy và dismiss thành công, False nếu không có popup
        """
        win = self._ctrl._main_window
        if win is None:
            return False
        try:
            if keyword.lower() in win.window_text().lower():
                win.type_keys("{ENTER}")
                logger.info(f"handle_popup: dismissed via title match ({keyword!r})")
                return True
        except Exception:
            pass
        for ctrl in win.descendants():
            try:
                if keyword.lower() in ctrl.window_text().lower():
                    win.type_keys("{ENTER}")
                    logger.info(f"handle_popup: dismissed via descendant match ({keyword!r})")
                    return True
            except Exception:
                pass
        return False

    # ── Cache management ──────────────────────────────────────────────────────

    def refresh_cache(self) -> None:
        """
        @brief  Scan lại toàn bộ UI của Spike và cập nhật internal cache
        @retval None
        """
        self._ctrl.build_cache()

    # ── Scroll ────────────────────────────────────────────────────────────────

    def scroll_to(self, keyword: str, max_scroll: int = 20) -> bool:
        """
        @brief  Scroll cửa sổ Spike cho đến khi tìm thấy element có text chứa keyword
        @param  keyword: Chuỗi cần tìm (không phân biệt hoa/thường)
        @param  max_scroll: Số lần scroll tối đa (default: 20)
        @retval bool — True nếu tìm thấy, False nếu không
        """
        return self._ctrl.scroll_to_text(keyword, max_scroll=max_scroll)

    # ── Top-level controls ────────────────────────────────────────────────────

    def preset(self) -> None:
        """
        @brief  Click nút Preset để reset Spike về trạng thái mặc định rồi xóa cache
        @retval None
        """
        self._ctrl.click_button_by_text("Preset")
        self._ctrl.invalidate_cache()
        logger.info("preset: OK")

    def auto_scale(self) -> None:
        """
        @brief  Click nút Auto Scale để Spike tự chỉnh biên độ hiển thị
        @retval None
        """
        self._ctrl.click_button_by_text("Auto")
        logger.info("auto_scale: OK")

    # ── Frequency ─────────────────────────────────────────────────────────────

    def set_frequency(
        self,
        center: Optional[str] = None,
        span: Optional[str] = None,
        start: Optional[str] = None,
        stop: Optional[str] = None,
    ) -> None:
        """
        @brief  Set các tham số tần số trong panel Frequency của Spike
        @param  center: Tần số trung tâm (ví dụ: "1 GHz"), None để bỏ qua
        @param  span:   Dải tần (ví dụ: "2 GHz"), None để bỏ qua
        @param  start:  Tần số bắt đầu (ví dụ: "100 MHz"), None để bỏ qua
        @param  stop:   Tần số kết thúc (ví dụ: "6 GHz"), None để bỏ qua
        @retval None
        """
        logger.info(f"set_frequency: center={center} span={span} start={start} stop={stop}")
        if center:
            self._ctrl.set_field_by_label("Center", center)
        if span:
            self._ctrl.set_field_by_label("Span", span)
        if start:
            self._ctrl.set_field_by_label("Start", start)
        if stop:
            self._ctrl.set_field_by_label("Stop", stop)

    # ── Amplitude ─────────────────────────────────────────────────────────────

    def set_amplitude(
        self,
        ref_level: Optional[str] = None,
        div: Optional[str] = None,
    ) -> None:
        """
        @brief  Set các tham số biên độ trong panel Amplitude của Spike
        @param  ref_level: Mức tham chiếu dBm (ví dụ: "-20"), None để bỏ qua
        @param  div:       Giá trị div/division (ví dụ: "10"), None để bỏ qua
        @retval None
        """
        logger.info(f"set_amplitude: ref_level={ref_level} div={div}")
        if ref_level:
            self._ctrl.set_field_by_label("Ref Level", ref_level)
        if div:
            self._ctrl.set_field_by_label("Div", div)

    # ── Bandwidth ─────────────────────────────────────────────────────────────

    def set_bandwidth(
        self,
        rbw_shape: Optional[str] = None,
        rbw: Optional[str] = None,
        vbw: Optional[str] = None,
        auto_rbw: Optional[bool] = None,
        auto_vbw: Optional[bool] = None,
    ) -> None:
        """
        @brief  Set các tham số Bandwidth trong panel BW của Spike
        @param  rbw_shape: Dạng filter RBW (ví dụ: "Nutall"), None để bỏ qua
        @param  rbw:       Resolution Bandwidth (ví dụ: "300 kHz"), None để bỏ qua
        @param  vbw:       Video Bandwidth (ví dụ: "300 kHz"), None để bỏ qua
        @param  auto_rbw:  True/False để set checkbox Auto RBW, None để bỏ qua
        @param  auto_vbw:  True/False để set checkbox Auto VBW, None để bỏ qua
        @retval None
        """
        logger.info(f"set_bandwidth: rbw_shape={rbw_shape} rbw={rbw} vbw={vbw} auto_rbw={auto_rbw} auto_vbw={auto_vbw}")
        if rbw_shape:
            self._ctrl.select_by_label("RBW Shape", rbw_shape)
        if rbw:
            self._ctrl.set_field_by_label("RBW", rbw)
        if vbw:
            self._ctrl.set_field_by_label("VBW", vbw)
        if auto_rbw is not None:
            self._ctrl.set_checkbox_by_label("Auto RBW", auto_rbw)
        if auto_vbw is not None:
            self._ctrl.set_checkbox_by_label("Auto VBW", auto_vbw)

    # ── Acquisition ───────────────────────────────────────────────────────────

    def set_acquisition(
        self,
        video_units: Optional[str] = None,
        detector: Optional[str] = None,
        swp_time: Optional[str] = None,
        swp_interval: Optional[str] = None,
    ) -> None:
        """
        @brief  Set các tham số Acquisition trong panel Acquisition của Spike
        @param  video_units:  Đơn vị video (ví dụ: "Log"), None để bỏ qua
        @param  detector:     Loại detector (ví dụ: "Max"), None để bỏ qua
        @param  swp_time:     Thời gian sweep (ví dụ: "2 ms"), None để bỏ qua
        @param  swp_interval: Khoảng cách giữa các sweep (ví dụ: "3 s"), None để bỏ qua
        @retval None
        """
        logger.info(f"set_acquisition: video_units={video_units} detector={detector} swp_time={swp_time} swp_interval={swp_interval}")
        if video_units:
            self._ctrl.select_by_label("Video Units", video_units)
        if detector:
            self._ctrl.select_by_label("Detector", detector)
        if swp_time:
            self._ctrl.set_field_by_label("Swp Time", swp_time)
        if swp_interval:
            self._ctrl.set_field_by_label("Swp Interval", swp_interval)

    # ── Trace ─────────────────────────────────────────────────────────────────

    def config_trace(
        self,
        trace: str,
        trace_type: str,
        avg: str,
        update: bool,
        hide: bool,
    ) -> None:
        """
        @brief  Cấu hình Trace trong panel Trace của Spike
        @param  trace:      Tên trace cần chọn (ví dụ: "One")
        @param  trace_type: Loại trace (ví dụ: "Clear & Write", "Average")
        @param  avg:        Số lần average (ví dụ: "10")
        @param  update:     True để bật checkbox Update, False để tắt
        @param  hide:       True để ẩn trace, False để hiện
        @retval None
        """
        logger.info(f"config_trace: trace={trace} type={trace_type} avg={avg}")
        self._ctrl.select_by_label("Trace", trace)
        self._ctrl.select_by_label("Type", trace_type)
        if not self._ctrl.set_field_by_label("Avg", avg):
            self._ctrl.set_field_by_label("Average", avg)
        self._ctrl.set_checkbox_by_label("Update", update)
        self._ctrl.set_checkbox_by_label("Hide", hide)

    # ── Marker ────────────────────────────────────────────────────────────────

    def config_marker(
        self,
        marker: str,
        mtype: str,
        place_on: str,
        freq: str,
        active: bool,
        peak_tracking: bool,
        threshold: str,
        excursion: str,
        do_peak_search: bool,
    ) -> None:
        """
        @brief  Cấu hình Marker trong panel Marker của Spike
        @param  marker:        Tên marker cần chọn (ví dụ: "One")
        @param  mtype:         Loại marker (ví dụ: "Normal", "Delta")
        @param  place_on:      Trace đặt marker lên (ví dụ: "Trace One")
        @param  freq:          Tần số đặt marker (ví dụ: "1 GHz")
        @param  active:        True để bật marker, False để tắt
        @param  peak_tracking: True để bật Pk Tracking, False để tắt
        @param  threshold:     Ngưỡng peak search dBm (ví dụ: "-100")
        @param  excursion:     Excursion dB (ví dụ: "6")
        @param  do_peak_search: True để click Peak Search sau khi config
        @retval None
        """
        logger.info(f"config_marker: marker={marker} type={mtype} freq={freq}")
        self._ctrl.select_by_label("Marker", marker)
        self._ctrl.select_by_label("Marker Type", mtype)
        self._ctrl.select_by_label("Place On", place_on)
        self._ctrl.set_field_by_label("Set Freq", freq)
        self._ctrl.set_checkbox_by_label("Active", active)
        self._ctrl.set_checkbox_by_label("Pk Tracking", peak_tracking)
        self._ctrl.set_field_by_label("Pk Threshold", threshold)
        self._ctrl.set_field_by_label("Pk Excurs.", excursion)
        if do_peak_search:
            self._ctrl.click_button_by_text("Peak Search")

    # ── OBW ───────────────────────────────────────────────────────────────────

    def config_obw(
        self,
        enable: bool,
        target: Optional[str] = None,
        percent: Optional[str] = None,
        move_to_center: bool = False,
    ) -> None:
        """
        @brief  Cấu hình Occupied Bandwidth (OBW) trong panel OBW của Spike
        @param  enable:         True để bật OBW, False để tắt
        @param  target:         Trace dùng làm nguồn tính OBW (ví dụ: "Trace One"), None để bỏ qua
        @param  percent:        Phần trăm công suất OBW (ví dụ: "99"), None để bỏ qua
        @param  move_to_center: True để click nút To Center sau khi config
        @retval None
        """
        logger.info(f"config_obw: enable={enable} target={target} percent={percent}")
        self._ctrl.set_checkbox_by_label("Enabled", enable)
        if enable:
            if target:
                self._ctrl.select_by_label("Target", target)
            if percent:
                self._ctrl.set_field_by_label("% Power", percent)
            if move_to_center:
                self._ctrl.click_button_by_text("To Center")

    # ── Trace Math ────────────────────────────────────────────────────────────

    def config_trace_math(
        self,
        enable: bool = False,
        op1: Optional[str] = None,
        op2: Optional[str] = None,
        result: Optional[str] = None,
        operation: Optional[str] = None,
        offset: Optional[str] = None,
    ) -> None:
        """
        @brief  Cấu hình Trace Math trong panel Trace Math của Spike
        @param  enable:    True để bật Trace Math, False để tắt
        @param  op1:       Trace nguồn thứ nhất (ví dụ: "Trace 3"), None để bỏ qua
        @param  op2:       Trace nguồn thứ hai (ví dụ: "Trace 3"), None để bỏ qua
        @param  result:    Trace lưu kết quả (ví dụ: "Trace 6"), None để bỏ qua
        @param  operation: Phép toán (ví dụ: "Power Diff", "Log Diff", "Log Offset"), None để bỏ qua
        @param  offset:    Giá trị offset dB — chỉ áp dụng khi operation là "Log Diff" hoặc "Log Offset"
        @retval None
        """
        logger.info(f"config_trace_math: enable={enable} op1={op1} op2={op2} op={operation}")
        self._ctrl.set_checkbox_by_label("Enabled", enable)
        if op1:
            self._ctrl.select_by_label("Op 1", op1)
        if op2:
            self._ctrl.select_by_label("Op 2", op2)
        if result:
            self._ctrl.select_by_label("Result", result)
        if operation:
            self._ctrl.select_by_label("Operation", operation)
        if operation in ("Log Diff", "Log Offset") and offset:
            self._ctrl.set_field_by_label("Offset", offset)
            logger.info(f"config_trace_math: Offset = {offset}")

    # ── Display Line ──────────────────────────────────────────────────────────

    def config_display_line(
        self,
        enable: bool = False,
        level: Optional[str] = None,
    ) -> None:
        """
        @brief  Cấu hình Display Line trong panel Display Line của Spike
        @param  enable: True để bật Display Line, False để tắt
        @param  level:  Mức hiển thị dBm (ví dụ: "-40 dBm"), None để bỏ qua
        @retval None
        """
        logger.info(f"config_display_line: enable={enable} level={level}")
        self._ctrl.set_checkbox_by_label("Enabled", enable)
        if level:
            self._ctrl.set_field_by_label("Level", level)
