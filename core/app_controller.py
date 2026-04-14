"""
AppController — wraps pywinauto to control the Windows target application.

Backends
--------
- "uia"  : Modern apps (WPF, WinForms with Accessibility, Electron)
- "win32": Legacy Win32 / MFC apps

Usage (in conftest fixture)
---------------------------
    ctrl = AppController()
    ctrl.connect()          # connect to already-running app
    # OR
    ctrl.launch()           # launch exe then connect

    ctrl.click("OK")
    ctrl.type_text("Username", "admin")
    ctrl.get_text("StatusLabel")
    ctrl.take_screenshot("step1.png")
    ctrl.disconnect()
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Optional, Union

from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    import pywinauto
    from pywinauto import Application, Desktop
    from pywinauto.controls.uiawrapper import UIAWrapper
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False
    logger.warning("pywinauto not installed — AppController will run in STUB mode")


class AppController:
    """High-level controller for the target Windows application."""

    def __init__(self, app_name: Optional[str] = None, backend: Optional[str] = None):
        cfg = get_settings().app
        self.app_name   = app_name or cfg.name
        self.backend    = backend  or cfg.backend
        self.exe_path   = cfg.exe_path
        self.timeout    = cfg.connect_timeout
        self.action_delay = cfg.action_delay

        self._app: Optional["Application"] = None
        self._main_window = None

    # ── Connection ────────────────────────────────────────────────────────────

    def connect(self) -> "AppController":
        """Connect to an already-running application by window title."""
        if not PYWINAUTO_AVAILABLE:
            logger.warning("[STUB] connect() called")
            return self
        logger.info(f"Connecting to app: '{self.app_name}' (backend={self.backend})")
        self._app = Application(backend=self.backend).connect(
            title_re=f".*{self.app_name}.*",
            timeout=self.timeout,
        )
        self._main_window = self._app.top_window()
        logger.info("Connected successfully")
        return self

    def launch(self) -> "AppController":
        """Launch the exe then connect to it."""
        if not PYWINAUTO_AVAILABLE:
            logger.warning("[STUB] launch() called")
            return self
        if not self.exe_path:
            raise ValueError("exe_path is not configured in settings.yaml")
        logger.info(f"Launching: {self.exe_path}")
        self._app = Application(backend=self.backend).start(self.exe_path)
        time.sleep(2)
        self._main_window = self._app.top_window()
        self._main_window.wait("ready", timeout=self.timeout)
        logger.info("App launched and ready")
        return self

    def disconnect(self) -> None:
        self._app = None
        self._main_window = None
        logger.info("App controller disconnected")

    # ── Element helpers ───────────────────────────────────────────────────────

    def _get_element(self, identifier: Union[str, dict]):
        """
        Find a UI element.
        identifier can be:
          - str  → searches by auto_id, title, or class_name
          - dict → passed directly to child_window(**identifier)
        """
        if self._main_window is None:
            raise RuntimeError("Not connected to any application")
        if isinstance(identifier, dict):
            return self._main_window.child_window(**identifier)
        # Try common attributes
        for key in ("auto_id", "title", "class_name"):
            try:
                el = self._main_window.child_window(**{key: identifier})
                el.wait("exists", timeout=3)
                return el
            except Exception:
                continue
        raise LookupError(f"Element not found: {identifier!r}")

    # ── Actions ───────────────────────────────────────────────────────────────

    def click(self, identifier: Union[str, dict]) -> None:
        logger.info(f"Click → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        self._get_element(identifier).click_input()
        time.sleep(self.action_delay)

    def double_click(self, identifier: Union[str, dict]) -> None:
        logger.info(f"Double-click → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        self._get_element(identifier).double_click_input()
        time.sleep(self.action_delay)

    def type_text(self, identifier: Union[str, dict], text: str) -> None:
        logger.info(f"Type '{text}' → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        el = self._get_element(identifier)
        el.set_focus()
        el.type_keys(text, with_spaces=True)
        time.sleep(self.action_delay)

    def set_value(self, identifier: Union[str, dict], value: str) -> None:
        """Clear then set value (for input fields)."""
        logger.info(f"Set value '{value}' → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        el = self._get_element(identifier)
        el.set_focus()
        el.type_keys("^a", pause=0.05)
        el.type_keys(value, with_spaces=True)
        time.sleep(self.action_delay)

    def get_text(self, identifier: Union[str, dict]) -> str:
        if not PYWINAUTO_AVAILABLE:
            return ""
        return self._get_element(identifier).window_text()

    def wait_for_element(self, identifier: Union[str, dict], timeout: int = 10) -> bool:
        try:
            self._get_element(identifier).wait("visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_element_enabled(self, identifier: Union[str, dict]) -> bool:
        if not PYWINAUTO_AVAILABLE:
            return False
        return self._get_element(identifier).is_enabled()

    def select_combobox(self, identifier: Union[str, dict], item: str) -> None:
        logger.info(f"Select '{item}' in combobox → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        self._get_element(identifier).select(item)
        time.sleep(self.action_delay)

    def check_checkbox(self, identifier: Union[str, dict], state: bool = True) -> None:
        if not PYWINAUTO_AVAILABLE:
            return
        el = self._get_element(identifier)
        current = el.get_check_state()
        if bool(current) != state:
            el.click_input()
        time.sleep(self.action_delay)

    # ── Screenshot ────────────────────────────────────────────────────────────

    def take_screenshot(self, filename: str) -> Optional[Path]:
        """Capture the main window and save to reports/screenshots/."""
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return None
        out_dir = Path("reports/screenshots")
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / filename
        try:
            self._main_window.capture_as_image().save(str(path))
            logger.info(f"Screenshot saved: {path}")
            return path
        except Exception as e:
            logger.warning(f"Screenshot failed: {e}")
            return None

    # ── Utility ───────────────────────────────────────────────────────────────

    def print_ui_tree(self, depth: int = 5) -> None:
        """Print UI element tree — useful when finding element identifiers."""
        if self._main_window is None:
            return
        self._main_window.print_control_identifiers(depth=depth)

    def __repr__(self) -> str:
        return f"AppController(app={self.app_name!r}, backend={self.backend!r})"
