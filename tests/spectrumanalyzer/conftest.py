"""
Fixtures cho Spectrum Analyzer tests — Spike.exe (Signal Hound).
spike_ctrl: AppController kết nối tới Spike.exe.
spike_page: SpikePage Page Object dùng chung cả session.
Cấu hình exe_path trong config/settings.yaml (mục spike).
Override bằng env var: SPIKE_EXE_PATH=...
"""
from __future__ import annotations

import time
from typing import Iterator

import pytest

from config import get_settings
from core.app_controller import AppController
from pages.spike_page import SpikePage


@pytest.fixture(scope="session")
def spike_ctrl() -> Iterator[AppController]:
    """Session-scoped fixture: connect hoặc launch Spike.exe."""
    cfg = get_settings().spike
    ctrl = AppController(app_name=cfg.name, backend=cfg.backend, exe_path=cfg.exe_path)
    try:
        ctrl.connect()
    except Exception:
        ctrl.launch()
        time.sleep(cfg.startup_wait)
    yield ctrl
    ctrl.disconnect()


@pytest.fixture(scope="session")
def spike_page(spike_ctrl: AppController) -> SpikePage:
    """Session-scoped fixture: SpikePage với popup đã được dismiss."""
    page = SpikePage(spike_ctrl)
    page.handle_popup("No Device")
    return page
