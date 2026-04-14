"""
SerialDevice — manages USB Serial (COM port) communication with the DUT.

Features
--------
- Auto-detect COM port by VID:PID or description keyword
- Send / receive with timeout
- Read voltage, status, ACK/NACK helpers
- Context manager support

Usage
-----
    dev = SerialDevice()
    dev.open()
    dev.send("PWR ON\\r\\n")
    response = dev.readline()
    dev.close()

    # or as context manager
    with SerialDevice(port="COM3") as dev:
        dev.send("STATUS?\\r\\n")
        print(dev.readline())
"""
from __future__ import annotations

import time
from typing import List, Optional

import serial
import serial.tools.list_ports

from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)


class SerialDeviceError(Exception):
    pass


class SerialDevice:
    """Low-level USB serial device handler."""

    def __init__(
        self,
        port: Optional[str] = None,
        baudrate: Optional[int] = None,
        timeout: Optional[float] = None,
    ):
        cfg = get_settings().serial
        self.port         = port      or cfg.default_port
        self.baudrate     = baudrate  or cfg.baudrate
        self.timeout      = timeout   or cfg.timeout
        self.bytesize     = cfg.bytesize
        self.parity       = cfg.parity
        self.stopbits     = cfg.stopbits
        self.write_timeout = cfg.write_timeout
        self._auto_detect = cfg.auto_detect

        self._ser: Optional[serial.Serial] = None

    # ── Connection ────────────────────────────────────────────────────────────

    def open(self) -> "SerialDevice":
        """Open the serial connection. Auto-detects port if configured."""
        if self._auto_detect:
            detected = self._detect_port()
            if detected:
                self.port = detected

        logger.info(f"Opening serial port {self.port} @ {self.baudrate} baud")
        try:
            self._ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
                write_timeout=self.write_timeout,
            )
            logger.info(f"Serial port opened: {self._ser.name}")
        except serial.SerialException as e:
            raise SerialDeviceError(f"Cannot open {self.port}: {e}") from e
        return self

    def close(self) -> None:
        if self._ser and self._ser.is_open:
            self._ser.close()
            logger.info(f"Serial port {self.port} closed")

    def is_open(self) -> bool:
        return self._ser is not None and self._ser.is_open

    # ── Auto-detection ────────────────────────────────────────────────────────

    @staticmethod
    def list_ports() -> List[str]:
        """Return all available COM port names."""
        ports = serial.tools.list_ports.comports()
        return [p.device for p in ports]

    @staticmethod
    def find_port_by_description(keyword: str) -> Optional[str]:
        """Find COM port whose description contains keyword."""
        for p in serial.tools.list_ports.comports():
            if keyword.lower() in p.description.lower():
                return p.device
        return None

    @staticmethod
    def find_port_by_vid_pid(vid: int, pid: int) -> Optional[str]:
        """Find COM port by USB Vendor ID and Product ID."""
        for p in serial.tools.list_ports.comports():
            if p.vid == vid and p.pid == pid:
                return p.device
        return None

    def _detect_port(self) -> Optional[str]:
        """Override this method per-project to auto-detect your specific device."""
        # Default: just return the configured port
        return None

    # ── Send / Receive ────────────────────────────────────────────────────────

    def send(self, data: str, encoding: str = "utf-8") -> int:
        """Send string data. Returns number of bytes written."""
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        payload = data.encode(encoding)
        written = self._ser.write(payload)
        logger.debug(f"TX ({written}B): {data!r}")
        return written

    def send_bytes(self, data: bytes) -> int:
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        written = self._ser.write(data)
        logger.debug(f"TX bytes ({written}B): {data!r}")
        return written

    def readline(self, encoding: str = "utf-8") -> str:
        """Read until newline or timeout."""
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        raw = self._ser.readline()
        text = raw.decode(encoding, errors="replace").strip()
        logger.debug(f"RX: {text!r}")
        return text

    def read_all(self, encoding: str = "utf-8") -> str:
        """Read all available bytes."""
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        raw = self._ser.read_all()
        return raw.decode(encoding, errors="replace").strip()

    def query(self, command: str, delay: float = 0.1) -> str:
        """Send command, wait briefly, read response."""
        self.flush()
        self.send(command)
        time.sleep(delay)
        return self.readline()

    def flush(self) -> None:
        if self.is_open():
            self._ser.reset_input_buffer()
            self._ser.reset_output_buffer()

    # ── Common helpers ────────────────────────────────────────────────────────

    def read_voltage(self, command: str = "VOLT?\r\n") -> float:
        """
        Send voltage query and parse float response.
        Override for your specific protocol.
        """
        resp = self.query(command)
        try:
            return float(resp.strip())
        except ValueError:
            logger.warning(f"Cannot parse voltage from: {resp!r}")
            return 0.0

    def is_connected(self, ping_command: str = "PING\r\n", expected: str = "OK") -> bool:
        """Check if device responds to a ping command."""
        try:
            resp = self.query(ping_command, delay=0.2)
            return expected.lower() in resp.lower()
        except Exception:
            return False

    def wait_for_response(
        self, expected: str, timeout: float = 5.0, poll: float = 0.2
    ) -> bool:
        """Poll until expected string appears in response or timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            resp = self.readline()
            if expected.lower() in resp.lower():
                return True
            time.sleep(poll)
        return False

    # ── Context manager ───────────────────────────────────────────────────────

    def __enter__(self) -> "SerialDevice":
        return self.open()

    def __exit__(self, *_) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"SerialDevice(port={self.port!r}, baud={self.baudrate}, open={self.is_open()})"
