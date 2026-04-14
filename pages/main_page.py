"""
MainPage — Page Object for the PC17 main window.

HOW TO FIND ELEMENT IDENTIFIERS
--------------------------------
Run this in a Python shell while your app is open:

    from pywinauto import Application
    app = Application(backend="uia").connect(title_re=".*PC17.*")
    app.top_window().print_control_identifiers(depth=5)

This will print all element auto_id, class_name, title values.
Replace the placeholder locators below with the real ones.
"""
from __future__ import annotations

from pages.base_page import BasePage


class MainPage(BasePage):
    """Page Object for the main PC17 application window."""

    # ── Element locators ──────────────────────────────────────────────────────
    # Replace with real auto_id / title / class_name from your app

    # Attenuator section
    BTN_ATTENUATOR_ON   = {"auto_id": "btnAttenuatorOn",   "control_type": "Button"}
    BTN_ATTENUATOR_OFF  = {"auto_id": "btnAttenuatorOff",  "control_type": "Button"}
    LBL_ATTENUATOR_STATUS = {"auto_id": "lblAttenuatorStatus"}

    # Connection section
    CMB_PORT            = {"auto_id": "cmbPort"}
    BTN_CONNECT         = {"auto_id": "btnConnect"}
    BTN_DISCONNECT      = {"auto_id": "btnDisconnect"}
    LBL_CONN_STATUS     = {"auto_id": "lblConnectionStatus"}

    # General
    LBL_APP_STATUS      = {"auto_id": "lblAppStatus"}
    BTN_APPLY           = {"auto_id": "btnApply"}
    BTN_RESET           = {"auto_id": "btnReset"}

    # ── Attenuator actions ────────────────────────────────────────────────────

    def turn_on_attenuator(self) -> None:
        """Click the Attenuator ON button in the UI."""
        self.click(self.BTN_ATTENUATOR_ON)

    def turn_off_attenuator(self) -> None:
        self.click(self.BTN_ATTENUATOR_OFF)

    def get_attenuator_status(self) -> str:
        return self.get_text(self.LBL_ATTENUATOR_STATUS)

    def is_attenuator_on(self) -> bool:
        status = self.get_attenuator_status().lower()
        return "on" in status or "ready" in status or "active" in status

    # ── Connection actions ────────────────────────────────────────────────────

    def select_port(self, port: str) -> None:
        self.select(self.CMB_PORT, port)

    def click_connect(self) -> None:
        self.click(self.BTN_CONNECT)

    def click_disconnect(self) -> None:
        self.click(self.BTN_DISCONNECT)

    def get_connection_status(self) -> str:
        return self.get_text(self.LBL_CONN_STATUS)

    def is_connected(self) -> bool:
        status = self.get_connection_status().lower()
        return "connected" in status

    # ── General actions ───────────────────────────────────────────────────────

    def get_app_status(self) -> str:
        return self.get_text(self.LBL_APP_STATUS)

    def click_apply(self) -> None:
        self.click(self.BTN_APPLY)

    def click_reset(self) -> None:
        self.click(self.BTN_RESET)
