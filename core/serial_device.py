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
        """
        @brief  Khởi tạo SerialDevice với thông số kết nối; mặc định lấy từ settings.serial
        @param  port: Tên COM port (ví dụ: "COM3"). Mặc định lấy từ settings.serial.default_port
        @param  baudrate: Tốc độ baud. Mặc định lấy từ settings.serial.baudrate
        @param  timeout: Timeout đọc (giây). Mặc định lấy từ settings.serial.timeout
        @retval None
        """
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
        """
        @brief  Mở kết nối serial; tự động detect port nếu auto_detect=True trong config
        @retval SerialDevice — self (để chain)
        """
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
        """
        @brief  Đóng kết nối serial nếu đang mở
        @retval None
        """
        if self._ser and self._ser.is_open:
            self._ser.close()
            logger.info(f"Serial port {self.port} closed")

    def is_open(self) -> bool:
        """
        @brief  Kiểm tra serial port có đang mở không
        @retval bool — True nếu port đang mở, False nếu không
        """
        return self._ser is not None and self._ser.is_open

    # ── Auto-detection ────────────────────────────────────────────────────────

    @staticmethod
    def list_ports() -> List[str]:
        """
        @brief  Trả về danh sách tất cả tên COM port đang có trên hệ thống
        @retval List[str] — danh sách tên port (ví dụ: ["COM3", "COM5"])
        """
        ports = serial.tools.list_ports.comports()
        return [p.device for p in ports]

    @staticmethod
    def find_port_by_description(keyword: str) -> Optional[str]:
        """
        @brief  Tìm COM port có description chứa từ khóa chỉ định
        @param  keyword: Từ khóa tìm kiếm trong description của port (không phân biệt hoa/thường)
        @retval Optional[str] — tên port nếu tìm thấy (ví dụ: "COM3"), None nếu không
        """
        for p in serial.tools.list_ports.comports():
            if keyword.lower() in p.description.lower():
                return p.device
        return None

    @staticmethod
    def find_port_by_vid_pid(vid: int, pid: int) -> Optional[str]:
        """
        @brief  Tìm COM port theo USB Vendor ID và Product ID
        @param  vid: USB Vendor ID (số nguyên, ví dụ: 0x0403)
        @param  pid: USB Product ID (số nguyên, ví dụ: 0x6001)
        @retval Optional[str] — tên port nếu tìm thấy, None nếu không
        """
        for p in serial.tools.list_ports.comports():
            if p.vid == vid and p.pid == pid:
                return p.device
        return None

    def _detect_port(self) -> Optional[str]:
        """
        @brief  Hook để override auto-detect port theo thiết bị cụ thể; mặc định trả về None
        @retval Optional[str] — tên port nếu detect được, None để dùng port đã cấu hình
        """
        # Default: just return the configured port
        return None

    # ── Send / Receive ────────────────────────────────────────────────────────

    def send(self, data: str, encoding: str = "utf-8") -> int:
        """
        @brief  Mã hóa và gửi chuỗi string qua serial port
        @param  data: Chuỗi dữ liệu cần gửi (ví dụ: "VOLT?\\r\\n")
        @param  encoding: Encoding để mã hóa string (default: "utf-8")
        @retval int — số byte đã ghi thành công
        """
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        payload = data.encode(encoding)
        written = self._ser.write(payload)
        logger.debug(f"TX ({written}B): {data!r}")
        return written

    def send_bytes(self, data: bytes) -> int:
        """
        @brief  Gửi raw bytes qua serial port
        @param  data: Dữ liệu bytes cần gửi
        @retval int — số byte đã ghi thành công
        """
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        written = self._ser.write(data)
        logger.debug(f"TX bytes ({written}B): {data!r}")
        return written

    def readline(self, encoding: str = "utf-8") -> str:
        """
        @brief  Đọc một dòng từ serial port (đến khi gặp newline hoặc timeout)
        @param  encoding: Encoding để decode bytes thành string (default: "utf-8")
        @retval str — dòng đọc được đã strip whitespace
        """
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        raw = self._ser.readline()
        text = raw.decode(encoding, errors="replace").strip()
        logger.debug(f"RX: {text!r}")
        return text

    def read_all(self, encoding: str = "utf-8") -> str:
        """
        @brief  Đọc tất cả bytes hiện có trong buffer của serial port
        @param  encoding: Encoding để decode bytes thành string (default: "utf-8")
        @retval str — toàn bộ dữ liệu đọc được đã strip whitespace
        """
        if not self.is_open():
            raise SerialDeviceError("Serial port is not open")
        raw = self._ser.read_all()
        return raw.decode(encoding, errors="replace").strip()

    def query(self, command: str, delay: float = 0.1) -> str:
        """
        @brief  Flush buffer, gửi lệnh, chờ một chút rồi đọc một dòng response
        @param  command: Lệnh cần gửi (ví dụ: "VOLT?\\r\\n")
        @param  delay: Thời gian chờ (giây) sau khi gửi trước khi đọc (default: 0.1)
        @retval str — dòng response đọc được
        """
        self.flush()
        self.send(command)
        time.sleep(delay)
        return self.readline()

    def flush(self) -> None:
        """
        @brief  Xoá input buffer và output buffer của serial port
        @retval None
        """
        if self.is_open():
            self._ser.reset_input_buffer()
            self._ser.reset_output_buffer()

    # ── Common helpers ────────────────────────────────────────────────────────

    def read_voltage(self, command: str = "VOLT?\r\n") -> float:
        """
        @brief  Gửi lệnh query voltage và parse kết quả thành float
        @param  command: Lệnh query (default: "VOLT?\\r\\n"); override cho protocol cụ thể
        @retval float — giá trị điện áp đọc được; 0.0 nếu không parse được
        """
        resp = self.query(command)
        try:
            return float(resp.strip())
        except ValueError:
            logger.warning(f"Cannot parse voltage from: {resp!r}")
            return 0.0

    def is_connected(self, ping_command: str = "PING\r\n", expected: str = "OK") -> bool:
        """
        @brief  Kiểm tra thiết bị có phản hồi lệnh ping không
        @param  ping_command: Lệnh ping gửi đi (default: "PING\\r\\n")
        @param  expected: Chuỗi mong đợi trong response (default: "OK")
        @retval bool — True nếu response chứa expected, False nếu không hoặc có exception
        """
        try:
            resp = self.query(ping_command, delay=0.2)
            return expected.lower() in resp.lower()
        except Exception:
            return False

    def wait_for_response(
        self, expected: str, timeout: float = 5.0, poll: float = 0.2
    ) -> bool:
        """
        @brief  Poll đọc response liên tục cho đến khi xuất hiện expected hoặc timeout
        @param  expected: Chuỗi mong đợi trong response (không phân biệt hoa/thường)
        @param  timeout: Số giây tối đa chờ (default: 5.0)
        @param  poll: Khoảng cách giữa các lần đọc (giây) (default: 0.2)
        @retval bool — True nếu expected xuất hiện trong timeout, False nếu hết thời gian
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            resp = self.readline()
            if expected.lower() in resp.lower():
                return True
            time.sleep(poll)
        return False

    # ── Context manager ───────────────────────────────────────────────────────

    def __enter__(self) -> "SerialDevice":
        """
        @brief  Context manager entry — gọi open() và trả về self
        @retval SerialDevice — self sau khi mở port
        """
        return self.open()

    def __exit__(self, *_) -> None:
        """
        @brief  Context manager exit — đóng serial port
        @retval None
        """
        self.close()

    def __repr__(self) -> str:
        """
        @brief  Trả về string đại diện của SerialDevice
        @retval str — string mô tả port, baudrate và trạng thái kết nối
        """
        return f"SerialDevice(port={self.port!r}, baud={self.baudrate}, open={self.is_open()})"
