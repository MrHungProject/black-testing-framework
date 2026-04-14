"""
VNA test suite — PUC_2.1 Power ON/OFF
"""
import time

import pytest

from core import testcase
from core.serial_device import SerialDevice
from pages.main_page import MainPage


# ════════════════════════════════════════════════════════════════════════════
#  TC1 · PUC_2.1 · Normal · Bật VNA
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_vna_puc_2_1_0001(main_page: MainPage, device: SerialDevice):
    """
    @test_id: test_vna_puc_2_1_0001
    @brief: Bật VNA
    @details: Verify rằng VNA có thể được bật nguồn từ UI của PC17
              và trạng thái phần cứng hiển thị đúng

    @pre:- PC17 application đang chạy
         - Module VNA đã được kết nối với hệ thống

    @test_procedure:
                    [code]
                        - Bật nguồn cho VNA từ UI của PC17
                        - Quan sát, ghi nhận đèn báo nguồn của VNA
                        hoặc đo điện áp cấp cho module VNA
                        - Kiểm tra trạng thái hiển thị trên UI
                    [!code]

    @pass_criteria:- Đèn báo nguồn VNA sáng hoặc điện áp cấp đúng mức
                   - UI hiển thị VNA đã bật và sẵn sàng hoạt động

    @test_level: software
    @test_type: functional
    @execution_type: Manual
    @hw_depend: yes
    """


# ════════════════════════════════════════════════════════════════════════════
#  TC2 · PUC_2.1 · Abnormal · Bật/tắt liên tục VNA
# ════════════════════════════════════════════════════════════════════════════


@testcase
def test_vna_puc_2_1_0002(main_page: MainPage, device: SerialDevice):
    """
    @test_id: test_vna_puc_2_1_0002
    @brief: Bật/tắt liên tục VNA
    @details: Verify rằng VNA có thể bật/tắt liên tục 5 lần mà không bị lỗi,
              trạng thái phần cứng và UI phải đúng sau mỗi chu kỳ

    @pre:- PC17 application đang chạy
         - Module VNA đã bật (tiếp tục từ TC1 PUC_2.1 Normal)

    @test_procedure:
                    [code]
                        - Xác nhận thiết bị đã khởi động hoàn tất trên UI
                        - Tắt nguồn module VNA từ UI
                        - Quan sát đèn báo nguồn VNA và ghi nhận trạng thái UI
                        - Bật nguồn module VNA từ UI
                        - Quan sát đèn báo nguồn VNA và ghi nhận trạng thái khởi động thành công
                        - Lặp lại 5 lần
                    [!code]

    @pass_criteria:- Sau mỗi lần tắt: đèn VNA tắt, UI hiển thị OFF
                   - Sau mỗi lần bật: đèn VNA sáng, UI hiển thị ON/Ready
                   - Hoàn thành đủ 5 chu kỳ không có lỗi

    @test_level: software
    @test_type: functional
    @execution_type: Manual
    @hw_depend: yes
    """
   