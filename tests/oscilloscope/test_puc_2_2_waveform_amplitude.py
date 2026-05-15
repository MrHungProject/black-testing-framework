"""
Oscilloscope waveform amplitude test suite — PUC_2.2 / 2.2.1 / 2.2.2
Hiển thị waveform SIN 5MHz với các biên độ khác nhau trên 4 kênh.
- PUC_2.2:   Max biên độ +-10V   (TC3-TC6)
- PUC_2.2.1: Biên độ giữa +-5V   (TC7-TC10)
- PUC_2.2.2: Biên độ min +-10mV  (TC11-TC14)
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage

_OSCILLOSCOPE_LABEL = "OSCILLOSCOPE"


class TestPuc22WaveformAmplitude:
    """PUC_2.2 / 2.2.1 / 2.2.2 — Waveform amplitude manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_2.2 · Max biên độ +-10V (TC3–TC6)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_oscilloscope_puc_2_2_tc_0003(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_tc_0003
        @brief: Test kênh 1 @ +-10V — SIN 5MHz, probes x1

        @details: Kết nối máy phát hàm sóng vào kênh 1 Oscilloscope, phát sóng SIN
                  chuẩn tại 5MHz biên độ +-10V, probe x1. Verify dạng sóng SIN chuẩn
                  với Peak-to-Peak 20V.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
             - Máy phát hàm sóng đã sẵn sàng
             - Que đo x1

        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1 của Oscilloscope
                2. Setting máy phát hàm phát sóng SIN chuẩn tại tần số 5MHz biên độ +-10V
                3. Vào phần setting cho kênh 1, chọn probes x1
                4. Nhấn Start để bắt đầu capture tín hiệu
                5. Nhấn Stop để dừng capture
                6. Quan sát dạng sóng trên màn hình PC17, ghi nhận dạng sóng và biên độ
            [!code]

        @pass_criteria:- Dạng sóng là SIN chuẩn với tần số 5MHz
                       - Biên độ sóng Peak-to-Peak là 20V

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        @note: Máy phát tối đa được biên độ là 10V
        """

    @testcase
    def test_oscilloscope_puc_2_2_tc_0004(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_tc_0004
        @brief: Test kênh 2 @ +-10V — SIN 5MHz, probes x1

        @details: Tương tự TC3 nhưng test cho kênh 2.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
        @test_procedure:
            [code]
                Tương tự TC3 nhưng kết nối vào kênh 2
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 20V
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_tc_0005(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_tc_0005
        @brief: Test kênh 3 @ +-10V — SIN 5MHz, probes x1

        @details: Tương tự TC3 nhưng test cho kênh 3.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
        @test_procedure:
            [code]
                Tương tự TC3 nhưng kết nối vào kênh 3
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 20V
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_tc_0006(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_tc_0006
        @brief: Test kênh 4 @ +-10V — SIN 5MHz, probes x1

        @details: Tương tự TC3 nhưng test cho kênh 4.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
        @test_procedure:
            [code]
                Tương tự TC3 nhưng kết nối vào kênh 4
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 20V
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_2.2.1 · Biên độ giữa +-5V (TC7–TC10)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_oscilloscope_puc_2_2_1_tc_0007(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_1_tc_0007
        @brief: Test kênh 1 @ +-5V — SIN 5MHz, probes x1

        @details: Tương tự TC3 nhưng biên độ +-5V.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1
                2. Phát SIN 5MHz biên độ +-5V
                3. Probe x1, capture rồi stop
                4. Quan sát PC17
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 10V
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_1_tc_0008(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_1_tc_0008
        @brief: Test kênh 2 @ +-5V — SIN 5MHz, probes x1

        @details: Tương tự TC7 nhưng test cho kênh 2.

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Tương tự TC7 nhưng kết nối vào kênh 2
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 10V
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_1_tc_0009(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_1_tc_0009
        @brief: Test kênh 3 @ +-5V — SIN 5MHz, probes x1

        @details: Tương tự TC7 nhưng test cho kênh 3.

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Tương tự TC7 nhưng kết nối vào kênh 3
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 10V
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_1_tc_0010(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_1_tc_0010
        @brief: Test kênh 4 @ +-5V — SIN 5MHz, probes x1

        @details: Tương tự TC7 nhưng test cho kênh 4.

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Tương tự TC7 nhưng kết nối vào kênh 4
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 10V
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_2.2.2 · Biên độ min +-10mV (TC11–TC14)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_oscilloscope_puc_2_2_2_tc_0011(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_2_tc_0011
        @brief: Test kênh 1 @ +-10mV — SIN 5MHz, probes x1

        @details: Tương tự TC3 nhưng biên độ +-10mV (biên độ min).

        @pre:- PC17 đã Connected, Oscilloscope đang bật
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1
                2. Phát SIN 5MHz biên độ +-10mV
                3. Probe x1, capture rồi stop
                4. Quan sát PC17
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 20mV
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_2_tc_0012(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_2_tc_0012
        @brief: Test kênh 2 @ +-10mV — SIN 5MHz, probes x1

        @details: Tương tự TC11 nhưng test cho kênh 2.

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1
                2. Phát SIN 5MHz biên độ +-10mV
                3. Probe x1, capture rồi stop
                4. Quan sát PC17
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 20mV
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_2_tc_0013(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_2_tc_0013
        @brief: Test kênh 3 @ +-10mV — SIN 5MHz, probes x1

        @details: Tương tự TC11 nhưng test cho kênh 3.

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1
                2. Phát SIN 5MHz biên độ +-10mV
                3. Probe x1, capture rồi stop
                4. Quan sát PC17
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 20mV
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_2_2_tc_0014(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_2_2_tc_0014
        @brief: Test kênh 4 @ +-10mV — SIN 5MHz, probes x1

        @details: Tương tự TC11 nhưng test cho kênh 4.

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1
                2. Phát SIN 5MHz biên độ +-10mV
                3. Probe x1, capture rồi stop
                4. Quan sát PC17
            [!code]
        @pass_criteria:- Dạng sóng SIN 5MHz, Peak-to-Peak 20mV
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
