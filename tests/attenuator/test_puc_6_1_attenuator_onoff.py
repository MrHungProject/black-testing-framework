"""
Attenuator ON/OFF test suite — PUC_6.1
Bật/tắt Attenuator từ UI PC17, verify trạng thái LED/UI khớp nhau.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc61AttenuatorOnOff:
    """PUC_6.1 — Attenuator bật/tắt manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · PUC_6.1 · Normal · Bật Attenuator
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_1_tc_0001(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_1_tc_0001
        @brief: Bật Attenuator từ UI PC17 và xác nhận trạng thái khởi động thành công

        @details: Verify rằng Attenuator có thể được bật từ UI PC17:
                  đèn báo nguồn sáng lên và UI hiển thị trạng thái đang bật/sẵn sàng.

        @pre:- PC17 đã Connected
             - Attenuator đang ở trạng thái tắt (OFF)

        @test_procedure:
            [code]
                1. Bật nguồn cho Attenuator từ UI của PC17
                2. Quan sát, ghi nhận đèn báo nguồn của Attenuator
                   hoặc đo điện áp cấp cho module Attenuator
                3. Ghi nhận trạng thái hiển thị trên UI PC17
            [!code]

        @pass_criteria:- Đèn báo của Attenuator đã sáng lên hoặc có điện áp đúng định mức
                       - UI PC17 hiển thị trạng thái Attenuator đã khởi động xong và đang bật

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC2 · PUC_6.1 · Abnormal · Bật/tắt liên tục Attenuator 5 lần
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_1_tc_0002(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_1_tc_0002
        @brief: Bật/tắt liên tục Attenuator 5 chu kỳ — LED và UI phải khớp nhau

        @details: Tiếp tục từ TC1 (Attenuator đang ON).
                  Mỗi chu kỳ: tắt → xác nhận OFF → bật → xác nhận ON.
                  Đèn báo nguồn và status trên PC17 phải luôn khớp nhau.

        @pre:- PC17 đã Connected
             - Attenuator đang bật (tiếp tục từ TC1)

        @test_procedure:
            [code]
                1. Trên UI PC17 xác nhận Attenuator đã khởi động hoàn tất
                2. Tắt nguồn module Attenuator từ UI PC17
                3. Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận OFF
                4. Bật nguồn module Attenuator từ UI PC17
                5. Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận ON
                6. Lặp lại các bước 2–5 năm lần
            [!code]

        @pass_criteria:- Đèn báo và status PC17 khớp nhau sau mỗi lần tắt (OFF)
                       - Đèn báo và status PC17 khớp nhau sau mỗi lần bật (ON)
                       - Hoàn thành đủ 5 chu kỳ không có exception

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
