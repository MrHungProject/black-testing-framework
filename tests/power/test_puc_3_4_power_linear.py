"""
Linear display mode test suite — PUC_3.4
Kiểm tra chế độ hiển thị Linear (mW/nW) của Power Meter từ UI PC17.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc34PowerLinear:
    """PUC_3.4 — Linear display mode manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.4 · Chế độ hiển thị Linear (TC29–TC33)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_power_puc_3_4_tc_0029(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_4_tc_0029
        @brief: Linear display — SignalGen 5GHz, 10dBm → expected 10mW

        @details: Verify PC17 hiển thị đúng giá trị công suất ở chế độ Linear (mW).
                  10dBm tương đương 10mW trên thang tuyến tính.

        @pre:- Bật nguồn Powermeter và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Powermeter
             - PC17 đã Connected, Average=10, Display=dB

        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz trên PC17
                - Set SignalGen: FREQ=5GHz, POW=10dBm, OUTPUT ON
                - Chuyển chế độ hiển thị sang Linear (mW)
                - Ghi nhận giá trị công suất mW trên PC17
                - Kiểm tra: giá trị = 10mW, sai số < 1.71%
            [!code]

        @pass_criteria:- PC17 hiển thị ~10mW
                       - Sai số < 1.71%

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_4_tc_0030(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_4_tc_0030
        @brief: Linear display — SignalGen 5GHz, 7dBm → expected 5.01mW

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=7dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW)
                - Ghi nhận giá trị mW, kiểm tra ≈ 5.01mW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~5.01mW, sai số < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_4_tc_0031(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_4_tc_0031
        @brief: Linear display — SignalGen 5GHz, 0dBm → expected 1mW

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=0dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW)
                - Ghi nhận giá trị mW, kiểm tra = 1mW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~1mW, sai số < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_4_tc_0032(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_4_tc_0032
        @brief: Linear display — SignalGen 5GHz, -13dBm → expected 0.0501mW

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=-13dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW)
                - Ghi nhận giá trị mW, kiểm tra ≈ 0.0501mW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~0.0501mW, sai số < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_4_tc_0033(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_4_tc_0033
        @brief: Linear display — SignalGen 5GHz, -55dBm → expected 3.16nW

        @details: -55dBm tương đương 3.162nW (3.162e-6 mW) trên thang tuyến tính.

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=-55dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW/nW)
                - Ghi nhận giá trị, kiểm tra ≈ 3.16nW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~3.16nW, sai số < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
