"""
testcase decorator — parses the @tag docstring format and attaches
pytest marks + metadata to the test function.

Usage
-----
    from core import testcase

    def test_attenuator_tc_0001(app, device):
        \"\"\"
        @test_id: test_attenuator_tc_0001
        @brief: Turn on Attenuator
        @details: Verify that the Attenuator can be powered on from PC17 UI
                  and hardware status is correct

        @pre:- PC17 application is running
             - Attenuator is connected

        @test_procedure:
            [code]
                - Turn on the Attenuator from PC17 UI
                - Observe LED indicator or measure supply voltage
                - Check status displayed on UI
            [!code]

        @pass_criteria:- Attenuator LED is ON or correct voltage is present
                       - UI shows Attenuator is ON and ready

        @test_level: system
        @test_type: functional
        @execution_type: semi-automatic
        @hw_depend: yes
        \"\"\"
        # === AUTOMATION CODE ===
        app.main_page.click_attenuator_on()
        assert device.read_voltage() > 0
"""
from __future__ import annotations

import functools
import re
import textwrap
from dataclasses import dataclass, field
from typing import Callable, List, Optional

import pytest


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class TestCaseMetadata:
    test_id:        str = ""
    brief:          str = ""
    details:        str = ""
    pre:            List[str] = field(default_factory=list)
    procedure_steps: List[str] = field(default_factory=list)   # từ [code] block
    procedure_raw:  str = ""
    pass_criteria:  List[str] = field(default_factory=list)
    test_level:     str = ""       # system | integration | unit
    test_type:      str = ""       # functional | regression | smoke …
    execution_type: str = ""       # automatic | semi-automatic | manual
    hw_depend:      bool = False


# ── Parser ────────────────────────────────────────────────────────────────────

_TAG_PATTERN = re.compile(
    r"@([\w\-]+)\s*:(.*?)(?=@[\w\-]+\s*:|$)",
    re.DOTALL,
)
_CODE_BLOCK_PATTERN = re.compile(r"\[code\](.*?)\[!code\]", re.DOTALL)
_LIST_ITEM_PATTERN  = re.compile(r"^\s*[-•]\s*(.+)", re.MULTILINE)


def _parse_list(text: str) -> List[str]:
    """Extract '-' or '•' bullet items from a text block."""
    items = _LIST_ITEM_PATTERN.findall(text)
    return [item.strip() for item in items if item.strip()]


def _parse_procedure(text: str):
    """
    Returns (steps: List[str], raw: str).
    Steps are extracted from [code]...[!code] blocks.
    """
    raw = text.strip()
    code_match = _CODE_BLOCK_PATTERN.search(text)
    steps: List[str] = []
    if code_match:
        block = code_match.group(1)
        steps = _parse_list(block)
    return steps, raw


def parse_docstring(doc: Optional[str]) -> TestCaseMetadata:
    """Parse the @tag-based docstring into TestCaseMetadata."""
    meta = TestCaseMetadata()
    if not doc:
        return meta

    doc = textwrap.dedent(doc)

    for match in _TAG_PATTERN.finditer(doc):
        tag   = match.group(1).strip().lower().replace("-", "_")
        value = match.group(2).strip()

        if tag == "test_id":
            meta.test_id = value

        elif tag == "brief":
            meta.brief = value

        elif tag == "details":
            meta.details = value

        elif tag == "pre":
            meta.pre = _parse_list(value) or [value.strip()]

        elif tag == "test_procedure":
            meta.procedure_steps, meta.procedure_raw = _parse_procedure(value)

        elif tag == "pass_criteria":
            meta.pass_criteria = _parse_list(value) or [value.strip()]

        elif tag == "test_level":
            meta.test_level = value.lower()

        elif tag == "test_type":
            meta.test_type = value.lower()

        elif tag == "execution_type":
            meta.execution_type = value.lower().replace("-", "_")

        elif tag == "hw_depend":
            meta.hw_depend = value.lower() in ("yes", "true", "1")

    return meta


# ── Decorator ─────────────────────────────────────────────────────────────────

def testcase(func: Callable) -> Callable:
    """
    Decorator that:
    1. Parses the @tag docstring → TestCaseMetadata
    2. Attaches metadata as func._tc_meta
    3. Applies pytest marks automatically
    """
    meta = parse_docstring(func.__doc__)
    func._tc_meta = meta

    marks: list = []

    # -- test_id mark (used by Excel/TestRail reporters)
    if meta.test_id:
        marks.append(pytest.mark.test_id(meta.test_id))

    # -- test_level  (system, integration, unit, …)
    if meta.test_level:
        marks.append(getattr(pytest.mark, meta.test_level))

    # -- test_type  (functional, regression, smoke, …)
    if meta.test_type:
        marks.append(getattr(pytest.mark, meta.test_type))

    # -- execution_type  (automatic, semi_automatic, manual)
    if meta.execution_type:
        marks.append(getattr(pytest.mark, meta.execution_type))

    # -- hw_depend
    if meta.hw_depend:
        marks.append(pytest.mark.hw_depend)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Apply marks (innermost first — order preserved by pytest)
    for mark in marks:
        wrapper = mark(wrapper)

    return wrapper
