"""
SystemPanel — kết nối / ngắt kết nối PC17 (FormMainEliteRF).

Luồng setup (gọi một lần qua setup_connection()):
    1. PC17.exe đã được start → top_window là cửa sổ khởi động ban đầu
    2. Tools → RF Test Set  (keyboard nav: DOWN×3 + ENTER)
    3. Đợi cửa sổ FormMainEliteRF xuất hiện
    4. Click System → Connect → Connection
    5. Đợi trạng thái "Connected"
"""
from __future__ import annotations

import time

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SystemPanel(BasePage):
    """Quản lý kết nối: setup, reconnect, disconnect."""

    MAIN_WINDOW_TITLE_RE = ".*FormMainEliteRF.*"
    NAV_WAIT        = 6   # giây chờ sau khi mở RF Test Set
    CONNECT_TIMEOUT = 30  # giây chờ trạng thái Connected

    def setup_connection(self) -> None:
        """
        @brief  Mở RF Test Set → điều hướng đến System → Connect panel.
                Không tự động connect thiết bị nào — mỗi test suite tự connect
                thiết bị cần thiết qua _ensure_connected fixture.
        @retval None
        """
        self._open_rf_test_set()
        self.open_connect_panel()

    def _open_rf_test_set(self) -> None:
        """
        @brief  Điều hướng qua menu Tools → RF Test Set rồi switch sang cửa sổ FormMainEliteRF
        @retval None
        """
        try:
            self._ctrl._main_window.set_focus()
            self._ctrl._main_window.bring_to_top()
        except Exception:
            pass
        time.sleep(1)

        try:
            self._ctrl._main_window.child_window(
                title="Tools", control_type="MenuItem"
            ).click_input()
        except Exception:
            self._ctrl.click_by_text("Tools")
        time.sleep(1)

        try:
            self._ctrl._main_window.set_focus()
        except Exception:
            pass

        # WinForms menu không expose submenu qua UIA → keyboard fallback
        self._ctrl.type_keys_on_window("{DOWN}{DOWN}{DOWN}{ENTER}")
        time.sleep(self.NAV_WAIT)
        self._ctrl.switch_window(self.MAIN_WINDOW_TITLE_RE, timeout=40)
        time.sleep(2)

    def connect_device(self, device_label: str) -> bool:
        """
        @brief  Click nút Connection của thiết bị chỉ định trong panel System - Connect
        @param  device_label: Tên thiết bị ("VNA Device", "Attenuator Device", "SPECTRUM", "Signal Genarator")
        @retval bool — True nếu click được, False nếu không tìm thấy
        """
        if self._ctrl._main_window is None:
            return False
        controls = list(self._ctrl._main_window.descendants())
        for i, c in enumerate(controls):
            try:
                if c.window_text().strip().lower() == device_label.lower():
                    for j in range(i + 1, min(i + 20, len(controls))):
                        try:
                            t = controls[j].window_text().strip().lower()
                            if t == "connection" and controls[j].is_enabled():
                                logger.info(f"SystemPanel: connect '{device_label}'")
                                controls[j].click_input()
                                return True
                        except Exception:
                            pass
            except Exception:
                pass
        logger.warning(f"SystemPanel: không tìm thấy Connection button cho '{device_label}'")
        return False

    def disconnect_device(self, device_label: str) -> bool:
        """
        @brief  Click nút Disconnect của thiết bị chỉ định trong panel System - Connect
        @param  device_label: Tên thiết bị cần ngắt kết nối
        @retval bool — True nếu click được, False nếu không tìm thấy
        """
        if self._ctrl._main_window is None:
            return False
        controls = list(self._ctrl._main_window.descendants())
        for i, c in enumerate(controls):
            try:
                if c.window_text().strip().lower() == device_label.lower():
                    for j in range(i + 1, min(i + 20, len(controls))):
                        try:
                            t = controls[j].window_text().strip().lower()
                            if t == "disconnect" and controls[j].is_enabled():
                                logger.info(f"SystemPanel: disconnect '{device_label}'")
                                controls[j].click_input()
                                return True
                        except Exception:
                            pass
            except Exception:
                pass
        logger.warning(f"SystemPanel: không tìm thấy Disconnect button cho '{device_label}'")
        return False

    def is_device_connected(self, device_label: str) -> bool:
        """
        @brief  Kiểm tra thiết bị chỉ định có trạng thái Connected không
        @param  device_label: Tên thiết bị cần kiểm tra
        @retval bool — True nếu Connected, False nếu không
        """
        if self._ctrl._main_window is None:
            return False
        controls = list(self._ctrl._main_window.descendants())
        for i, c in enumerate(controls):
            try:
                if c.window_text().strip().lower() == device_label.lower():
                    for j in range(i + 1, min(i + 10, len(controls))):
                        try:
                            t = controls[j].window_text().strip().lower()
                            if "connected" in t and "disconnect" not in t:
                                return True
                        except Exception:
                            pass
            except Exception:
                pass
        return False

    def is_connected(self) -> bool:
        """
        @brief  Kiểm tra trạng thái kết nối bằng cách tìm control có text "Connected"
        @retval bool — True nếu control "Connected" tồn tại và enabled, False nếu không
        """
        return self._ctrl.has_element_with_text("Connected")

    def click_disconnect(self) -> None:
        """
        @brief  Click button "Disconnect" để ngắt kết nối thiết bị
        @retval None
        """
        self._ctrl.click_by_text("Disconnect")

    def open_connect_panel(self) -> None:
        """
        @brief  Mở System card → panel Connect (nếu chưa mở)
        @retval None
        """
        if not self._ctrl.has_element_with_text("Connect"):
            logger.info("SystemPanel: mở System card …")
            try:
                self._ctrl._main_window.child_window(
                    auto_id="CardSystem", control_type="Pane"
                ).click_input()
            except Exception:
                self._ctrl.click_by_text("System")
            self._ctrl.wait_for_text("Connect", timeout=5)

        ok = self._ctrl.click_by_text("Connect", retries=5)
        if not ok:
            raise RuntimeError("PC17: Không click được 'Connect'")
        time.sleep(0.5)
        logger.info("SystemPanel: Connect panel đã mở")

    def reconnect(self) -> None:
        """
        @brief  Kết nối lại theo flow: mở System card nếu chưa mở → Connect → Connection → Connected
        @retval None
        """
        logger.info("Reconnect: kiểm tra System card …")

        self.open_connect_panel()

        if self._ctrl.has_element_with_text("Disconnect"):
            logger.info("Reconnect: đang Connected → Disconnect rồi reconnect …")
            self._ctrl.click_by_text("Disconnect")
            time.sleep(2)

        ok = self._ctrl.click_by_text("Connection", retries=5)
        if not ok:
            raise RuntimeError("PC17: Không click được 'Connection' khi reconnect")

        if not self._ctrl.wait_for_text("Connected", timeout=self.CONNECT_TIMEOUT):
            raise RuntimeError("PC17: Device không đạt 'Connected' sau reconnect")
        logger.info("Reconnect: Connected OK")
