"""
BasePage — Page Object Model base class.

Every page of your app should extend this and define
element locators + high-level actions.

Example
-------
    class MainPage(BasePage):
        BTN_ATTENUATOR_ON  = {"auto_id": "btnAttenuatorOn"}
        LBL_STATUS         = {"auto_id": "lblStatus"}

        def click_attenuator_on(self):
            self.click(self.BTN_ATTENUATOR_ON)

        def get_status(self) -> str:
            return self.get_text(self.LBL_STATUS)
"""
from __future__ import annotations

from typing import Union

from core.app_controller import AppController
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Abstract base for all Page Object classes."""

    def __init__(self, controller: AppController):
        self._ctrl = controller

    # ── Delegated actions ─────────────────────────────────────────────────────

    def click(self, identifier: Union[str, dict]) -> None:
        self._ctrl.click(identifier)

    def double_click(self, identifier: Union[str, dict]) -> None:
        self._ctrl.double_click(identifier)

    def type_text(self, identifier: Union[str, dict], text: str) -> None:
        self._ctrl.type_text(identifier, text)

    def set_value(self, identifier: Union[str, dict], value: str) -> None:
        self._ctrl.set_value(identifier, value)

    def get_text(self, identifier: Union[str, dict]) -> str:
        return self._ctrl.get_text(identifier)

    def is_enabled(self, identifier: Union[str, dict]) -> bool:
        return self._ctrl.is_element_enabled(identifier)

    def wait_for(self, identifier: Union[str, dict], timeout: int = 10) -> bool:
        return self._ctrl.wait_for_element(identifier, timeout)

    def select(self, identifier: Union[str, dict], item: str) -> None:
        self._ctrl.select_combobox(identifier, item)

    def screenshot(self, name: str) -> None:
        self._ctrl.take_screenshot(name)
