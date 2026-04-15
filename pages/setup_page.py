"""
SetupPage — Lớp setup chung, tái sử dụng cho mọi test case.

Flow chuẩn:
    1. S2VNA đang chạy (simulator)
    2. PC17 mở → "Run Flow"
    3. Tools → RF Test Set → FormMainEliteRF
    4. System Connect → kết nối VNA (+ATT tùy test)

Dùng trong conftest fixture:
    @pytest.fixture(scope="session")
    def system_setup(main_page):
        setup = SetupPage(main_page)
        setup.full_setup()
        yield setup
"""
from __future__ import annotations

import time

from pages.main_page import MainPage
from utils.logger import get_logger

logger = get_logger(__name__)


class SetupPage:
    """
    Encapsulates all common setup steps — reusable across test suites.

    Dùng scope="session" để chỉ setup 1 lần cho cả session,
    hoặc scope="class"/"function" nếu cần reset giữa các test.
    """

    def __init__(self, main_page: MainPage):
        self._page = main_page
        self._vna_connected  = False
        self._att_connected  = False

    # ── Setup steps ───────────────────────────────────────────────────────────

    def open_rf_test_set(self) -> "SetupPage":
        """Bước 1: Từ Run Flow → mở FormMainEliteRF."""
        logger.info("[SETUP] Navigating: Tools → RF Test Set")
        self._page.open_rf_test_set()
        return self

    def connect_vna(self) -> "SetupPage":
        """Bước 2a: Kết nối VNA qua System Connect."""
        logger.info("[SETUP] Connecting VNA...")
        self._page.connect_vna()
        self._vna_connected = True
        logger.info("[SETUP] VNA connected")
        return self

    def connect_att(self) -> "SetupPage":
        """Bước 2b: Kết nối ATT qua System Connect."""
        logger.info("[SETUP] Connecting ATT...")
        self._page.connect_att()
        self._att_connected = True
        logger.info("[SETUP] ATT connected")
        return self

    def close_connect_panel(self) -> "SetupPage":
        """Đóng panel System Connect sau khi connect xong."""
        self._page.close_system_connect()
        return self

    # ── Preset setups — gọi 1 dòng trong fixture ────────────────────────────

    def full_setup(self) -> "SetupPage":
        """
        Connect VNA + ATT.
        Không cần navigate — app_ctrl fixture đã mở FormMainEliteRF sẵn.
        """
        self._page.open_system_connect()
        self._page.click(self._page.BTN_CONNECTION_VNA)
        time.sleep(1.0)
        self._page.click(self._page.BTN_CONNECTION_ATT)
        time.sleep(2.0)
        self.close_connect_panel()
        self._vna_connected = True
        self._att_connected = True
        logger.info("[SETUP] Full setup complete (VNA + ATT connected)")
        return self

    def vna_only_setup(self) -> "SetupPage":
        """Connect VNA. app_ctrl fixture đã mở FormMainEliteRF sẵn."""
        self.connect_vna()
        self.close_connect_panel()
        logger.info("[SETUP] VNA-only setup complete")
        return self

    def att_only_setup(self) -> "SetupPage":
        """Connect ATT. app_ctrl fixture đã mở FormMainEliteRF sẵn."""
        self.connect_att()
        self.close_connect_panel()
        logger.info("[SETUP] ATT-only setup complete")
        return self

    # ── State ─────────────────────────────────────────────────────────────────

    @property
    def vna_connected(self) -> bool:
        return self._vna_connected

    @property
    def att_connected(self) -> bool:
        return self._att_connected

    def verify_vna_ready(self) -> bool:
        """Kiểm tra VNA đã sẵn sàng (dùng trong assert của test)."""
        return self._page.is_vna_on()

    def get_vna_status(self) -> str:
        return self._page.get_vna_status()
