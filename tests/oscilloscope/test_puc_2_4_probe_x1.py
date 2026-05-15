"""
Oscilloscope probe X1 — PUC_2.4
Hỗ trợ probe X1 cho 4 kênh, cấu hình hiển thị amplitude: 2mV/div → 10V/div
(theo các bậc 1, 2, 5).
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc24ProbeX1:
    """PUC_2.4 — Probe X1 amplitude/div manual test suite (TC16–TC27)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    @testcase
    def test_oscilloscope_puc_2_4_tc_0016(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0016
        @brief: SIN 1MHz +-10mV, probes x1, 2mV/div — 4 kênh

        @details: Phát SIN 1MHz biên độ +-10mV vào kênh 1–4, probe x1, V/div=2mV.
                  Verify dạng sóng đúng, biên độ và V/div hiển thị chuẩn.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
             - Máy phát hàm sóng, que đo x1

        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1 của Oscilloscope
                2. Setting máy phát: SIN 1MHz biên độ +-10mV
                3. Nhấn Start để capture, Nhấn Stop để dừng
                4. Setting PC17: kênh 1–4, probe x1, 2mV/div
                5. Quan sát dạng sóng, ghi nhận biên độ và V/div
            [!code]

        @pass_criteria:- Dạng sóng SIN 1MHz
                       - Peak-to-Peak 20mV
                       - 2mV/div (1 ô có giá trị 2mV)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0017(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0017
        @brief: SIN 1MHz +-10mV, probes x1, 5mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Tương tự TC16, đổi 5mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 20mV, 5mV/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0018(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0018
        @brief: SIN 1MHz +-50mV, probes x1, 10mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-50mV; PC17 set probe x1, 10mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 100mV, 10mV/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0019(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0019
        @brief: SIN 1MHz +-50mV, probes x1, 20mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-50mV; PC17 set probe x1, 20mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 100mV, 20mV/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0020(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0020
        @brief: SIN 1MHz +-200mV, probes x1, 50mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-200mV; PC17 set probe x1, 50mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 400mV, 50mV/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0021(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0021
        @brief: SIN 1MHz +-200mV, probes x1, 100mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-200mV; PC17 set probe x1, 100mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 400mV, 100mV/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0022(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0022
        @brief: SIN 1MHz +-500mV, probes x1, 200mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-500mV; PC17 set probe x1, 200mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 1V, 200mV/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0023(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0023
        @brief: SIN 1MHz +-2V, probes x1, 500mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-2V; PC17 set probe x1, 500mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 4V, 500mV/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0024(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0024
        @brief: SIN 1MHz +-3V, probes x1, 1V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-3V; PC17 set probe x1, 1V/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 6V, 1V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0025(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0025
        @brief: SIN 1MHz +-5V, probes x1, 2V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-5V; PC17 set probe x1, 2V/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 10V, 2V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0026(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0026
        @brief: SIN 1MHz +-10V, probes x1, 5V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-10V; PC17 set probe x1, 5V/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 20V, 5V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_4_tc_0027(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_4_tc_0027
        @brief: SIN 1MHz +-20V, probes x1, 10V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-20V; PC17 set probe x1, 10V/div
            [!code]
        @pass_criteria:- SIN 1MHz, Peak-to-Peak 40V, 10V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
