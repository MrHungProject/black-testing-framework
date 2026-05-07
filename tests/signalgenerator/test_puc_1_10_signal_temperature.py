"""
Signal Generator temperature display test suite — PUC_1.10
PC17 hiển thị nhiệt độ của Signal Generator và cảnh báo khi vượt ngưỡng.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc110Temperature:
    """PUC_1.10 — Temperature display test suite. TC56–TC58."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC56 · PUC_1.10 · Test normal · Hiển thị nhiệt độ khi đang hoạt động
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_10_tc_0056(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_10_tc_0056
        @brief: PC17 hiển thị giá trị nhiệt độ hợp lệ của Signal Generator khi đang hoạt động

        @details: Verify PC17 đọc và hiển thị nhiệt độ của Signal Generator.
                  Giá trị hiển thị phải là số hợp lệ (không rỗng, không phải "--").

        @pre:- Signal Generator đang hoạt động (phát tín hiệu hoặc ở trạng thái ON)
             - PC17 đã Connected

        @test_procedure:
            [code]
                - Bật Signal Generator và đợi thiết bị ổn định
                - Quan sát giá trị nhiệt độ hiển thị trên UI PC17
                - Ghi nhận giá trị nhiệt độ
            [!code]

        @pass_criteria:- PC17 hiển thị giá trị nhiệt độ hợp lệ của Signal Generator
                       - Giá trị nhiệt độ không rỗng và là số thực hợp lệ

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC57 · PUC_1.10 · Test abnormal · Popup warning khi nhiệt độ vượt ngưỡng
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_10_tc_0057(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_10_tc_0057
        @brief: PC17 hiển thị popup warning khi nhiệt độ Signal Generator vượt ngưỡng cho phép

        @details: Khi nhiệt độ vượt ngưỡng cảnh báo, PC17 phải hiển thị popup warning
                  để thông báo cho người dùng. Cần giả lập nhiệt độ cao bằng cách tác động vào sensor.

        @pre:- Signal Generator đang hoạt động
             - Có thiết bị giả lập hoặc cách tác động vào sensor nhiệt

        @test_procedure:
            [code]
                - Bật Signal Generator và đợi hiển thị nhiệt độ bình thường
                - Tác động vào sensor để giả lập nhiệt độ vượt ngưỡng
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 hiển thị popup warning khi nhiệt độ vượt ngưỡng

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC58 · PUC_1.10 · Test abnormal · Popup error khi sensor nhiệt bị hỏng
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_10_tc_0058(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_10_tc_0058
        @brief: PC17 hiển thị popup error khi sensor nhiệt độ của Signal Generator bị hỏng

        @details: Khi sensor nhiệt bị hỏng (không đọc được giá trị), PC17 phải hiển thị
                  popup error để thông báo lỗi phần cứng.

        @pre:- Signal Generator đang hoạt động
             - Có cách giả lập hỏng sensor (ngắt kết nối hoặc short circuit)

        @test_procedure:
            [code]
                - Bật Signal Generator và đợi hiển thị nhiệt độ bình thường
                - Giả lập sensor nhiệt bị hỏng (ngắt kết nối sensor)
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 hiển thị popup error khi sensor nhiệt độ bị hỏng

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
