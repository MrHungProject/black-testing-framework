"""
Oscilloscope DDS pulse signal generation — PUC_2.11
Phát tín hiệu xung Square, Frequency đến 25MHz, Duty cycle 100/89/34/10/1 %.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc211DdsPulse:
    """PUC_2.11 — DDS pulse signal generation manual test suite (TC146–TC150)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # Common procedure:
    #   1. Kết nối output PC17 với kênh 1 scope ngoài
    #   2. Setting PC17 phát Square tại tần số TC, +-3.5V
    #   3. Start phát PC17, capture scope ngoài
    #   4. Stop, đo tần số và độ rộng xung trên scope ngoài
    # Pass criteria: tần số đúng setting PC17, độ rộng xung đúng

    @testcase
    def test_oscilloscope_puc_2_11_tc_0146(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_11_tc_0146
        @brief: DDS Pulse — PC17 phát Square 1000Hz +-3.5V

        @details: Phát tín hiệu xung Square 1000Hz, biên độ +-3.5V.
                  Duty cycle theo group: 100/89/34/10/1 %.

        @pre:- PC17 đã Connected, scope ngoài sẵn sàng, que đo x1
        @test_procedure:[code] PC17 phát Square 1000Hz +-3.5V, scope ngoài đo [!code]
        @pass_criteria:- Tần số scope ngoài = 1000Hz
                       - Độ rộng xung đúng theo duty cycle
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_11_tc_0147(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_11_tc_0147
        @brief: DDS Pulse — PC17 phát Square 729,463 Hz +-3.5V

        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát Square 729463Hz +-3.5V, scope ngoài đo [!code]
        @pass_criteria:- Tần số = 729463Hz, độ rộng xung đúng
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_11_tc_0148(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_11_tc_0148
        @brief: DDS Pulse — PC17 phát Square 5,498,649 Hz +-3.5V

        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát Square 5.498649MHz +-3.5V [!code]
        @pass_criteria:- Tần số = 5.498649MHz, độ rộng xung đúng
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_11_tc_0149(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_11_tc_0149
        @brief: DDS Pulse — PC17 phát Square 15,205,131 Hz +-3.5V

        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát Square 15.205131MHz +-3.5V [!code]
        @pass_criteria:- Tần số = 15.205131MHz, độ rộng xung đúng
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_11_tc_0150(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_11_tc_0150
        @brief: DDS Pulse — PC17 phát Square 25,000,000 Hz +-3.5V (biên trên)

        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát Square 25MHz +-3.5V [!code]
        @pass_criteria:- Tần số = 25MHz, độ rộng xung đúng
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
