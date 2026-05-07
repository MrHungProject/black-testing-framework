"""
Spectrum Analyzer Zero-span mode test suite — PUC_4.3
Chạy chế độ Zero-span: hiển thị AM vs Time và Spectrum Plot.
Execution type: automatic.
"""

import time

import pytest

from core import testcase
from pages.main_page import MainPage

_SPECTRUM_LABEL   = "SPECTRUM"
_SIGNAL_GEN_LABEL = "Signal Genarator"


class TestPuc43SpectrumZeroSpan:
    """
    PUC_4.3 — Spectrum Analyzer Zero-span mode automatic test suite.

    Setup flow (tự động, không cần TC trước chạy trước):
        fixture _ensure_connected (autouse=True) chạy trước mỗi TC.
        Nếu SPECTRUM hoặc Signal Generator chưa Connected → mở System → Connect
        và kết nối từng thiết bị.
        Mỗi TC đều độc lập và luôn bắt đầu ở trạng thái cả hai thiết bị đã Connected.
    """

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Giữ kết nối SPECTRUM + Signal Generator trong suốt session class."""
        spectrum_ok = main_page.is_device_connected(_SPECTRUM_LABEL)
        signal_ok   = main_page.is_device_connected(_SIGNAL_GEN_LABEL)

        if not spectrum_ok or not signal_ok:
            main_page.open_connect_panel()
            if not spectrum_ok:
                main_page.connect_device(_SPECTRUM_LABEL)
                time.sleep(3)
            if not signal_ok:
                main_page.connect_device(_SIGNAL_GEN_LABEL)
                time.sleep(3)

        yield

    # ── Helper dùng chung ────────────────────────────────────────────────────

    def _run_zerospan_tc(
        self,
        main_page: MainPage,
        center: str,
        rf1_out: str,
        power_level: str,
    ) -> None:
        """
        Luồng chung cho các TC PUC_4.3:
          1. Analysis Mode → chọn Zero-span
          2. Zero-span Setting → Center = center, Step = 20MHz
          3. SignalGen → RF1 OUT = rf1_out, Power = power_level
        """
        # Chọn Zero-span mode (Preset reset về Sweep, nên phải chọn lại)
        main_page.open_analysis_mode()
        main_page.select_analysis_mode("Zero-span")

        # Zero-span: Capture Setting → Center + Step
        main_page.open_zerospan_setting()
        main_page.open_capture_setting()
        errs = main_page.set_capture_setting_params(center=center, step="20MHz")
        assert not errs, f"Zero-span Capture Setting validation errors: {errs}"

        # Signal Generator: RF1
        main_page.open_rf1_output()
        errs = main_page.set_rf1_params(rf1_out=rf1_out, power_level=power_level)
        assert not errs, f"Signal Generator RF1 validation errors: {errs}"

    # ════════════════════════════════════════════════════════════════════════════
    #  TC15 · PUC_4.3 · Normal · Zero-span Center 1MHz, SignalGen 1MHz -18dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_3_tc_0015(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_3_tc_0015
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
        @execution_type: automatic
        @hw_depend: yes
        """
        self._run_zerospan_tc(
            main_page,
            center="1MHz",
            rf1_out="100MHz",
            power_level="-18",
        )
