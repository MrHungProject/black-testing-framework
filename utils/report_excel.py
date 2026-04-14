"""
ExcelReporter — generates an Excel test report from pytest results.

Called by conftest.py hook: pytest_sessionfinish
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from utils.logger import get_logger

logger = get_logger(__name__)

try:
    from openpyxl import Workbook
    from openpyxl.styles import (
        Alignment, Border, Font, PatternFill, Side
    )
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    logger.warning("openpyxl not installed — Excel report disabled")


# ── Colour palette ────────────────────────────────────────────────────────────

_GREEN  = "FF92D050"
_RED    = "FFFF0000"
_YELLOW = "FFFFC000"
_BLUE   = "FF4472C4"
_GREY   = "FFD9D9D9"
_WHITE  = "FFFFFFFF"


def _fill(hex_color: str) -> "PatternFill":
    return PatternFill("solid", fgColor=hex_color)


def _bold(size: int = 11) -> "Font":
    return Font(bold=True, size=size)


def _center() -> "Alignment":
    return Alignment(horizontal="center", vertical="center", wrap_text=True)


def _thin_border() -> "Border":
    side = Side(style="thin")
    return Border(left=side, right=side, top=side, bottom=side)


# ── Data container ────────────────────────────────────────────────────────────

class TestResult:
    __slots__ = (
        "test_id", "brief", "test_level", "test_type",
        "execution_type", "hw_depend", "outcome",
        "duration", "error_message", "nodeid",
    )

    def __init__(self, **kwargs):
        for slot in self.__slots__:
            setattr(self, slot, kwargs.get(slot, ""))


# ── Reporter ──────────────────────────────────────────────────────────────────

class ExcelReporter:
    """Builds an Excel workbook from a list of TestResult objects."""

    COLUMNS = [
        ("Test ID",        20),
        ("Brief",          40),
        ("Level",          12),
        ("Type",           14),
        ("Execution",      16),
        ("HW Depend",      11),
        ("Result",         10),
        ("Duration (s)",   13),
        ("Error / Notes",  50),
    ]

    def __init__(self, output_path: Optional[str] = None):
        from config import get_settings
        cfg = get_settings().report
        self.output_path = Path(output_path or cfg.excel_dir) / cfg.excel_filename

    def generate(self, results: List[TestResult]) -> Path:
        if not OPENPYXL_AVAILABLE:
            logger.error("Cannot generate Excel report: openpyxl not installed")
            return self.output_path

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        wb = Workbook()
        self._build_summary_sheet(wb, results)
        self._build_details_sheet(wb, results)

        wb.save(self.output_path)
        logger.info(f"Excel report saved: {self.output_path}")
        return self.output_path

    # ── Summary sheet ─────────────────────────────────────────────────────────

    def _build_summary_sheet(self, wb: "Workbook", results: List[TestResult]) -> None:
        ws = wb.active
        ws.title = "Summary"

        total   = len(results)
        passed  = sum(1 for r in results if r.outcome == "passed")
        failed  = sum(1 for r in results if r.outcome == "failed")
        skipped = sum(1 for r in results if r.outcome == "skipped")
        errors  = sum(1 for r in results if r.outcome == "error")

        rows = [
            ("Report generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("Total",   total),
            ("PASSED",  passed),
            ("FAILED",  failed),
            ("SKIPPED", skipped),
            ("ERROR",   errors),
            ("Pass rate", f"{(passed/total*100):.1f}%" if total else "N/A"),
        ]

        ws.column_dimensions["A"].width = 20
        ws.column_dimensions["B"].width = 20

        for r_idx, (label, value) in enumerate(rows, start=1):
            label_cell = ws.cell(r_idx, 1, label)
            value_cell = ws.cell(r_idx, 2, value)
            label_cell.font = _bold()
            label_cell.fill = _fill(_GREY)
            label_cell.border = _thin_border()
            label_cell.alignment = _center()
            value_cell.border = _thin_border()
            value_cell.alignment = _center()

            if label == "PASSED":
                value_cell.fill = _fill(_GREEN)
            elif label in ("FAILED", "ERROR"):
                value_cell.fill = _fill(_RED)
            elif label == "SKIPPED":
                value_cell.fill = _fill(_YELLOW)

    # ── Details sheet ─────────────────────────────────────────────────────────

    def _build_details_sheet(self, wb: "Workbook", results: List[TestResult]) -> None:
        ws = wb.create_sheet("Test Results")

        # Header row
        for col_idx, (header, width) in enumerate(self.COLUMNS, start=1):
            cell = ws.cell(1, col_idx, header)
            cell.font = Font(bold=True, color="FFFFFFFF", size=11)
            cell.fill = _fill(_BLUE)
            cell.alignment = _center()
            cell.border = _thin_border()
            ws.column_dimensions[cell.column_letter].width = width

        ws.row_dimensions[1].height = 24

        # Data rows
        for r_idx, result in enumerate(results, start=2):
            outcome = result.outcome.upper()
            row_fill = {
                "PASSED":  _fill(_GREEN),
                "FAILED":  _fill(_RED),
                "SKIPPED": _fill(_YELLOW),
            }.get(outcome, _fill(_WHITE))

            values = [
                result.test_id,
                result.brief,
                result.test_level,
                result.test_type,
                result.execution_type,
                "Yes" if result.hw_depend else "No",
                outcome,
                f"{float(result.duration):.2f}" if result.duration else "",
                result.error_message,
            ]

            for col_idx, value in enumerate(values, start=1):
                cell = ws.cell(r_idx, col_idx, value)
                cell.border = _thin_border()
                cell.alignment = Alignment(vertical="center", wrap_text=True)
                if col_idx == 7:  # Result column → coloured
                    cell.fill = row_fill
                    cell.font = _bold()
                    cell.alignment = _center()
