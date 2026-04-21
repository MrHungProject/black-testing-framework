"""
Attenuator attenuation control test suite — PUC_6.2
Điều khiển hệ số suy hao từ UI PC17, verify công suất đo được bằng Power Meter.
Kết nối: SignalGen → Attenuator → Power Meter.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc62AttenuatorAttenuation:
    """PUC_6.2 — Attenuator attenuation control manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC3 · PUC_6.2 · Normal · Suy hao 0dBm, SignalGen 1GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0003(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0003
        @brief: Suy hao 0dBm — SignalGen 1GHz 10dBm → Power Meter đo được 10dBm

        @details: Verify Attenuator không suy hao tín hiệu khi hệ số suy hao = 0dBm.
                  Kết nối: SignalGen → Attenuator → Power Meter.
                  Ngõ vào: 1GHz, 10dBm. Suy hao: 0dBm. Ngõ ra kỳ vọng: 10dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                Chuẩn bị:
                1. Signal Generator
                2. Bật nguồn cho Attenuator
                3. Power Meter
                Step:
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 0dBm
                3. Setting SignalGen: FREQ=1GHz, POW=10dBm
                4. Bật Power Meter
                5. Điều khiển Signal Gen bắt đầu phát tín hiệu
                6. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 0dBm = 10dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC4 · PUC_6.2 · Normal · Suy hao 10dBm, SignalGen 1GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0004(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0004
        @brief: Suy hao 10dBm — SignalGen 1GHz 10dBm → Power Meter đo được 0dBm

        @details: Verify Attenuator suy hao đúng 10dBm tại tần số 1GHz.
                  Ngõ vào: 1GHz, 10dBm. Suy hao: 10dBm. Ngõ ra kỳ vọng: 0dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 10dBm
                3. Setting SignalGen: FREQ=1GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 10dBm = 0dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC5 · PUC_6.2 · Normal · Suy hao 20dBm, SignalGen 1GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0005(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0005
        @brief: Suy hao 20dBm — SignalGen 1GHz 10dBm → Power Meter đo được -10dBm

        @details: Verify Attenuator suy hao đúng 20dBm tại tần số 1GHz.
                  Ngõ vào: 1GHz, 10dBm. Suy hao: 20dBm. Ngõ ra kỳ vọng: -10dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 20dBm
                3. Setting SignalGen: FREQ=1GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 20dBm = -10dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC6 · PUC_6.2 · Normal · Suy hao 30dBm, SignalGen 1GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0006(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0006
        @brief: Suy hao 30dBm — SignalGen 1GHz 10dBm → Power Meter đo được -20dBm

        @details: Verify Attenuator suy hao đúng 30dBm tại tần số 1GHz.
                  Ngõ vào: 1GHz, 10dBm. Suy hao: 30dBm. Ngõ ra kỳ vọng: -20dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 30dBm
                3. Setting SignalGen: FREQ=1GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 30dBm = -20dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC7 · PUC_6.2 · Normal · Suy hao 5dBm, SignalGen 5GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0007(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0007
        @brief: Suy hao 5dBm — SignalGen 5GHz 10dBm → Power Meter đo được 5dBm

        @details: Verify Attenuator suy hao đúng 5dBm tại tần số 5GHz.
                  Ngõ vào: 5GHz, 10dBm. Suy hao: 5dBm. Ngõ ra kỳ vọng: 5dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 5dBm
                3. Setting SignalGen: FREQ=5GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 5dBm = 5dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC8 · PUC_6.2 · Normal · Suy hao 16dBm, SignalGen 5GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0008(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0008
        @brief: Suy hao 16dBm — SignalGen 5GHz 10dBm → Power Meter đo được -6dBm

        @details: Verify Attenuator suy hao đúng 16dBm tại tần số 5GHz.
                  Ngõ vào: 5GHz, 10dBm. Suy hao: 16dBm. Ngõ ra kỳ vọng: -6dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 16dBm
                3. Setting SignalGen: FREQ=5GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 16dBm = -6dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC9 · PUC_6.2 · Normal · Suy hao 24dBm, SignalGen 5GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0009(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0009
        @brief: Suy hao 24dBm — SignalGen 5GHz 10dBm → Power Meter đo được -14dBm

        @details: Verify Attenuator suy hao đúng 24dBm tại tần số 5GHz.
                  Ngõ vào: 5GHz, 10dBm. Suy hao: 24dBm. Ngõ ra kỳ vọng: -14dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 24dBm
                3. Setting SignalGen: FREQ=5GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 24dBm = -14dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC10 · PUC_6.2 · Normal · Suy hao 29dBm, SignalGen 5GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0010(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0010
        @brief: Suy hao 29dBm — SignalGen 5GHz 10dBm → Power Meter đo được -19dBm

        @details: Verify Attenuator suy hao đúng 29dBm tại tần số 5GHz (cận biên trên cho phép).
                  Ngõ vào: 5GHz, 10dBm. Suy hao: 29dBm. Ngõ ra kỳ vọng: -19dBm.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 29dBm
                3. Setting SignalGen: FREQ=5GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = 10dBm - 29dBm = -19dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC11 · PUC_6.2 · Abnormal · Suy hao 31dBm (out of range), SignalGen 5GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0011(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0011
        @brief: Suy hao 31dBm — vượt giới hạn trên → PC17 trả về out of range

        @details: Verify PC17 báo lỗi khi hệ số suy hao 31dBm vượt quá giới hạn cho phép.
                  Attenuator không được thực hiện suy hao, PC17 phải hiển thị thông báo lỗi.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = 31dBm
                3. Setting SignalGen: FREQ=5GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận phản hồi của PC17
            [!code]

        @pass_criteria:- PC17 hiển thị thông báo lỗi "out of range"
                       - Không crash hoặc treo ứng dụng

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC12 · PUC_6.2 · Abnormal · Suy hao -1dBm (out of range), SignalGen 5GHz 10dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_attenuator_puc_6_2_tc_0012(self, main_page: MainPage):
        """
        @test_id: test_attenuator_puc_6_2_tc_0012
        @brief: Suy hao -1dBm — dưới giới hạn tối thiểu → PC17 trả về out of range

        @details: Verify PC17 báo lỗi khi hệ số suy hao -1dBm nằm dưới giới hạn cho phép.
                  Attenuator không được thực hiện suy hao, PC17 phải hiển thị thông báo lỗi.

        @pre:- Bật nguồn Attenuator, Signal Generator và Power Meter
             - Kết nối: Signal Gen → Attenuator → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                1. Kết nối 3 thiết bị: Signal Gen → Attenuator → Power Meter
                2. Setting trên PC17 hệ số suy hao = -1dBm
                3. Setting SignalGen: FREQ=5GHz, POW=10dBm
                4. Bật Power Meter, Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận phản hồi của PC17
            [!code]

        @pass_criteria:- PC17 hiển thị thông báo lỗi "out of range"
                       - Không crash hoặc treo ứng dụng

        @test_level: software
        @test_type: functional
        @execution_type: manual
        @hw_depend: yes
        """
