"""
Fixtures cho Power Measurement tests (PUC_3.2).
SignalGenerator: SCPI over Serial (USB/GPIB).
"""
from __future__ import annotations

import math
import os

import pytest

from core.serial_device import SerialDevice
from utils.logger import get_logger

logger = get_logger(__name__)

TOLERANCE_PCT = 1.71  # sai số cho phép (% tính trên thang tuyến tính mW)


class SignalGenerator:
    """SCPI wrapper điều khiển Signal Generator qua Serial port."""

    def __init__(self, device: SerialDevice):
        self._dev = device

    def set_frequency(self, freq_hz: float) -> None:
        self._dev.send(f"FREQ {freq_hz:.0f}Hz\r\n")
        logger.info(f"SignalGen: FREQ = {freq_hz / 1e6:.6g} MHz")

    def set_power(self, power_dbm: float) -> None:
        self._dev.send(f"POW {power_dbm:.2f}DBM\r\n")
        logger.info(f"SignalGen: POW = {power_dbm} dBm")

    def output_on(self) -> None:
        self._dev.send("OUTP ON\r\n")
        logger.info("SignalGen: OUTPUT ON")

    def output_off(self) -> None:
        self._dev.send("OUTP OFF\r\n")
        logger.info("SignalGen: OUTPUT OFF")


def power_error_pct(measured_dbm: float, expected_dbm: float) -> float:
    """
    Tính sai số công suất theo % trên thang tuyến tính (mW).
    Công thức: |measured_mW - expected_mW| / expected_mW * 100
    """
    measured_mw = 10 ** (measured_dbm / 10)
    expected_mw = 10 ** (expected_dbm / 10)
    return abs(measured_mw - expected_mw) / expected_mw * 100


@pytest.fixture(scope="session")
def signal_gen() -> "SignalGenerator":
    """
    Session-scoped fixture cho Signal Generator.
    Port mặc định COM4 — override bằng env var SIGNAL_GEN_PORT.
    """
    port = os.getenv("SIGNAL_GEN_PORT", "COM4")
    dev = SerialDevice(port=port, baudrate=9600)
    dev.open()
    gen = SignalGenerator(dev)
    gen.output_off()  # trạng thái an toàn khi khởi động
    yield gen
    gen.output_off()
    dev.close()
