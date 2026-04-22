"""DetailPanel — tab Detail của FormMainEliteRF (Temperature, Serial Number)."""
from __future__ import annotations

import time

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class DetailPanel(BasePage):
    """Đọc thông tin thiết bị từ tab Detail."""

    def click_detail(self) -> bool:
        """
        @brief  Click tab/button "Detail" để mở panel thông tin thiết bị
        @retval bool — True nếu click thành công
        """
        ok = self._ctrl.click_by_text("Detail")
        if not ok:
            raise RuntimeError("PC17: Không click được 'Detail'")
        time.sleep(2)
        return ok

    def get_temperature(self) -> str:
        """
        @brief  Lấy giá trị Temperature từ Detail panel
        @retval str — giá trị temperature hiển thị trên UI; chuỗi rỗng nếu không tìm thấy
        """
        return self._ctrl.get_text_after_label("Temperature")

    def get_serial_number(self) -> str:
        """
        @brief  Lấy Serial Number từ Detail panel
        @retval str — serial number hiển thị trên UI; chuỗi rỗng nếu không tìm thấy
        """
        return self._ctrl.get_text_after_label("Serial Number")
