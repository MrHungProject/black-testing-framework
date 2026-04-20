"""
Power Measurement test suite — PUC_3.2 / PUC_3.3 / PUC_3.4
Đo công suất tín hiệu đơn tần trong dải 1MHz–26.5GHz, -60dBm đến 26dBm.
Sai số công suất cho phép: < 1.71%.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc32PowerMeasurement:
    """PUC_3.2 / PUC_3.3 / PUC_3.4 — Power Measurement manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.2 · Test biên (TC3–TC6)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_2_tc03(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc03
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
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc04(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc04
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
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc05(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc05
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
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc06(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc06
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
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.2 · Test normal (TC7–TC22)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_2_tc07(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc07
        @brief: Test normal — SignalGen 10MHz, -59dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=-59dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc08(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc08
        @brief: Test normal — SignalGen 10MHz, -25dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=-25dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc09(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc09
        @brief: Test normal — SignalGen 10MHz, 15dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=15dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc10(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc10
        @brief: Test normal — SignalGen 10MHz, 25dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=10MHz, POW=25dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc11(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc11
        @brief: Test normal — SignalGen 5GHz, -58dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=-58dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc12(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc12
        @brief: Test normal — SignalGen 5GHz, -23dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=-23dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc13(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc13
        @brief: Test normal — SignalGen 5GHz, 17dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=17dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc14(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc14
        @brief: Test normal — SignalGen 5GHz, -24dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=5GHz, POW=-24dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc15(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc15
        @brief: Test normal — SignalGen 15MHz, -57dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=-57dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc16(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc16
        @brief: Test normal — SignalGen 15MHz, -21dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=-21dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc17(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc17
        @brief: Test normal — SignalGen 15MHz, 13dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=13dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc18(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc18
        @brief: Test normal — SignalGen 15MHz, 22dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=15MHz, POW=22dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc19(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc19
        @brief: Test normal — SignalGen 24GHz, -58dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=-58dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc20(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc20
        @brief: Test normal — SignalGen 24GHz, -23dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=-23dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc21(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc21
        @brief: Test normal — SignalGen 24GHz, 17dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=17dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc22(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc22
        @brief: Test normal — SignalGen 24GHz, -24dBm

        @pre:- PC17 đã Connected
        @test_procedure:
            [code]
                - Set SignalGen: FREQ=24GHz, POW=-24dBm, OUTPUT ON
                - Đọc power trên PC17, kiểm tra sai số < 1.71%
            [!code]
        @pass_criteria:- Sai số công suất < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.2 · Test abnormal (TC23–TC24)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_2_tc23(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc23
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
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_2_tc24(self, main_page: MainPage):
        """
        @test_id: test_puc_3_2_tc24
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
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.3 · Average parameter tests (TC25–TC28)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_3_tc25(self, main_page: MainPage):
        """
        @test_id: test_puc_3_3_tc25
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
    def test_puc_3_3_tc26(self, main_page: MainPage):
        """
        @test_id: test_puc_3_3_tc26
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
    def test_puc_3_3_tc27(self, main_page: MainPage):
        """
        @test_id: test_puc_3_3_tc27
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
    def test_puc_3_3_tc28(self, main_page: MainPage):
        """
        @test_id: test_puc_3_3_tc28
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

    # ════════════════════════════════════════════════════════════════════════════
    #  PUC_3.4 · Chế độ hiển thị Linear (TC29–TC33)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_4_tc29(self, main_page: MainPage):
        """
        @test_id: test_puc_3_4_tc29
        @brief: Linear display — SignalGen 5GHz, 10dBm → expected 10mW

        @details: Verify PC17 hiển thị đúng giá trị công suất ở chế độ Linear (mW).
                  10dBm tương đương 10mW trên thang tuyến tính.

        @pre:- Bật nguồn Powermeter và Signal Generator
             - Kết nối đầu ra SignalGen với đầu vào Powermeter
             - PC17 đã Connected, Average=10, Display=dB

        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz trên PC17
                - Set SignalGen: FREQ=5GHz, POW=10dBm, OUTPUT ON
                - Chuyển chế độ hiển thị sang Linear (mW)
                - Ghi nhận giá trị công suất mW trên PC17
                - Kiểm tra: giá trị = 10mW, sai số < 1.71%
            [!code]

        @pass_criteria:- PC17 hiển thị ~10mW
                       - Sai số < 1.71%

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_4_tc30(self, main_page: MainPage):
        """
        @test_id: test_puc_3_4_tc30
        @brief: Linear display — SignalGen 5GHz, 7dBm → expected 5.01mW

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=7dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW)
                - Ghi nhận giá trị mW, kiểm tra ≈ 5.01mW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~5.01mW, sai số < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_4_tc31(self, main_page: MainPage):
        """
        @test_id: test_puc_3_4_tc31
        @brief: Linear display — SignalGen 5GHz, 0dBm → expected 1mW

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=0dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW)
                - Ghi nhận giá trị mW, kiểm tra = 1mW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~1mW, sai số < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_4_tc32(self, main_page: MainPage):
        """
        @test_id: test_puc_3_4_tc32
        @brief: Linear display — SignalGen 5GHz, -13dBm → expected 0.0501mW

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=-13dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW)
                - Ghi nhận giá trị mW, kiểm tra ≈ 0.0501mW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~0.0501mW, sai số < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_puc_3_4_tc33(self, main_page: MainPage):
        """
        @test_id: test_puc_3_4_tc33
        @brief: Linear display — SignalGen 5GHz, -55dBm → expected 3.16nW

        @details: -55dBm tương đương 3.162nW (3.162e-6 mW) trên thang tuyến tính.

        @pre:- Bật nguồn Powermeter và Signal Generator, PC17 Connected, Average=10
        @test_procedure:
            [code]
                - Set Average=10, tần số Powermeter = 5GHz
                - Set SignalGen: FREQ=5GHz, POW=-55dBm, OUTPUT ON
                - Chuyển hiển thị sang Linear (mW/nW)
                - Ghi nhận giá trị, kiểm tra ≈ 3.16nW, sai số < 1.71%
            [!code]
        @pass_criteria:- PC17 hiển thị ~3.16nW, sai số < 1.71%
        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
