"""
Spectrum Analyzer Sweep mode test suite — PUC_4.1
Hiển thị phổ tín hiệu đơn tần bất kì từ 100kHz đến 20GHz (chế độ Swept mode).
Hiển thị 5 tín hiệu từ 100kHz → 20GHz, có nền nhiễu (frame).
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc41SpectrumSweep:
    """PUC_4.1 — Spectrum Analyzer Sweep mode manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC3 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 1MHz -18dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_1_tc03(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc03
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC4 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 1GHz 0dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_1_tc04(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc04
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC5 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 5GHz 3dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_1_tc05(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc05
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC6 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 10GHz 5dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_1_tc06(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc06
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
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC7 · PUC_4.1 · Normal · Sweep 100kHz–20GHz, SignalGen 18GHz 8dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_4_1_tc07(self, main_page: MainPage):
        """
        @test_id: test_spectrum_puc_4_1_tc07
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
        @execution_type: manual
        @hw_depend: yes
        """
