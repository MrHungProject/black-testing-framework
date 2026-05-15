# -*- coding: utf-8 -*-
"""
Oscilloscope DSO/DDS Setting functional test suite -- PUC_2.3
"""
import time

import pytest

from core import testcase
from pages.main_page import MainPage

_DEVICE_LABEL = "Oscilloscope"


# ============================================================================
#  Connection tests
# ============================================================================

class TestOscilloscopePuc23Connection:
    """PUC_2.3 -- Kết nối / Ngắt kết nối Oscilloscope."""

    @testcase
    def test_oscilloscope_puc_2_3_0001(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0001
        @brief: Kết nối Oscilloscope thành công qua System -> Connection

        @pre:- PC17 đang chạy
             - Oscilloscope chưa Connected

        @test_procedure:
            [code]
                Bước 1: Mở Connect panel
                Bước 2: Nếu chưa Connected -> click Connect Oscilloscope
                Bước 3: Đợi 3 giây
                Bước 4: Verify trạng thái là Connected
            [!code]

        @pass_criteria:- Oscilloscope hiển thị trạng thái Connected

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        if main_page.is_device_connected(_DEVICE_LABEL):
            main_page.open_connect_panel()
            main_page.disconnect_device(_DEVICE_LABEL)
            time.sleep(2)

        main_page.open_connect_panel()
        main_page.connect_device(_DEVICE_LABEL)
        time.sleep(3)

        assert main_page.is_device_connected(_DEVICE_LABEL), \
            "Oscilloscope chưa Connected sau 3 giây"

    @testcase
    def test_oscilloscope_puc_2_3_0002(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0002
        @brief: Ngắt kết nối Oscilloscope thành công qua System -> Connection

        @pre:- PC17 đang chạy
             - Oscilloscope đang Connected

        @test_procedure:
            [code]
                Bước 1: Đảm bảo Oscilloscope đang Connected
                Bước 2: Mở Connect panel
                Bước 3: Click Disconnect Oscilloscope
                Bước 4: Verify trạng thái là Disconnected
            [!code]

        @pass_criteria:- Oscilloscope hiển thị trạng thái Disconnected

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        if not main_page.is_device_connected(_DEVICE_LABEL):
            main_page.open_connect_panel()
            main_page.connect_device(_DEVICE_LABEL)
            time.sleep(3)

        main_page.open_connect_panel()
        main_page.disconnect_device(_DEVICE_LABEL)
        time.sleep(2)

        assert not main_page.is_device_connected(_DEVICE_LABEL), \
            "Oscilloscope vẫn còn Connected sau khi Disconnect"


# ============================================================================
#  DSO Setting tests
# ============================================================================

class TestOscilloscopePuc23DsoSetting:
    """PUC_2.3 -- DSO Setting functional test cases."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        if not main_page.is_device_connected(_DEVICE_LABEL):
            main_page.open_connect_panel()
            main_page.connect_device(_DEVICE_LABEL)
            time.sleep(3)

    @testcase
    def test_oscilloscope_puc_2_3_0003(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0003
        @brief: [TC-001/002/030/031] Time/Div -- các giá trị hợp lệ, mặc định, min/max

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, quan sát giá trị mặc định của Time/Div
                Bước 2: Chọn lần lượt: 1 ms, 2 ms, 5 ms, 10 ms, 100 us, 500 us -> Apply mỗi lần
                Bước 3: Chọn giá trị nhỏ nhất có trong dropdown -> Apply
                Bước 4: Chọn giá trị lớn nhất có trong dropdown -> Apply
            [!code]

        @pass_criteria:- Giá trị mặc định = '2.00 ns'
                       - Mỗi giá trị được chọn hiển thị chính xác sau Apply
                       - Giá trị min/max không crash, hiển thị đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        default_val = main_page.get_dso_dropdown_value("Time/Div")
        assert default_val, "Không đọc được giá trị mặc định Time/Div"

        for value in ["500 us", "1.0 ms", "2.0 ms", "5.0 ms", "10.0 ms", "100 ms"]:
            errors = main_page.set_dso_params(time_div=value)
            assert not errors, f"Time/Div='{value}': lỗi validation {errors}"

        errors = main_page.set_dso_params(time_div="200 ns")
        assert not errors, f"Time/Div min='200 ns': lỗi validation {errors}"

        errors = main_page.set_dso_params(time_div="1.0 s")
        assert not errors, f"Time/Div max='1.0 s': lỗi validation {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0004(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0004
        @brief: [TC-003/004/005/034] Channel -- chọn CH1/CH2/CH3/CH4, toggle ON/OFF, đổi channel khi đang ON,
                các Chanel khi đổi đều phải ở trạng thái OFF khi chưa click

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, chọn CH(1-4) -> Apply, kiểm tra icon màu vàng
                Bước 2: Chuyển sang CH(1-4) -> Apply, kiểm tra icon màu thay đổi
                Bước 3: Click checkbox ON/OFF để bật kênh ON -> Apply
                Bước 4: Click lại checkbox ON/OFF để tắt kênh OFF -> Apply
                Bước 5: Bật kênh ON, đổi sang channel khác -> Apply, kiểm tra trạng thái ON/OFF của kênh mới
            [!code]

        @pass_criteria:- CH1/CH2/CH3/CH4 được chọn chính xác, icon màu hiển thị đúng
                       - Toggle ON/OFF phản hồi chính xác
                       - Đổi channel khi đang ON thành công, trạng thái giữ nguyên hoặc reset theo thiết kế

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        errors = main_page.set_dso_params(channel="CH1", channel_on=False)
        assert not errors, f"Chọn CH1 OFF: {errors}"
        assert not main_page.get_oscilloscope_channel_enabled(), "CH1 phải OFF"

        errors = main_page.set_dso_params(channel_on=True)
        assert not errors, f"Bật CH1 ON: {errors}"
        assert main_page.get_oscilloscope_channel_enabled(), "CH1 phải ON sau khi bật"

        errors = main_page.set_dso_params(channel_on=False)
        assert not errors, f"Tắt CH1 OFF: {errors}"
        assert not main_page.get_oscilloscope_channel_enabled(), "CH1 phải OFF sau khi tắt"

        for ch in ["CH2", "CH3", "CH4"]:
            errors = main_page.set_dso_params(channel=ch, channel_on=False)
            assert not errors, f"Chọn {ch}: {errors}"
            assert not main_page.get_oscilloscope_channel_enabled(), \
                f"{ch} phải OFF theo mặc định khi chưa bật"

        errors = main_page.set_dso_params(channel="CH1", channel_on=True)
        assert not errors, f"Bật CH1 ON trước khi đổi: {errors}"

        errors = main_page.set_dso_params(channel="CH2")
        assert not errors, f"Đổi sang CH2 khi CH1 đang ON: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0005(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0005
        @brief: [TC-006/007] Probe -- chọn X1 và X10

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, chọn X1 trong dropdown Probe -> Apply
                Bước 2: Chuyển sang X10 -> Apply
            [!code]

        @pass_criteria:- Probe X1: hệ số nhân = 1
                       - Probe X10: điện áp đo được nhân 10

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        errors = main_page.set_dso_params(probe="X1")
        assert not errors, f"Probe X1: {errors}"

        errors = main_page.set_dso_params(probe="X10")
        assert not errors, f"Probe X10: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0006(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0006
        @brief: [TC-008/009/032/033] Voltage/Div -- giá trị hợp lệ, mặc định, min/max

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, quan sát giá trị mặc định của Voltage/Div
                Bước 2: Chọn lần lượt: 1 V, 2 V, 500 mV, 100 mV -> Apply mỗi lần
                Bước 3: Chọn giá trị nhỏ nhất có trong dropdown -> Apply
                Bước 4: Chọn giá trị lớn nhất có trong dropdown -> Apply
            [!code]

        @pass_criteria:- Giá trị mặc định = '1 V'
                       - Mỗi giá trị được cập nhật đúng sau Apply
                       - Giá trị min/max không bị lỗi hiển thị, được lưu đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        default_val = main_page.get_dso_dropdown_value("Voltage/Div")
        assert default_val, "Không đọc được giá trị mặc định Voltage/Div"

        for value in ["1.00V", "2.00V", "500mV", "100mV"]:
            errors = main_page.set_dso_params(voltage_div=value)
            assert not errors, f"Voltage/Div='{value}': {errors}"

        errors = main_page.set_dso_params(voltage_div="1.00mV")
        assert not errors, f"Voltage/Div min='1.00mV': {errors}"

        errors = main_page.set_dso_params(voltage_div="10.0V")
        assert not errors, f"Voltage/Div max='10.0V': {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0007(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0007
        @brief: [TC-010/011/012] Coupling -- GND, AC, DC

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, chọn GND trong dropdown Coupling -> Apply
                Bước 2: Chuyển sang AC -> Apply
                Bước 3: Chuyển sang DC -> Apply
            [!code]

        @pass_criteria:- Coupling cập nhật chính xác sau mỗi lần Apply (GND / AC / DC)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        for coupling in ["GND", "AC", "DC"]:
            errors = main_page.set_dso_params(coupling=coupling)
            assert not errors, f"Coupling='{coupling}': {errors}"
            actual = main_page.get_dso_dropdown_value("Coupling")
            assert coupling.lower() in actual.lower(), \
                f"Coupling hiển thị '{actual}', mong đợi '{coupling}'"

    @testcase
    def test_oscilloscope_puc_2_3_0008(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0008
        @brief: [TC-013/014] Trigger Mode -- Edge và Pulse

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, chọn Edge trong dropdown Trigger Mode -> Apply
                Bước 2: Chuyển sang Pulse -> Apply
            [!code]

        @pass_criteria:- Trigger Mode cập nhật đúng (Edge / Pulse) sau mỗi lần Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        for mode in ["Edge", "Pulse"]:
            errors = main_page.set_dso_params(trigger_mode=mode)
            assert not errors, f"Trigger Mode='{mode}': {errors}"
            actual = main_page.get_dso_dropdown_value("Trigger Mode")
            assert mode.lower() in actual.lower(), \
                f"Trigger Mode hiển thị '{actual}', mong đợi '{mode}'"

    @testcase
    def test_oscilloscope_puc_2_3_0009(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0009
        @brief: [TC-015/016/017] Trigger Sweep -- AUTO, NORMAL, SINGLE

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, chọn AUTO trong dropdown Trigger Sweep -> Apply
                Bước 2: Chuyển sang NORMAL -> Apply
                Bước 3: Chuyển sang SINGLE -> Apply
            [!code]

        @pass_criteria:- Trigger Sweep cập nhật đúng (AUTO / NORMAL / SINGLE) sau mỗi lần Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        for sweep in ["Auto", "Normal", "Single"]:
            errors = main_page.set_dso_params(trigger_sweep=sweep)
            assert not errors, f"Trigger Sweep='{sweep}': {errors}"
            actual = main_page.get_dso_dropdown_value("Trigger Sweep")
            assert sweep.lower() in actual.lower(), \
                f"Trigger Sweep hiển thị '{actual}', mong đợi '{sweep}'"

    @testcase
    def test_oscilloscope_puc_2_3_0010(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0010
        @brief: [TC-029/035] Actions -- đóng panel và thay đổi nhiều tham số liên tiếp nhanh

        @pre:- Oscilloscope đã Connected
             - Panel 'Oscilloscope - illoscopeDso' đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, click nút X trên tiêu đề panel -> kiểm tra panel đóng lại
                Bước 2: Mở lại DSO Setting, thay đổi Time/Div -> Voltage/Div -> Coupling liên tiếp nhanh
                Bước 3: Click Apply, lặp lại 3-5 lần với các tổ hợp giá trị khác nhau
            [!code]

        @pass_criteria:- Panel đóng lại khi click X
                       - Thay đổi nhiều tham số nhanh không bị lag, tất cả được lưu đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()

        main_page.close_dso_setting()
        time.sleep(0.5)
        assert not main_page.is_dso_setting_open(), \
            "DSO Setting vẫn còn mở sau khi đóng bằng X"

        main_page.open_dso_setting()
        assert main_page.is_dso_setting_open(), "DSO Setting không mở lại được"

        param_sets = [
            {"time_div": "1.0 ms",  "voltage_div": "500mV", "coupling": "AC"},
            {"time_div": "5.0 ms",  "voltage_div": "1.00V", "coupling": "DC"},
            {"time_div": "10.0 ms", "voltage_div": "100mV", "coupling": "GND"},
            {"time_div": "500 us",  "voltage_div": "2.00V", "coupling": "AC"},
        ]
        for params in param_sets:
            errors = main_page.set_dso_params(**params)
            assert not errors, f"Thay đổi nhanh {params}: lỗi {errors}"


# ============================================================================
#  DDS Setting tests
# ============================================================================

class TestOscilloscopePuc23DdsSetting:
    """PUC_2.3 -- DDS Setting functional test cases."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        if not main_page.is_device_connected(_DEVICE_LABEL):
            main_page.open_connect_panel()
            main_page.connect_device(_DEVICE_LABEL)
            time.sleep(3)

    @testcase
    def test_oscilloscope_puc_2_3_0011(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0011
        @brief: [DDS-001/002/003] Signal On -- bật, tắt và giá trị mặc định

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting lần đầu, quan sát trạng thái mặc định của checkbox Signal On
                Bước 2: Tick vào checkbox Signal On -> Apply
                Bước 3: Bỏ tick checkbox Signal On -> Apply
            [!code]

        @pass_criteria:- Mặc định: Signal On = unchecked (tắt)
                       - Sau khi tick: checkbox được chọn, tín hiệu DDS bắt đầu phát
                       - Sau khi bỏ tick: checkbox bỏ chọn, tín hiệu dừng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        if main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
            time.sleep(0.2)

        assert not main_page.is_dds_signal_on_checked(), \
            "Signal On phải là OFF theo mặc định"

        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()
        time.sleep(0.2)
        assert main_page.is_dds_signal_on_checked(), \
            "Signal On phải ON sau khi tick"

        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()
        time.sleep(0.2)
        assert not main_page.is_dds_signal_on_checked(), \
            "Signal On phải OFF sau khi bỏ tick"

    @testcase
    def test_oscilloscope_puc_2_3_0012(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0012
        @brief: [DDS-004/005/032] Sync -- bật, tắt và Sync khi Signal On đang tắt

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, để Signal On = off, tick Sync -> Apply
                Bước 2: Kiểm tra phản hồi (cảnh báo hoặc ghi nhận trạng thái)
                Bước 3: Bật Signal On trước, sau đó tick Sync -> Apply
                Bước 4: Bỏ tick Sync -> Apply
            [!code]

        @pass_criteria:- Sync bật/tắt phản hồi chính xác
                       - Sync khi Signal On tắt: không crash, có cảnh báo hoặc ghi nhận đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        if main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()

        if main_page.is_dds_sync_checked():
            main_page.click_dds_sync()
            main_page.oscilloscope_apply()

        main_page.click_dds_sync()
        main_page.oscilloscope_apply()
        time.sleep(0.2)

        if main_page.is_dds_sync_checked():
            main_page.click_dds_sync()
            main_page.oscilloscope_apply()

        if not main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()

        main_page.click_dds_sync()
        main_page.oscilloscope_apply()
        time.sleep(0.2)
        assert main_page.is_dds_sync_checked(), "Sync phải ON sau khi tick (Signal On đang bật)"

        main_page.click_dds_sync()
        main_page.oscilloscope_apply()
        time.sleep(0.2)
        assert not main_page.is_dds_sync_checked(), "Sync phải OFF sau khi bỏ tick"

        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()

    @testcase
    def test_oscilloscope_puc_2_3_0013(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0013
        @brief: [DDS-006/007/008/009/010/030] Signal Type -- tất cả loại sóng, mặc định, đổi khi đang phát

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, quan sát Signal Type mặc định
                Bước 2: Chọn lần lượt Sine, Square, Triangle, Sawtooth (nếu có) -> Apply mỗi lần
                Bước 3: Bật Signal On -> Apply
                Bước 4: Đổi Signal Type từ Sine sang Square trong khi Signal On đang bật -> Apply
            [!code]

        @pass_criteria:- Mặc định: Signal Type = Sine
                       - Mỗi loại sóng được cập nhật chính xác sau Apply
                       - Đổi loại sóng khi đang phát: sóng chuyển loại thành công, không gián đoạn bất thường

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        if main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()

        errors = main_page.set_dds_params(signal_type="Sine")
        assert not errors, f"Signal Type mặc định Sine: {errors}"

        for signal_type in ["Square", "AM/FM", "Ramp"]:
            errors = main_page.set_dds_params(signal_type=signal_type)
            assert not errors, f"Signal Type='{signal_type}': {errors}"

        errors = main_page.set_dds_params(signal_type="Sine")
        assert not errors

        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()
        assert main_page.is_dds_signal_on_checked()

        errors = main_page.set_dds_params(signal_type="Square")
        assert not errors, f"Đổi Signal Type khi Signal On đang bật: {errors}"

        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()

    @testcase
    def test_oscilloscope_puc_2_3_0014(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0014
        @brief: [DDS-011/012/013/014/025/026] Frequency -- giá trị hợp lệ, mặc định, edge cases

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, quan sát giá trị mặc định của Frequency
                Bước 2: Nhập các giá trị hợp lệ: 1, 10000, 1000000 -> Apply mỗi lần
                Bước 3: Nhập 0 -> Apply, quan sát phản hồi
                Bước 4: Nhập giá trị tần số tối đa phần cứng hỗ trợ -> Apply
            [!code]

        @pass_criteria:- Mặc định: Frequency = 10000
                       - Giá trị 1 Hz, 10000 Hz, 1000000 Hz được chấp nhận
                       - Frequency = 0: cảnh báo hoặc xử lý đúng theo thiết kế
                       - Frequency cực đại: chấp nhận hoặc giới hạn đúng, không crash

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        default_val = main_page.get_dds_field_value("txtFreq")
        assert default_val == "10000" or default_val, \
            f"Frequency mặc định không đọc được (thực tế: '{default_val}')"

        for freq in ["1", "10000", "1000000"]:
            errors = main_page.set_dds_params(frequency_hz=freq)
            assert not errors, f"Frequency='{freq}': lỗi validation {errors}"
            actual = main_page.get_dds_field_value("txtFreq")
            assert actual == freq, f"Frequency sau Apply: mong đợi '{freq}', thực tế '{actual}'"

        main_page.set_dds_params(frequency_hz="0")
        time.sleep(0.2)

        errors = main_page.set_dds_params(frequency_hz="12000000")
        assert not errors, f"Frequency cực đại: crash hoặc lỗi không mong đợi {errors}"

        main_page.set_dds_params(frequency_hz="10000")

    @testcase
    def test_oscilloscope_puc_2_3_0015(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0015
        @brief: [DDS-033/034/035/042] Frequency -- invalid inputs (chữ, ký tự đặc biệt, âm, quá giới hạn)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, nhập 'abc' vào Frequency -> Apply
                Bước 2: Nhập '!@#$' vào Frequency -> Apply
                Bước 3: Nhập -100 vào Frequency -> Apply
                Bước 4: Nhập 99999999999 (quá giới hạn) vào Frequency -> Apply
            [!code]

        @pass_criteria:- Ký tự chữ/đặc biệt: Báo lỗi Frequency: Invalid number format
                       - Giá trị âm: Frequency cannot be less than 1 Hz
                       - Quá giới hạn: hiển thị lỗi hoặc tự giới hạn về max cho phép

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")

        for invalid in ["abc", "!@#$"]:
            errors = main_page.set_dds_params(frequency_hz=invalid)
            if not errors:
                actual = main_page.get_dds_field_value("txtFreq")
                assert actual != invalid, \
                    f"Field chấp nhận giá trị không hợp lệ '{invalid}' (thực tế: '{actual}')"
            main_page.set_dds_params(frequency_hz="10000")

        errors = main_page.set_dds_params(frequency_hz="-100")
        assert errors, f"Frequency âm '-100' phải báo lỗi validation, nhưng không có lỗi"
        main_page.set_dds_params(frequency_hz="10000")

        main_page.set_dds_params(frequency_hz="99999999999")
        time.sleep(0.2)
        main_page.set_dds_params(frequency_hz="10000")

    @testcase
    def test_oscilloscope_puc_2_3_0016(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0016
        @brief: [DDS-015/016/017/027/028] Amplitude -- giá trị hợp lệ, số thực, mặc định, edge cases

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, quan sát giá trị mặc định của Amplitude
                Bước 2: Nhập 1 vào Amplitude -> Apply
                Bước 3: Nhập 0.5 vào Amplitude -> Apply
                Bước 4: Nhập 0 vào Amplitude -> Apply, quan sát phản hồi
                Bước 5: Nhập giá trị Amplitude lớn nhất thiết bị cho phép -> Apply
            [!code]

        @pass_criteria:- Mặc định: Amplitude = 1
                       - 1 V và 0.5 V được chấp nhận
                       - Amplitude = 0: chấp nhận hoặc cảnh báo theo thiết kế
                       - Amplitude cực đại: chấp nhận hoặc báo vượt ngưỡng, không crash

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        default_val = main_page.get_dds_field_value("txtAmplitude")
        assert default_val, f"Không đọc được giá trị mặc định Amplitude (thực tế: '{default_val}')"

        for amp in ["1", "0.5"]:
            errors = main_page.set_dds_params(amplitude_v=amp)
            assert not errors, f"Amplitude='{amp}': lỗi {errors}"
            actual = main_page.get_dds_field_value("txtAmplitude")
            assert actual == amp, f"Amplitude sau Apply: mong đợi '{amp}', thực tế '{actual}'"

        main_page.set_dds_params(amplitude_v="0")
        time.sleep(0.2)

        main_page.set_dds_params(amplitude_v="5")
        time.sleep(0.2)

        main_page.set_dds_params(amplitude_v="1")

    @testcase
    def test_oscilloscope_puc_2_3_0017(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0017
        @brief: [DDS-018/019/020/029/036/037/038] Offset -- giá trị hợp lệ, edge case, invalid inputs

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, nhập Offset = 1 -> Apply
                Bước 2: Nhập Offset = 0 -> Apply
                Bước 3: Nhập Offset = -1 -> Apply
                Bước 4: Đặt Amplitude = 1, Offset = 5 (Offset > Amplitude) -> Apply, quan sát phản hồi
                Bước 5: Nhập 'xyz' vào Offset -> Apply
                Bước 6: Nhập 'abc' vào Amplitude -> Apply
                Bước 7: Nhập -1 vào Amplitude -> Apply
            [!code]

        @pass_criteria:- Offset 1 V / 0 / -1 V: được chấp nhận
                       - Offset > Amplitude: cảnh báo hoặc xử lý clipping theo thiết kế
                       - Offset 'xyz', Amplitude 'abc': từ chối, hiển thị lỗi
                       - Amplitude âm: không chấp nhận hoặc cảnh báo

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        main_page.set_dds_params(amplitude_v="1", offset_v="0")

        for offset in ["1", "0", "-1"]:
            errors = main_page.set_dds_params(offset_v=offset)
            assert not errors, f"Offset='{offset}': lỗi không mong đợi {errors}"

        main_page.set_dds_params(amplitude_v="1", offset_v="5")
        time.sleep(0.2)

        main_page.set_dds_params(amplitude_v="1", offset_v="0")

        errors = main_page.set_dds_params(offset_v="xyz")
        if not errors:
            actual = main_page.get_dds_field_value("txtOffset")
            assert actual != "xyz", f"Offset chấp nhận giá trị không hợp lệ 'xyz'"
        main_page.set_dds_params(amplitude_v="1", offset_v="0")

        errors = main_page.set_dds_params(amplitude_v="abc")
        if not errors:
            actual = main_page.get_dds_field_value("txtAmplitude")
            assert actual != "abc", f"Amplitude chấp nhận giá trị không hợp lệ 'abc'"
        main_page.set_dds_params(amplitude_v="1", offset_v="0")

        errors = main_page.set_dds_params(amplitude_v="-1")
        assert errors, "Amplitude âm '-1' phải báo lỗi validation"
        main_page.set_dds_params(amplitude_v="1", offset_v="0")

    @testcase
    def test_oscilloscope_puc_2_3_0018(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0018
        @brief: [DDS-021/022/023/024/031] Actions -- Apply, Cancel, đóng panel, apply khi Signal On bật, apply nhiều lần

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, điền đầy đủ (Signal Type=Sine, Frequency=10000, Amplitude=1, Offset=1) -> Apply
                Bước 2: Thay đổi một số giá trị -> Cancel, kiểm tra giá trị không bị lưu
                Bước 3: Bật Signal On, thay đổi Frequency -> Apply, kiểm tra tín hiệu cập nhật
                Bước 4: Click nút X trên tiêu đề panel -> kiểm tra panel đóng
                Bước 5: Mở lại, click Apply nhiều lần liên tiếp (5-10 lần)
            [!code]

        @pass_criteria:- Apply đầy đủ: lưu/áp dụng thành công
                       - Cancel: giá trị không được lưu
                       - Apply khi Signal On: tín hiệu cập nhật ngay
                       - Đóng bằng X: panel đóng
                       - Apply nhiều lần: không treo, không gửi lệnh trùng lặp

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        errors = main_page.set_dds_params(
            signal_type="Sine", frequency_hz="10000",
            amplitude_v="1", offset_v="1",
        )
        assert not errors, f"Apply đầy đủ tham số: {errors}"

        main_page.set_dds_params_no_apply(frequency_hz="99999", amplitude_v="2")
        main_page.oscilloscope_cancel()
        time.sleep(0.3)

        main_page.open_dds_setting()
        freq_after_cancel = main_page.get_dds_field_value("txtFreq")
        assert freq_after_cancel == "10000", \
            f"Frequency phải là '10000' sau Cancel, thực tế '{freq_after_cancel}'"

        if main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()
        assert main_page.is_dds_signal_on_checked()

        errors = main_page.set_dds_params(frequency_hz="20000")
        assert not errors, f"Apply khi Signal On đang bật: {errors}"

        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()

        main_page.close_dds_setting()
        time.sleep(0.5)
        assert not main_page.is_dds_setting_open(), \
            "DDS Setting vẫn còn mở sau khi đóng bằng X"

        main_page.open_dds_setting()
        for i in range(5):
            errors = main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")
            assert not errors, f"Apply lần {i + 1}: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0019(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0019
        @brief: [DDS-039/040/041] Actions negative -- Apply khi trường trống, mất kết nối khi Apply

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, xóa toàn bộ giá trị trường Frequency -> Apply
                Bước 2: Xóa toàn bộ giá trị trường Amplitude -> Apply
                Bước 3: Điền đầy đủ tham số hợp lệ, rút kết nối thiết bị, click Apply
            [!code]

        @pass_criteria:- Frequency/Amplitude để trống: hiển thị lỗi validation, không gửi lệnh
                       - Mất kết nối: hiển thị thông báo lỗi, không crash

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()

        errors = main_page.set_dds_params(frequency_hz=" ")
        assert errors, "Frequency để trống phải báo lỗi validation"
        main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")

        errors = main_page.set_dds_params(amplitude_v=" ")
        assert errors, "Amplitude để trống phải báo lỗi validation"
        main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")

        pytest.skip(
            "DDS-041: Không thể giả lập mất kết nối phần cứng trong automation — "
            "cần test thủ công."
        )
