"""
Signal Generator step point sweep test suite — PUC_1.6
PC17 phát tín hiệu theo các điểm tần số đặt trước, tối đa 1024 điểm.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc16StepPoint:
    """PUC_1.6 — Step point sweep test suite. TC44–TC45."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC44 · PUC_1.6 · Test normal · 1024 điểm, D:0.5s — phát xong sau 8min 32s
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_6_tc_0044(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_6_tc_0044
        @brief: Quét 1024 điểm tần số từ 500MHz đến 1000MHz, dwell 0.5s — hoàn thành sau ~8min 32s

        @details: Verify Signal Generator hỗ trợ tối đa 1024 điểm tần số trong mode Step point.
                  Tổng thời gian phát = 1024 × 0.5s = 512s ≈ 8min 32s.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Chọn chức năng quét tần số theo mode Step point, phát tín hiệu CW
                - Setting: A = 500MHz, B = 1000MHz, C = 1024 điểm, D = 0.5s
                - Nhấn button trên PC17 để thực hiện phát tín hiệu
                - Ghi lại tần số và công suất mỗi lần tần số nhảy sau khoảng thời gian D
            [!code]

        @pass_criteria:- Signal Generator phát đủ 1024 điểm tần số thành công
                       - Hoàn thành sau khoảng 8 phút 32 giây
                       - Sai số công suất, tần số và thời gian theo thông số của hãng (TBD)

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC45 · PUC_1.6 · Test abnormal · 1025 điểm — vượt giới hạn tối đa
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_6_tc_0045(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_6_tc_0045
        @brief: PC17 trả về lỗi khi setting số điểm tần số 1025 vượt giới hạn tối đa 1024

        @details: Số điểm tần số tối đa trong mode Step point là 1024.
                  Setting 1025 điểm phải bị từ chối với thông báo lỗi.

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Chọn mode Step point
                - Setting: A = 500MHz, B = 1000MHz, C = 1025 điểm, D = 0.5s
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 trả về lỗi step out of range

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
