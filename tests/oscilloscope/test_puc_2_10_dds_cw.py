"""
Oscilloscope DDS CW signal generation — PUC_2.10
Phát tín hiệu CW từ 0.1Hz → 250MHz; Sai số tần số 0.1%; Amplitude max +-3.5V.
Test 23 điểm tần số phân bố từ 0.1Hz đến 250MHz.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc210DdsCw:
    """PUC_2.10 — DDS CW signal generation manual test suite (TC123–TC145)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # Common procedure cho mọi TC:
    #   1. Kết nối output của Oscilloscope (PC17) với kênh 1 của Oscilloscope ngoài
    #   2. Setting PC17 phát SIN +-3.5V tại tần số TC tương ứng
    #   3. Start phát trên PC17, capture trên scope ngoài
    #   4. Stop phát, Stop capture
    #   5. Quan sát scope ngoài, ghi nhận tần số tín hiệu
    # Pass criteria: tần số scope ngoài đúng giá trị PC17 phát, sai số 0.1%

    @testcase
    def test_oscilloscope_puc_2_10_tc_0123(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0123
        @brief: DDS CW — PC17 phát SIN 0.1Hz +-3.5V

        @pre:- PC17 đã Connected, có scope ngoài, que đo x1
        @test_procedure:[code] PC17 phát SIN 0.1Hz +-3.5V, scope ngoài capture [!code]
        @pass_criteria:- Tần số scope ngoài = 0.1Hz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0124(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0124
        @brief: DDS CW — PC17 phát SIN 371Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 371Hz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 371Hz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0125(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0125
        @brief: DDS CW — PC17 phát SIN 542,228.8 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 542228.8Hz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 542228.8Hz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0126(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0126
        @brief: DDS CW — PC17 phát SIN 5,017,834.7 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 5.0178347MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 5.0178347MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0127(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0127
        @brief: DDS CW — PC17 phát SIN 16,100,495.4 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 16.1004954MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 16.1004954MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0128(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0128
        @brief: DDS CW — PC17 phát SIN 38,453,175.6 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 38.4531756MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 38.4531756MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0129(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0129
        @brief: DDS CW — PC17 phát SIN 60,225,339.9 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 60.2253399MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 60.2253399MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0130(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0130
        @brief: DDS CW — PC17 phát SIN 71,650,911.2 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 71.6509112MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 71.6509112MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0131(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0131
        @brief: DDS CW — PC17 phát SIN 83,465,907.3 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 83.4659073MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 83.4659073MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0132(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0132
        @brief: DDS CW — PC17 phát SIN 97,700,305.9 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 97.7003059MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 97.7003059MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0133(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0133
        @brief: DDS CW — PC17 phát SIN 104,918,617 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 104.918617MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 104.918617MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0134(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0134
        @brief: DDS CW — PC17 phát SIN 121,642,619.5 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 121.6426195MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 121.6426195MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0135(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0135
        @brief: DDS CW — PC17 phát SIN 136,483,009.8 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 136.4830098MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 136.4830098MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0136(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0136
        @brief: DDS CW — PC17 phát SIN 148,828,995.7 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 148.8289957MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 148.8289957MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0137(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0137
        @brief: DDS CW — PC17 phát SIN 155,316,780.1 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 155.3167801MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 155.3167801MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0138(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0138
        @brief: DDS CW — PC17 phát SIN 167,543,371.3 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 167.5433713MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 167.5433713MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0139(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0139
        @brief: DDS CW — PC17 phát SIN 181,975,125.8 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 181.9751258MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 181.9751258MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0140(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0140
        @brief: DDS CW — PC17 phát SIN 198,614,252.2 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 198.6142522MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 198.6142522MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0141(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0141
        @brief: DDS CW — PC17 phát SIN 205,131,496 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 205.131496MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 205.131496MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0142(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0142
        @brief: DDS CW — PC17 phát SIN 217,501,864.3 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 217.5018643MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 217.5018643MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0143(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0143
        @brief: DDS CW — PC17 phát SIN 226,442,653.2 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 226.4426532MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 226.4426532MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0144(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0144
        @brief: DDS CW — PC17 phát SIN 248,205,910.1 Hz +-3.5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 248.2059101MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 248.2059101MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_10_tc_0145(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_10_tc_0145
        @brief: DDS CW — PC17 phát SIN 250,000,000 Hz +-3.5V (biên trên)
        @pre:- PC17 đã Connected
        @test_procedure:[code] PC17 phát SIN 250MHz +-3.5V [!code]
        @pass_criteria:- Tần số scope ngoài = 250MHz, sai số 0.1%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
