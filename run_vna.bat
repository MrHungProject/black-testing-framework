@echo off
echo ============================================================
echo  BLACK TESTING FRAMEWORK - VNA TEST RUN
echo ============================================================
echo.
echo  TC1: Connection + Detail check
echo  TC2: Disconnect/Reconnect 5 cycles
echo  TC3: Measurement (S11/S21) + Stimulus + Marker
echo ============================================================
echo.

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] .venv not found. Run: python -m venv .venv ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Chạy VNA tests
echo [RUN] pytest tests/vna/ -v
echo.
pytest tests/vna/ -v --tb=short

echo.
echo ============================================================
echo  Reports:
echo    HTML  : reports\html\report.html
echo    Excel : reports\excel\vna_report.xlsx
echo    Log   : reports\logs\pytest.log
echo ============================================================
echo.

start "" "reports\html\report.html"

pause
