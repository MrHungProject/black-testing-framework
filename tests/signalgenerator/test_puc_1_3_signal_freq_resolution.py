"""
Signal Generator frequency resolution test suite — PUC_1.3
PC17 điều khiển tín hiệu tần số đơn tần với độ phân giải 1Hz.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc13FreqResolution:
    """
    PUC_1.3 — Kiểm tra độ phân giải tần số 1Hz.
    TC27–TC31: test normal tại nhiều điểm tần số.
    TC32: test abnormal với độ phân giải sub-Hz.
    """

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC27 · PUC_1.3 · Test normal · 0dBm @ 585,495,239 Hz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_3_tc_0027(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_3_tc_0027
        @brief: Kiểm tra độ phân giải tần số 1Hz quanh điểm 585,495,239 Hz

        @details: Verify UI PC17 cho phép setting tần số với độ phân giải 1Hz.
                  Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn quanh tần số trung tâm,
                  bước nhảy 1Hz. Ghi nhận công suất tại từng điểm.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 585,495,239 Hz (trung tâm), công suất = 0dBm
                - Điều chỉnh 5 điểm tần số nhỏ hơn (step 1Hz): 585,495,234 → 585,495,238  
                - Điều chỉnh 5 điểm tần số lớn hơn (step 1Hz): 585,495,240 → 585,495,244 Hz
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting tần số có độ phân giải 0.001Hz
                       - Sai số công suất và tần số theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC28 · PUC_1.3 · Test normal · 0dBm @ 6,588,912,835 Hz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_3_tc_0028(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_3_tc_0028
        @brief: Kiểm tra độ phân giải tần số 1Hz quanh điểm 6,588,912,835 Hz

        @details: Verify UI PC17 cho phép setting tần số với độ phân giải 1Hz tại vùng ~6.6GHz.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 6,588,912,835 Hz, công suất = 0dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 1Hz
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting tần số có độ phân giải 1Hz
                       - Sai số công suất và tần số theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC29 · PUC_1.3 · Test normal · 0dBm @ 11,364,293,484 Hz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_3_tc_0029(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_3_tc_0029
        @brief: Kiểm tra độ phân giải tần số 1Hz quanh điểm 11,364,293,484 Hz

        @details: Verify UI PC17 cho phép setting tần số với độ phân giải 1Hz tại vùng ~11.4GHz.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 11,364,293,484 Hz, công suất = 0dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 1Hz
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting tần số có độ phân giải 1Hz
                       - Sai số công suất và tần số theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC30 · PUC_1.3 · Test normal · 0dBm @ 14,035,894,162 Hz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_3_tc_0030(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_3_tc_0030
        @brief: Kiểm tra độ phân giải tần số 1Hz quanh điểm 14,035,894,162 Hz

        @details: Verify UI PC17 cho phép setting tần số với độ phân giải 1Hz tại vùng ~14GHz.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 14,035,894,162 Hz, công suất = 0dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 1Hz
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting tần số có độ phân giải 1Hz
                       - Sai số công suất và tần số theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC31 · PUC_1.3 · Test normal · 0dBm @ 17,728,894,123 Hz
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_3_tc_0031(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_3_tc_0031
        @brief: Kiểm tra độ phân giải tần số 1Hz quanh điểm 17,728,894,123 Hz

        @details: Verify UI PC17 cho phép setting tần số với độ phân giải 1Hz tại vùng ~17.7GHz.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Setting Signal Generator: tần số = 17,728,894,123 Hz, công suất = 0dBm
                - Điều chỉnh 5 điểm nhỏ hơn và 5 điểm lớn hơn với bước 1Hz
                - Ghi nhận giá trị công suất và tần số mà Power Meter đo được tại mỗi điểm
            [!code]

        @pass_criteria:- UI PC17 cho phép setting tần số có độ phân giải 1Hz
                       - Sai số công suất và tần số theo thông số của hãng (TBD)

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC32 · PUC_1.3 · Test abnormal · Độ phân giải sub-Hz (0.5Hz) — không hỗ trợ
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_3_tc_0032(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_3_tc_0032
        @brief: Kiểm tra PC17 từ chối setting tần số với độ phân giải nhỏ hơn 1Hz (sub-Hz)

        @details: PC17 chỉ hỗ trợ độ phân giải 1Hz. Setting tần số dạng X.5Hz (e.g. 17,728,894,123.5 Hz)
                  phải bị từ chối với thông báo lỗi.

        @pre:- Signal Generator đang bật
             - PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Signal Generator: tần số = 17,728,894,123.5 Hz (sub-Hz resolution), công suất = 0dBm
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi không hỗ trợ độ phân giải sub-Hz

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
