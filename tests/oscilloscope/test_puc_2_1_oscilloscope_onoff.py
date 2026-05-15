"""
Oscilloscope ON/OFF test suite — PUC_2.1
Bật/tắt Oscilloscope từ UI PC17, verify đèn báo nguồn và trạng thái UI khớp nhau.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage

_OSCILLOSCOPE_LABEL = "OSCILLOSCOPE"


class TestPuc21OscilloscopeOnOff:
    """PUC_2.1 — Oscilloscope bật/tắt manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · PUC_2.1 · Normal · Bật Oscilloscope
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_oscilloscope_puc_2_1_tc_0001(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_1_tc_0001
        @brief: Bật Oscilloscope từ UI PC17 và xác nhận trạng thái khởi động thành công

        @details: Verify rằng Oscilloscope có thể được bật từ UI PC17:
                  đèn báo nguồn sáng lên (hoặc có điện áp định mức) và UI hiển thị
                  trạng thái đã khởi động xong và đang bật.

        @pre:- PC17 đã Connected
             - Oscilloscope đang ở trạng thái tắt (OFF)

        @test_procedure:
            [code]
                1. Bật nguồn cho Oscilloscope từ UI của PC17
                2. Quan sát, ghi nhận đèn báo nguồn của Oscilloscope hoặc đo điện áp
                   cấp cho module Oscilloscope và trạng thái hiển thị của UI
            [!code]

        @pass_criteria:- Đèn báo của Oscilloscope đã sáng lên (hoặc có điện áp đúng định mức)
                       - UI PC17 hiển thị Oscilloscope đã khởi động xong và đang bật

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC2 · PUC_2.1 · Abnormal · Bật/tắt liên tục Oscilloscope 5 lần
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_oscilloscope_puc_2_1_tc_0002(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_1_tc_0002
        @brief: Bật/tắt liên tục Oscilloscope 5 chu kỳ — trạng thái LED và UI khớp nhau

        @details: Tiếp tục từ TC1 (Oscilloscope đang ON).
                  Mỗi chu kỳ: tắt → xác nhận OFF → bật → xác nhận ON.
                  Đèn báo nguồn và status trên PC17 phải luôn khớp nhau.

        @pre:- PC17 đã Connected
             - Oscilloscope đang bật (tiếp tục từ TC1)

        @test_procedure:
            [code]
                1. Trên UI PC17 xác nhận thiết bị đã khởi động hoàn tất
                2. Tắt nguồn module Oscilloscope từ UI PC17
                3. Quan sát đèn báo nguồn và status UI → xác nhận OFF
                4. Trên UI PC17 bật nguồn module Oscilloscope
                5. Quan sát đèn báo nguồn và status UI → xác nhận đã khởi động thành công
                6. Lặp lại các bước 2–5 năm lần
            [!code]

        @pass_criteria:- Đèn báo của Oscilloscope và status PC17 khớp nhau sau mỗi lần OFF
                       - Đèn báo và status PC17 khớp nhau sau mỗi lần ON
                       - Hoàn thành đủ 5 chu kỳ không có exception

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
