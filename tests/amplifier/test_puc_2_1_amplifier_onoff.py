"""
Amplifier ON/OFF test suite — PUC_2.1
Bật/tắt Amplifier từ UI PC17, verify trạng thái LED/UI khớp nhau.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc21AmplifierOnOff:
    """PUC_2.1 — Amplifier bật/tắt manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · PUC_2.1 · Normal · Bật Amplifier
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_2_1_tc01(self, main_page: MainPage):
        """
        @test_id: test_amplifier_puc_2_1_tc01
        @brief: Bật Amplifier từ UI PC17 và xác nhận trạng thái khởi động thành công

        @details: Verify rằng Amplifier có thể được bật từ UI PC17:
                  đèn báo nguồn sáng lên và UI hiển thị trạng thái đang bật/sẵn sàng.

        @pre:- PC17 đã Connected
             - Amplifier đang ở trạng thái tắt (OFF)

        @test_procedure:
            [code]
                1. Bật nguồn cho Amplifier từ UI của PC17
                2. Quan sát, ghi nhận đèn báo nguồn của Amplifier
                   hoặc đo điện áp cấp cho module Amplifier
                3. Ghi nhận trạng thái hiển thị trên UI PC17
            [!code]

        @pass_criteria:- Đèn báo của Amplifier đã sáng lên hoặc có điện áp đúng định mức
                       - UI PC17 hiển thị trạng thái Amplifier đã khởi động xong và đang bật

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC2 · PUC_2.1 · Abnormal · Bật/tắt liên tục Amplifier 5 lần
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_2_1_tc02(self, main_page: MainPage):
        """
        @test_id: test_amplifier_puc_2_1_tc02
        @brief: Bật/tắt liên tục Amplifier 5 chu kỳ — LED và UI phải khớp nhau

        @details: Tiếp tục từ TC1 (Amplifier đang ON).
                  Mỗi chu kỳ: tắt → xác nhận OFF → bật → xác nhận ON.
                  Đèn báo nguồn và status trên PC17 phải luôn khớp nhau.

        @pre:- PC17 đã Connected
             - Amplifier đang bật (tiếp tục từ TC1)

        @test_procedure:
            [code]
                1. Trên UI PC17 xác nhận Amplifier đã khởi động hoàn tất
                2. Tắt nguồn module Amplifier từ UI PC17
                3. Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận OFF
                4. Bật nguồn module Amplifier từ UI PC17
                5. Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận ON
                6. Lặp lại các bước 2–5 năm lần
            [!code]

        @pass_criteria:- Đèn báo và status PC17 khớp nhau sau mỗi lần tắt (OFF)
                       - Đèn báo và status PC17 khớp nhau sau mỗi lần bật (ON)
                       - Hoàn thành đủ 5 chu kỳ không có exception

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
