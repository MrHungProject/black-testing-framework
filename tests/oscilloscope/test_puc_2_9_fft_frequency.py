"""
Oscilloscope FFT frequency measurement — PUC_2.9
FFT: đo tần số tín hiệu từ 0.1Hz → 250MHz; Độ chính xác 0.1%.
Test 23 điểm tần số phân bố từ 0.1Hz đến 250MHz.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc29FftFrequency:
    """PUC_2.9 — FFT frequency measurement manual test suite (TC100–TC122)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # Common procedure cho mọi TC:
    #   1. Kết nối máy phát hàm sóng với kênh 1 của Oscilloscope
    #   2. Setting máy phát SIN +-5V tại tần số TC tương ứng
    #   3. Chuyển chức năng của Oscilo sang FFT (spectrum)
    #   4. Start capture, Stop
    #   5. Quan sát màn hình PC17, ghi nhận giá trị tần số cột phổ thành phần
    # Pass criteria: có duy nhất 1 cột dải tần đúng tần số phát, độ chính xác 0.1%

    @testcase
    def test_oscilloscope_puc_2_9_tc_0100(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0100
        @brief: FFT — Phát SIN 0.1Hz, +-5V
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 0.1Hz +-5V, chuyển sang FFT mode, capture [!code]
        @pass_criteria:- 1 cột phổ tại 0.1Hz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0101(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0101
        @brief: FFT — Phát SIN 150 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 150Hz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 150Hz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0102(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0102
        @brief: FFT — Phát SIN 888,729.5 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 888729.5 Hz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 888.7295kHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0103(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0103
        @brief: FFT — Phát SIN 2,356,325.7 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 2.3563257MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 2.3563257MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0104(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0104
        @brief: FFT — Phát SIN 8,524,154.1 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 8.5241541MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 8.5241541MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0105(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0105
        @brief: FFT — Phát SIN 15,626,166.5 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 15.6261665MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 15.6261665MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0106(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0106
        @brief: FFT — Phát SIN 58,312,974 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 58.312974MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 58.312974MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0107(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0107
        @brief: FFT — Phát SIN 74,016,185.7 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 74.0161857MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 74.0161857MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0108(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0108
        @brief: FFT — Phát SIN 82,972,151.4 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 82.9721514MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 82.9721514MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0109(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0109
        @brief: FFT — Phát SIN 97,316,722.7 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 97.3167227MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 97.3167227MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0110(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0110
        @brief: FFT — Phát SIN 110,851,616 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 110.851616MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 110.851616MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0111(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0111
        @brief: FFT — Phát SIN 117,968,267.6 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 117.9682676MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 117.9682676MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0112(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0112
        @brief: FFT — Phát SIN 129,113,050.5 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 129.1130505MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 129.1130505MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0113(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0113
        @brief: FFT — Phát SIN 149,797,190 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 149.79719MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 149.79719MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0114(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0114
        @brief: FFT — Phát SIN 155,163,644.8 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 155.1636448MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 155.1636448MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0115(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0115
        @brief: FFT — Phát SIN 173,941,830.9 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 173.9418309MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 173.9418309MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0116(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0116
        @brief: FFT — Phát SIN 183,766,764.4 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 183.7667644MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 183.7667644MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0117(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0117
        @brief: FFT — Phát SIN 194,368,140.4 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 194.3681404MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 194.3681404MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0118(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0118
        @brief: FFT — Phát SIN 203,068,422.2 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 203.0684222MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 203.0684222MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0119(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0119
        @brief: FFT — Phát SIN 213,436,270.7 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 213.4362707MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 213.4362707MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0120(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0120
        @brief: FFT — Phát SIN 230,796,340.9 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 230.7963409MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 230.7963409MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0121(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0121
        @brief: FFT — Phát SIN 240,158,783.3 Hz
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 240.1587833MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 240.1587833MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_9_tc_0122(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_9_tc_0122
        @brief: FFT — Phát SIN 250,000,000 Hz (biên trên)
        @pre:- PC17 đã Connected
        @test_procedure:[code] Phát SIN 250MHz, FFT mode [!code]
        @pass_criteria:- 1 cột phổ tại 250MHz, độ chính xác 0.1%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
