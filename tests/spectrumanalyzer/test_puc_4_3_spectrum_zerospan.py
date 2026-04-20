"""
Spectrum Analyzer Zero-span mode test suite — PUC_4.3
Chạy chế độ Zero-span: hiển thị AM vs Time và Spectrum Plot.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc43SpectrumZeroSpan:
    """PUC_4.3 — Spectrum Analyzer Zero-span mode manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC15 · PUC_4.3 · Normal · Zero-span Center 1MHz, SignalGen 1MHz -18dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_3_tc15(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_3_tc15
        @brief: Zero-span mode — Center 1MHz, SignalGen 1MHz -18dBm → AM vs Time và Spectrum Plot

        @details: Verify PC17 Spectrum Analyzer chạy đúng chế độ Zero-span mode.
                  Cài đặt Zero-span: Center=1MHz, Step=20MHz.
                  SignalGen phát 1MHz, -18dBm.
                  Biểu đồ AM vs Time và Spectrum Plot phải hiển thị đúng tín hiệu.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                Chuẩn bị:
                1. Máy phát tín hiệu Signal Gen
                2. Bật module Spectrum Analyzer
                Step:
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17 chế độ Zero-span mode:
                   Center=1MHz, Step=20MHz
                3. Setting SignalGen: FREQ=1MHz, POW=-18dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát biểu đồ AM vs Time trên PC17, ghi nhận kết quả
                6. Quan sát Spectrum Plot trên PC17, ghi nhận kết quả
            [!code]

        @pass_criteria:- TBD (biểu đồ AM vs Time hiển thị đúng tín hiệu)
                       - TBD (Spectrum Plot hiển thị đúng tín hiệu tại 1MHz)

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
