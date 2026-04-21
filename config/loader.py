"""
Loads settings.yaml → typed Pydantic models.
Environment variables override yaml values:
    SERIAL_PORT=COM5   → serial.default_port
    APP_EXE_PATH=...   → app.exe_path
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    name: str = "FormMainEliteRF"
    exe_path: str = ""
    backend: str = "uia"
    connect_timeout: int = 15
    action_delay: float = 0.3


class S2VnaConfig(BaseModel):
    name: str = "S2VNA"
    exe_path: str = ""
    backend: str = "uia"
    connect_timeout: int = 15
    startup_wait: int = 3


class SerialConfig(BaseModel):
    default_port: str = "COM3"
    baudrate: int = 115200
    bytesize: int = 8
    parity: str = "N"
    stopbits: int = 1
    timeout: float = 2.0
    write_timeout: float = 2.0
    auto_detect: bool = True


class RelayConfig(BaseModel):
    enabled: bool = False
    port: str = "COM10"
    baudrate: int = 9600
    channels: int = 4
    power_cycle_delay: float = 3.0


class ReportConfig(BaseModel):
    output_dir: str = "reports"
    html_dir: str = "reports/html"
    excel_dir: str = "reports/excel"
    log_dir: str = "reports/logs"
    excel_filename: str = "test_results.xlsx"
    include_screenshots: bool = True
    screenshot_on_fail: bool = True


class TestRailConfig(BaseModel):
    enabled: bool = False
    url: str = ""
    username: str = ""
    api_key: str = ""
    project_id: int = 1
    suite_id: int = 1


class SpikeConfig(BaseModel):
    name: str = "Spike"
    exe_path: str = ""
    backend: str = "uia"
    connect_timeout: int = 15
    startup_wait: int = 3


class Settings(BaseModel):
    app: AppConfig = Field(default_factory=AppConfig)
    s2vna: S2VnaConfig = Field(default_factory=S2VnaConfig)
    spike: SpikeConfig = Field(default_factory=SpikeConfig)
    serial: SerialConfig = Field(default_factory=SerialConfig)
    relay: RelayConfig = Field(default_factory=RelayConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)
    testrail: TestRailConfig = Field(default_factory=TestRailConfig)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    config_path = Path(__file__).parent / "settings.yaml"
    data: dict = {}
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    settings = Settings.model_validate(data)

    # ── Environment variable overrides (dùng trong CI/CD) ─────────────────
    if port := os.getenv("SERIAL_PORT"):
        settings.serial.default_port = port
    if exe := os.getenv("APP_EXE_PATH"):
        settings.app.exe_path = exe
    if relay_port := os.getenv("RELAY_PORT"):
        settings.relay.port = relay_port
    if s2vna_exe := os.getenv("S2VNA_EXE_PATH"):
        settings.s2vna.exe_path = s2vna_exe
    if spike_exe := os.getenv("SPIKE_EXE_PATH"):
        settings.spike.exe_path = spike_exe

    return settings
