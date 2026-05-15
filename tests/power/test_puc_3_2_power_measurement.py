"""
Power Measurement test suite — PUC_3.2
Đo công suất tín hiệu đơn tần trong dải 1MHz–26.5GHz, -60dBm đến 26dBm.
Sai số công suất cho phép: < 1.71%.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc32PowerMeasurement:
    """PUC_3.2 — Power Measurement manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.2 · Test biên (TC3–TC6)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_power_puc_3_2_tc_0003(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0003
        @brief: Test biên — SignalGen 1MHz, 0dBm

        @details: Kiểm tra đo công suất tại tần số biên dưới 1MHz với công suất 0dBm.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối với đầu vào Powermeter

        @test_procedure:
            [code]
                - Set SignalGen: FREQ=1MHz, POW=0dBm, OUTPUT ON
                - Đọc giá trị công suất hiển thị trên PC17
                - Tính sai số so với giá trị đặt
            [!code]

        @pass_criteria:- PC17 hiển thị công suất hợp lệ
                       - Sai số công suất < 1.71%

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0004(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0004
        @brief: Test biên — SignalGen 26.5GHz, 0dBm

        @details: Kiểm tra đo công suất tại tần số biên trên 26.5GHz với công suất 0dBm.

        @pre:- PC17 đã Connected
             - Signal Generator hỗ trợ 26.5GHz

        @test_procedure:
            [code]
                - Set SignalGen: FREQ=26.5GHz, POW=0dBm, OUTPUT ON
                - Đọc giá trị công suất hiển thị trên PC17
                - Tính sai số so với giá trị đặt
            [!code]

        @pass_criteria:- PC17 hiển thị công suất hợp lệ
                       - Sai số công suất < 1.71%

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0005(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0005
        @brief: Test biên — SignalGen 20MHz, -60dBm

        @details: Kiểm tra đo công suất tại mức công suất biên dưới -60dBm.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối

        @test_procedure:
            [code]
                - Set SignalGen: FREQ=20MHz, POW=-60dBm, OUTPUT ON
                - Đọc giá trị công suất hiển thị trên PC17
                - Tính sai số so với giá trị đặt
            [!code]

        @pass_criteria:- PC17 hiển thị công suất hợp lệ
                       - Sai số công suất < 1.71%

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0006(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0006
        @brief: Test biên — SignalGen 20MHz, 26dBm

        @details: Kiểm tra đo công suất tại mức công suất biên trên 26dBm.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối

        @test_procedure:
            [code]
                - Set SignalGen: FREQ=20MHz, POW=26dBm, OUTPUT ON
                - Đọc giá trị công suất hiển thị trên PC17
                - Tính sai số so với giá trị đặt
            [!code]

        @pass_criteria:- PC17 hiển thị công suất hợp lệ
                       - Sai số công suất < 1.71%

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.2 · Test normal (TC7–TC22)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_power_puc_3_2_tc_0007(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0007
        @brief: Test normal — SignalGen 10MHz, -59dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=-59dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0008(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0008
        @brief: Test normal — SignalGen 10MHz, -25dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=-25dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0009(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0009
        @brief: Test normal — SignalGen 10MHz, 15dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=15dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0010(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0010
        @brief: Test normal — SignalGen 10MHz, 25dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=25dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0011(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0011
        @brief: Test normal — SignalGen 5GHz, -58dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=-58dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0012(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0012
        @brief: Test normal — SignalGen 5GHz, -23dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=-23dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0013(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0013
        @brief: Test normal — SignalGen 5GHz, 17dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=17dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0014(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0014
        @brief: Test normal — SignalGen 5GHz, -24dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=-24dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0015(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0015
        @brief: Test normal — SignalGen 15MHz, -57dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=-57dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0016(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0016
        @brief: Test normal — SignalGen 15MHz, -21dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=-21dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0017(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0017
        @brief: Test normal — SignalGen 15MHz, 13dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=13dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0018(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0018
        @brief: Test normal — SignalGen 15MHz, 22dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=22dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0019(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0019
        @brief: Test normal — SignalGen 24GHz, -58dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=-58dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0020(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0020
        @brief: Test normal — SignalGen 24GHz, -23dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=-23dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0021(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0021
        @brief: Test normal — SignalGen 24GHz, 17dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=17dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0022(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0022
        @brief: Test normal — SignalGen 24GHz, -24dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=-24dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.2 · Test abnormal (TC23–TC24)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_power_puc_3_2_tc_0023(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0023
        @brief: Test abnormal — SignalGen 27GHz vượt dải tần cho phép

        @details: Tần số 27GHz vượt giới hạn trên 26.5GHz.
                  PC17 phải trả về thông báo lỗi out of range tần số.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối

        @test_procedure:
            [code]
                - Set SignalGen: FREQ=27GHz, POW=0dBm, OUTPUT ON
                - Quan sát PC17 hiển thị thông báo lỗi tần số out of range
            [!code]

        @pass_criteria:- PC17 hiển thị thông báo lỗi "out of range" tần số
                       - Không crash hoặc treo ứng dụng

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_power_puc_3_2_tc_0024(self, main_page: MainPage):
        """
        @test_id: test_power_puc_3_2_tc_0024
        @brief: Test abnormal — SignalGen 999,999Hz dưới dải tần cho phép

        @details: Tần số 999,999Hz thấp hơn giới hạn dưới 1MHz.
                  PC17 phải trả về thông báo lỗi out of range tần số.

        @pre:- PC17 đã Connected
             - Signal Generator đã kết nối

        @test_procedure:
            [code]
                - Set SignalGen: FREQ=999,999Hz, POW=0dBm, OUTPUT ON
                - Quan sát PC17 hiển thị thông báo lỗi tần số out of range
            [!code]

        @pass_criteria:- PC17 hiển thị thông báo lỗi "out of range" tần số
                       - Không crash hoặc treo ứng dụng

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
