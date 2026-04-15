"""
BasePage — Page Object Model base class.

Every page of your app should extend this and define
element locators + high-level actions.

Example
-------
    class MainPage(BasePage):
        BTN_ATTENUATOR_ON  = {"auto_id": "btnAttenuatorOn"}
        LBL_STATUS         = {"auto_id": "lblStatus"}

        def click_attenuator_on(self):
            self.click(self.BTN_ATTENUATOR_ON)

        def get_status(self) -> str:
            return self.get_text(self.LBL_STATUS)
"""
from __future__ import annotations

from typing import Union

from core.app_controller import AppController
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Abstract base for all Page Object classes."""

    def __init__(self, controller: AppController):
        """
        @brief  Khởi tạo BasePage với AppController được inject vào
        @param  controller: AppController instance đã kết nối tới app
        @retval None
        """
        self._ctrl = controller

    # ── Delegated actions ─────────────────────────────────────────────────────

    def click(self, identifier: Union[str, dict]) -> None:
        """
        @brief  Delegate click action xuống AppController
        @param  identifier: str hoặc dict xác định element cần click
        @retval None
        """
        self._ctrl.click(identifier)

    def double_click(self, identifier: Union[str, dict]) -> None:
        """
        @brief  Delegate double-click action xuống AppController
        @param  identifier: str hoặc dict xác định element cần double-click
        @retval None
        """
        self._ctrl.double_click(identifier)

    def type_text(self, identifier: Union[str, dict], text: str) -> None:
        """
        @brief  Delegate type_text action xuống AppController
        @param  identifier: str hoặc dict xác định element nhận input
        @param  text: Chuỗi ký tự cần nhập
        @retval None
        """
        self._ctrl.type_text(identifier, text)

    def set_value(self, identifier: Union[str, dict], value: str) -> None:
        """
        @brief  Delegate set_value (xoá rồi nhập) xuống AppController
        @param  identifier: str hoặc dict xác định input element
        @param  value: Giá trị mới cần nhập
        @retval None
        """
        self._ctrl.set_value(identifier, value)

    def get_text(self, identifier: Union[str, dict]) -> str:
        """
        @brief  Delegate get_text xuống AppController để lấy window_text của element
        @param  identifier: str hoặc dict xác định element
        @retval str — nội dung text của element
        """
        return self._ctrl.get_text(identifier)

    def is_enabled(self, identifier: Union[str, dict]) -> bool:
        """
        @brief  Kiểm tra element có đang enabled không, delegate xuống AppController
        @param  identifier: str hoặc dict xác định element
        @retval bool — True nếu element enabled, False nếu không
        """
        return self._ctrl.is_element_enabled(identifier)

    def wait_for(self, identifier: Union[str, dict], timeout: int = 10) -> bool:
        """
        @brief  Đợi element trở nên visible, delegate xuống AppController
        @param  identifier: str hoặc dict xác định element cần chờ
        @param  timeout: Số giây tối đa chờ (default: 10)
        @retval bool — True nếu element visible trong timeout, False nếu timeout
        """
        return self._ctrl.wait_for_element(identifier, timeout)

    def select(self, identifier: Union[str, dict], item: str) -> None:
        """
        @brief  Chọn item trong combobox, delegate xuống AppController
        @param  identifier: str hoặc dict xác định combobox element
        @param  item: Tên item cần chọn
        @retval None
        """
        self._ctrl.select_combobox(identifier, item)

    def screenshot(self, name: str) -> None:
        """
        @brief  Chụp ảnh màn hình app, delegate xuống AppController
        @param  name: Tên file ảnh đầu ra (ví dụ: "step1.png")
        @retval None
        """
        self._ctrl.take_screenshot(name)

    def click_by_text(self, text: str, retries: int = 5) -> bool:
        """
        @brief  Tìm và click control theo window_text(), delegate xuống AppController
        @param  text: Chuỗi text cần khớp
        @param  retries: Số lần thử lại tối đa (default: 5)
        @retval bool — True nếu click thành công, False nếu không tìm thấy
        """
        return self._ctrl.click_by_text(text, retries=retries)

    def wait_for_text(self, text: str, timeout: int = 10) -> bool:
        """
        @brief  Đợi control có window_text() == text xuất hiện, delegate xuống AppController
        @param  text: Chuỗi text cần chờ xuất hiện
        @param  timeout: Số giây tối đa chờ (default: 10)
        @retval bool — True nếu text xuất hiện trong timeout, False nếu timeout
        """
        return self._ctrl.wait_for_text(text, timeout=timeout)

    def has_text(self, text: str) -> bool:
        """
        @brief  Kiểm tra có control nào có window_text() == text và enabled không, delegate xuống AppController
        @param  text: Chuỗi text cần tìm kiếm
        @retval bool — True nếu tìm thấy control phù hợp, False nếu không
        """
        return self._ctrl.has_element_with_text(text)
