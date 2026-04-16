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

    def __init__(
        self,
        app_name: Optional[str] = None,
        backend: Optional[str] = None,
        exe_path: Optional[str] = None,
    ):
        """
        @brief  Khởi tạo AppController với tên app và backend pywinauto
        @param  app_name: Tên cửa sổ app (dùng title_re matching). Mặc định lấy từ settings.app.name
        @param  backend: Backend pywinauto — "uia" hoặc "win32". Mặc định lấy từ settings.app.backend
        @param  exe_path: Đường dẫn tới exe cần launch. Mặc định lấy từ settings.app.exe_path
        @retval None
        """
        cfg = get_settings().app
        self.app_name   = app_name or cfg.name
        self.backend    = backend  or cfg.backend
        self.exe_path   = exe_path if exe_path is not None else cfg.exe_path
        self.timeout    = cfg.connect_timeout
        self.action_delay = cfg.action_delay

        self._app: Optional["Application"] = None
        self._main_window = None

    # ── Connection ────────────────────────────────────────────────────────────

    def connect(self) -> "AppController":
        """
        @brief  Kết nối tới ứng dụng đang chạy bằng window title
        @retval AppController — self (để chain)
        """
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
        """
        @brief  Khởi động exe rồi kết nối tới app
        @retval AppController — self (để chain)
        """
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
        """
        @brief  Ngắt kết nối và giải phóng tham chiếu app/window
        @retval None
        """
        self._app = None
        self._main_window = None
        logger.info("App controller disconnected")

    # ── Element helpers ───────────────────────────────────────────────────────

    def _get_element(self, identifier: Union[str, dict]):
        """
        @brief  Tìm một UI element trong main window
        @param  identifier: str (auto_id / title / class_name) hoặc dict truyền thẳng vào child_window()
        @retval UIAWrapper — pywinauto control object tương ứng
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
        """
        @brief  Click vào element được chỉ định
        @param  identifier: str hoặc dict xác định element cần click
        @retval None
        """
        logger.info(f"Click → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        self._get_element(identifier).click_input()
        time.sleep(self.action_delay)

    def double_click(self, identifier: Union[str, dict]) -> None:
        """
        @brief  Double-click vào element được chỉ định
        @param  identifier: str hoặc dict xác định element cần double-click
        @retval None
        """
        logger.info(f"Double-click → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        self._get_element(identifier).double_click_input()
        time.sleep(self.action_delay)

    def type_text(self, identifier: Union[str, dict], text: str) -> None:
        """
        @brief  Set focus vào element rồi gõ chuỗi text
        @param  identifier: str hoặc dict xác định element nhận input
        @param  text: Chuỗi ký tự cần nhập
        @retval None
        """
        logger.info(f"Type '{text}' → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        el = self._get_element(identifier)
        el.set_focus()
        el.type_keys(text, with_spaces=True)
        time.sleep(self.action_delay)

    def set_value(self, identifier: Union[str, dict], value: str) -> None:
        """
        @brief  Xoá nội dung cũ (Ctrl+A) rồi nhập giá trị mới vào input field
        @param  identifier: str hoặc dict xác định input element
        @param  value: Giá trị mới cần nhập
        @retval None
        """
        logger.info(f"Set value '{value}' → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        el = self._get_element(identifier)
        el.set_focus()
        el.type_keys("^a", pause=0.05)
        el.type_keys(value, with_spaces=True)
        time.sleep(self.action_delay)

    def get_text(self, identifier: Union[str, dict]) -> str:
        """
        @brief  Lấy window_text() của element
        @param  identifier: str hoặc dict xác định element
        @retval str — nội dung text của element; chuỗi rỗng nếu pywinauto không khả dụng
        """
        if not PYWINAUTO_AVAILABLE:
            return ""
        return self._get_element(identifier).window_text()

    def wait_for_element(self, identifier: Union[str, dict], timeout: int = 10) -> bool:
        """
        @brief  Đợi cho đến khi element trở nên visible
        @param  identifier: str hoặc dict xác định element cần chờ
        @param  timeout: Số giây tối đa chờ element (default: 10)
        @retval bool — True nếu element visible trong timeout, False nếu timeout
        """
        try:
            self._get_element(identifier).wait("visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_element_enabled(self, identifier: Union[str, dict]) -> bool:
        """
        @brief  Kiểm tra element có đang enabled (không bị disabled/grayed) không
        @param  identifier: str hoặc dict xác định element
        @retval bool — True nếu element enabled, False nếu disabled hoặc pywinauto không khả dụng
        """
        if not PYWINAUTO_AVAILABLE:
            return False
        return self._get_element(identifier).is_enabled()

    def select_combobox(self, identifier: Union[str, dict], item: str) -> None:
        """
        @brief  Chọn một item trong combobox/dropdown
        @param  identifier: str hoặc dict xác định combobox element
        @param  item: Tên item cần chọn
        @retval None
        """
        logger.info(f"Select '{item}' in combobox → {identifier}")
        if not PYWINAUTO_AVAILABLE:
            return
        self._get_element(identifier).select(item)
        time.sleep(self.action_delay)

    def check_checkbox(self, identifier: Union[str, dict], state: bool = True) -> None:
        """
        @brief  Đặt trạng thái checkbox (check hoặc uncheck)
        @param  identifier: str hoặc dict xác định checkbox element
        @param  state: True để check, False để uncheck (default: True)
        @retval None
        """
        if not PYWINAUTO_AVAILABLE:
            return
        el = self._get_element(identifier)
        current = el.get_check_state()
        if bool(current) != state:
            el.click_input()
        time.sleep(self.action_delay)

    # ── Screenshot ────────────────────────────────────────────────────────────

    def take_screenshot(self, filename: str) -> Optional[Path]:
        """
        @brief  Chụp ảnh main window và lưu vào thư mục reports/screenshots/
        @param  filename: Tên file ảnh đầu ra (ví dụ: "step1.png")
        @retval Optional[Path] — đường dẫn file ảnh nếu thành công, None nếu thất bại
        """
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
        @brief  Tìm và click control theo window_text() — scan toàn bộ descendants
        @param  text: Chuỗi text cần khớp (so sánh không phân biệt hoa/thường)
        @param  retries: Số lần thử lại tối đa, mỗi lần cách nhau 1 giây (default: 5)
        @retval bool — True nếu tìm thấy và click thành công, False nếu không tìm thấy
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
        """
        @brief  Đợi cho đến khi xuất hiện control có window_text() == text
        @param  text: Chuỗi text cần chờ xuất hiện
        @param  timeout: Số giây tối đa chờ (default: 15)
        @retval bool — True nếu text xuất hiện trong timeout, False nếu timeout
        """
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
        """
        @brief  Kiểm tra có control nào có window_text() == text và đang enabled không
        @param  text: Chuỗi text cần tìm kiếm trong các descendants
        @retval bool — True nếu tìm thấy control phù hợp và enabled, False nếu không
        """
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
        """
        @brief  Gửi phím tắt trực tiếp vào main window (dùng cho menu keyboard navigation)
        @param  keys: Chuỗi phím theo cú pháp pywinauto (ví dụ: "{DOWN}{ENTER}")
        @retval None
        """
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return
        try:
            self._main_window.set_focus()
            self._main_window.bring_to_top()
            time.sleep(0.3)
        except Exception:
            pass
        self._main_window.type_keys(keys)
        time.sleep(self.action_delay)

    def is_running(self) -> bool:
        """
        @brief  Kiểm tra app có đang chạy và cửa sổ còn hiển thị không
        @retval bool — True nếu main window tồn tại và visible, False nếu không
        """
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return False
        try:
            return self._main_window.exists() and self._main_window.is_visible()
        except Exception:
            return False

    def switch_window(self, title_re: str, timeout: int = 20) -> None:
        """
        @brief  Chuyển _main_window sang cửa sổ khác sau khi navigation (ví dụ: mở RF Test Set từ Tools)
        @param  title_re: Regex pattern khớp với tiêu đề cửa sổ đích
        @param  timeout: Số giây tối đa chờ cửa sổ xuất hiện (default: 20)
        @retval None
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
        @brief  Lấy text của control ngay sau control có window_text chứa label (WinForms text-scan pattern)
        @param  label: Chuỗi label cần tìm trong danh sách text của các descendants
        @retval str — text của control liền sau label; chuỗi rỗng nếu không tìm thấy
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

    def click_button_by_text(self, text: str, retries: int = 5) -> bool:
        """
        @brief  Tìm và click control có control_type=Button với window_text() khớp text
        @param  text: Chuỗi text cần khớp (không phân biệt hoa/thường)
        @param  retries: Số lần thử lại, mỗi lần cách 0.5s (default: 5)
        @retval bool — True nếu click thành công, False nếu không tìm thấy
        """
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return False
        for _ in range(retries):
            for ctrl in self._main_window.descendants():
                try:
                    if (
                        ctrl.window_text().strip().lower() == text.lower()
                        and ctrl.is_enabled()
                        and "Button" in str(ctrl.element_info.control_type)
                    ):
                        ctrl.click_input()
                        time.sleep(self.action_delay)
                        logger.info(f"click_button_by_text({text!r}) OK")
                        return True
                except Exception:
                    pass
            time.sleep(0.5)
        logger.warning(f"click_button_by_text({text!r}) — not found after {retries} retries")
        return False

    def set_field_by_label(self, label: str, value: str) -> bool:
        """
        @brief  Tìm Edit control ngay sau label và set giá trị mới (Ctrl+A → xóa → gõ → Enter)
        @param  label: Text chính xác của label cần tìm
        @param  value: Giá trị cần nhập vào Edit field
        @retval bool — True nếu tìm và set thành công, False nếu không tìm thấy
        """
        if not PYWINAUTO_AVAILABLE or self._main_window is None:
            return False
        controls = list(self._main_window.descendants())
        for i, ctrl in enumerate(controls):
            try:
                if ctrl.window_text().strip() == label:
                    for j in range(i + 1, min(i + 10, len(controls))):
                        target = controls[j]
                        try:
                            if "Edit" in str(target.element_info.control_type):
                                target.click_input()
                                time.sleep(0.2)
                                target.type_keys("^a{BACKSPACE}")
                                target.set_edit_text(str(value))
                                target.type_keys("{ENTER}")
                                logger.info(f"set_field_by_label({label!r}) = {value!r}")
                                return True
                        except Exception:
                            pass
            except Exception:
                pass
        logger.warning(f"set_field_by_label({label!r}) — field not found")
        return False

    def select_from_desktop_popup(self, value: str, retries: int = 5) -> bool:
        """
        @brief  Chọn item từ popup window ở Desktop level (ví dụ: dropdown Trace selector)
        @param  value: Text chính xác của item cần chọn
        @param  retries: Số lần thử lại, mỗi lần cách 0.5s (default: 5)
        @retval bool — True nếu chọn thành công, False nếu không tìm thấy
        """
        if not PYWINAUTO_AVAILABLE:
            return False
        from pywinauto import Desktop
        for _ in range(retries):
            for win in Desktop(backend="uia").windows():
                try:
                    for ctrl in win.descendants():
                        try:
                            if ctrl.window_text().strip() == value and ctrl.is_enabled():
                                ctrl.click_input()
                                time.sleep(self.action_delay)
                                logger.info(f"select_from_desktop_popup({value!r}) OK")
                                return True
                        except Exception:
                            pass
                except Exception:
                    pass
            time.sleep(0.5)
        logger.warning(f"select_from_desktop_popup({value!r}) — not found after {retries} retries")
        return False

    def print_ui_tree(self, depth: int = 5) -> None:
        """
        @brief  In cây UI element ra stdout — hữu ích khi cần tìm identifier của element
        @param  depth: Độ sâu tối đa của cây in ra (default: 5)
        @retval None
        """
        if self._main_window is None:
            return
        self._main_window.print_control_identifiers(depth=depth)

    def __repr__(self) -> str:
        """
        @brief  Trả về string đại diện của AppController
        @retval str — string mô tả tên app và backend đang dùng
        """
        return f"AppController(app={self.app_name!r}, backend={self.backend!r})"
