"""
Oscilloscope Time/Div sweep — PUC_2.8
Thay đổi thời gian hiển thị trên màn hình từ 2ns/div → 1000s/div, cho 4 kênh
(theo các bậc 1, 2, 4).
Common signal: SIN 1MHz +-5V, probes x1, 5V/div.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc28TimeDiv:
    """PUC_2.8 — Time/Div sweep manual test suite (TC64–TC99)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ── Helper docstring (chuẩn cho mọi TC) ──────────────────────────────────
    #
    # @pre:- PC17 đã Connected, Oscilloscope đang bật
    #      - Máy phát hàm sóng, que đo x1
    # @test_procedure:
    #     [code]
    #         1. Kết nối máy phát hàm sóng với kênh 1
    #         2. Setting máy phát SIN 1MHz +-5V
    #         3. PC17: kênh 1–4, probe x1, 5V/div, Time/Div tương ứng TC
    #         4. Start, Stop, quan sát dạng sóng
    #     [!code]
    # @pass_criteria:- SIN 1MHz, Peak-to-Peak 10V, 5V/div, s/div đúng giá trị TC
    # @test_level: software / @test_type: functional
    # @execution_type: manual / @hw_depend: yes

    @testcase
    def test_oscilloscope_puc_2_8_tc_0064(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0064
        @brief: Time/Div = 2ns/div — SIN 1MHz +-5V, probes x1, 5V/div, 4 kênh
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 2ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 2ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0065(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0065
        @brief: Time/Div = 4ns/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 4ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 4ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0066(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0066
        @brief: Time/Div = 10ns/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 10ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 10ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0067(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0067
        @brief: Time/Div = 20ns/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 20ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 20ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0068(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0068
        @brief: Time/Div = 40ns/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 40ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 40ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0069(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0069
        @brief: Time/Div = 100ns/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 100ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 100ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0070(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0070
        @brief: Time/Div = 200ns/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 200ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 200ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0071(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0071
        @brief: Time/Div = 400ns/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 400ns/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 400ns/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0072(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0072
        @brief: Time/Div = 1us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 1us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 1us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0073(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0073
        @brief: Time/Div = 2us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 2us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 2us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0074(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0074
        @brief: Time/Div = 4us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 4us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 4us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0075(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0075
        @brief: Time/Div = 10us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 10us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 10us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0076(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0076
        @brief: Time/Div = 20us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 20us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 20us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0077(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0077
        @brief: Time/Div = 40us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 40us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 40us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0078(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0078
        @brief: Time/Div = 100us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 100us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 100us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0079(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0079
        @brief: Time/Div = 200us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 200us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 200us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0080(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0080
        @brief: Time/Div = 400us/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 400us/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 400us/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        @note: Có thể không hiển thị lên biểu đồ ở mức Time/Div lớn
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0081(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0081
        @brief: Time/Div = 1ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 1ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 1ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0082(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0082
        @brief: Time/Div = 2ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 2ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 2ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0083(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0083
        @brief: Time/Div = 4ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 4ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 4ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0084(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0084
        @brief: Time/Div = 10ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 10ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 10ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0085(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0085
        @brief: Time/Div = 20ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 20ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 20ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0086(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0086
        @brief: Time/Div = 40ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 40ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 40ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0087(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0087
        @brief: Time/Div = 100ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 100ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 100ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0088(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0088
        @brief: Time/Div = 200ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 200ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 200ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0089(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0089
        @brief: Time/Div = 400ms/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 400ms/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 400ms/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0090(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0090
        @brief: Time/Div = 1s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 1s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 1s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0091(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0091
        @brief: Time/Div = 2s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 2s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 2s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0092(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0092
        @brief: Time/Div = 4s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 4s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 4s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0093(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0093
        @brief: Time/Div = 10s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 10s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 10s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0094(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0094
        @brief: Time/Div = 20s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 20s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 20s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0095(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0095
        @brief: Time/Div = 40s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 40s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 40s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0096(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0096
        @brief: Time/Div = 100s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 100s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 100s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0097(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0097
        @brief: Time/Div = 200s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 200s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 200s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0098(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0098
        @brief: Time/Div = 400s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 400s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 400s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_oscilloscope_puc_2_8_tc_0099(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_8_tc_0099
        @brief: Time/Div = 1000s/div
        @pre:- PC17 đã Connected
        @test_procedure:[code] SIN 1MHz +-5V, probe x1, 5V/div, 1000s/div [!code]
        @pass_criteria:- SIN 1MHz, P2P 10V, 5V/div, 1000s/div
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
