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
    import comtypes
    comtypes.CoInitialize()
except Exception:
    pass

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
        time.sleep(5)
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

    # ── Text-based element helpers (dùng khi auto_id không hoạt động) ─────────

    def click_by_text(self, text: str, retries: int = 5) -> bool:
        """
        Tìm và click control theo window_text() — scan toàn bộ descendants.
        Retry tối đa `retries` lần, mỗi lần cách nhau 1 giây.
        """
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return False
        for _ in range(retries):
            for ctrl in self._main_window.descendants():
                try:
                    if ctrl.window_text().strip().lower() == text.lower() and ctrl.is_enabled():
                        ctrl.click_input()
                        time.sleep(self.action_delay)
                        logger.info(f"click_by_text({text!r}) OK")
                        return True
                except Exception:
                    pass
            time.sleep(1)
        logger.warning(f"click_by_text({text!r}) — not found after {retries} retries")
        return False

    def wait_for_text(self, text: str, timeout: int = 15) -> bool:
        """Đợi cho đến khi xuất hiện control có window_text() == text."""
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return False
        for _ in range(timeout):
            for ctrl in self._main_window.descendants():
                try:
                    if ctrl.window_text().strip() == text:
                        return True
                except Exception:
                    pass
            time.sleep(1)
        logger.warning(f"wait_for_text({text!r}) — timeout after {timeout}s")
        return False

    def has_element_with_text(self, text: str) -> bool:
        """Kiểm tra có control nào có window_text() == text và enabled không."""
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return False
        for ctrl in self._main_window.descendants():
            try:
                if ctrl.window_text().strip() == text and ctrl.is_enabled():
                    return True
            except Exception:
                pass
        return False

    def type_keys_on_window(self, keys: str) -> None:
        """Gửi phím tắt trực tiếp vào main window (dùng cho menu keyboard nav)."""
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return
        self._main_window.type_keys(keys)
        time.sleep(self.action_delay)

    def is_running(self) -> bool:
        """Kiểm tra app có đang chạy và cửa sổ còn hiển thị không."""
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return False
        try:
            return self._main_window.exists() and self._main_window.is_visible()
        except Exception:
            return False

    def switch_window(self, title_re: str, timeout: int = 20) -> None:
        """
        Chuyển _main_window sang cửa sổ khác sau khi navigation.
        Ví dụ: sau khi mở RF Test Set từ menu Tools.
        """
        if not PYWINAUTO_AVAILABLE or self._app is None:
            return
        logger.info(f"Switching to window: {title_re!r}")
        win = self._app.window(title_re=title_re)
        win.wait("visible", timeout=timeout)
        self._main_window = win
        logger.info(f"Switched to: {win.window_text()!r}")

    # ── Utility ───────────────────────────────────────────────────────────────

    def get_text_after_label(self, label: str) -> str:
        """
        Lấy text của control ngay sau control có window_text chứa label.
        Dùng khi app không có auto_id ổn định (WinForms text-scan pattern).
        """
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return ""
        texts = []
        for ctrl in self._main_window.descendants():
            try:
                t = ctrl.window_text().strip()
                if t:
                    texts.append(t)
            except Exception:
                pass
        for i, t in enumerate(texts):
            if label.lower() in t.lower() and i + 1 < len(texts):
                return texts[i + 1]
        logger.warning(f"get_text_after_label({label!r}) — label not found")
        return ""

    def print_ui_tree(self, depth: int = 5) -> None:
        """Print UI element tree — useful when finding element identifiers."""
        if self._main_window is None:
            return
        self._main_window.print_control_identifiers(depth=depth)

    def __repr__(self) -> str:
        return f"AppController(app={self.app_name!r}, backend={self.backend!r})"
