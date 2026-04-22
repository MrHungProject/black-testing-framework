"""VnaPanel — toàn bộ tương tác với VNA panel trong FormMainEliteRF."""
from __future__ import annotations

import time

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class VnaPanel(BasePage):
    """Measurement, Stimulus, Markers."""

    _TAB_KEYWORDS = ("Stimulus", "Measurement", "Markers")

    # ── VNA open ──────────────────────────────────────────────────────────────

    def ensure_vna_open(self) -> None:
        """
        @brief  Đảm bảo VNA panel đang mở (có ít nhất 1 trong các tab Stimulus/Measurement/Markers)
        @retval None
        """
        if self._ctrl._main_window is None:
            return
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if ctrl.window_text().strip() in self._TAB_KEYWORDS:
                    return
            except Exception:
                pass
        try:
            vna_panel = self._ctrl._main_window.child_window(
                auto_id="CardCollapeVNA", control_type="Pane"
            )
            vna_panel.wait("exists ready", timeout=10)
            vna_panel.click_input()
            time.sleep(1)
        except Exception:
            pass

    # ── Measurement tab ───────────────────────────────────────────────────────

    def open_measurement(self) -> None:
        """
        @brief  Click tab Measurement trong VNA panel
        @retval None
        """
        logger.info("VNA: mở tab Measurement")
        self.ensure_vna_open()
        if not self._ctrl.click_by_text("Measurement", retries=10):
            raise RuntimeError("VNA: Không click được 'Measurement'")
        time.sleep(2)

    def select_s_parameter(self, name: str) -> None:
        """
        @brief  Chọn S-parameter trong Measurement panel
        @param  name: Tên S-parameter cần chọn (ví dụ: 'S11', 'S21')
        @retval None
        """
        if not self._ctrl.click_by_text(name):
            raise RuntimeError(f"VNA: Không chọn được S-parameter '{name}'")
        logger.info(f"VNA: S-parameter '{name}' đã chọn")

    def click_apply(self) -> None:
        """
        @brief  Click nút Apply để xác nhận thay đổi cấu hình
        @retval None
        """
        if not self._ctrl.click_by_text("Apply"):
            raise RuntimeError("VNA: Không click được 'Apply'")
        logger.info("VNA: Apply OK")

    # ── Stimulus tab ──────────────────────────────────────────────────────────

    def open_stimulus(self) -> None:
        """
        @brief  Click tab Stimulus trong VNA panel
        @retval None
        """
        logger.info("VNA: mở tab Stimulus")
        self.ensure_vna_open()
        if not self._ctrl.click_by_text("Stimulus", retries=5):
            raise RuntimeError("VNA: Không click được 'Stimulus'")
        time.sleep(2)

    def set_stimulus_params(
        self,
        start: str = "2GHz",
        stop: str = "6GHz",
        center: str = "9.05GHz",
        span: str = "3GHz",
        points: str = "301",
        if_bw: str = "10kHz",
        power: str = "0",
    ) -> None:
        """
        @brief  Điền toàn bộ thông số Stimulus rồi click Apply
        @param  start: Start Frequency (default: "2GHz")
        @param  stop: Stop Frequency (default: "6GHz")
        @param  center: Center Frequency (default: "9.05GHz")
        @param  span: Span Frequency (default: "3GHz")
        @param  points: Number of Points (default: "301")
        @param  if_bw: IF Bandwidth (default: "10kHz")
        @param  power: Power dBm (default: "0")
        @retval None
        """
        logger.info(
            f"VNA Stimulus: start={start}, stop={stop}, center={center}, "
            f"span={span}, points={points}, IF_BW={if_bw}, power={power}"
        )
        self._ctrl.set_field_by_label("Start Frequency", start)
        self._ctrl.set_field_by_label("Stop Frequency", stop)
        self._ctrl.set_field_by_label("Center Frequency", center)
        self._ctrl.set_field_by_label("Span Frequency", span)
        self._ctrl.set_field_by_label("Number of Points", points)
        self._ctrl.set_field_by_label("IF Bandwidth", if_bw)
        self._ctrl.set_field_by_label("Power", power)
        self.click_apply()
        logger.info("VNA Stimulus: tất cả thông số đã được set và Apply")

    # ── Markers tab ───────────────────────────────────────────────────────────

    def open_markers(self) -> None:
        """
        @brief  Click tab Markers trong VNA panel
        @retval None
        """
        logger.info("VNA: mở tab Markers")
        self.ensure_vna_open()
        if not self._ctrl.click_by_text("Markers", retries=5):
            raise RuntimeError("VNA: Không click được 'Markers'")
        time.sleep(1)

    def click_add_marker(self) -> None:
        """
        @brief  Click nút 'Add Marker' (thử Button-type trước, fallback text scan)
        @retval None
        """
        if not self._ctrl.click_button_by_text("Add Marker"):
            if not self._ctrl.click_by_text("Add Marker"):
                raise RuntimeError("VNA: Không click được 'Add Marker'")
        logger.info("VNA: Add Marker OK")

    def open_trace_dropdown(self) -> None:
        """
        @brief  Click 'Trace 1' để mở dropdown chọn trace cho marker
        @retval None
        """
        if not self._ctrl.click_by_text("Trace 1", retries=5):
            raise RuntimeError("VNA: Không mở được Trace dropdown")
        time.sleep(1)

    def select_trace(self, value: str = "Trace 2") -> None:
        """
        @brief  Chọn trace từ popup xuất hiện ở Desktop level
        @param  value: Tên trace cần chọn (default: "Trace 2")
        @retval None
        """
        if not self._ctrl.select_from_desktop_popup(value):
            raise RuntimeError(f"VNA: Không chọn được trace '{value}'")
        logger.info(f"VNA: Trace '{value}' đã chọn")

    def setup_marker(self) -> None:
        """
        @brief  Tạo 2 marker: Marker 1 trên Trace 1 (mặc định), Marker 2 trên Trace 2
        @retval None
        """
        logger.info("VNA: setup marker — Marker1 (Trace1) + Marker2 (Trace2)")
        self.open_markers()
        time.sleep(0.5)
        self.click_add_marker()
        logger.info("VNA: Marker 1 thêm vào Trace 1")
        time.sleep(0.5)
        self.open_trace_dropdown()
        self.select_trace("Trace 2")
        self.click_add_marker()
        logger.info("VNA: Marker 2 thêm vào Trace 2")

    def extract_markers(self) -> list:
        """
        @brief  Đọc dữ liệu marker từ panel 'Active Markers' (vị trí GHz + giá trị dB)
        @retval list[dict] — danh sách {"name", "position", "value"}, rỗng nếu không tìm thấy
        """
        if self._ctrl._main_window is None:
            return []
        panel = None
        for ctrl in self._ctrl._main_window.descendants():
            try:
                if "Active Markers" in ctrl.window_text():
                    panel = ctrl.parent()
                    break
            except Exception:
                pass
        if not panel:
            raise RuntimeError("VNA: Không tìm thấy panel 'Active Markers'")

        texts = []
        for ctrl in panel.descendants():
            try:
                t = ctrl.window_text().strip()
                if t:
                    texts.append(t)
            except Exception:
                pass

        values = [t for t in texts if "GHz" in t or "dB" in t]
        markers = []
        i = 0
        while i < len(values) - 1:
            if "GHz" in values[i] and "dB" in values[i + 1]:
                markers.append({
                    "name": f"Marker {len(markers) + 1}",
                    "position": values[i],
                    "value": values[i + 1],
                })
                i += 2
            else:
                i += 1

        if markers:
            logger.info(f"VNA: extract_markers — tìm thấy {len(markers)} marker(s)")
            for m in markers:
                logger.info(
                    f"  {m['name']:10s} | position = {m['position']:>12s} | value = {m['value']}"
                )
        else:
            logger.warning("VNA: extract_markers — không tìm thấy marker nào trong 'Active Markers' panel")

        return markers
