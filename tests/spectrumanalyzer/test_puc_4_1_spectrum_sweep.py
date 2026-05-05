"""
Spectrum Analyzer Sweep mode test suite — PUC_4.1
Hiển thị phổ tín hiệu đơn tần bất kì từ 100kHz đến 20GHz (chế độ Swept mode).
Hiển thị 5 tín hiệu từ 100kHz → 20GHz, có nền nhiễu (frame).
Execution type: manual.
"""

import time

import pytest

from core import testcase
from pages.main_page import MainPage

_SPECTRUM_LABEL   = "SPECTRUM"
_SIGNAL_GEN_LABEL = "Signal Genarator"


class TestPuc41SpectrumSweep:
    """
    PUC_4.1 — Spectrum Analyzer Sweep mode manual test suite.

    Setup flow (tự động, không cần TC trước chạy trước):
        fixture _ensure_connected (autouse=True) chạy trước mỗi TC.
        Nếu SPECTRUM hoặc Signal Generator chưa Connected → mở System → Connect
        và kết nối từng thiết bị.
        Mỗi TC đều độc lập và luôn bắt đầu ở trạng thái cả hai thiết bị đã Connected.
    """

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Connect nếu chưa connected. Sau mỗi TC nhấn Preset để reset UI."""
        main_page.open_connect_panel()

        if not main_page.is_device_connected(_SPECTRUM_LABEL):
            main_page.connect_device(_SPECTRUM_LABEL)
            time.sleep(3)

        if not main_page.is_device_connected(_SIGNAL_GEN_LABEL):
            main_page.connect_device(_SIGNAL_GEN_LABEL)
            time.sleep(3)

        yield

        main_page.click_spectrum_preset()

    # ── Helper dùng chung ────────────────────────────────────────────────────

    def _run_sweep_tc(self, main_page: MainPage, rf1_out: str, power_level: str) -> list:
        """
        Luồng chung cho TC4–TC7 PUC_4.1 (Analysis Mode đã được set ở TC3):
          1. Spectrum → Sweep Settings → Frequency (Start=100kHz Stop=20GHz Step=20MHz)
          2. SignalGen → RF1 OUT = rf1_out, Power = power_level
          3. Peak Search → trả về danh sách markers
        """
        # Spectrum: Frequency
        main_page.open_sweep_settings()
        main_page.open_frequency()
        errs = main_page.set_frequency_params(start="100kHz", stop="20GHz", step="20MHz")
        assert not errs, f"Spectrum Frequency validation errors: {errs}"

        # Signal Generator: RF1
        main_page.open_rf1_output()
        errs = main_page.set_rf1_params(rf1_out=rf1_out, power_level=power_level)
        assert not errs, f"Signal Generator RF1 validation errors: {errs}"

        # Markers: xóa cũ rồi Peak Search (Sweep Settings đã mở, click Markers trực tiếp)
        main_page.open_sweep_settings()
        main_page.open_spectrum_markers()
        main_page.remove_all_markers()
        main_page.click_peak_search()
        main_page.spectrum._click_apply()
        return main_page.extract_spectrum_markers()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC3 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 1MHz -18dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_1_tc_0003(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc_0003
        @brief: Sweep mode — SignalGen 1MHz -18dBm → 1 cột phổ tại 1MHz, công suất -20dBm

        @details: Verify PC17 hiển thị đúng phổ tín hiệu đơn tần trong chế độ Swept mode.
                  Cài đặt Sweep: Start=100kHz, Stop=20GHz, Step=20MHz.
                  SignalGen phát 1MHz, -18dBm. Chỉ xuất hiện 1 cột phổ tại tần số tương ứng.

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
                2. Setting Spectrum trên PC17 chế độ Sweep mode:
                   Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=1MHz, POW=-18dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát biểu đồ phổ trên PC17, ghi nhận tần số và công suất cột phổ
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 1MHz
                       - Công suất hiển thị là -20dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_sweep_tc(main_page, rf1_out="80MHz", power_level="-18")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC4 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 1GHz 0dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_1_tc_0004(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc_0004
        @brief: Sweep mode — SignalGen 1GHz 0dBm → 1 cột phổ tại 1GHz, công suất 0dBm

        @details: Tương tự TC3 nhưng SignalGen phát 1GHz, 0dBm.
                  Cài đặt Sweep: Start=100kHz, Stop=20GHz, Step=20MHz.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17 chế độ Sweep mode:
                   Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=1GHz, POW=0dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát biểu đồ phổ trên PC17, ghi nhận tần số và công suất cột phổ
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 1GHz
                       - Công suất hiển thị tương ứng với giá trị đặt (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_sweep_tc(main_page, rf1_out="1GHz", power_level="0")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC5 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 5GHz 3dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_1_tc_0005(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc_0004
        @brief: Sweep mode — SignalGen 5GHz 3dBm → 1 cột phổ tại 5GHz, công suất 3dBm

        @details: Tương tự TC3 nhưng SignalGen phát 5GHz, 3dBm.
                  Cài đặt Sweep: Start=100kHz, Stop=20GHz, Step=20MHz.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17 chế độ Sweep mode:
                   Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=5GHz, POW=3dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát biểu đồ phổ trên PC17, ghi nhận tần số và công suất cột phổ
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 5GHz
                       - Công suất hiển thị tương ứng với giá trị đặt (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_sweep_tc(main_page, rf1_out="5GHz", power_level="3")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC6 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 10GHz 5dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_1_tc_0006(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc_0006
        @brief: Sweep mode — SignalGen 10GHz 5dBm → 1 cột phổ tại 10GHz, công suất 5dBm

        @details: Tương tự TC3 nhưng SignalGen phát 10GHz, 5dBm.
                  Cài đặt Sweep: Start=100kHz, Stop=20GHz, Step=20MHz.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17 chế độ Sweep mode:
                   Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=10GHz, POW=5dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát biểu đồ phổ trên PC17, ghi nhận tần số và công suất cột phổ
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 10GHz
                       - Công suất hiển thị tương ứng với giá trị đặt (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_sweep_tc(main_page, rf1_out="10GHz", power_level="5")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC7 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 18GHz 8dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_1_tc_0007(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc_0007
        @brief: Sweep mode — SignalGen 18GHz 8dBm → 1 cột phổ tại 18GHz, công suất 8dBm

        @details: Tương tự TC3 nhưng SignalGen phát 18GHz, 8dBm.
                  Cài đặt Sweep: Start=100kHz, Stop=20GHz, Step=20MHz.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17 chế độ Sweep mode:
                   Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=18GHz, POW=8dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát biểu đồ phổ trên PC17, ghi nhận tần số và công suất cột phổ
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 18GHz
                       - Công suất hiển thị tương ứng với giá trị đặt (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_sweep_tc(main_page, rf1_out="18GHz", power_level="8")
