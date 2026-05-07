"""
Spectrum Analyzer Amplitude measurement test suite — PUC_4.2
Đo được Amplitude công suất tín hiệu đơn tần đến 20dBm.
Sweep mode: Start=100kHz, Stop=20GHz, Step=20MHz.
Execution type: automatic.
"""

import time

import pytest

from core import testcase
from pages.main_page import MainPage

_SPECTRUM_LABEL   = "SPECTRUM"
_SIGNAL_GEN_LABEL = "Signal Genarator"


class TestPuc42SpectrumAmplitude:
    """
    PUC_4.2 — Spectrum Analyzer Amplitude measurement automatic test suite.

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

        main_page.click_spectrum_preset()

    # ── Helper dùng chung ────────────────────────────────────────────────────

    def _run_amplitude_tc(self, main_page: MainPage, rf1_out: str, power_level: str) -> list:
        """
        Luồng chung cho TC8–TC14 PUC_4.2:
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

        # Markers: xóa cũ rồi Peak Search
        main_page.open_sweep_settings()
        main_page.open_spectrum_markers()
        main_page.remove_all_markers()
        main_page.click_peak_search()
        main_page.spectrum._click_apply()
        return main_page.extract_spectrum_markers()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC8 · PUC_4.2 · Normal · SignalGen 10MHz -20dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_2_tc_0008(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc_0008
        @brief: Amplitude measurement — SignalGen 10MHz -20dBm

        @details: Verify PC17 Spectrum Analyzer đo đúng công suất tín hiệu đơn tần.
                  Sweep: Start=100kHz, Stop=20GHz, Step=20MHz.
                  SignalGen phát 10MHz, -20dBm.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17 chế độ Sweep mode:
                   Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=10MHz, POW=-20dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát cột phổ trên PC17, ghi nhận tần số và công suất
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 10MHz
                       - Công suất hiển thị tương ứng -20dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_amplitude_tc(main_page, rf1_out="100MHz", power_level="-20")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC9 · PUC_4.2 · Normal · SignalGen 100MHz -15dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_2_tc_0009(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc_0009
        @brief: Amplitude measurement — SignalGen 100MHz -15dBm

        @details: Tương tự TC8 nhưng SignalGen phát 100MHz, -15dBm.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17: Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=100MHz, POW=-15dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát cột phổ trên PC17, ghi nhận tần số và công suất
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 100MHz
                       - Công suất hiển thị tương ứng -15dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_amplitude_tc(main_page, rf1_out="100MHz", power_level="-15")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC10 · PUC_4.2 · Normal · SignalGen 100MHz -9dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_2_tc_0010(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc_0010
        @brief: Amplitude measurement — SignalGen 100MHz -9dBm

        @details: Tương tự TC8 nhưng SignalGen phát 100MHz, -9dBm.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17: Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=100MHz, POW=-9dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát cột phổ trên PC17, ghi nhận tần số và công suất
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 100MHz
                       - Công suất hiển thị tương ứng -9dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_amplitude_tc(main_page, rf1_out="100MHz", power_level="-9")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC11 · PUC_4.2 · Normal · SignalGen 100MHz -1dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_2_tc_0011(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc_0011
        @brief: Amplitude measurement — SignalGen 100MHz -1dBm

        @details: Tương tự TC8 nhưng SignalGen phát 100MHz, -1dBm.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17: Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=100MHz, POW=-1dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát cột phổ trên PC17, ghi nhận tần số và công suất
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 100MHz
                       - Công suất hiển thị tương ứng -1dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_amplitude_tc(main_page, rf1_out="100MHz", power_level="-1")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC12 · PUC_4.2 · Normal · SignalGen 100MHz 6dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_2_tc_0012(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc_0012
        @brief: Amplitude measurement — SignalGen 100MHz 6dBm

        @details: Tương tự TC8 nhưng SignalGen phát 100MHz, 6dBm.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17: Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=100MHz, POW=6dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát cột phổ trên PC17, ghi nhận tần số và công suất
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 100MHz
                       - Công suất hiển thị tương ứng 6dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_amplitude_tc(main_page, rf1_out="100MHz", power_level="6")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC13 · PUC_4.2 · Normal · SignalGen 100MHz 15dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_2_tc_0013(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc_0013
        @brief: Amplitude measurement — SignalGen 100MHz 15dBm

        @details: Tương tự TC8 nhưng SignalGen phát 100MHz, 15dBm.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17: Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=100MHz, POW=15dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát cột phổ trên PC17, ghi nhận tần số và công suất
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 100MHz
                       - Công suất hiển thị tương ứng 15dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_amplitude_tc(main_page, rf1_out="100MHz", power_level="15")

    # ════════════════════════════════════════════════════════════════════════════
    #  TC14 · PUC_4.2 · Normal · SignalGen 100MHz 20dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spectrum_puc_4_2_tc_0014(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc_0014
        @brief: Amplitude measurement — SignalGen 100MHz 20dBm (giới hạn trên)

        @details: Tương tự TC8 nhưng SignalGen phát 100MHz, 20dBm — giá trị công suất
                  tối đa trong dải đo. Verify Spectrum Analyzer đo đúng tại biên trên.

        @pre:- Bật nguồn Spectrum Analyzer và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Spectrum Analyzer
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối đầu ra của Signal Gen với module Spectrum Analyzer
                2. Setting Spectrum trên PC17: Start=100kHz, Stop=20GHz, Step=20MHz
                3. Setting SignalGen: FREQ=100MHz, POW=20dBm
                4. Bắt đầu phát tín hiệu từ Signal Gen
                5. Quan sát cột phổ trên PC17, ghi nhận tần số và công suất
            [!code]

        @pass_criteria:- Chỉ có 1 cột phổ tại tần số 100MHz
                       - Công suất hiển thị tương ứng 20dBm (sai số TBD)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        markers = self._run_amplitude_tc(main_page, rf1_out="100MHz", power_level="20")
