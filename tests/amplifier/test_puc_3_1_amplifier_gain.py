"""
Amplifier Gain measurement test suite — PUC_3.1
Đo độ khuếch đại (gain) của Amplifier tại các tần số khác nhau.
Kết nối: SignalGen → Amplifier → Power Meter.
Execution type: manual.
"""

import pytest

from core import testcase
from pages.main_page import MainPage


class TestPuc31AmplifierGain:
    """PUC_3.1 — Amplifier Gain measurement manual test suite."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Đảm bảo PC17 Connected trước mỗi TC."""
        if not main_page.is_connected():
            main_page.reconnect()

    # ════════════════════════════════════════════════════════════════════════════
    #  TC3 · PUC_3.1 · Normal · SignalGen 1GHz -20dBm → Gain +37dB → 17dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_1_tc03(self, main_page: MainPage):
        """
        @test_id: test_amplifier_puc_3_1_tc03
        @brief: Gain measurement — SignalGen 1GHz -20dBm → Power Meter đo được 17dBm (gain +37dB)

        @details: Verify Amplifier khuếch đại đúng tại tần số 1GHz.
                  Kết nối: SignalGen → Amplifier → Power Meter.
                  Ngõ vào: 1GHz, -20dBm. Gain kỳ vọng: +37dB → Ngõ ra: 17dBm.

        @pre:- Bật nguồn Amplifier và Signal Generator
             - Bật Power Meter
             - Kết nối: Signal Gen → Amplifier → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                Chuẩn bị:
                1. Signal Generator
                2. Bật nguồn cho Amplifier
                3. Power Meter
                Step:
                1. Kết nối 3 thiết bị: Signal Gen → Amplifier → Power Meter
                2. Setting SignalGen: FREQ=1GHz, POW=-20dBm
                3. Bật Power Meter
                4. Điều khiển Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = -20dBm + 37dB = 17dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC4 · PUC_3.1 · Normal · SignalGen 9GHz -30dBm → Gain +47dB → 17dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_1_tc04(self, main_page: MainPage):
        """
        @test_id: test_amplifier_puc_3_1_tc04
        @brief: Gain measurement — SignalGen 9GHz -30dBm → Power Meter đo được 17dBm (gain +7dB)

        @details: Verify Amplifier khuếch đại đúng tại tần số 9GHz.
                  Kết nối: SignalGen → Amplifier → Power Meter.
                  Ngõ vào: 9GHz, -30dBm. Gain kỳ vọng: +7dB → Ngõ ra: 17dBm.

        @pre:- Bật nguồn Amplifier và Signal Generator
             - Bật Power Meter
             - Kết nối: Signal Gen → Amplifier → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                Chuẩn bị:
                1. Signal Generator
                2. Bật nguồn cho Amplifier
                3. Power Meter
                Step:
                1. Kết nối 3 thiết bị: Signal Gen → Amplifier → Power Meter
                2. Setting SignalGen: FREQ=9GHz, POW=-30dBm
                3. Bật Power Meter
                4. Điều khiển Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = -30dBm + 7dB = 17dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """

    # ════════════════════════════════════════════════════════════════════════════
    #  TC5 · PUC_3.1 · Normal · SignalGen 18GHz -10dBm → Gain +27dB → 17dBm
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_puc_3_1_tc05(self, main_page: MainPage):
        """
        @test_id: test_amplifier_puc_3_1_tc05
        @brief: Gain measurement — SignalGen 18GHz -10dBm → Power Meter đo được 17dBm (gain +27dB)

        @details: Verify Amplifier khuếch đại đúng tại tần số 18GHz.
                  Kết nối: SignalGen → Amplifier → Power Meter.
                  Ngõ vào: 18GHz, -10dBm. Gain kỳ vọng: +27dB → Ngõ ra: 17dBm.

        @pre:- Bật nguồn Amplifier và Signal Generator
             - Bật Power Meter
             - Kết nối: Signal Gen → Amplifier → Power Meter
             - PC17 đã Connected

        @test_procedure:
            [code]
                Chuẩn bị:
                1. Signal Generator
                2. Bật nguồn cho Amplifier
                3. Power Meter
                Step:
                1. Kết nối 3 thiết bị: Signal Gen → Amplifier → Power Meter
                2. Setting SignalGen: FREQ=18GHz, POW=-10dBm
                3. Bật Power Meter
                4. Điều khiển Signal Gen bắt đầu phát tín hiệu
                5. Ghi nhận giá trị công suất Power Meter đo được
            [!code]

        @pass_criteria:- Giá trị công suất đo được = -10dBm + 27dB = 17dBm
                       - Sai số: TBD

        @test_level: software
        @test_type: fat
        @execution_type: manual
        @hw_depend: yes
        """
