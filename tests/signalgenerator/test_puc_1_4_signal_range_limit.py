"""
Signal Generator range limit test suite — PUC_1.4
PC17 phát tín hiệu với công suất lên đến 13dBm cho dải tần đến 18GHz.
Verify PC17 trả về lỗi đúng khi vượt quá giới hạn công suất và tần số.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc14RangeLimit:
    """PUC_1.4 — Kiểm tra giới hạn công suất và tần số (abnormal cases)."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC22 · PUC_1.4 · Test abnormal · 13dBm @ 18GHz — out of power range
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_4_tc_0022(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_4_tc_0022
        @brief: Kiểm tra PC17 trả về lỗi khi cài 13dBm @ 18GHz — công suất không hỗ trợ tại dải tần này

        @details: Tại dải tần 18GHz, công suất tối đa hỗ trợ nhỏ hơn 13dBm.
                  PC17 phải phát hiện và trả về thông báo lỗi.

        @pre:- Signal Generator đang bật
             - PC17 đã Connected

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 18GHz, công suất = 13dBm
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi không support công suất này tại range 18GHz

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC23 · PUC_1.4 · Test abnormal · 0dBm @ 21GHz — tần số out of range
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_4_tc_0023(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_4_tc_0023
        @brief: Kiểm tra PC17 trả về lỗi khi cài tần số 21GHz vượt dải cho phép

        @details: Dải tần hỗ trợ tối đa là 20GHz. Setting 21GHz phải bị từ chối.

        @pre:- Signal Generator đang bật
             - PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 21GHz, công suất = 0dBm
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi tần số out of range

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC24 · PUC_1.4 · Test abnormal · 0dBm @ 90MHz — tần số out of range
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_4_tc_0024(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_4_tc_0024
        @brief: Kiểm tra PC17 trả về lỗi khi cài tần số 90MHz dưới dải cho phép

        @details: Dải tần hỗ trợ tối thiểu là 100MHz. Setting 90MHz phải bị từ chối.

        @pre:- Signal Generator đang bật
             - PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 90MHz, công suất = 0dBm
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi tần số out of range

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC25 · PUC_1.4 · Test abnormal · 8dBm @ 500MHz — công suất out of range
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_4_tc_0025(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_4_tc_0025
        @brief: Kiểm tra PC17 trả về lỗi khi cài công suất 8dBm vượt ngưỡng tối đa 7dBm

        @details: Công suất tối đa hỗ trợ là 7dBm. Setting 8dBm phải bị từ chối.

        @pre:- Signal Generator đang bật
             - PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 500MHz, công suất = 8dBm
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi công suất out of range

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC26 · PUC_1.4 · Test abnormal · -21dBm @ 500MHz — công suất out of range
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_4_tc_0026(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_4_tc_0026
        @brief: Kiểm tra PC17 trả về lỗi khi cài công suất -21dBm thấp hơn ngưỡng tối thiểu -20dBm

        @details: Công suất tối thiểu hỗ trợ là -20dBm. Setting -21dBm phải bị từ chối.

        @pre:- Signal Generator đang bật
             - PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 500MHz, công suất = -21dBm
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi công suất out of range

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
