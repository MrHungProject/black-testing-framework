"""
Signal Generator software trigger test suite — PUC_1.7
PC17 điều khiển phát tín hiệu theo software trigger.
Note: TC46 covered bởi TC33–TC45. TC47 TBD (stop behavior).
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc17SwTrigger:
    """PUC_1.7 — Software trigger test suite. TC46–TC47."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC46 · PUC_1.7 · Test normal · Covered bởi TC33–TC45
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_7_tc_0046(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_7_tc_0046
        @brief: Software trigger — test case covered bởi TC33 đến TC45 (Dwell time và Step point)

        @details: Chức năng software trigger được verify qua toàn bộ các TC trong PUC_1.5 và PUC_1.6.
                  Khi user nhấn button trên PC17 UI là software trigger kích hoạt phát tín hiệu.

        @pre:- PC17 đã Connected

        @test_procedure:
            [code]
                - Tham chiếu kết quả từ TC33 đến TC45
                - Xác nhận button trigger trên PC17 UI hoạt động đúng trong mọi test case trên
            [!code]

        @pass_criteria:- Software trigger hoạt động đúng — tham chiếu pass criteria từ TC33–TC45

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC47 · PUC_1.7 · Test normal · Hành vi khi nhấn Stop trong lúc đang phát — TBD
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_7_tc_0047(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_7_tc_0047
        @brief: Kiểm tra hành vi khi nhấn Stop trong lúc Signal Generator đang phát — TBD

        @details: Cần xác định: có button Stop không? Xử lý gì khi đang phát mà nhấn Stop?
                  Test case này cần được định nghĩa thêm sau khi có thông số từ hãng.

        @pre:- Signal Generator đang phát tín hiệu theo Dwell/Step sweep mode

        @test_procedure:
            [code]
                - Khởi động phát tín hiệu theo mode Dwell sweep (ví dụ TC33)
                - Trong khi đang phát, nhấn button Stop trên PC17 UI
                - Quan sát phản hồi và trạng thái của Signal Generator
            [!code]

        @pass_criteria:- TBD — cần xác định theo spec của hãng

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
