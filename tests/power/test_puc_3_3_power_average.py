"""
Average parameter test suite — PUC_3.3
Kiểm tra tham số Average (1–2000) của Power Meter từ UI PC17.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc33PowerAverage:
    """PUC_3.3 — Average parameter manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.3 · Average parameter tests (TC25–TC28)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_power_puc_3_3_tc_0025(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_3_tc_0025
        @brief: Test normal — Average 1→100, SignalGen 5GHz 10dBm

        @details: Verify rằng:
                  - Công suất hiển thị trong dải sai số < 1.71%
                  - Khi Average=1: độ biến thiên công suất cao
                  - Khi Average=100: độ biến thiên công suất nhỏ lại

        @pre:- Bật nguồn Powermeter và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Powermeter
             - PC17 đã Connected, hiển thị chế độ dBm

        @test_procedure:
            [code]
                - Set tần số Powermeter trên PC17 = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=10dBm, OUTPUT ON
                - Set Average = 1, quan sát độ biến thiên công suất trên PC17
                - Set Average = 100, quan sát độ biến thiên công suất trên PC17
                - Ghi nhận sai số công suất so với giá trị đặt
            [!code]

        @pass_criteria:- Công suất hiển thị trong dải sai số < 1.71%
                       - Độ biến thiên ở Average=100 nhỏ hơn rõ rệt so với Average=1

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_3_tc_0026(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_3_tc_0026
        @brief: Test abnormal — Average=0, SignalGen 5GHz 10dBm

        @details: Average=0 nằm ngoài dải hợp lệ. PC17 phải báo lỗi.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối

        @test_procedure:
            [code]
                - Set tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=10dBm, OUTPUT ON
                - Set Average = 0 trên PC17
                - Ghi nhận phản hồi của PC17
            [!code]

        @pass_criteria:- PC17 hiển thị thông báo lỗi "Average out of range"
                       - Không crash hoặc treo ứng dụng

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_3_tc_0027(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_3_tc_0027
        @brief: Test abnormal — Average=-1, SignalGen 5GHz 10dBm

        @details: Average=-1 nằm ngoài dải hợp lệ. PC17 phải báo lỗi.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối

        @test_procedure:
            [code]
                - Set tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=10dBm, OUTPUT ON
                - Set Average = -1 trên PC17
                - Ghi nhận phản hồi của PC17
            [!code]

        @pass_criteria:- PC17 hiển thị thông báo lỗi "Average out of range"
                       - Không crash hoặc treo ứng dụng

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_3_tc_0028(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_3_tc_0028
        @brief: Test abnormal — Average=2001, SignalGen 5GHz 10dBm

        @details: Average=2001 vượt giới hạn trên cho phép. PC17 phải báo lỗi.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối

        @test_procedure:
            [code]
                - Set tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=10dBm, OUTPUT ON
                - Set Average = 2001 trên PC17
                - Ghi nhận phản hồi của PC17
            [!code]

        @pass_criteria:- PC17 hiển thị thông báo lỗi "Average out of range"
                       - Không crash hoặc treo ứng dụng

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
