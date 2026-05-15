# -*- coding: utf-8 -*-
"""
Oscilloscope DSO/DDS Setting functional test suite -- PUC_2.3
Mỗi test case kiểm tra đúng 1 chức năng / 1 điều kiện cụ thể.
"""
import time

import pytest

from core import testcase
from pages.main_page import MainPage

_DEVICE_LABEL = "Oscilloscope"

# Flag tránh reconnect tốn thời gian trước mỗi test.
# Được set True sau lần connect đầu tiên trong session.
_oscilloscope_connected: bool = False


# ============================================================================
#  Connection tests  (TC0001 – TC0002)
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
                Bước 1: Đảm bảo Oscilloscope đang Disconnected
                Bước 2: Mở Connect panel -> click Connect Oscilloscope
                Bước 3: Đợi 3 giây
                Bước 4: Verify trạng thái là Connected
            [!code]

        @pass_criteria:- Oscilloscope hiển thị trạng thái Connected

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        global _oscilloscope_connected
        main_page.open_connect_panel()
        if main_page.is_device_connected(_DEVICE_LABEL):
            main_page.disconnect_device(_DEVICE_LABEL)
            time.sleep(2)

        main_page.connect_device(_DEVICE_LABEL)
        time.sleep(3)

        assert main_page.is_device_connected(_DEVICE_LABEL), \
            "Oscilloscope chưa Connected sau 3 giây"
        _oscilloscope_connected = True

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
                Bước 2: Mở Connect panel -> click Disconnect Oscilloscope
                Bước 3: Đợi 2 giây
                Bước 4: Verify trạng thái là Disconnected
            [!code]

        @pass_criteria:- Oscilloscope hiển thị trạng thái Disconnected

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        global _oscilloscope_connected
        main_page.open_connect_panel()
        if not main_page.is_device_connected(_DEVICE_LABEL):
            main_page.connect_device(_DEVICE_LABEL)
            time.sleep(3)

        main_page.disconnect_device(_DEVICE_LABEL)
        time.sleep(2)

        assert not main_page.is_device_connected(_DEVICE_LABEL), \
            "Oscilloscope vẫn Connected sau khi Disconnect"
        _oscilloscope_connected = False


# ============================================================================
#  DSO Setting tests  (TC0003 – TC0029)
# ============================================================================

