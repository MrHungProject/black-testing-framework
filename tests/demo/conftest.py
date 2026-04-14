"""
Demo conftest — cung cấp mock fixtures để chạy không cần hardware thật.
Chỉ dùng cho demo/dev. Khi test thật, dùng root conftest.py.
"""
from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch


# ── Mock AppController ────────────────────────────────────────────────────────

class MockAppController:
    """Giả lập pywinauto AppController."""

    def __init__(self):
        self._state: dict = {
            "attenuator": "OFF",
            "connection": "Disconnected",
        }

    def click(self, identifier):
        # Giả lập click button
        if "On" in str(identifier) or "on" in str(identifier):
            self._state["attenuator"] = "ON"
        elif "Off" in str(identifier) or "off" in str(identifier):
            self._state["attenuator"] = "OFF"
        elif "Connect" in str(identifier):
            self._state["connection"] = "Connected"

    def get_text(self, identifier) -> str:
        if "Attenuator" in str(identifier) or "Status" in str(identifier):
            return self._state["attenuator"]
        if "Conn" in str(identifier):
            return self._state["connection"]
        return "OK"

    def double_click(self, identifier): pass
    def type_text(self, identifier, text): pass
    def set_value(self, identifier, value): pass
    def wait_for_element(self, identifier, timeout=10): return True
    def is_element_enabled(self, identifier): return True
    def select_combobox(self, identifier, item): pass
    def check_checkbox(self, identifier, state=True): pass
    def take_screenshot(self, filename): return None
    def connect(self): return self
    def disconnect(self): pass


# ── Mock SerialDevice ─────────────────────────────────────────────────────────

class MockSerialDevice:
    """Giả lập USB Serial device."""

    def __init__(self):
        self._voltage = 0.0
        self._powered = False

    def open(self): return self
    def close(self): pass
    def is_open(self): return True
    def send(self, data, **kw): return len(data)
    def flush(self): pass

    def read_voltage(self, command="VOLT?\r\n") -> float:
        # Trả về voltage theo trạng thái
        return 3.3 if self._powered else 0.0

    def query(self, command, delay=0.1) -> str:
        return "OK"

    def readline(self) -> str:
        return "OK"

    def is_connected(self, **kw) -> bool:
        return True

    def wait_for_response(self, expected, **kw) -> bool:
        return True

    # Helper cho demo
    def set_powered(self, state: bool):
        self._powered = state

    def __enter__(self): return self.open()
    def __exit__(self, *_): self.close()


# ── Mock MainPage ─────────────────────────────────────────────────────────────

class MockMainPage:
    def __init__(self, ctrl: MockAppController, device: MockSerialDevice):
        self._ctrl   = ctrl
        self._device = device

    def turn_on_attenuator(self):
        self._ctrl.click({"auto_id": "btnAttenuatorOn"})
        self._device.set_powered(True)       # phản ánh trạng thái hardware

    def turn_off_attenuator(self):
        self._ctrl.click({"auto_id": "btnAttenuatorOff"})
        self._device.set_powered(False)

    def get_attenuator_status(self) -> str:
        return self._ctrl.get_text({"auto_id": "lblAttenuatorStatus"})

    def is_attenuator_on(self) -> bool:
        return self.get_attenuator_status().upper() == "ON"

    def click_connect(self):
        self._ctrl.click({"auto_id": "btnConnect"})

    def get_connection_status(self) -> str:
        return self._ctrl.get_text({"auto_id": "lblConnectionStatus"})

    def is_connected(self) -> bool:
        return "connected" in self.get_connection_status().lower()


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def app_ctrl():
    yield MockAppController()


@pytest.fixture(scope="session")
def device():
    yield MockSerialDevice()


@pytest.fixture(scope="session")
def main_page(app_ctrl, device):
    yield MockMainPage(app_ctrl, device)
