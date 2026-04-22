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
        @brief  Thực hiện toàn bộ flow setup kết nối: mở RF Test Set → click System → Connect → Connection → đợi "Connected"
        @retval None
        """
        self._open_rf_test_set()
        if not self._ctrl.click_by_text("System"):
            try:
                self._ctrl._main_window.child_window(
                    auto_id="CardSystem", control_type="Pane"
                ).click_input()
            except Exception:
                raise RuntimeError("PC17: Không click được 'System'")
        time.sleep(1)
        self._ctrl.click_by_text("Connect")
        time.sleep(2)
        ok = self._ctrl.click_by_text("Connection", retries=5)
        if not ok:
            raise RuntimeError("PC17: Không click được 'Connection'")
        if not self._ctrl.wait_for_text("Connected", timeout=self.CONNECT_TIMEOUT):
            raise RuntimeError("PC17: Device did not reach 'Connected' state")

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

    def reconnect(self) -> None:
        """
        @brief  Kết nối lại theo flow: mở System card nếu chưa mở → Connect → Connection → Connected
        @retval None
        """
        logger.info("Reconnect: kiểm tra System card …")

        if not self._ctrl.has_element_with_text("Connect"):
            logger.info("Reconnect: System card đang đóng → mở card …")
            try:
                self._ctrl._main_window.child_window(
                    auto_id="CardSystem", control_type="Pane"
                ).click_input()
            except Exception:
                self._ctrl.click_by_text("System")
            time.sleep(2)

        logger.info("Reconnect: click Connect để mở panel …")
        ok = self._ctrl.click_by_text("Connect", retries=5)
        if not ok:
            raise RuntimeError("PC17: Không click được 'Connect' khi reconnect")
        time.sleep(2)

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
