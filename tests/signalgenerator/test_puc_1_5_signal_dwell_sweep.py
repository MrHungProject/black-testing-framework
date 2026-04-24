"""
Signal Generator dwell time sweep test suite — PUC_1.5
PC17 điều khiển phát chức năng quét tần số theo mode Dwell time:
phát CW từ tần số A đến B với bước nhảy tần C và thời gian dừng mỗi điểm D.
"""
import pytest

from core import testcase
from pages.main_page import MainPage


class TestSignalPuc15DwellSweep:
    """
    PUC_1.5 — Dwell time sweep test suite.
    TC33–TC37: test normal với các dải tần và thông số khác nhau.
    TC38–TC43: test abnormal với thông số C, D không hợp lệ.
    """

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC33 · PUC_1.5 · Test normal · A:1288MHz→B:5308MHz, C:5, D:0.4s
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_5_tc_0033(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0033
        @brief: Quét tần số dải 1288–5308MHz với 5 bước nhảy, dwell time 0.4s mỗi điểm

        @details: Verify Signal Generator quét tần số đúng theo mode Dwell time.
                  D ≥ t_hop + t_settle + t_meas_margin để đảm bảo đo chính xác.

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Chọn chức năng quét tần số theo mode Dwell time, phát tín hiệu CW
                - Setting: A = 1288MHz, B = 5308MHz, C = 5, D = 0.4s
                - Nhấn button trên PC17 để thực hiện phát tín hiệu
                - Ghi lại tần số và công suất mỗi lần tần số nhảy sau khoảng thời gian D
            [!code]

        @pass_criteria:- Signal Generator quét đúng các tần số từ A đến B theo bước C
                       - Thời gian dừng tại mỗi điểm đúng D = 0.4s
                       - Sai số công suất, tần số và thời gian theo thông số của hãng (TBD)

        @test_level: software
        @test_type: functional
        @execution_type: semi_automatic
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC34 · PUC_1.5 · Test normal · A:5308MHz→B:10539MHz, C:7, D:1s
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_5_tc_0034(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0034
        @brief: Quét tần số dải 5308–10539MHz với 7 bước nhảy, dwell time 1s mỗi điểm

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Chọn chức năng quét tần số theo mode Dwell time, phát tín hiệu CW
                - Setting: A = 5308MHz, B = 10539MHz, C = 7, D = 1s
                - Nhấn button trên PC17 để thực hiện phát tín hiệu
                - Ghi lại tần số và công suất mỗi lần tần số nhảy sau khoảng thời gian D
            [!code]

        @pass_criteria:- Signal Generator quét đúng các tần số từ A đến B theo bước C
                       - Sai số công suất, tần số và thời gian theo thông số của hãng (TBD)

        @test_level: software
        @test_type: functional
        @execution_type: semi_automatic
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC35 · PUC_1.5 · Test normal · A:10539MHz→B:13108MHz, C:10, D:3.5s
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_5_tc_0035(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0035
        @brief: Quét tần số dải 10539–13108MHz với 10 bước nhảy, dwell time 3.5s mỗi điểm

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Chọn chức năng quét tần số theo mode Dwell time, phát tín hiệu CW
                - Setting: A = 10539MHz, B = 13108MHz, C = 10, D = 3.5s
                - Nhấn button trên PC17 để thực hiện phát tín hiệu
                - Ghi lại tần số và công suất mỗi lần tần số nhảy sau khoảng thời gian D
            [!code]

        @pass_criteria:- Signal Generator quét đúng các tần số từ A đến B theo bước C
                       - Sai số công suất, tần số và thời gian theo thông số của hãng (TBD)

        @test_level: software
        @test_type: functional
        @execution_type: semi_automatic
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC36 · PUC_1.5 · Test normal · A:13108MHz→B:18630MHz, C:17, D:10s
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_5_tc_0036(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0036
        @brief: Quét tần số dải 13108–18630MHz với 17 bước nhảy, dwell time 10s mỗi điểm

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Chọn chức năng quét tần số theo mode Dwell time, phát tín hiệu CW
                - Setting: A = 13108MHz, B = 18630MHz, C = 17, D = 10s
                - Nhấn button trên PC17 để thực hiện phát tín hiệu
                - Ghi lại tần số và công suất mỗi lần tần số nhảy sau khoảng thời gian D
            [!code]

        @pass_criteria:- Signal Generator quét đúng các tần số từ A đến B theo bước C
                       - Sai số công suất, tần số và thời gian theo thông số của hãng (TBD)

        @test_level: software
        @test_type: functional
        @execution_type: semi_automatic
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC37 · PUC_1.5 · Test normal · A:18630MHz→B:19567MHz, C:20, D:30s
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_5_tc_0037(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0037
        @brief: Quét tần số dải 18630–19567MHz với 20 bước nhảy, dwell time 30s mỗi điểm

        @pre:- Signal Generator đang bật
             - Power Meter đã kết nối vào output của Signal Generator

        @test_procedure:
            [code]
                - Kết nối output của Signal Generator vào input của Power Meter
                - Chọn chức năng quét tần số theo mode Dwell time, phát tín hiệu CW
                - Setting: A = 18630MHz, B = 19567MHz, C = 20, D = 30s
                - Nhấn button trên PC17 để thực hiện phát tín hiệu
                - Ghi lại tần số và công suất mỗi lần tần số nhảy sau khoảng thời gian D
            [!code]

        @pass_criteria:- Signal Generator quét đúng các tần số từ A đến B theo bước C
                       - Sai số công suất, tần số và thời gian theo thông số của hãng (TBD)

        @test_level: software
        @test_type: functional
        @execution_type: semi_automatic
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC38–TC43 · PUC_1.5 · Test abnormal · C hoặc D không hợp lệ
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_signal_puc_1_5_tc_0038(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0038
        @brief: PC17 báo lỗi khi số bước nhảy C < 0

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Dwell sweep: A = 500MHz, B = 1000MHz, C < 0, D = 1.5s
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 báo lỗi C phải > 0

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_5_tc_0039(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0039
        @brief: PC17 báo lỗi khi số bước nhảy C = 0

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Dwell sweep: A = 500MHz, B = 1000MHz, C = 0, D = 1.5s
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 báo lỗi C phải > 0

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_5_tc_0040(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0040
        @brief: PC17 báo lỗi khi số bước nhảy C vượt giá trị tối đa

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Dwell sweep: A = 500MHz, B = 1000MHz, C > max, D = 1.5s
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 báo lỗi C out of range

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_5_tc_0041(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0041
        @brief: PC17 báo lỗi khi dwell time D < 0

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Dwell sweep: A = 500MHz, B = 1000MHz, C = 10, D < 0
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 báo lỗi D phải > 0

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_5_tc_0042(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0042
        @brief: PC17 báo lỗi khi dwell time D = 0

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Dwell sweep: A = 500MHz, B = 1000MHz, C = 10, D = 0
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 báo lỗi D phải > 0

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    @testcase
    def test_signal_puc_1_5_tc_0043(self, main_page: MainPage):
        """
        @test_id: test_signal_puc_1_5_tc_0043
        @brief: PC17 báo lỗi khi dwell time D vượt giá trị tối đa

        @pre:- Signal Generator đang bật — PC17 đã Connected

        @test_procedure:
            [code]
                - Setting Dwell sweep: A = 500MHz, B = 1000MHz, C = 10, D > max
                - Quan sát phản hồi từ UI PC17
            [!code]

        @pass_criteria:- PC17 báo lỗi D out of range

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
