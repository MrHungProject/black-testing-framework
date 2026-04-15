"""
S2VnaPage — Page Object cho ứng dụng S2VNA simulator.

Chỉ được dùng trong bộ test VNA (tests/vna/).
Fixture s2vna_ctrl và s2vna_page được khai báo trong tests/vna/conftest.py.

HOW TO FIND ELEMENT IDENTIFIERS
---------------------------------
    from pywinauto import Application
    app = Application(backend="uia").connect(title_re=".*S2VNA.*")
    app.top_window().print_control_identifiers(depth=5)
"""
from __future__ import annotations

from pages.base_page import BasePage


class S2VnaPage(BasePage):
    """Page Object cho cửa sổ chính của S2VNA."""

    # ── Element locators ──────────────────────────────────────────────────────
    # Thay bằng auto_id / title / class_name thực tế từ app S2VNA

    # Trạng thái kết nối / instrument
    LBL_STATUS          = {"auto_id": "lblStatus"}
    LBL_CONN_STATUS     = {"auto_id": "lblConnectionStatus"}
    BTN_CONNECT         = {"auto_id": "btnConnect"}
    BTN_DISCONNECT      = {"auto_id": "btnDisconnect"}

    # Điều khiển nguồn / sweep
    BTN_POWER_ON        = {"auto_id": "btnPowerOn",  "control_type": "Button"}
    BTN_POWER_OFF       = {"auto_id": "btnPowerOff", "control_type": "Button"}
    LBL_POWER_STATUS    = {"auto_id": "lblPowerStatus"}

    # Sweep / measurement
    BTN_SWEEP           = {"auto_id": "btnSweep"}
    LBL_FREQ_START      = {"auto_id": "lblFreqStart"}
    LBL_FREQ_STOP       = {"auto_id": "lblFreqStop"}
    TXT_FREQ_START      = {"auto_id": "txtFreqStart"}
    TXT_FREQ_STOP       = {"auto_id": "txtFreqStop"}
    BTN_APPLY           = {"auto_id": "btnApply"}

    # ── Connection actions ────────────────────────────────────────────────────

    def click_connect(self) -> None:
        """
        @brief  Click button Connect để kết nối S2VNA
        @retval None
        """
        self.click(self.BTN_CONNECT)

    def click_disconnect(self) -> None:
        """
        @brief  Click button Disconnect để ngắt kết nối S2VNA
        @retval None
        """
        self.click(self.BTN_DISCONNECT)

    def get_connection_status(self) -> str:
        """
        @brief  Lấy text hiển thị trạng thái kết nối từ label LBL_CONN_STATUS
        @retval str — text trạng thái kết nối (ví dụ: "Connected", "Disconnected")
        """
        return self.get_text(self.LBL_CONN_STATUS)

    def is_connected(self) -> bool:
        """
        @brief  Kiểm tra S2VNA có đang kết nối không
        @retval bool — True nếu connection status chứa "connected", False nếu không
        """
        return "connected" in self.get_connection_status().lower()

    # ── Power actions ─────────────────────────────────────────────────────────

    def power_on(self) -> None:
        """
        @brief  Click button Power On để bật nguồn S2VNA
        @retval None
        """
        self.click(self.BTN_POWER_ON)

    def power_off(self) -> None:
        """
        @brief  Click button Power Off để tắt nguồn S2VNA
        @retval None
        """
        self.click(self.BTN_POWER_OFF)

    def get_power_status(self) -> str:
        """
        @brief  Lấy text trạng thái nguồn từ label LBL_POWER_STATUS
        @retval str — text trạng thái nguồn (ví dụ: "ON", "OFF", "Ready")
        """
        return self.get_text(self.LBL_POWER_STATUS)

    def is_powered_on(self) -> bool:
        """
        @brief  Kiểm tra S2VNA có đang bật nguồn không
        @retval bool — True nếu power status chứa "on" hoặc "ready", False nếu không
        """
        status = self.get_power_status().lower()
        return "on" in status or "ready" in status

    # ── Sweep / measurement actions ───────────────────────────────────────────

    def set_freq_start(self, freq: str) -> None:
        """
        @brief  Đặt giá trị tần số bắt đầu vào input TXT_FREQ_START
        @param  freq: Tần số bắt đầu (ví dụ: "1000000" Hz hoặc "1e6")
        @retval None
        """
        self.set_value(self.TXT_FREQ_START, freq)

    def set_freq_stop(self, freq: str) -> None:
        """
        @brief  Đặt giá trị tần số kết thúc vào input TXT_FREQ_STOP
        @param  freq: Tần số kết thúc (ví dụ: "3000000000" Hz hoặc "3e9")
        @retval None
        """
        self.set_value(self.TXT_FREQ_STOP, freq)

    def click_sweep(self) -> None:
        """
        @brief  Click button Sweep để bắt đầu quá trình sweep đo lường
        @retval None
        """
        self.click(self.BTN_SWEEP)

    def click_apply(self) -> None:
        """
        @brief  Click button Apply để áp dụng cài đặt
        @retval None
        """
        self.click(self.BTN_APPLY)

    # ── General ───────────────────────────────────────────────────────────────

    def get_status(self) -> str:
        """
        @brief  Lấy text trạng thái chung từ label LBL_STATUS
        @retval str — text trạng thái hiện tại của S2VNA
        """
        return self.get_text(self.LBL_STATUS)

    def is_ready(self) -> bool:
        """
        @brief  Kiểm tra S2VNA có ở trạng thái sẵn sàng không
        @retval bool — True nếu status chứa "ready", False nếu không
        """
        return "ready" in self.get_status().lower()
