"""
Signal Generator hardware (external) trigger test suite — PUC_1.8
PC17 điều khiển phát tín hiệu theo external trigger qua GPIO21 (sườn xuống).
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc18HwTrigger:
    """PUC_1.8 — External (hardware) trigger test suite. TC48–TC49."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC48 · PUC_1.8 · Test normal · External trigger qua GPIO21
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_8_tc_0048(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_8_tc_0048
        @brief: Signal Generator phát tín hiệu khi nhận external trigger qua GPIO21 (sườn xuống)

        @details: Verify Signal Generator khởi động phát tín hiệu khi nhận xung sườn xuống
                  từ thiết bị tạo xung bên ngoài kết nối vào GPIO21.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator
             - Board mạch tạo xung (sườn xuống) đã kết nối vào GPIO21

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Kết nối đầu ra của thiết bị tạo xung vào GPIO21
                - Chọn chức năng quét tần số theo mode Dwell time trên PC17
                - Setting: A = 500MHz, B = 1000MHz, C = 10, D = 1s
                - Gửi xung sườn xuống vào GPIO21 để trigger phát tín hiệu
                - Quan sát Signal Generator bắt đầu phát
            [!code]

        @pass_criteria:- Thiết bị bắt đầu phát tín hiệu đúng theo các tham số đã setting
                       - Phát tín hiệu được trigger bởi xung sườn xuống từ GPIO21

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC49 · PUC_1.8 · Test normal · Hành vi khi trigger lại trong khi đang chạy — TBD
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_8_tc_0049(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_8_tc_0049
        @brief: Kiểm tra hành vi khi nhận trigger tiếp theo trong khi đang phát tín hiệu — TBD

        @details: Cần xác định xử lý khi trigger được gửi trong khi thiết bị đang phát:
                  ignore, restart, hoặc queue. Cần thông số từ hãng.

        @pre:- Signal Generator đang phát tín hiệu theo external trigger
             - Board mạch tạo xung đã kết nối vào GPIO21

        @test_procedure:
            [code]
                - Khởi động phát tín hiệu theo TC48
                - Trong khi đang phát, gửi thêm một xung trigger vào GPIO21
                - Quan sát phản hồi và trạng thái của Signal Generator
            [!code]

        @pass_criteria:- TBD — cần xác định theo spec của hãng

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
