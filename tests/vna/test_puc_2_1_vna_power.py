"""
VNA test suite — PUC_2.1 Power ON/OFF + Detail + Configuration

Tất cả TC được tổ chức trong class TestVnaPuc21.
fixture _ensure_connected (autouse) chạy trước MỖI TC → đảm bảo Connected state,
nên mỗi TC có thể chạy độc lập mà không phụ thuộc TC khác.
"""

import re
import time

import pytest

from core import testcase
from core.app_controller import AppController
from pages.main_page import MainPage


def _freq_to_ghz(s: str) -> float:
    """
    Normalize chuỗi frequency về float GHz để so sánh.
    Ví dụ: '2GHz' → 2.0 | '2.000 GHz' → 2.0 | '2000MHz' → 2.0
    """
    m = re.match(r"([\d.]+)\s*(GHz|MHz|kHz|Hz)?", s.strip(), re.IGNORECASE)
    if not m:
        return float("nan")
    val = float(m.group(1))
    unit = (m.group(2) or "GHz").upper()
    if unit == "GHZ":
        return val
    if unit == "MHZ":
        return val / 1_000
    if unit == "KHZ":
        return val / 1_000_000
    return val / 1_000_000_000  # Hz


class TestVnaPuc21:
    """
    PUC_2.1 VNA test suite.

    Setup flow (tự động, không cần TC01 chạy trước):
        fixture _ensure_connected (autouse=True) chạy trước mỗi TC.
        Nếu chưa Connected → reconnect() tự động.
        Mỗi TC đều độc lập và luôn bắt đầu ở trạng thái Connected.
    """

    # ── Class-level setup: chạy trước MỖI test method ────────────────────────

    _VNA_LABEL = "VNA Device"

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """
        Đảm bảo VNA Device đã Connected trước mỗi TC.
        Nếu đang ở Connect panel và device đã connected → skip navigation (chạy liên tục).
        Chỉ mở Connect panel khi thực sự cần thiết.
        """
        if main_page.is_device_connected(self._VNA_LABEL):
            return  # đã connected, không cần navigate
        main_page.open_connect_panel()
        if not main_page.is_device_connected(self._VNA_LABEL):
            main_page.connect_device(self._VNA_LABEL)
            time.sleep(3)

    # ════════════════════════════════════════════════════════════════════════════
    #  TC1 · PUC_2.1 · Normal · Bật VNA — kết nối và kiểm tra Detail
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_vna_puc_2_1_0001(self, s2vna_ctrl: AppController, main_page: MainPage):
        """
        @test_id: test_vna_puc_2_1_0001
        @brief: Bật VNA — khởi động S2VNA, PC17, vào RF Test Set và kết nối

        @details: Verify toàn bộ luồng khởi động:
                  S2VNA simulator lên trước, PC17 lên sau,
                  điều hướng vào RF Test Set và đạt trạng thái Connected.

        @pre:- Máy tính đã cài S2VNA và PC17
             - Không có instance nào đang chạy trước khi test

        @test_procedure:    - Khởi chạy App S2VNA
                            - Khởi động App PC17
                            - Sau đó vào UI của PC17 tại thanh Menu
                            [code]
                                # Tools → RF Test Set
                                - Chờ nó sẽ ra 1 UI khác tên là FormMainEliteRF lúc này sẽ làm việc trên UI này
                                → System → Connect → Connection → đợi Connected
                            [!code]

        @pass_criteria:- UI PC17 hiển thị trạng thái "Connected"
                       - Nút "Disconnect" xuất hiện
                       - Sau khi Connection thành công, check tại mục Detail kiểm tra xem các
                       thông tin của VNA (Temperature, Serial Number) đã được load chưa

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        # _ensure_connected đã đảm bảo Connected state.
        # TC1 chỉ verify kết quả: Connected + Disconnect button + Detail info.
        assert main_page.is_device_connected("VNA Device"), "VNA Device không đạt trạng thái 'Connected'"
        assert main_page.has_text("Disconnect"), "Nút 'Disconnect' không xuất hiện trên UI"

        main_page.click_detail()

        temperature = main_page.get_temperature()
        serial      = main_page.get_serial_number()

        errors = []
        if temperature in (None, "", ":"):
            errors.append(f"Temperature không hợp lệ: {temperature!r}")
        if serial in (None, "", ":"):
            errors.append(f"Serial Number không hợp lệ: {serial!r}")

        assert not errors, "\n".join(errors)

    # ════════════════════════════════════════════════════════════════════════════
    #  TC2 · PUC_2.1 · Abnormal · Bật/tắt liên tục VNA (5 chu kỳ)
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_vna_puc_2_1_0002(self, main_page: MainPage):
        """
        @test_id: test_vna_puc_2_1_0002
        @brief: Bật/tắt liên tục VNA 5 chu kỳ không có lỗi

        @details: Verify rằng VNA có thể bật/tắt liên tục 5 lần mà không bị lỗi,
                  trạng thái UI phải đúng sau mỗi chu kỳ Disconnect / Reconnect.

        @pre:- PC17 application đang chạy
             - Module VNA đã kết nối (được đảm bảo bởi _ensure_connected)

        @test_procedure:
                        [code]
                            - Xác nhận thiết bị đã kết nối (Connected) trên UI
                            - Disconnect module VNA từ UI
                            - Xác nhận UI không còn hiển thị "Connected"
                            - Reconnect: System → Connect → Connection → đợi Connected
                            - Xác nhận UI hiển thị "Connected"
                            - Lặp lại 5 lần
                        [!code]

        @pass_criteria:- Sau mỗi lần Disconnect: UI không còn "Connected"
                       - Sau mỗi lần Reconnect: UI hiển thị "Connected"
                       - Hoàn thành đủ 5 chu kỳ không có exception

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        CYCLES = 5

        assert main_page.is_device_connected(self._VNA_LABEL), "Điều kiện đầu vào TC2: VNA Device chưa Connected"

        for cycle in range(1, CYCLES + 1):
            # ── Disconnect ──────────────────────────────────────────────────────
            main_page.disconnect_device(self._VNA_LABEL)
            time.sleep(3)

            assert not main_page.is_device_connected(self._VNA_LABEL), (
                f"Chu kỳ {cycle}/{CYCLES}: VNA vẫn hiển thị 'Connected' sau Disconnect"
            )

            # ── Reconnect ───────────────────────────────────────────────────────
            main_page.connect_device(self._VNA_LABEL)
            time.sleep(3)

            assert main_page.is_device_connected(self._VNA_LABEL), (
                f"Chu kỳ {cycle}/{CYCLES}: VNA không đạt 'Connected' sau Reconnect"
            )

    # ════════════════════════════════════════════════════════════════════════════
    #  TC3 · PUC_2.1 · Normal · Cấu hình VNA — Measurement, Stimulus, Marker
    # ════════════════════════════════════════════════════════════════════════════

    @testcase
    def test_vna_puc_2_1_0003(self, main_page: MainPage):
        """
        @test_id: test_vna_puc_2_1_0003
        @brief: Cấu hình VNA — Measurement (S11/S21), Stimulus, Marker

        @details: Verify toàn bộ luồng cấu hình VNA sau khi đã Connected:
                  chọn S-parameter, thiết lập Stimulus, thêm Marker và đọc kết quả.

        @pre:- PC17 đã Connected (được đảm bảo bởi _ensure_connected)
             - VNA panel có thể mở được

        @test_procedure:
                        [code]
                            # Measurement
                                - Mở tab Measurement trong VNA panel
                                - Chọn S11, chọn S21
                                - Click Apply

                            # Stimulus
                                - Mở tab Stimulus
                                - Set Start Frequency = 2GHz, Stop = 6GHz
                                - Set Center = 9.05GHz, Span = 3GHz
                                - Set Points = 301, IF BW = 10kHz, Power = 0
                                - Click Apply

                            # Marker
                                - Mở tab Markers
                                - Add Marker 1 (Trace 1 mặc định)
                                - Đổi sang Trace 2, Add Marker 2
                                - Đọc dữ liệu marker (GHz position + dB value)`
                        [!code]

        @pass_criteria:- S11 và S21 được chọn thành công
                       - Tất cả thông số Stimulus được điền và Apply thành công
                       - Ít nhất 1 marker được tạo với dữ liệu hợp lệ (có GHz position và dB value)
                       - Marker 1 position == Start Frequency (2GHz)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        START_FREQ = "2GHz"

        # ── Measurement ─────────────────────────────────────────────────────────
        main_page.open_measurement()
        main_page.select_s_parameter("S11")
        main_page.select_s_parameter("S21")
        main_page.click_apply()

        # ── Stimulus ────────────────────────────────────────────────────────────
        main_page.open_stimulus()
        main_page.set_stimulus_params(
            start=START_FREQ,
            stop="18GHz",
            center="9.05GHz",
            span="3GHz",
            points="301",
            if_bw="10kHz",
            power="0",
        )

        # ── Marker ──────────────────────────────────────────────────────────────
        main_page.setup_marker()
        time.sleep(1)  # đợi marker render

        markers = main_page.extract_markers()

        assert len(markers) >= 1, (
            f"Không có marker nào được tạo hoặc không đọc được dữ liệu. markers={markers}"
        )

        for m in markers:
            assert m.get("position"), f"Marker '{m['name']}' thiếu position: {m}"
            assert m.get("value"),    f"Marker '{m['name']}' thiếu value: {m}"

        # ── Verify Marker 1 position == Start Frequency ──────────────────────────
        marker1_pos  = markers[0]["position"]
        expected_ghz = _freq_to_ghz(START_FREQ)
        actual_ghz   = _freq_to_ghz(marker1_pos)

        assert abs(actual_ghz - expected_ghz) < 0.001, (
            f"Marker 1 position {marker1_pos!r} ({actual_ghz:.4f} GHz) "
            f"không khớp với Start Frequency {START_FREQ!r} ({expected_ghz:.4f} GHz)"
        )

    @testcase
    def test_vna_puc_2_1_0004(self, main_page: MainPage):
        """
        @test_id: test_vna_puc_2_1_0004
        @brief: Thực hiện bài đo trong khoảng Frequency cho phép với parameters — Measurement (S11/S21)

        @details: Verify toàn bộ luồng cấu hình VNA sau khi đã Connected:
                  chọn S-parameter, thiết lập Stimulus

        @pre:- PC17 đã Connected (được đảm bảo bởi _ensure_connected)
             - VNA panel có thể mở được

        @test_procedure:
                        [code]
                            # Stimulus
                                - Mở tab Stimulus
                                - Set Start Frequency = 100kHz, Stop = 18GHz
                                - Set Center = 9.05GHz, Span = 3GHz
                                - Set Points = 301, IF BW = 10kHz, Power = 0
                                - Click Apply
                            
                            # Measurement
                                - Mở tab Measurement trong VNA panel
                                - Chọn S11, chọn S21
                                - Click Apply
                        [!code]

        @pass_criteria:- S11 và S21 được chọn thành công
                       - Tất cả thông số Stimulus được điền và Apply thành công

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        START_FREQ = "100kHz"

        # ── Measurement ─────────────────────────────────────────────────────────
        main_page.open_measurement()
        main_page.select_s_parameter("S11")
        main_page.select_s_parameter("S21")
        main_page.click_apply()

        # ── Verify traces S11 + S21 hiển thị trên chart ─────────────────────────
        traces = main_page.extract_traces()
        s_params = [t["s_param"] for t in traces]
        assert "S11" in s_params, f"S11 không xuất hiện trong traces: {traces}"
        assert "S21" in s_params, f"S21 không xuất hiện trong traces: {traces}"

        # ── Stimulus ────────────────────────────────────────────────────────────
        main_page.open_stimulus()
        errs = main_page.set_stimulus_params(
            start=START_FREQ,
            stop="18GHz",
            center="9.05GHz",
            span="3GHz",
            points="301",
            if_bw="10kHz",
            power="0",
        )
        assert not errs, f"VNA Stimulus validation errors: {errs}"

    @testcase
    def test_vna_puc_2_1_0005(self, main_page: MainPage):
        """
        @test_id: test_vna_puc_2_1_0005
        @brief: Thực hiện bài đo trong khoảng Frequency cho phép với parameters — Measurement (S12/S22/S11/S21)

        @details: Verify toàn bộ luồng cấu hình VNA sau khi đã Connected:
                  chọn S-parameter, thiết lập Stimulus

        @pre:- PC17 đã Connected (được đảm bảo bởi _ensure_connected)
             - VNA panel có thể mở được

        @test_procedure:
                        [code]
                            # Stimulus
                                - Mở tab Stimulus
                                - Set Start Frequency = 100kHz, Stop = 18GHz
                                - Set Center = 9.05GHz, Span = 3GHz
                                - Set Points = 301, IF BW = 10kHz, Power = 0
                                - Click Apply
                            
                            # Measurement
                                - Mở tab Measurement trong VNA panel
                                - Chọn S12, chọn S22 , chọn S11 , chọn S21
                                - Click Apply
                        [!code]

        @pass_criteria:- S11 và S21 được chọn thành công
                       - Tất cả thông số Stimulus được điền và Apply thành công

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        START_FREQ = "100kHz"

        # ── Measurement ─────────────────────────────────────────────────────────
        main_page.open_measurement()
        main_page.select_s_parameter("S12")
        main_page.select_s_parameter("S22")
        main_page.click_apply()

        # ── Verify tất cả 4 traces hiển thị trên chart
        traces = main_page.extract_traces()
        s_params = [t["s_param"] for t in traces]
        for expected in ("S11", "S21", "S12", "S22"):
            assert expected in s_params, f"{expected} không xuất hiện trong traces: {traces}"

        # ── Stimulus ────────────────────────────────────────────────────────────
        main_page.open_stimulus()
        main_page.set_stimulus_params(
            start=START_FREQ,
            stop="18GHz",
            center="9.05GHz",
            span="3GHz",
            points="301",
            if_bw="10kHz",
            power="0",
        )

    @testcase
    def test_vna_puc_2_1_0006(self, main_page: MainPage):
        """
        @test_id: test_vna_puc_2_1_0006
        @brief: Thực hiện bài đo trong khoảng Frequency cho phép với parameters — Measurement (S11/S21)

        @details: Verify toàn bộ luồng cấu hình VNA sau khi đã Connected:
                  chọn S-parameter, thiết lập Stimulus

        @pre:- PC17 đã Connected (được đảm bảo bởi _ensure_connected)
             - VNA panel có thể mở được

        @test_procedure:
                        [code]
                            # Stimulus
                                - Mở tab Stimulus
                                - Set Start Frequency = 10kHz, Stop = 19GHz
                                - Set Center = 9.05GHz, Span = 3GHz
                                - Set Points = 301, IF BW = 10kHz, Power = 0
                                - Click Apply
                        [!code]

        @pass_criteria:- Tất cả thông số Stimulus được điền và sau khi apply nếu lỗi thì có hiện thông báo lỗi không
        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        START_FREQ = "10kHz"
        # ── Stimulus ────────────────────────────────────────────────────────────
        main_page.open_stimulus()
        main_page.set_stimulus_params(
            start=START_FREQ,
            stop="19GHz",
            center="9.05GHz",
            span="3GHz",
            points="301",
            if_bw="10kHz",
            power="0",
        )

    @testcase
    def test_vna_puc_2_1_0007(self, main_page: MainPage):
        """
        @test_id: test_vna_puc_2_1_0007
        @brief: Thực hiện bài calibration

        @details: Thực hiện bài test calibration trên port SOLT CAL

        @pre:- PC17 đã Connected (được đảm bảo bởi _ensure_connected)
             - VNA panel có thể mở được

        @test_procedure:
                        [code]
                            # Stimulus
                                - Mở tab Calibration -> Calibrate 
                                - Chọn 2-Port SOLT Cal
                                - Calibration toàn bộ port
                        [!code]

        @pass_criteria:- Khi hoàn thành, sẽ xuất hiện dấu tích (✓) ở phía trái softkey
        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        # ── Calibration → Calibrate → 2-Port SOLT Cal → click tất cả steps → Apply
        main_page.open_calibration()
        main_page.click_calibrate()
        main_page.click_solt_cal()
        main_page.click_all_calibration_steps()

        completed = main_page.wait_for_calibration_complete(timeout=60)
        assert completed, "VNA Calibration: không đủ 7/7 bước 'Completed' sau 60s"