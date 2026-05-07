"""
tests/vna/conftest.py
─────────────────────
Fixtures dành riêng cho bộ test VNA.

S2VNA chỉ được khởi động khi chạy các test trong thư mục này,
KHÔNG ảnh hưởng đến các bộ test khác (attenuator, demo, v.v.).

Thứ tự khởi động: S2VNA trước → sau đó test mới chạy.
"""
from __future__ import annotations

import time
from typing import Iterator

import pytest

from config import get_settings
from core.app_controller import AppController
from pages.s2vna_page import S2VnaPage
from utils.logger import get_logger

logger = get_logger("vna.conftest")


@pytest.fixture(scope="session")
def s2vna_ctrl() -> Iterator[AppController]:
    """
    Khởi động / kết nối S2VNA — chỉ dùng trong tests/vna/.
    Nếu S2VNA đã mở sẵn thì connect vào; nếu chưa thì tự launch.
    """
    cfg = get_settings().s2vna
    ctrl = AppController(app_name=cfg.name, backend=cfg.backend)
    ctrl.exe_path = cfg.exe_path
    ctrl.timeout  = cfg.connect_timeout

    try:
        ctrl.connect()
        logger.info("S2VNA already running — connected")
    except Exception:
        logger.info("S2VNA not running — launching...")
        ctrl.launch()

    time.sleep(cfg.startup_wait)
    yield ctrl

    # Không tắt S2VNA sau session để tránh mất trạng thái
    ctrl.disconnect()


@pytest.fixture(scope="session")
def s2vna_page(s2vna_ctrl: AppController) -> S2VnaPage:
    """Page Object cho S2VNA — dùng trong mọi test VNA."""
    return S2VnaPage(s2vna_ctrl)


