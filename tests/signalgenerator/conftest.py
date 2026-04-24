"""
tests/signalgenerator/conftest.py
──────────────────────────────────
Fixtures dùng riêng cho Signal Generator test suite.
"""
from __future__ import annotations

import pytest

from pages.main_page import MainPage
from utils.logger import get_logger

logger = get_logger(__name__)
