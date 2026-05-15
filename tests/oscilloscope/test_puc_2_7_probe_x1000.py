"""
Oscilloscope probe X1000 — PUC_2.7
Hỗ trợ probe X1000 cho 4 kênh, cấu hình hiển thị amplitude: 2V/div → 10000V/div
(theo các bậc 1, 2, 5). Giá trị biên độ trên PC hiển thị sẽ x100 lần giá trị
điện áp phát bởi máy phát sóng (tham chiếu probe x10 trong SUT description).
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc27ProbeX1000:
    """PUC_2.7 — Probe X1000 amplitude/div manual test suite (TC52–TC63)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    @testcase
    def test_oscilloscope_puc_2_7_tc_0052(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0052
        @brief: SIN 1MHz +-100mV, probes x1000, 2V/div — 4 kênh

        @details: Probe x1000: PC17 hiển thị biên độ x1000 lần giá trị máy phát.

        @pre:- PC17 đã Connected, Oscilloscope đang bật
             - Que đo x1000
        @test_procedure:
            [code]
                1. Kết nối máy phát hàm sóng với kênh 1–4
                2. Setting máy phát SIN 1MHz +-100mV
                3. PC17: probe x1000, 2V/div
                4. Start, Stop, quan sát dạng sóng
            [!code]
        @pass_criteria:- Biên độ hiển thị x1000 (Peak-to-Peak 200V), 2V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0053(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0053
        @brief: SIN 1MHz +-100mV, probes x1000, 5V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-100mV; PC17 set probe x1000, 5V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 200V (x1000), 5V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0054(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0054
        @brief: SIN 1MHz +-500mV, probes x1000, 10V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-500mV; PC17 set probe x1000, 10V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 1000V (x1000), 10V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0055(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0055
        @brief: SIN 1MHz +-500mV, probes x1000, 20V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-500mV; PC17 set probe x1000, 20V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 1000V (x1000), 20V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0056(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0056
        @brief: SIN 1MHz +-2V, probes x1000, 50V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-2V; PC17 set probe x1000, 50V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 4000V (x1000), 50V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0057(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0057
        @brief: SIN 1MHz +-2V, probes x1000, 100V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-2V; PC17 set probe x1000, 100V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 4000V (x1000), 100V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0058(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0058
        @brief: SIN 1MHz +-5V, probes x1000, 200V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-5V; PC17 set probe x1000, 200V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 10000V (x1000), 200V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0059(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0059
        @brief: SIN 1MHz +-10V, probes x1000, 500V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-10V; PC17 set probe x1000, 500V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 20000V (x1000), 500V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0060(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0060
        @brief: SIN 1MHz +-10V, probes x1000, 1000V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Phát SIN 1MHz +-10V; PC17 set probe x1000, 1000V/div
            [!code]
        @pass_criteria:- Peak-to-Peak hiển thị 20000V (x1000), 1000V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0061(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0061
        @brief: Dùng điện lưới để đo, probes x1000, 2000V/div — 4 kênh

        @pre:- PC17 đã Connected
             - Điện lưới sẵn sàng (cẩn thận an toàn điện)
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x1000, 2000V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 2000V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0062(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0062
        @brief: Dùng điện lưới để đo, probes x1000, 5000V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x1000, 5000V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 5000V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_7_tc_0063(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_7_tc_0063
        @brief: Dùng điện lưới để đo, probes x1000, 10000V/div — 4 kênh

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                Đo điện lưới; PC17 set probe x1000, 10000V/div
            [!code]
        @pass_criteria:- Dạng sóng hiển thị, 10000V/div
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
