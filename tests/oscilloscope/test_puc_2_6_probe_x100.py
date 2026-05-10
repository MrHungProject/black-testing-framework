"""
Oscilloscope probe X100 — PUC_2.6
Hỗ trợ probe X100 cho 4 kênh, cấu hình hiển thị amplitude: 200mV/div → 1000V/div
(theo các bậc 1, 2, 5). Giá trị biên độ trên PC hiển thị sẽ x100 lần giá trị
điện áp phát bởi máy phát sóng.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc26ProbeX100:
    """PUC_2.6 — Probe X100 amplitude/div manual test suite (TC40–TC51)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    @testcase
    def test_oscilloscope_puc_2_6_tc_0040(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0040
        @brief: SIN 1MHz +-100mV, probes x100, 200mV/div — 4 kênh

        @details: Probe x100: PC17 hiển thị biên độ x100 lần giá trị máy phát.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
             - Que đo x100
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1–4
                2. Setting máy phát SIN 1MHz +-100mV
                3. PC17: probe x100, 200mV/div
                4. Start, Stop, quan sát dạng sóng
            [!code]
        @pass_criteria:- Biên độ trên PC x100 lần (Peak-to-Peak 20V), 200mV/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0041(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0041
        @brief: SIN 1MHz +-100mV, probes x100, 500mV/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-100mV; PC17 set probe x100, 500mV/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 20V (x100), 500mV/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0042(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0042
        @brief: SIN 1MHz +-500mV, probes x100, 1V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-500mV; PC17 set probe x100, 1V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 100V (x100), 1V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0043(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0043
        @brief: SIN 1MHz +-500mV, probes x100, 2V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-500mV; PC17 set probe x100, 2V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 100V (x100), 2V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0044(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0044
        @brief: SIN 1MHz +-2V, probes x100, 5V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-2V; PC17 set probe x100, 5V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 400V (x100), 5V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0045(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0045
        @brief: SIN 1MHz +-2V, probes x100, 10V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-2V; PC17 set probe x100, 10V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 400V (x100), 10V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0046(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0046
        @brief: SIN 1MHz +-5V, probes x100, 20V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-5V; PC17 set probe x100, 20V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 1000V (x100), 20V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0047(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0047
        @brief: SIN 1MHz +-10V, probes x100, 50V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-10V; PC17 set probe x100, 50V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 2000V (x100), 50V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0048(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0048
        @brief: SIN 1MHz +-10V, probes x100, 100V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-10V; PC17 set probe x100, 100V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 2000V (x100), 100V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0049(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0049
        @brief: Dùng điện lưới để đo, probes x100, 200V/div — 4 kênh

        @pre:- PC17 đã Connected
             - Điện lưới sẵn sàng (cẩn thận an toàn điện)
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x100, 200V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 200V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0050(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0050
        @brief: Dùng điện lưới để đo, probes x100, 500V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x100, 500V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 500V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_6_tc_0051(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_6_tc_0051
        @brief: Dùng điện lưới để đo, probes x100, 1000V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x100, 1000V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 1000V/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
