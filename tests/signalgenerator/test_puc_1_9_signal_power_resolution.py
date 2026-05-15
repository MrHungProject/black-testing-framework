"""
Signal Generator power resolution test suite — PUC_1.9
PC17 phát công suất tín hiệu với độ phân giải 0.01 dBm.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc19PowerResolution:
    """
    PUC_1.9 — Kiểm tra độ phân giải công suất 0.01 dBm.
    TC50–TC54: test normal tại nhiều mức công suất.
    TC55: test abnormal với độ phân giải sub-0.01dBm.
    """

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC50 · PUC_1.9 · Test normal · -19.5dBm @ 1GHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_9_tc_0050(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_9_tc_0050
        @brief: Kiểm tra độ phân giải công suất 0.01dBm quanh điểm -19.5dBm @ 1GHz

        @details: Verify UI PC17 cho phép setting công suất với độ phân giải 0.01dBm.
                  Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn quanh -19.5dBm, bước 0.01dBm.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 1GHz, công suất = -19.5dBm
                - Điều chỉnh 5 điểm công suất nhỏ hơn (step 0.01dBm): -19.55 → -19.51 dBm
                - Điều chỉnh 5 điểm công suất lớn hơn (step 0.01dBm): -19.49 → -19.45 dBm
                - Ghi nhận giá trị công suất mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting công suất có độ phân giải 0.01dBm
                       - Sai số công suất theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC51 · PUC_1.9 · Test normal · -10.5dBm @ 1GHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_9_tc_0051(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_9_tc_0051
        @brief: Kiểm tra độ phân giải công suất 0.01dBm quanh điểm -10.5dBm @ 1GHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 1GHz, công suất = -10.5dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 0.01dBm
                - Ghi nhận giá trị công suất mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting công suất có độ phân giải 0.01dBm
                       - Sai số công suất theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC52 · PUC_1.9 · Test normal · -5.2dBm @ 1GHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_9_tc_0052(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_9_tc_0052
        @brief: Kiểm tra độ phân giải công suất 0.01dBm quanh điểm -5.2dBm @ 1GHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 1GHz, công suất = -5.2dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 0.01dBm
                - Ghi nhận giá trị công suất mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting công suất có độ phân giải 0.01dBm
                       - Sai số công suất theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC53 · PUC_1.9 · Test normal · 0dBm @ 1GHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_9_tc_0053(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_9_tc_0053
        @brief: Kiểm tra độ phân giải công suất 0.01dBm quanh điểm 0dBm @ 1GHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 1GHz, công suất = 0dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 0.01dBm
                - Ghi nhận giá trị công suất mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting công suất có độ phân giải 0.01dBm
                       - Sai số công suất theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC54 · PUC_1.9 · Test normal · 5dBm @ 1GHz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_9_tc_0054(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_9_tc_0054
        @brief: Kiểm tra độ phân giải công suất 0.01dBm quanh điểm 5dBm @ 1GHz

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 1GHz, công suất = 5dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 0.01dBm
                - Ghi nhận giá trị công suất mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting công suất có độ phân giải 0.01dBm
                       - Sai số công suất theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC55 · PUC_1.9 · Test abnormal · 5.005dBm — độ phân giải sub-0.01dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_9_tc_0055(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_9_tc_0055
        @brief: PC17 trả về lỗi khi cài công suất 5.005dBm — độ phân giải 0.001dBm không được hỗ trợ

        @details: Độ phân giải công suất tối thiểu hỗ trợ là 0.01dBm.
                  Setting 5.005dBm (độ phân giải 0.001dBm) phải bị từ chối.

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 1GHz, công suất = 5.005dBm
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi không hỗ trợ độ phân giải của giá trị công suất này

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
