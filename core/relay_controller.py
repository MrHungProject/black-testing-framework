"""
RelayController — controls external relay board via serial.

Enable in settings.yaml:  relay.enabled: true

Protocol CH340 relay boards:
    ON:  bytes [0xA0, channel, 0x01, checksum]
    OFF: bytes [0xA0, channel, 0x00, checksum]
"""
from __future__ import annotations

import time
from typing import Optional

import serial

from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)


class RelayControllerError(Exception):
    pass


class RelayController:
    """Controls a USB relay board for power-cycling the DUT."""

    def __init__(self):
        cfg = get_settings().relay
        self.enabled      = cfg.enabled
        self.port         = cfg.port
        self.baudrate     = cfg.baudrate
        self.channels     = cfg.channels
        self.cycle_delay  = cfg.power_cycle_delay

        self._ser: Optional[serial.Serial] = None

    # ── Connection ────────────────────────────────────────────────────────────

    def connect(self) -> "RelayController":
        if not self.enabled:
            logger.info("RelayController is DISABLED (relay.enabled=false in settings)")
            return self
        logger.info(f"Connecting relay board on {self.port}")
        self._ser = serial.Serial(self.port, self.baudrate, timeout=1)
        return self

    def disconnect(self) -> None:
        if self._ser and self._ser.is_open:
            self._ser.close()
            logger.info("Relay board disconnected")

    def is_connected(self) -> bool:
        return self._ser is not None and self._ser.is_open

    # ── Relay control ─────────────────────────────────────────────────────────

    def on(self, channel: int = 1) -> None:
        self._validate_channel(channel)
        logger.info(f"Relay CH{channel} → ON")
        if self.is_connected():
            self._send_relay_command(channel, state=True)

    def off(self, channel: int = 1) -> None:
        self._validate_channel(channel)
        logger.info(f"Relay CH{channel} → OFF")
        if self.is_connected():
            self._send_relay_command(channel, state=False)

    def all_on(self) -> None:
        for ch in range(1, self.channels + 1):
            self.on(ch)

    def all_off(self) -> None:
        for ch in range(1, self.channels + 1):
            self.off(ch)

    def power_cycle(self, channel: int = 1) -> None:
        """OFF → wait → ON."""
        logger.info(f"Power cycling relay CH{channel} (delay={self.cycle_delay}s)")
        self.off(channel)
        time.sleep(self.cycle_delay)
        self.on(channel)
        logger.info("Power cycle complete")

    # ── Internal ──────────────────────────────────────────────────────────────

    def _validate_channel(self, channel: int) -> None:
        if not (1 <= channel <= self.channels):
            raise RelayControllerError(
                f"Invalid channel {channel}. Valid range: 1–{self.channels}"
            )

    def _send_relay_command(self, channel: int, state: bool) -> None:
        cmd_byte = 0x01 if state else 0x00
        checksum = (0xA0 + channel + cmd_byte) & 0xFF
        packet = bytes([0xA0, channel, cmd_byte, checksum])
        self._ser.write(packet)
        time.sleep(0.05)

    # ── Context manager ───────────────────────────────────────────────────────

    def __enter__(self) -> "RelayController":
        return self.connect()

    def __exit__(self, *_) -> None:
        self.all_off()
        self.disconnect()
