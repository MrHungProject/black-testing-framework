"""
Spike Sweep configuration test suite.
Tự động cấu hình Spike.exe: Frequency, Amplitude, Bandwidth, Acquisition,
Trace, Marker, OBW, Trace Math, Display Line.
Execution type: automatic.
"""

import pytest

from core import testcase
from pages.spike_page import SpikePage


class TestSpikeSweepConfig:
    """Spike.exe — Sweep mode configuration test suite."""

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · Normal · Cấu hình đầy đủ Sweep mode trên Spike.exe
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_spike_sweep_full_config(self, spike_page: SpikePage):
        """
        @test_id: test_spike_sweep_full_config
        @brief: Cấu hình đầy đủ Spike Sweep mode — Frequency, Amplitude, Bandwidth, Acquisition, Trace, Marker, OBW, Trace Math, Display Line

        @details: Verify toàn bộ luồng cấu hình Spike.exe trong chế độ Sweep:
                  - Set tần số Center=1GHz, Span=2GHz
                  - Set Amplitude Ref Level=-20dBm, Div=10
                  - Set Bandwidth RBW Shape=Nutall, RBW=300kHz, VBW=300kHz
                  - Set Acquisition Video Units=Log, Detector=Max, Swp Time=2ms, Swp Interval=3s
                  - Config Trace One: Clear & Write, Avg=10
                  - Config Marker One: Normal, Place On Trace One, Freq=1GHz, Peak Search
                  - Config OBW: Enable, Target=Trace One, 99%
                  - Config Trace Math: Enable, Power Diff
                  - Config Display Line: Enable, Level=-40dBm

        @pre:- Spike.exe đã được cài đặt tại C:\\Program Files\\Signal Hound\\Spike\\Spike.exe
             - Spike.exe đang chạy hoặc có thể khởi động tự động
             - Popup "No Device" đã được dismiss (xử lý tự động bởi fixture)

        @test_procedure:
            [code]
                1. Set Frequency: Center=1GHz, Span=2GHz
                2. Set Amplitude: Ref Level=-20, Div=10
                3. Set Bandwidth: RBW Shape=Nutall, RBW=300kHz, VBW=300kHz,
                   Auto RBW=False, Auto VBW=True
                4. Set Acquisition: Video Units=Log, Detector=Max,
                   Swp Time=2ms, Swp Interval=3s
                5. Config Trace: Trace=One, Type=Clear & Write, Avg=10,
                   Update=True, Hide=False
                6. Config Marker: Marker=One, Type=Normal, Place On=Trace One,
                   Freq=1GHz, Active=True, Peak Tracking=False,
                   Pk Threshold=-100, Pk Excurs.=6, Peak Search=True
                7. Config OBW: Enabled=True, Target=Trace One, %Power=99,
                   Move To Center=False
                8. Scroll đến Display Line section
                9. Config Trace Math: Enabled=True, Op1=Trace 3, Op2=Trace 3,
                   Result=Trace 6, Operation=Power Diff
                10. Config Display Line: Enabled=True, Level=-40dBm
            [!code]

        @pass_criteria:- Tất cả các tham số được set thành công không có exception
                       - UI Spike.exe phản hồi đúng sau mỗi bước cấu hình

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        # Build cache 1 lần — tất cả label-based methods bên dưới dùng lại cache này
        spike_page.refresh_cache()

        # ── Frequency ────────────────────────────────────────────────────────
        spike_page.set_frequency(center="1 GHz", span="2 GHz")

        # ── Amplitude ────────────────────────────────────────────────────────
        spike_page.set_amplitude(ref_level="-20", div="10")

        # ── Bandwidth ────────────────────────────────────────────────────────
        spike_page.set_bandwidth(
            rbw_shape="Nutall",
            rbw="300 kHz",
            vbw="300 kHz",
            auto_rbw=False,
            auto_vbw=True,
        )

        # ── Acquisition ──────────────────────────────────────────────────────
        spike_page.set_acquisition(
            video_units="Log",
            detector="Max",
            swp_time="2 ms",
            swp_interval="3 s",
        )

        # ── Trace ────────────────────────────────────────────────────────────
        spike_page.config_trace(
            trace="One",
            trace_type="Clear & Write",
            avg="10",
            update=True,
            hide=False,
        )

        # ── Marker ───────────────────────────────────────────────────────────
        spike_page.config_marker(
            marker="One",
            mtype="Normal",
            place_on="Trace One",
            freq="1 GHz",
            active=True,
            peak_tracking=False,
            threshold="-100",
            excursion="6",
            do_peak_search=True,
        )

        # ── OBW ──────────────────────────────────────────────────────────────
        spike_page.config_obw(
            enable=True,
            target="Trace One",
            percent="99",
            move_to_center=False,
        )

        # ── Scroll đến Display Line section ──────────────────────────────────
        spike_page.scroll_to("Display Line")

        # ── Trace Math ───────────────────────────────────────────────────────
        spike_page.config_trace_math(
            enable=True,
            op1="Trace 3",
            op2="Trace 3",
            result="Trace 6",
            operation="Power Diff",
        )

        # ── Display Line ─────────────────────────────────────────────────────
        spike_page.config_display_line(enable=True, level="-40 dBm")
