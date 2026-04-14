"""
MainPage — Page Object cho cửa sổ FormMainEliteRF của PC17.

Luồng setup (gọi một lần qua setup_connection()):
    1. PC17.exe đã được start → top_window là cửa sổ khởi động ban đầu
    2. Tools → RF Test Set  (keyboard nav: DOWN×3 + ENTER)
    3. Đợi cửa sổ FormMainEliteRF xuất hiện
    4. Click System → Connect → Connection
    5. Đợi trạng thái "Connected"

Tìm element bằng scan descendants() theo window_text() vì app dùng WinForms
và auto_id không ổn định.
"""
from __future__ import annotations

import time

from pages.base_page import BasePage


class MainPage(BasePage):
    """Page Object cho FormMainEliteRF — cửa sổ chính của PC17."""

    MAIN_WINDOW_TITLE_RE = ".*FormMainEliteRF.*"
    NAV_WAIT        = 3   # giây chờ sau khi mở RF Test Set
    CONNECT_TIMEOUT = 15  # giây chờ trạng thái Connected

    # ── Setup flow (gọi 1 lần trong fixture) ─────────────────────────────────

    def setup_connection(self) -> None:
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
        """Tools → RF Test Set → switch sang cửa sổ FormMainEliteRF."""
        try:
            self._ctrl._main_window.child_window(
                title="Tools", control_type="MenuItem"
            ).click_input()
        except Exception:
            self._ctrl.click_by_text("Tools")
        time.sleep(1)
        # WinForms menu không expose submenu qua UIA → keyboard fallback
        self._ctrl.type_keys_on_window("{DOWN}{DOWN}{DOWN}{ENTER}")
        time.sleep(self.NAV_WAIT)
        self._ctrl.switch_window(self.MAIN_WINDOW_TITLE_RE, timeout=20)
        time.sleep(2)  # đợi FormMainEliteRF ổn định trước khi click System

    # ── Trạng thái kết nối ────────────────────────────────────────────────────

    def is_connected(self) -> bool:
        return self._ctrl.has_element_with_text("Connected")

    def click_disconnect(self) -> None:
        self._ctrl.click_by_text("Disconnect")
