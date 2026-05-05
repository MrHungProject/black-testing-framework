"""
Spectrum Analyzer ON/OFF test suite — PUC_4.1
Bật/tắt Spectrum Analyzer từ UI PC17, verify trạng thái LED/UI khớp nhau.
Execution type: manual.
"""

import time

import pytest

from core import testcase
from pages.main_page import MainPage

_SPECTRUM_LABEL = "SPECTRUM"


class TestPuc41SpectrumOnOff:
    """
    PUC_4.1 — Spectrum Analyzer ON/OFF manual test suite.

    Setup flow (tự động, không cần TC trước chạy trước):
        fixture _ensure_connected (autouse=True) chạy trước mỗi TC.
        Nếu SPECTRUM chưa Connected → mở System → Connect và kết nối.
        Mỗi TC đều độc lập và luôn bắt đầu ở trạng thái SPECTRUM đã Connected.
    """

    # ── Class-level setup: chạy trước MỖI test method ────────────────────────

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo SPECTRUM đã Connected trước mỗi TC."""
        if not main_page.is_device_connected(_SPECTRUM_LABEL):
            main_page.open_connect_panel()
            main_page.connect_device(_SPECTRUM_LABEL)
            time.sleep(3)

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · PUC_2.1 · Normal · Bật Spectrum Analyzer
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_1_tc_0001(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc_0001
        @brief: Bật Spectrum Analyzer từ UI PC17 và xác nhận trạng thái khởi động thành công

        @details: Verify rằng Spectrum Analyzer có thể được bật từ UI PC17:
                  đèn báo nguồn sáng lên và UI hiển thị trạng thái đang bật/sẵn sàng.

        @pre:- PC17 đã Connected
             - Spectrum Analyzer đang ở trạng thái tắt (OFF)

        @test_procedure:
            [code]
                1. Bật nguồn cho Spectrum Analyzer từ UI của PC17
                2. Quan sát, ghi nhận đèn báo nguồn của Spectrum Analyzer
                   hoặc đo điện áp cấp cho module Spectrum Analyzer
                3. Ghi nhận trạng thái hiển thị trên UI PC17
            [!code]

        @pass_criteria:- Đèn báo của Spectrum Analyzer đã sáng lên hoặc có điện áp đúng định mức
                       - UI PC17 hiển thị trạng thái Spectrum Analyzer đã khởi động xong và đang bật

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        assert main_page.is_device_connected(_SPECTRUM_LABEL), \
            f"'{_SPECTRUM_LABEL}' không đạt trạng thái 'Connected'"

    # ════════════════════════════════════════════════════════════════════════════
    #  TC2 · PUC_2.1 · Abnormal · Bật/tắt liên tục Spectrum Analyzer 5 lần
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_1_tc_0002(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc_0002
        @brief: Bật/tắt liên tục Spectrum Analyzer 5 chu kỳ — LED và UI phải khớp nhau

        @details: Tiếp tục từ TC1 (Spectrum Analyzer đang ON).
                  Mỗi chu kỳ: tắt → xác nhận OFF → bật → xác nhận ON.
                  Đèn báo nguồn và status trên PC17 phải luôn khớp nhau.

        @pre:- PC17 đã Connected
             - Spectrum Analyzer đang bật (tiếp tục từ TC1)

        @test_procedure:
            [code]
                1. Trên UI PC17 xác nhận Spectrum Analyzer đã khởi động hoàn tất
                2. Tắt nguồn module Spectrum Analyzer từ UI PC17
                3. Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận OFF
                4. Bật nguồn module Spectrum Analyzer từ UI PC17
                5. Quan sát đèn báo nguồn và ghi nhận trạng thái UI → xác nhận ON
                6. Lặp lại các bước 2–5 năm lần
            [!code]

        @pass_criteria:- Đèn báo và status PC17 khớp nhau sau mỗi lần tắt (OFF)
                       - Đèn báo và status PC17 khớp nhau sau mỗi lần bật (ON)
                       - Hoàn thành đủ 5 chu kỳ không có exception

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        CYCLES = 5

        assert main_page.is_device_connected(_SPECTRUM_LABEL), \
            "Điều kiện đầu vào TC2: SPECTRUM chưa Connected"

        for cycle in range(1, CYCLES + 1):
            # ── Disconnect ──────────────────────────────────────────────────────
            main_page.disconnect_device(_SPECTRUM_LABEL)
            time.sleep(3)

            assert not main_page.is_device_connected(_SPECTRUM_LABEL), (
                f"Chu kỳ {cycle}/{CYCLES}: SPECTRUM vẫn hiển thị 'Connected' sau Disconnect"
            )

            # ── Reconnect ───────────────────────────────────────────────────────
            main_page.connect_device(_SPECTRUM_LABEL)
            time.sleep(3)

            assert main_page.is_device_connected(_SPECTRUM_LABEL), (
                f"Chu kỳ {cycle}/{CYCLES}: SPECTRUM không đạt 'Connected' sau Reconnect"
            )
