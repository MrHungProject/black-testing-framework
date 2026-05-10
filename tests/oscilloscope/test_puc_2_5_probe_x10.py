"""
Oscilloscope probe X10 — PUC_2.5
Hỗ trợ probe X10 cho 4 kênh, cấu hình hiển thị amplitude: 20mV/div → 100V/div
(theo các bậc 1, 2, 5).
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc25ProbeX10:
    """PUC_2.5 — Probe X10 amplitude/div manual test suite (TC28–TC39)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    @testcase
    def test_oscilloscope_puc_2_5_tc_0028(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0028
        @brief: SIN 1MHz +-100mV, probes x10, 20mV/div — 4 kênh

        @details: Probe x10: PC17 hiển thị biên độ x10 lần giá trị máy phát.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
             - Que đo x10
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1–4
                2. Setting máy phát SIN 1MHz +-100mV
                3. PC17: probe x10, 20mV/div
                4. Start, Stop, quan sát dạng sóng
            [!code]
        @pass_criteria:- SIN 1MHz, biên độ hiển thị x10 lần (1V Peak-to-Peak), 20mV/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0029(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0029
        @brief: SIN 1MHz +-100mV, probes x10, 50mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-100mV; PC17 set probe x10, 50mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 200mV (x10), 50mV/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0030(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0030
        @brief: SIN 1MHz +-500mV, probes x10, 100mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-500mV; PC17 set probe x10, 100mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 1V (x10), 100mV/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0031(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0031
        @brief: SIN 1MHz +-500mV, probes x10, 200mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-500mV; PC17 set probe x10, 200mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 1V (x10), 200mV/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0032(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0032
        @brief: SIN 1MHz +-2V, probes x10, 500mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-2V; PC17 set probe x10, 500mV/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 4V (x10), 500mV/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0033(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0033
        @brief: SIN 1MHz +-2V, probes x10, 1V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-2V; PC17 set probe x10, 1V/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 4V (x10), 1V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0034(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0034
        @brief: SIN 1MHz +-5V, probes x10, 2V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-5V; PC17 set probe x10, 2V/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 10V (x10), 2V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0035(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0035
        @brief: SIN 1MHz +-10V, probes x10, 5V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-10V; PC17 set probe x10, 5V/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 20V (x10), 5V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0036(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0036
        @brief: SIN 1MHz +-10V, probes x10, 10V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-10V; PC17 set probe x10, 10V/div
            [!code]
        @pass_criteria:- SIN 1MHz, hiển thị Peak-to-Peak 20V (x10), 10V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0037(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0037
        @brief: Dùng điện lưới để đo, probes x10, 20V/div — 4 kênh

        @pre:- PC17 đã Connected
             - Điện lưới sẵn sàng (cẩn thận an toàn điện)
        @test_procedure:
            [code]
                Đo điện lưới (AC mains); PC17 set probe x10, 20V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 20V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0038(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0038
        @brief: Dùng điện lưới để đo, probes x10, 50V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x10, 50V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 50V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_5_tc_0039(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_5_tc_0039
        @brief: Dùng điện lưới để đo, probes x10, 100V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x10, 100V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 100V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
