"""
Signal Generator CW tone test suite — PUC_1.2
PC17 điều khiển phát tín hiệu đơn tần bất kỳ trong dải 100MHz–20GHz,
công suất bất kỳ từ -20 → 7 dBm.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc12CW:
    """
    PUC_1.2 — Phát tín hiệu đơn tần (CW) test suite.
    TC3–TC21: test biên và test normal với Power Meter đo giá trị thực.
    """

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    _PROCEDURE_COMMON = """
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator phát tín hiệu đơn tần tại công suất và tần số tương ứng
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]"""

    _PASS_COMMON = "- Sai số công suất đo được nằm trong ngưỡng ± 1.25 dB so với giá trị đặt"

    # ════════════════════════════════════════════════════════════════════════════
    #  TC3 · PUC_1.2 · Test biên · Phát 0dBm @ 100MHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_2_tc_0003(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0003
        @brief: Phát tín hiệu CW 0dBm tại tần số biên thấp 100MHz

        @details: Verify Signal Generator phát đúng công suất 0dBm tại tần số biên thấp 100MHz.
                  Đo bằng Power Meter, sai số cho phép ± 1.25 dB.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 100MHz, công suất = 0dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 0dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC4 · PUC_1.2 · Test biên · Phát 0dBm @ 20000MHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_2_tc_0004(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0004
        @brief: Phát tín hiệu CW 0dBm tại tần số biên cao 20000MHz

        @details: Verify Signal Generator phát đúng công suất tại tần số biên cao 20GHz.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 20000MHz, công suất = 0dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 0dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC5 · PUC_1.2 · Test biên · Phát -20dBm @ 100MHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_2_tc_0005(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0005
        @brief: Phát tín hiệu CW công suất biên thấp -20dBm @ 100MHz

        @details: Verify Signal Generator phát đúng công suất biên thấp -20dBm tại 100MHz.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 100MHz, công suất = -20dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: -20dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC6 · PUC_1.2 · Test biên · Phát 7dBm @ 100MHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_2_tc_0006(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0006
        @brief: Phát tín hiệu CW công suất biên cao 7dBm @ 100MHz

        @details: Verify Signal Generator phát đúng công suất biên cao 7dBm tại 100MHz.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 100MHz, công suất = 7dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 7dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC7–TC21 · PUC_1.2 · Test normal · Các điểm tần số và công suất thông thường
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_2_tc_0007(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0007
        @brief: Phát tín hiệu CW -18dBm @ 463MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 463MHz, công suất = -18dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: -18dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0008(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0008
        @brief: Phát tín hiệu CW -18dBm @ 6922MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 6922MHz, công suất = -18dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: -18dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0009(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0009
        @brief: Phát tín hiệu CW -18dBm @ 10729MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 10729MHz, công suất = -18dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: -18dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0010(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0010
        @brief: Phát tín hiệu CW -18dBm @ 12898MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 12898MHz, công suất = -18dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: -18dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0011(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0011
        @brief: Phát tín hiệu CW -18dBm @ 18203MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 18203MHz, công suất = -18dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: -18dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0012(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0012
        @brief: Phát tín hiệu CW 0dBm @ 4021MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 4021MHz, công suất = 0dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 0dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0013(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0013
        @brief: Phát tín hiệu CW 0dBm @ 4650MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 4650MHz, công suất = 0dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 0dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0014(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0014
        @brief: Phát tín hiệu CW 0dBm @ 11355MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 11355MHz, công suất = 0dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 0dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0015(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0015
        @brief: Phát tín hiệu CW 0dBm @ 15690MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 15690MHz, công suất = 0dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 0dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0016(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0016
        @brief: Phát tín hiệu CW 0dBm @ 19800MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 19800MHz, công suất = 0dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 0dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0017(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0017
        @brief: Phát tín hiệu CW 6dBm @ 3036MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 3036MHz, công suất = 6dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 6dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0018(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0018
        @brief: Phát tín hiệu CW 6dBm @ 4579MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 4579MHz, công suất = 6dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 6dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0019(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0019
        @brief: Phát tín hiệu CW 6dBm @ 10170MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 10170MHz, công suất = 6dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 6dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0020(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0020
        @brief: Phát tín hiệu CW 6dBm @ 15494MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 15494MHz, công suất = 6dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 6dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_2_tc_0021(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_2_tc_0021
        @brief: Phát tín hiệu CW 6dBm @ 19155MHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 19155MHz, công suất = 6dBm
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được
            [!code]

        @pass_criteria:- Công suất đo được: 6dBm ± 1.25 dB

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
