"""
Root conftest.py
────────────────
- Session-scoped fixtures: app controller, serial device, relay
- Pytest hooks: collect metadata → Excel report on session finish
- Screenshot on test failure
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, List

import pytest

from config import get_settings
from core.app_controller import AppController
from core.relay_controller import RelayController
from core.serial_device import SerialDevice
from core.testcase_decorator import TestCaseMetadata
from pages.main_page import MainPage
from utils.logger import get_logger
from utils.report_excel import ExcelReporter, TestResult

logger = get_logger("conftest")

# Ensure report directories exist at startup
for d in ("reports/html", "reports/excel", "reports/logs", "reports/screenshots"):
    Path(d).mkdir(parents=True, exist_ok=True)


# ════════════════════════════════════════════════════════════════════════════
#  Session-scoped fixtures
# ════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def app_ctrl() -> AppController:
    """
    Connects to the target Windows application.
    The app must already be running before the test session starts.
    To auto-launch, change .connect() → .launch() below.
    """
    ctrl = AppController()
    ctrl.connect()          # change to ctrl.launch() if needed
    yield ctrl
    ctrl.disconnect()


@pytest.fixture(scope="session")
def main_page(app_ctrl: AppController) -> MainPage:
    """Page Object for the main window — shared across the session."""
    return MainPage(app_ctrl)


@pytest.fixture(scope="session")
def device() -> SerialDevice:
    """Opens the serial connection to the DUT (USB COM port)."""
    dev = SerialDevice()
    dev.open()
    yield dev
    dev.close()


@pytest.fixture(scope="session")
def relay() -> RelayController:
    """Relay board controller (disabled by default until hardware present)."""
    ctrl = RelayController()
    ctrl.connect()
    yield ctrl
    ctrl.disconnect()


# ════════════════════════════════════════════════════════════════════════════
#  Per-test fixtures
# ════════════════════════════════════════════════════════════════════════════

@pytest.fixture(autouse=True)
def _log_test_boundaries(request):
    """Log test start/end with the test ID from docstring metadata."""
    meta: TestCaseMetadata = getattr(request.function, "_tc_meta", None)
    tc_id = meta.test_id if meta else request.node.nodeid
    brief = meta.brief    if meta else ""

    logger.info("=" * 70)
    logger.info(f"START  [{tc_id}]  {brief}")
    logger.info("=" * 70)

    start = time.time()
    yield
    elapsed = time.time() - start

    logger.info(f"END    [{tc_id}]  duration={elapsed:.2f}s")
    logger.info("")


# ════════════════════════════════════════════════════════════════════════════
#  Reporting hooks
# ════════════════════════════════════════════════════════════════════════════

_session_results: List[TestResult] = []


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """
    Collect result per test (called 3 times: setup / call / teardown).
    We only capture the 'call' phase for the main pass/fail verdict.
    """
    if report.when != "call":
        return

    # Walk up to find the test function
    # report.nodeid example: "tests/attenuator/test_tc_0001.py::test_attenuator_tc_0001"
    item = getattr(report, "_pytest_item", None)  # set below if available
    meta: TestCaseMetadata = getattr(getattr(item, "function", None), "_tc_meta", None) \
                              if item else None

    error_msg = ""
    if report.failed:
        error_msg = str(report.longrepr) if report.longrepr else ""
        # Trim to first 500 chars for Excel
        error_msg = error_msg[:500]

    result = TestResult(
        test_id        = meta.test_id        if meta else report.nodeid,
        brief          = meta.brief          if meta else "",
        test_level     = meta.test_level     if meta else "",
        test_type      = meta.test_type      if meta else "",
        execution_type = meta.execution_type if meta else "",
        hw_depend      = meta.hw_depend      if meta else False,
        outcome        = report.outcome,
        duration       = f"{report.duration:.2f}",
        error_message  = error_msg,
        nodeid         = report.nodeid,
    )
    _session_results.append(result)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach item reference to report so logreport can access metadata."""
    outcome = yield
    report = outcome.get_result()
    report._pytest_item = item


def pytest_runtest_logreport(report):  # noqa: F811  (intentional re-def for item attach)
    if report.when != "call":
        return

    item = getattr(report, "_pytest_item", None)
    meta: TestCaseMetadata = getattr(
        getattr(item, "function", None), "_tc_meta", None
    ) if item else None

    # Screenshot on failure
    if report.failed and item:
        cfg = get_settings()
        if cfg.report.screenshot_on_fail:
            ctrl: AppController = item.funcargs.get("app_ctrl")
            if ctrl:
                ts = time.strftime("%Y%m%d_%H%M%S")
                safe_id = (meta.test_id if meta else "unknown").replace("/", "_")
                ctrl.take_screenshot(f"FAIL_{safe_id}_{ts}.png")

    error_msg = ""
    if report.failed and report.longrepr:
        error_msg = str(report.longrepr)[:500]

    _session_results.append(TestResult(
        test_id        = meta.test_id        if meta else report.nodeid,
        brief          = meta.brief          if meta else "",
        test_level     = meta.test_level     if meta else "",
        test_type      = meta.test_type      if meta else "",
        execution_type = meta.execution_type if meta else "",
        hw_depend      = meta.hw_depend      if meta else False,
        outcome        = report.outcome,
        duration       = f"{report.duration:.2f}",
        error_message  = error_msg,
        nodeid         = report.nodeid,
    ))


def pytest_sessionfinish(session, exitstatus):
    """Generate Excel report at end of session."""
    if not _session_results:
        return
    reporter = ExcelReporter()
    reporter.generate(_session_results)
    logger.info(f"Session finished — {len(_session_results)} test(s) collected")
