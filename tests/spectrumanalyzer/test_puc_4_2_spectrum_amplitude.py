"""
Spectrum Analyzer Amplitude measurement test suite — PUC_4.2
Đo được Amplitude công suất tín hiệu đơn tần đến 20dBm.
Sweep mode: Start=100kHz, Stop=20GHz, Step=20MHz.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc42SpectrumAmplitude:
    """PUC_4.2 — Spectrum Analyzer Amplitude measurement manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC8 · PUC_4.2 · Normal · SignalGen 10MHz -20dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_2_tc08(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc08
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC9 · PUC_4.2 · Normal · SignalGen 100MHz -15dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_2_tc09(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc09
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC10 · PUC_4.2 · Normal · SignalGen 100MHz -9dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_2_tc10(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc10
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC11 · PUC_4.2 · Normal · SignalGen 100MHz -1dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_2_tc11(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc11
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC12 · PUC_4.2 · Normal · SignalGen 100MHz 6dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_2_tc12(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc12
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC13 · PUC_4.2 · Normal · SignalGen 100MHz 15dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_2_tc13(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc13
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC14 · PUC_4.2 · Normal · SignalGen 100MHz 20dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_2_tc14(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_2_tc14
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
        @execution_type: manual
        @hw_depend: yes
        """
