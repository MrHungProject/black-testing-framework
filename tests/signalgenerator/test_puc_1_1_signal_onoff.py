"""
Signal Generator ON/OFF test suite — PUC_1.1
Bật/tắt Signal Generator từ UI PC17, verify trạng thái LED/UI khớp nhau.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc11OnOff:
    """PUC_1.1 — Signal Generator bật/tắt test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · PUC_1.1 · Normal · Bật Signal Generator
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_1_tc_0001(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_1_tc_0001
        @brief: Bật Signal Generator từ UI PC17 và xác nhận trạng thái khởi động thành công

        @details: Verify rằng Signal Generator có thể được bật từ UI PC17:
                  đèn báo nguồn sáng lên hoặc có điện áp đúng định mức cấp cho module,
                  UI hiển thị trạng thái đã khởi động xong và đang bật.

        @pre:- Hệ thống chưa có nguồn, khởi động từ đầu
             - PC17 đã được bật và Connected
             - Signal Generator đang ở trạng thái tắt (OFF)

        @test_procedure:
            [code]
                - Khởi động hệ thống từ lúc chưa có nguồn, bật phần mềm PC17
                - Bật nguồn cho Signal Generator từ UI của PC17
                - Quan sát đèn báo nguồn của Signal Generator hoặc đo điện áp cấp cho module
                - Ghi nhận trạng thái hiển thị trên UI PC17
            [!code]

        @pass_criteria:- Đèn báo của Signal Generator đã sáng lên hoặc có điện áp đúng định mức
                       - UI PC17 hiển thị trạng thái Signal Generator đã khởi động xong và đang bật

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC2 · PUC_1.1 · Normal · Bật/tắt liên tục Signal Generator 5 chu kỳ
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_1_tc_0002(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_1_tc_0002
        @brief: Bật/tắt liên tục Signal Generator 5 chu kỳ — trạng thái LED và UI phải khớp nhau

        @details: Tiếp tục từ TC1 (Signal Generator đang ON).
                  Mỗi chu kỳ: tắt → xác nhận OFF → bật → xác nhận ON.
                  Đèn báo nguồn và status trên PC17 phải luôn khớp nhau.

        @pre:- PC17 đã Connected
             - Signal Generator đang bật (tiếp tục từ TC1)

        @test_procedure:
            [code]
                - Xác nhận thiết bị đã khởi động hoàn tất trên UI PC17
                - Tắt nguồn module Signal Generator từ UI PC17
                - Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận OFF
                - Bật nguồn module Signal Generator từ UI PC17
                - Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận ON
                - Lặp lại các bước trên 5 lần
            [!code]

        @pass_criteria:- Đèn báo Signal Generator và status trên PC17 khớp nhau sau mỗi lần tắt
                       - Đèn báo Signal Generator và status trên PC17 khớp nhau sau mỗi lần bật
                       - Hoàn thành đủ 5 chu kỳ không có exception

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
