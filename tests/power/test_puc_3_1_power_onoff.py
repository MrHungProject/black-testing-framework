"""
Power Meter ON/OFF test suite — PUC_3.1
Bật/tắt Power Meter từ UI PC17, verify trạng thái LED/UI khớp nhau.
"""

import time

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc31PowerMeterOnOff:
    """
    PUC_3.1 — Power Meter bật/tắt test suite.
    _ensure_connected (autouse) đảm bảo PC17 Connected trước mỗi TC.
    """

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · PUC_3.1 · Normal · Bật Power Meter
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_power_puc_3_1_tc_0001(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_1_tc_0001
        @brief: Bật Power Meter từ UI PC17 và xác nhận trạng thái khởi động thành công

        @details: Verify rằng Power Meter có thể được bật từ UI PC17:
                  đèn báo nguồn sáng lên và UI hiển thị trạng thái đang bật/sẵn sàng.

        @pre:- PC17 đã Connected
             - Power Meter đang ở trạng thái tắt (OFF)

        @test_procedure:
            [code]
                - Bật nguồn Power Meter từ UI PC17
                - Đợi Power Meter khởi động hoàn tất
                - Quan sát đèn báo nguồn của Power Meter
                - Ghi nhận trạng thái hiển thị trên UI PC17
            [!code]

        @pass_criteria:- Đèn báo của Power Meter sáng lên (hoặc có điện áp đúng định mức)
                       - UI PC17 hiển thị Power Meter đã khởi động xong và đang bật

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC2 · PUC_3.1 · Abnormal · Bật/tắt liên tục Power Meter 5 lần
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_power_puc_3_1_tc_0002(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_1_tc_0002
        @brief: Bật/tắt liên tục Power Meter 5 chu kỳ — trạng thái LED và UI phải khớp nhau

        @details: Tiếp tục từ TC1 (Power Meter đang ON).
                  Mỗi chu kỳ: tắt → xác nhận OFF → bật → xác nhận ON.
                  Đèn báo nguồn và status trên PC17 phải luôn khớp nhau.

        @pre:- PC17 đã Connected
             - Power Meter đang bật (tiếp tục từ TC1)

        @test_procedure:
            [code]
                - Xác nhận Power Meter đang ON
                - Tắt Power Meter từ UI PC17
                - Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận OFF
                - Bật Power Meter từ UI PC17
                - Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận ON
                - Lặp lại 5 lần
            [!code]

        @pass_criteria:- Đèn báo và status PC17 khớp nhau sau mỗi lần tắt (OFF)
                       - Đèn báo và status PC17 khớp nhau sau mỗi lần bật (ON)
                       - Hoàn thành đủ 5 chu kỳ không có exception

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """