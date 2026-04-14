"""
S2VnaPage — Page Object cho ứng dụng S2VNA simulator.

Chỉ được dùng trong bộ test VNA (tests/vna/).
Fixture s2vna_ctrl và s2vna_page được khai báo trong tests/vna/conftest.py.

HOW TO FIND ELEMENT IDENTIFIERS
---------------------------------
    from pywinauto import Application
    app = Application(backend="uia").connect(title_re=".*S2VNA.*")
    app.top_window().print_control_identifiers(depth=5)
"""
from __future__ import annotations

from pages.base_page import BasePage


class S2VnaPage(BasePage):
    """Page Object cho cửa sổ chính của S2VNA."""

    # ── Element locators ──────────────────────────────────────────────────────
    # Thay bằng auto_id / title / class_name thực tế từ app S2VNA

    # Trạng thái kết nối / instrument
    LBL_STATUS          = {"auto_id": "lblStatus"}
    LBL_CONN_STATUS     = {"auto_id": "lblConnectionStatus"}
    BTN_CONNECT         = {"auto_id": "btnConnect"}
    BTN_DISCONNECT      = {"auto_id": "btnDisconnect"}

    # Điều khiển nguồn / sweep
    BTN_POWER_ON        = {"auto_id": "btnPowerOn",  "control_type": "Button"}
    BTN_POWER_OFF       = {"auto_id": "btnPowerOff", "control_type": "Button"}
    LBL_POWER_STATUS    = {"auto_id": "lblPowerStatus"}

    # Sweep / measurement
    BTN_SWEEP           = {"auto_id": "btnSweep"}
    LBL_FREQ_START      = {"auto_id": "lblFreqStart"}
    LBL_FREQ_STOP       = {"auto_id": "lblFreqStop"}
    TXT_FREQ_START      = {"auto_id": "txtFreqStart"}
    TXT_FREQ_STOP       = {"auto_id": "txtFreqStop"}
    BTN_APPLY           = {"auto_id": "btnApply"}

    # ── Connection actions ────────────────────────────────────────────────────

    def click_connect(self) -> None:
        self.click(self.BTN_CONNECT)

    def click_disconnect(self) -> None:
        self.click(self.BTN_DISCONNECT)

    def get_connection_status(self) -> str:
        return self.get_text(self.LBL_CONN_STATUS)

    def is_connected(self) -> bool:
        return "connected" in self.get_connection_status().lower()

    # ── Power actions ─────────────────────────────────────────────────────────

    def power_on(self) -> None:
        self.click(self.BTN_POWER_ON)

    def power_off(self) -> None:
        self.click(self.BTN_POWER_OFF)

    def get_power_status(self) -> str:
        return self.get_text(self.LBL_POWER_STATUS)

    def is_powered_on(self) -> bool:
        status = self.get_power_status().lower()
        return "on" in status or "ready" in status

    # ── Sweep / measurement actions ───────────────────────────────────────────

    def set_freq_start(self, freq: str) -> None:
        """freq ví dụ: '1000000' (Hz) hoặc '1e6'"""
        self.set_value(self.TXT_FREQ_START, freq)

    def set_freq_stop(self, freq: str) -> None:
        self.set_value(self.TXT_FREQ_STOP, freq)

    def click_sweep(self) -> None:
        self.click(self.BTN_SWEEP)

    def click_apply(self) -> None:
        self.click(self.BTN_APPLY)

    # ── General ───────────────────────────────────────────────────────────────

    def get_status(self) -> str:
        return self.get_text(self.LBL_STATUS)

    def is_ready(self) -> bool:
        return "ready" in self.get_status().lower()
