"""
tests/spectrumanalyzer/conftest.py
────────────────────────────────────
Fixtures dành riêng cho Spectrum Analyzer tests.

Spike.exe phải khởi động trước PC17 (Elite).
Override main_page để đảm bảo thứ tự: Spike → PC17.
"""
from __future__ import annotations

import time
from typing import Iterator

import pytest

from config import get_settings
from core.app_controller import AppController
from pages.spike_page import SpikePage
from utils.logger import get_logger

logger = get_logger("spectrum.conftest")


@pytest.fixture(scope="session")
def spike_ctrl() -> Iterator[AppController]:
    """Kết nối / launch Spike.exe — chỉ dùng trong tests/spectrumanalyzer/."""
    cfg = get_settings().spike
    ctrl = AppController(app_name=cfg.name, backend=cfg.backend, exe_path=cfg.exe_path)
    try:
        ctrl.connect()
        logger.info("Spike already running — connected")
    except Exception:
        logger.info("Spike not running — launching...")
        ctrl.launch()

    time.sleep(cfg.startup_wait)
    yield ctrl
    ctrl.disconnect()


@pytest.fixture(scope="session")
def spike_page(spike_ctrl: AppController) -> SpikePage:
    """Page Object cho Spike — dùng trong mọi Spectrum test."""
    page = SpikePage(spike_ctrl)
    page.dismiss_demo()           # nhấn Enter skip màn hình demo khi khởi động
    page.handle_popup("No Device")  # dismiss 'No Device' popup tiếp theo
    return page


@pytest.fixture(scope="session")
def main_page(spike_ctrl: AppController, app_ctrl: AppController):
    """Override root main_page: Spike phải lên trước PC17 (Elite)."""
    from pages.main_page import MainPage
    page = MainPage(app_ctrl)
    page.setup_connection()
    return page