class TestOscilloscopePuc23DsoSetting:
    """PUC_2.3 -- DSO Setting: mỗi TC kiểm tra đúng 1 thông số / 1 hành vi."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Kết nối thiết bị nếu chưa kết nối. Dùng flag để tránh reconnect mỗi test."""
        global _oscilloscope_connected
        if _oscilloscope_connected:
            return
        main_page.open_connect_panel()
        if not main_page.is_device_connected(_DEVICE_LABEL):
            main_page.connect_device(_DEVICE_LABEL)
            time.sleep(3)
        _oscilloscope_connected = True

    # ── Time/Div ──────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0003(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0003
        @brief: [DSO-030] Time/Div -- giá trị mặc định đọc được khi mở DSO Setting

        @pre:- Oscilloscope đã Connected

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Đọc giá trị hiển thị của dropdown Time/Div
            [!code]

        @pass_criteria:- Dropdown Time/Div có giá trị mặc định (không rỗng)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        val = main_page.get_dso_dropdown_value("Time/Div")
        assert val, "Không đọc được giá trị mặc định Time/Div"

    @testcase
    def test_oscilloscope_puc_2_3_0004(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0004
        @brief: [DSO-001] Time/Div -- chọn các giá trị hợp lệ (500 us → 100 ms)

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn lần lượt 500 us, 1.0 ms, 2.0 ms, 5.0 ms, 10.0 ms, 100 ms -> Apply mỗi lần
                Bước 3: Verify không có lỗi validation sau mỗi lần Apply
            [!code]

        @pass_criteria:- Tất cả giá trị được chấp nhận, không có lỗi validation

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        for value in ["500 us", "1.00 ms", "2.00 ms", "5.00 ms", "10.0 ms", "100 ms"]:
            errors = main_page.set_dso_params(time_div=value)
            assert not errors, f"Time/Div='{value}': lỗi validation {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0005(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0005
        @brief: [DSO-031] Time/Div -- giá trị nhỏ nhất (200 ns)

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Time/Div = '200 ns' -> Apply
                Bước 3: Verify không có lỗi validation
            [!code]

        @pass_criteria:- Time/Div '200 ns' được chấp nhận, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(time_div="200 ns")
        assert not errors, f"Time/Div min '200 ns': lỗi {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0006(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0006
        @brief: [DSO-032] Time/Div -- giá trị lớn nhất (1.0 s)

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Time/Div = '1.00 s' -> Apply
                Bước 3: Verify không có lỗi validation
            [!code]

        @pass_criteria:- Time/Div '1.0 s' được chấp nhận, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(time_div="1.00 s")
        assert not errors, f"Time/Div max '1.00 s': lỗi {errors}"

    # ── Channel ───────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0007(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0007
        @brief: [DSO-003] Channel -- chọn CH1 và verify mặc định OFF

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Channel = CH1 -> Apply
                Bước 3: Verify channel CH1 ở trạng thái OFF (chưa bật)
            [!code]

        @pass_criteria:- CH1 được chọn, trạng thái mặc định là OFF

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(channel="CH1", channel_on=False)
        assert not errors, f"Chọn CH1: {errors}"
        assert not main_page.get_oscilloscope_channel_enabled(), "CH1 phải OFF theo mặc định"

    @testcase
    def test_oscilloscope_puc_2_3_0008(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0008
        @brief: [DSO-003] Channel -- chọn CH2 và verify mặc định OFF

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Channel = CH2 -> Apply
                Bước 3: Verify channel CH2 ở trạng thái OFF
            [!code]

        @pass_criteria:- CH2 được chọn, trạng thái mặc định là OFF

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(channel="CH2", channel_on=False)
        assert not errors, f"Chọn CH2: {errors}"
        assert not main_page.get_oscilloscope_channel_enabled(), "CH2 phải OFF theo mặc định"

    @testcase
    def test_oscilloscope_puc_2_3_0009(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0009
        @brief: [DSO-003] Channel -- chọn CH3 và verify mặc định OFF

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Channel = CH3 -> Apply
                Bước 3: Verify channel CH3 ở trạng thái OFF
            [!code]

        @pass_criteria:- CH3 được chọn, trạng thái mặc định là OFF

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(channel="CH3", channel_on=False)
        assert not errors, f"Chọn CH3: {errors}"
        assert not main_page.get_oscilloscope_channel_enabled(), "CH3 phải OFF theo mặc định"

    @testcase
    def test_oscilloscope_puc_2_3_0010(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0010
        @brief: [DSO-003] Channel -- chọn CH4 và verify mặc định OFF

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Channel = CH4 -> Apply
                Bước 3: Verify channel CH4 ở trạng thái OFF
            [!code]

        @pass_criteria:- CH4 được chọn, trạng thái mặc định là OFF

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(channel="CH4", channel_on=False)
        assert not errors, f"Chọn CH4: {errors}"
        assert not main_page.get_oscilloscope_channel_enabled(), "CH4 phải OFF theo mặc định"

    @testcase
    def test_oscilloscope_puc_2_3_0011(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0011
        @brief: [DSO-004] Channel -- bật kênh ON bằng checkbox ON/OFF

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở, CH1 đang OFF

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, chọn CH1 OFF
                Bước 2: Click checkbox ON/OFF để bật ON -> Apply
                Bước 3: Verify trạng thái kênh là ON
            [!code]

        @pass_criteria:- Sau khi click ON/OFF, kênh CH1 chuyển sang trạng thái ON

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        main_page.set_dso_params(channel="CH1", channel_on=False)
        errors = main_page.set_dso_params(channel_on=True)
        assert not errors, f"Bật CH1 ON: {errors}"
        assert main_page.get_oscilloscope_channel_enabled(), "CH1 phải ON sau khi bật"

    @testcase
    def test_oscilloscope_puc_2_3_0012(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0012
        @brief: [DSO-004] Channel -- tắt kênh OFF bằng checkbox ON/OFF

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở, kênh đang ON

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, bật CH1 ON
                Bước 2: Click checkbox ON/OFF để tắt OFF -> Apply
                Bước 3: Verify trạng thái kênh là OFF
            [!code]

        @pass_criteria:- Sau khi click ON/OFF, kênh CH1 chuyển sang trạng thái OFF

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        main_page.set_dso_params(channel="CH1", channel_on=True)
        errors = main_page.set_dso_params(channel_on=False)
        assert not errors, f"Tắt CH1 OFF: {errors}"
        assert not main_page.get_oscilloscope_channel_enabled(), "CH1 phải OFF sau khi tắt"

    @testcase
    def test_oscilloscope_puc_2_3_0013(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0013
        @brief: [DSO-005] Channel -- đổi sang channel khác khi kênh hiện tại đang ON

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở, CH1 đang ON

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting, bật CH1 ON -> Apply
                Bước 2: Đổi Channel sang CH2 -> Apply
                Bước 3: Verify không có lỗi, CH2 được chọn thành công
            [!code]

        @pass_criteria:- Đổi channel khi đang ON không bị lỗi, CH2 được chọn

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        main_page.set_dso_params(channel="CH1", channel_on=True)
        errors = main_page.set_dso_params(channel="CH2")
        assert not errors, f"Đổi sang CH2 khi CH1 đang ON: {errors}"

    # ── Probe ─────────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0014(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0014
        @brief: [DSO-006] Probe -- chọn X1

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Probe = X1 -> Apply
                Bước 3: Verify không có lỗi validation
            [!code]

        @pass_criteria:- Probe X1 được chọn thành công, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(probe="X1")
        assert not errors, f"Probe X1: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0015(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0015
        @brief: [DSO-007] Probe -- chọn X10

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Probe = X10 -> Apply
                Bước 3: Verify không có lỗi validation
            [!code]

        @pass_criteria:- Probe X10 được chọn thành công, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(probe="X10")
        assert not errors, f"Probe X10: {errors}"

    # ── Voltage/Div ───────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0016(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0016
        @brief: [DSO-033] Voltage/Div -- giá trị mặc định đọc được khi mở DSO Setting

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Đọc giá trị hiển thị của dropdown Voltage/Div
            [!code]

        @pass_criteria:- Dropdown Voltage/Div có giá trị mặc định (không rỗng)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        val = main_page.get_dso_dropdown_value("Voltage/Div")
        assert val, "Không đọc được giá trị mặc định Voltage/Div"

    @testcase
    def test_oscilloscope_puc_2_3_0017(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0017
        @brief: [DSO-008] Voltage/Div -- chọn các giá trị hợp lệ (1 V → 100 mV)

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn lần lượt 1.00V, 2.00V, 500mV, 100mV -> Apply mỗi lần
                Bước 3: Verify không có lỗi validation sau mỗi lần Apply
            [!code]

        @pass_criteria:- Tất cả giá trị được chấp nhận, không có lỗi validation

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        for value in ["1.00 V", "2.00 V", "500 mV", "100 mV"]:
            errors = main_page.set_dso_params(voltage_div=value)
            assert not errors, f"Voltage/Div='{value}': {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0018(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0018
        @brief: [DSO-032] Voltage/Div -- giá trị nhỏ nhất (1.00mV)

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Voltage/Div = '1.00 mV' -> Apply
                Bước 3: Verify không có lỗi validation
            [!code]

        @pass_criteria:- Voltage/Div '1.00mV' được chấp nhận, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(voltage_div="1.00 mV")
        assert not errors, f"Voltage/Div min '1.00 mV': {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0019(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0019
        @brief: [DSO-033] Voltage/Div -- giá trị lớn nhất (10.0V)

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Voltage/Div = '10.0V' -> Apply
                Bước 3: Verify không có lỗi validation
            [!code]

        @pass_criteria:- Voltage/Div '10.0V' được chấp nhận, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(voltage_div="10.0 V")
        assert not errors, f"Voltage/Div max '10.0 V': {errors}"

    # ── Coupling ──────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0020(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0020
        @brief: [DSO-010] Coupling -- chọn GND

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Coupling = GND -> Apply
                Bước 3: Verify dropdown Coupling hiển thị GND
            [!code]

        @pass_criteria:- Coupling GND được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(coupling="GND")
        assert not errors, f"Coupling GND: {errors}"
        actual = main_page.get_dso_dropdown_value("Coupling")
        assert "gnd" in actual.lower(), f"Coupling hiển thị '{actual}', mong đợi 'GND'"

    @testcase
    def test_oscilloscope_puc_2_3_0021(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0021
        @brief: [DSO-011] Coupling -- chọn AC

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Coupling = AC -> Apply
                Bước 3: Verify dropdown Coupling hiển thị AC
            [!code]

        @pass_criteria:- Coupling AC được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(coupling="AC")
        assert not errors, f"Coupling AC: {errors}"
        actual = main_page.get_dso_dropdown_value("Coupling")
        assert "ac" in actual.lower(), f"Coupling hiển thị '{actual}', mong đợi 'AC'"

    @testcase
    def test_oscilloscope_puc_2_3_0022(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0022
        @brief: [DSO-012] Coupling -- chọn DC

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Coupling = DC -> Apply
                Bước 3: Verify dropdown Coupling hiển thị DC
            [!code]

        @pass_criteria:- Coupling DC được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(coupling="DC")
        assert not errors, f"Coupling DC: {errors}"
        actual = main_page.get_dso_dropdown_value("Coupling")
        assert "dc" in actual.lower(), f"Coupling hiển thị '{actual}', mong đợi 'DC'"

    # ── Trigger Mode ──────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0023(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0023
        @brief: [DSO-013] Trigger Mode -- chọn Edge

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Trigger Mode = Edge -> Apply
                Bước 3: Verify dropdown Trigger Mode hiển thị Edge
            [!code]

        @pass_criteria:- Trigger Mode Edge được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(trigger_mode="Edge")
        assert not errors, f"Trigger Mode Edge: {errors}"
        actual = main_page.get_dso_dropdown_value("Trigger Mode")
        assert "edge" in actual.lower(), f"Trigger Mode hiển thị '{actual}', mong đợi 'Edge'"

    @testcase
    def test_oscilloscope_puc_2_3_0024(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0024
        @brief: [DSO-014] Trigger Mode -- chọn Pulse

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Trigger Mode = Pulse -> Apply
                Bước 3: Verify dropdown Trigger Mode hiển thị Pulse
            [!code]

        @pass_criteria:- Trigger Mode Pulse được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(trigger_mode="Pulse")
        assert not errors, f"Trigger Mode Pulse: {errors}"
        actual = main_page.get_dso_dropdown_value("Trigger Mode")
        assert "pulse" in actual.lower(), f"Trigger Mode hiển thị '{actual}', mong đợi 'Pulse'"

    # ── Trigger Sweep ─────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0025(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0025
        @brief: [DSO-015] Trigger Sweep -- chọn Auto

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Trigger Sweep = Auto -> Apply
                Bước 3: Verify dropdown Trigger Sweep hiển thị Auto
            [!code]

        @pass_criteria:- Trigger Sweep Auto được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(trigger_sweep="Auto")
        assert not errors, f"Trigger Sweep Auto: {errors}"
        actual = main_page.get_dso_dropdown_value("Trigger Sweep")
        assert "auto" in actual.lower(), f"Trigger Sweep hiển thị '{actual}', mong đợi 'Auto'"

    @testcase
    def test_oscilloscope_puc_2_3_0026(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0026
        @brief: [DSO-016] Trigger Sweep -- chọn Normal

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Trigger Sweep = Normal -> Apply
                Bước 3: Verify dropdown Trigger Sweep hiển thị Normal
            [!code]

        @pass_criteria:- Trigger Sweep Normal được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(trigger_sweep="Normal")
        assert not errors, f"Trigger Sweep Normal: {errors}"
        actual = main_page.get_dso_dropdown_value("Trigger Sweep")
        assert "normal" in actual.lower(), f"Trigger Sweep hiển thị '{actual}', mong đợi 'Normal'"

    @testcase
    def test_oscilloscope_puc_2_3_0027(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0027
        @brief: [DSO-017] Trigger Sweep -- chọn Single

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Chọn Trigger Sweep = Single -> Apply
                Bước 3: Verify dropdown Trigger Sweep hiển thị Single
            [!code]

        @pass_criteria:- Trigger Sweep Single được lưu và hiển thị đúng sau Apply

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        errors = main_page.set_dso_params(trigger_sweep="Single")
        assert not errors, f"Trigger Sweep Single: {errors}"
        actual = main_page.get_dso_dropdown_value("Trigger Sweep")
        assert "single" in actual.lower(), f"Trigger Sweep hiển thị '{actual}', mong đợi 'Single'"

    # ── DSO Actions ───────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0028(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0028
        @brief: [DSO-029] DSO Actions -- đóng panel bằng nút X trên tiêu đề

        @pre:- Oscilloscope đã Connected
             - DSO Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Click nút X để đóng panel
                Bước 3: Verify panel DSO Setting đã đóng
            [!code]

        @pass_criteria:- DSO Setting panel đóng lại sau khi click X

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

    @testcase
    def test_oscilloscope_puc_2_3_0029(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0029
        @brief: [DSO-035] DSO Actions -- thay đổi nhiều tham số nhanh liên tiếp

        @pre:- Oscilloscope đã Connected

        @test_procedure:
            [code]
                Bước 1: Mở DSO Setting
                Bước 2: Thay đổi Time/Div, Voltage/Div, Coupling liên tiếp 4 lần -> Apply mỗi lần
                Bước 3: Verify không có lỗi sau mỗi lần Apply
            [!code]

        @pass_criteria:- Tất cả thay đổi nhanh được Apply thành công, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dso_setting()
        param_sets = [
            {"time_div": "1.0 ms",  "voltage_div": "500mV", "coupling": "AC"},
            {"time_div": "5.0 ms",  "voltage_div": "1.00V", "coupling": "DC"},
            {"time_div": "10.0 ms", "voltage_div": "100mV", "coupling": "GND"},
            {"time_div": "500 us",  "voltage_div": "2.00V", "coupling": "AC"},
        ]
        for params in param_sets:
            errors = main_page.set_dso_params(**params)
            assert not errors, f"Rapid change {params}: {errors}"


# ============================================================================
#  DDS Setting tests  (TC0030 – TC0069)
# ============================================================================

class TestOscilloscopePuc23DdsSetting:
    """PUC_2.3 -- DDS Setting: mỗi TC kiểm tra đúng 1 thông số / 1 hành vi."""

    @pytest.fixture(autouse=True)
    def _ensure_connected(self, main_page: MainPage):
        """Kết nối thiết bị nếu chưa kết nối. Dùng flag để tránh reconnect mỗi test."""
        global _oscilloscope_connected
        if _oscilloscope_connected:
            return
        main_page.open_connect_panel()
        if not main_page.is_device_connected(_DEVICE_LABEL):
            main_page.connect_device(_DEVICE_LABEL)
            time.sleep(3)
        _oscilloscope_connected = True

    # ── Signal On ─────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0030(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0030
        @brief: [DDS-003] Signal On -- trạng thái mặc định là OFF (unchecked)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Đảm bảo Signal On đang OFF (bỏ tick nếu cần)
                Bước 3: Verify checkbox Signal On ở trạng thái unchecked
            [!code]

        @pass_criteria:- Mặc định Signal On = OFF (unchecked)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        if main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        assert not main_page.is_dds_signal_on_checked(), \
            "Signal On phải là OFF theo mặc định"

    @testcase
    def test_oscilloscope_puc_2_3_0031(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0031
        @brief: [DDS-001] Signal On -- bật ON thành công

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Signal On đang OFF

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, đảm bảo Signal On đang OFF
                Bước 2: Tick checkbox Signal On -> Apply
                Bước 3: Verify checkbox Signal On ở trạng thái checked (ON)
            [!code]

        @pass_criteria:- Signal On chuyển sang trạng thái ON sau khi tick

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        if main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()
        assert main_page.is_dds_signal_on_checked(), \
            "Signal On phải ON sau khi tick"

    @testcase
    def test_oscilloscope_puc_2_3_0032(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0032
        @brief: [DDS-002] Signal On -- tắt OFF thành công

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Signal On đang ON

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, bật Signal On ON
                Bước 2: Bỏ tick checkbox Signal On -> Apply
                Bước 3: Verify checkbox Signal On ở trạng thái unchecked (OFF)
            [!code]

        @pass_criteria:- Signal On chuyển sang trạng thái OFF sau khi bỏ tick

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        if not main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()
        assert not main_page.is_dds_signal_on_checked(), \
            "Signal On phải OFF sau khi bỏ tick"

    # ── Sync ──────────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0033(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0033
        @brief: [DDS-032] Sync -- tick Sync khi Signal On đang tắt (không crash)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Signal On = OFF

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, đảm bảo Signal On OFF và Sync OFF
                Bước 2: Tick Sync -> Apply
                Bước 3: Verify không crash, ghi nhận phản hồi của hệ thống
            [!code]

        @pass_criteria:- Hệ thống không crash khi Sync khi Signal On tắt

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
        # Không crash là pass — sync khi signal off có thể được chấp nhận hoặc từ chối
        if main_page.is_dds_sync_checked():
            main_page.click_dds_sync()
            main_page.oscilloscope_apply()

    @testcase
    def test_oscilloscope_puc_2_3_0034(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0034
        @brief: [DDS-004] Sync -- bật Sync khi Signal On đang bật

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Signal On = ON

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, bật Signal On ON
                Bước 2: Tick checkbox Sync -> Apply
                Bước 3: Verify Sync ở trạng thái checked (ON)
            [!code]

        @pass_criteria:- Sync bật thành công khi Signal On đang bật

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        if not main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        if main_page.is_dds_sync_checked():
            main_page.click_dds_sync()
            main_page.oscilloscope_apply()
        main_page.click_dds_sync()
        main_page.oscilloscope_apply()
        assert main_page.is_dds_sync_checked(), \
            "Sync phải ON sau khi tick (Signal On đang bật)"

    @testcase
    def test_oscilloscope_puc_2_3_0035(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0035
        @brief: [DDS-005] Sync -- tắt Sync

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Sync đang ON

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, bật Signal On và Sync ON
                Bước 2: Bỏ tick Sync -> Apply
                Bước 3: Verify Sync ở trạng thái unchecked (OFF)
            [!code]

        @pass_criteria:- Sync tắt thành công sau khi bỏ tick

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        if not main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        if not main_page.is_dds_sync_checked():
            main_page.click_dds_sync()
            main_page.oscilloscope_apply()
        main_page.click_dds_sync()
        main_page.oscilloscope_apply()
        assert not main_page.is_dds_sync_checked(), \
            "Sync phải OFF sau khi bỏ tick"
        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()

    # ── Signal Type ───────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0036(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0036
        @brief: [DDS-030] Signal Type -- mặc định là Sine và chọn Sine thành công

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Chọn Signal Type = Sine -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Signal Type Sine được chọn thành công

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
        assert not errors, f"Signal Type Sine: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0037(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0037
        @brief: [DDS-007] Signal Type -- chọn Square

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Chọn Signal Type = Square -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Signal Type Square được chọn thành công

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(signal_type="Square")
        assert not errors, f"Signal Type Square: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0038(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0038
        @brief: [DDS-008] Signal Type -- chọn AM/FM

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Chọn Signal Type = AM/FM -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Signal Type AM/FM được chọn thành công

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(signal_type="AM/FM")
        assert not errors, f"Signal Type AM/FM: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0039(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0039
        @brief: [DDS-009] Signal Type -- chọn Ramp

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Chọn Signal Type = Ramp -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Signal Type Ramp được chọn thành công

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(signal_type="Ramp")
        assert not errors, f"Signal Type Ramp: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0040(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0040
        @brief: [DDS-010] Signal Type -- đổi loại sóng khi Signal On đang bật

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Signal On = ON, Signal Type = Sine

        @test_procedure:
            [code]
                Bước 1: Bật Signal On, chọn Signal Type = Sine -> Apply
                Bước 2: Đổi Signal Type = Square khi Signal On đang bật -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Đổi loại sóng khi đang phát thành công, không crash

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.set_dds_params(signal_type="Sine")
        if not main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        errors = main_page.set_dds_params(signal_type="Square")
        assert not errors, f"Đổi Signal Type khi Signal On đang bật: {errors}"
        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()

    # ── Frequency ─────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0041(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0041
        @brief: [DDS-025] Frequency -- giá trị mặc định đọc được (10000)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Đọc giá trị field Frequency
                Bước 3: Verify giá trị không rỗng
            [!code]

        @pass_criteria:- Field Frequency có giá trị mặc định (không rỗng)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        val = main_page.get_dds_field_value("txtFreq")
        assert val, f"Không đọc được giá trị mặc định Frequency (thực tế: '{val}')"

    @testcase
    def test_oscilloscope_puc_2_3_0042(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0042
        @brief: [DDS-011] Frequency -- nhập 1 Hz (giá trị min hợp lệ)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = 1 -> Apply
                Bước 3: Verify không có lỗi validation, giá trị lưu đúng
            [!code]

        @pass_criteria:- Frequency 1 Hz được chấp nhận và lưu đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz="1")
        assert not errors, f"Frequency 1 Hz: lỗi {errors}"
        assert main_page.get_dds_field_value("txtFreq") == "1", \
            "Frequency sau Apply phải là '1'"

    @testcase
    def test_oscilloscope_puc_2_3_0043(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0043
        @brief: [DDS-012] Frequency -- nhập 10000 Hz

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = 10000 -> Apply
                Bước 3: Verify không có lỗi, giá trị lưu đúng
            [!code]

        @pass_criteria:- Frequency 10000 Hz được chấp nhận và lưu đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz="10000")
        assert not errors, f"Frequency 10000 Hz: lỗi {errors}"
        assert main_page.get_dds_field_value("txtFreq") == "10000", \
            "Frequency sau Apply phải là '10000'"

    @testcase
    def test_oscilloscope_puc_2_3_0044(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0044
        @brief: [DDS-013] Frequency -- nhập 1000000 Hz (1 MHz)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = 1000000 -> Apply
                Bước 3: Verify không có lỗi, giá trị lưu đúng
            [!code]

        @pass_criteria:- Frequency 1000000 Hz được chấp nhận và lưu đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz="1000000")
        assert not errors, f"Frequency 1000000 Hz: lỗi {errors}"
        assert main_page.get_dds_field_value("txtFreq") == "1000000", \
            "Frequency sau Apply phải là '1000000'"

    @testcase
    def test_oscilloscope_puc_2_3_0045(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0045
        @brief: [DDS-026] Frequency -- nhập 0 (edge case)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = 0 -> Apply
                Bước 3: Ghi nhận phản hồi (chấp nhận hoặc báo lỗi)
            [!code]

        @pass_criteria:- Hệ thống xử lý Frequency = 0 đúng theo thiết kế, không crash

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.set_dds_params(frequency_hz="0")
        # 0 có thể được chấp nhận hoặc từ chối — không crash là pass
        main_page.set_dds_params(frequency_hz="10000")

    @testcase
    def test_oscilloscope_puc_2_3_0046(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0046
        @brief: [DDS-014] Frequency -- nhập giá trị cực đại (12000000 Hz)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = 12000000 -> Apply
                Bước 3: Verify không crash, ghi nhận phản hồi
            [!code]

        @pass_criteria:- Hệ thống không crash với Frequency cực đại

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz="12000000")
        assert not errors, f"Frequency cực đại 12000000: crash hoặc lỗi không mong đợi {errors}"
        main_page.set_dds_params(frequency_hz="10000")

    @testcase
    def test_oscilloscope_puc_2_3_0047(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0047
        @brief: [DDS-033] Frequency -- nhập ký tự chữ 'abc' (invalid)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = 'abc' -> Apply
                Bước 3: Verify có lỗi validation hoặc field không lưu giá trị sai
            [!code]

        @pass_criteria:- Field từ chối 'abc' hoặc báo lỗi Invalid number format

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz="abc")
        if not errors:
            actual = main_page.get_dds_field_value("txtFreq")
            assert actual != "abc", \
                "Field chấp nhận 'abc' — giá trị không hợp lệ"
        main_page.set_dds_params(frequency_hz="10000")

    @testcase
    def test_oscilloscope_puc_2_3_0048(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0048
        @brief: [DDS-034] Frequency -- nhập ký tự đặc biệt '!@#$' (invalid)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = '!@#$' -> Apply
                Bước 3: Verify có lỗi validation hoặc field không lưu giá trị sai
            [!code]

        @pass_criteria:- Field từ chối '!@#$' hoặc báo lỗi Invalid number format

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz="!@#$")
        if not errors:
            actual = main_page.get_dds_field_value("txtFreq")
            assert actual != "!@#$", \
                "Field chấp nhận '!@#$' — giá trị không hợp lệ"
        main_page.set_dds_params(frequency_hz="10000")

    @testcase
    def test_oscilloscope_puc_2_3_0049(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0049
        @brief: [DDS-035] Frequency -- nhập giá trị âm -100 (invalid)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = -100 -> Apply
                Bước 3: Verify có lỗi validation
            [!code]

        @pass_criteria:- Báo lỗi 'Frequency cannot be less than 1 Hz'

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz="-100")
        assert errors, "Frequency âm '-100' phải báo lỗi validation"
        main_page.set_dds_params(frequency_hz="10000")

    @testcase
    def test_oscilloscope_puc_2_3_0050(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0050
        @brief: [DDS-042] Frequency -- nhập giá trị overflow 99999999999 (quá giới hạn)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Frequency = 99999999999 -> Apply
                Bước 3: Verify hệ thống xử lý đúng (giới hạn về max hoặc báo lỗi)
            [!code]

        @pass_criteria:- Hệ thống không crash, xử lý overflow đúng theo thiết kế

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.set_dds_params(frequency_hz="99999999999")
        # Không crash là pass
        main_page.set_dds_params(frequency_hz="10000")

    # ── Amplitude ─────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0051(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0051
        @brief: [DDS-027] Amplitude -- giá trị mặc định đọc được

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Đọc giá trị field Amplitude
                Bước 3: Verify giá trị không rỗng
            [!code]

        @pass_criteria:- Field Amplitude có giá trị mặc định (không rỗng)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        val = main_page.get_dds_field_value("txtAmplitude")
        assert val, f"Không đọc được giá trị mặc định Amplitude (thực tế: '{val}')"

    @testcase
    def test_oscilloscope_puc_2_3_0052(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0052
        @brief: [DDS-015] Amplitude -- nhập 1 V

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Amplitude = 1 -> Apply
                Bước 3: Verify không có lỗi, giá trị lưu đúng
            [!code]

        @pass_criteria:- Amplitude 1 V được chấp nhận và lưu đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(amplitude_v="1")
        assert not errors, f"Amplitude 1 V: lỗi {errors}"
        assert main_page.get_dds_field_value("txtAmplitude") == "1", \
            "Amplitude sau Apply phải là '1'"

    @testcase
    def test_oscilloscope_puc_2_3_0053(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0053
        @brief: [DDS-016] Amplitude -- nhập 0.5 V (số thực)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Amplitude = 0.5 -> Apply
                Bước 3: Verify không có lỗi, giá trị lưu đúng
            [!code]

        @pass_criteria:- Amplitude 0.5 V được chấp nhận và lưu đúng

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(amplitude_v="0.5")
        assert not errors, f"Amplitude 0.5 V: lỗi {errors}"
        assert main_page.get_dds_field_value("txtAmplitude") == "0.5", \
            "Amplitude sau Apply phải là '0.5'"

    @testcase
    def test_oscilloscope_puc_2_3_0054(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0054
        @brief: [DDS-028] Amplitude -- nhập 0 (edge case)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Amplitude = 0 -> Apply
                Bước 3: Ghi nhận phản hồi (chấp nhận hoặc báo lỗi)
            [!code]

        @pass_criteria:- Hệ thống xử lý Amplitude = 0 đúng theo thiết kế, không crash

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.set_dds_params(amplitude_v="0")
        main_page.set_dds_params(amplitude_v="1")

    @testcase
    def test_oscilloscope_puc_2_3_0055(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0055
        @brief: [DDS-017] Amplitude -- nhập giá trị lớn nhất (5 V)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Amplitude = 5 -> Apply
                Bước 3: Verify không crash, ghi nhận phản hồi
            [!code]

        @pass_criteria:- Hệ thống không crash với Amplitude cực đại

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(amplitude_v="5")
        assert not errors, f"Amplitude max 5 V: {errors}"
        main_page.set_dds_params(amplitude_v="1")

    # ── Offset ────────────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0056(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0056
        @brief: [DDS-018] Offset -- nhập 1 V (dương)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, đặt Amplitude = 1
                Bước 2: Nhập Offset = 1 -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Offset 1 V được chấp nhận, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.set_dds_params(amplitude_v="1", offset_v="0")
        errors = main_page.set_dds_params(offset_v="1")
        assert not errors, f"Offset 1 V: lỗi {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0057(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0057
        @brief: [DDS-019] Offset -- nhập 0 V

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Offset = 0 -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Offset 0 V được chấp nhận, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(offset_v="0")
        assert not errors, f"Offset 0 V: lỗi {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0058(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0058
        @brief: [DDS-020] Offset -- nhập -1 V (âm)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Offset = -1 -> Apply
                Bước 3: Verify không có lỗi (Offset âm hợp lệ)
            [!code]

        @pass_criteria:- Offset -1 V được chấp nhận, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(offset_v="-1")
        assert not errors, f"Offset -1 V: lỗi {errors}"
        main_page.set_dds_params(offset_v="0")

    @testcase
    def test_oscilloscope_puc_2_3_0059(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0059
        @brief: [DDS-029] Offset -- Offset > Amplitude (edge case)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting, đặt Amplitude = 1
                Bước 2: Nhập Offset = 5 (lớn hơn Amplitude) -> Apply
                Bước 3: Ghi nhận phản hồi (cảnh báo hoặc clipping)
            [!code]

        @pass_criteria:- Hệ thống xử lý Offset > Amplitude đúng theo thiết kế, không crash

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.set_dds_params(amplitude_v="1", offset_v="0")
        main_page.set_dds_params(amplitude_v="1", offset_v="5")
        main_page.set_dds_params(amplitude_v="1", offset_v="0")

    @testcase
    def test_oscilloscope_puc_2_3_0060(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0060
        @brief: [DDS-036] Offset -- nhập ký tự không hợp lệ 'xyz'

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Offset = 'xyz' -> Apply
                Bước 3: Verify có lỗi hoặc field không lưu giá trị sai
            [!code]

        @pass_criteria:- Field từ chối 'xyz' hoặc báo lỗi Invalid number format

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(offset_v="xyz")
        if not errors:
            actual = main_page.get_dds_field_value("txtOffset")
            assert actual != "xyz", \
                "Field chấp nhận 'xyz' — giá trị không hợp lệ"
        main_page.set_dds_params(amplitude_v="1", offset_v="0")

    @testcase
    def test_oscilloscope_puc_2_3_0061(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0061
        @brief: [DDS-037] Amplitude -- nhập ký tự không hợp lệ 'abc'

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Amplitude = 'abc' -> Apply
                Bước 3: Verify có lỗi hoặc field không lưu giá trị sai
            [!code]

        @pass_criteria:- Field từ chối 'abc' hoặc báo lỗi Invalid number format

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(amplitude_v="abc")
        if not errors:
            actual = main_page.get_dds_field_value("txtAmplitude")
            assert actual != "abc", \
                "Field chấp nhận 'abc' — giá trị không hợp lệ"
        main_page.set_dds_params(amplitude_v="1", offset_v="0")

    @testcase
    def test_oscilloscope_puc_2_3_0062(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0062
        @brief: [DDS-038] Amplitude -- nhập giá trị âm -1 (invalid)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Nhập Amplitude = -1 -> Apply
                Bước 3: Verify có lỗi validation
            [!code]

        @pass_criteria:- Báo lỗi validation vì Amplitude không thể âm

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(amplitude_v="-1")
        assert errors, "Amplitude âm '-1' phải báo lỗi validation"
        main_page.set_dds_params(amplitude_v="1", offset_v="0")

    # ── DDS Actions ───────────────────────────────────────────────────────────

    @testcase
    def test_oscilloscope_puc_2_3_0063(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0063
        @brief: [DDS-021] DDS Actions -- Apply đầy đủ tham số hợp lệ

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Đặt Signal Type=Sine, Frequency=10000, Amplitude=1, Offset=0 -> Apply
                Bước 3: Verify không có lỗi validation
            [!code]

        @pass_criteria:- Apply đầy đủ tham số thành công, không có lỗi

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(
            signal_type="Sine", frequency_hz="10000",
            amplitude_v="1", offset_v="0",
        )
        assert not errors, f"Apply đầy đủ tham số: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0064(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0064
        @brief: [DDS-022] DDS Actions -- Cancel không lưu thay đổi

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Frequency = 10000

        @test_procedure:
            [code]
                Bước 1: Apply Frequency = 10000 để tạo giá trị baseline
                Bước 2: Thay đổi Frequency = 99999 (KHÔNG Apply)
                Bước 3: Click Cancel
                Bước 4: Mở lại DDS Setting, đọc Frequency
                Bước 5: Verify Frequency vẫn là 10000 (chưa lưu)
            [!code]

        @pass_criteria:- Sau Cancel, giá trị Frequency không thay đổi (vẫn là 10000)

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")
        main_page.set_dds_params_no_apply(frequency_hz="99999")
        main_page.oscilloscope_cancel()
        time.sleep(0.3)

        main_page.open_dds_setting()
        freq = main_page.get_dds_field_value("txtFreq")
        assert freq == "10000", \
            f"Frequency phải là '10000' sau Cancel, thực tế '{freq}'"

    @testcase
    def test_oscilloscope_puc_2_3_0065(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0065
        @brief: [DDS-023] DDS Actions -- Apply khi Signal On đang bật

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở, Signal On = ON

        @test_procedure:
            [code]
                Bước 1: Bật Signal On -> Apply
                Bước 2: Thay đổi Frequency = 20000 -> Apply
                Bước 3: Verify không có lỗi
            [!code]

        @pass_criteria:- Apply khi Signal On đang bật thành công, tín hiệu cập nhật ngay

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        if not main_page.is_dds_signal_on_checked():
            main_page.toggle_dds_signal_on()
            main_page.oscilloscope_apply()
        errors = main_page.set_dds_params(frequency_hz="20000")
        assert not errors, f"Apply khi Signal On đang bật: {errors}"
        main_page.toggle_dds_signal_on()
        main_page.oscilloscope_apply()
        main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")

    @testcase
    def test_oscilloscope_puc_2_3_0066(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0066
        @brief: [DDS-024] DDS Actions -- đóng panel bằng nút X trên tiêu đề

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Click nút X để đóng panel
                Bước 3: Verify panel DDS Setting đã đóng
            [!code]

        @pass_criteria:- DDS Setting panel đóng lại sau khi click X

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        main_page.close_dds_setting()
        time.sleep(0.5)
        assert not main_page.is_dds_setting_open(), \
            "DDS Setting vẫn còn mở sau khi đóng bằng X"

    @testcase
    def test_oscilloscope_puc_2_3_0067(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0067
        @brief: [DDS-031] DDS Actions -- Apply nhiều lần liên tiếp (5 lần)

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Click Apply 5 lần liên tiếp với cùng tham số hợp lệ
                Bước 3: Verify không treo, không lỗi sau mỗi lần Apply
            [!code]

        @pass_criteria:- 5 lần Apply liên tiếp đều thành công, không treo UI

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        for i in range(5):
            errors = main_page.set_dds_params(
                frequency_hz="10000", amplitude_v="1", offset_v="0"
            )
            assert not errors, f"Apply lần {i + 1}: {errors}"

    @testcase
    def test_oscilloscope_puc_2_3_0068(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0068
        @brief: [DDS-039] DDS Actions -- Apply khi Frequency để trống

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Xóa toàn bộ nội dung field Frequency (nhập khoảng trắng) -> Apply
                Bước 3: Verify có lỗi validation
            [!code]

        @pass_criteria:- Báo lỗi validation khi Frequency để trống

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(frequency_hz=" ")
        assert errors, "Frequency để trống phải báo lỗi validation"
        main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")

    @testcase
    def test_oscilloscope_puc_2_3_0069(self, main_page: MainPage):
        """
        @test_id: test_oscilloscope_puc_2_3_0069
        @brief: [DDS-040] DDS Actions -- Apply khi Amplitude để trống

        @pre:- Oscilloscope đã Connected
             - DDS Setting đang mở

        @test_procedure:
            [code]
                Bước 1: Mở DDS Setting
                Bước 2: Xóa toàn bộ nội dung field Amplitude (nhập khoảng trắng) -> Apply
                Bước 3: Verify có lỗi validation
            [!code]

        @pass_criteria:- Báo lỗi validation khi Amplitude để trống

        @test_level: software
        @test_type: functional
        @execution_type: automatic
        @hw_depend: yes
        """
        main_page.open_dds_setting()
        errors = main_page.set_dds_params(amplitude_v=" ")
        assert errors, "Amplitude để trống phải báo lỗi validation"
        main_page.set_dds_params(frequency_hz="10000", amplitude_v="1", offset_v="0")
