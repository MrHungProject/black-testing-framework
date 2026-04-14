@echo off
echo ============================================================
echo  BLACK TESTING FRAMEWORK - DEMO RUN
echo ============================================================
echo.

REM Cài dependencies nếu chưa có
echo [1/3] Checking dependencies...
pip install pytest pytest-html openpyxl pydantic pydantic-settings PyYAML pyserial 2>nul
echo.

REM Chạy demo tests
echo [2/3] Running demo tests...
echo.
pytest tests/demo/ -v --tb=short

echo.
echo [3/3] Reports generated:
echo   HTML  : reports\html\report.html
echo   Excel : reports\excel\test_results.xlsx
echo   Log   : reports\logs\
echo.

REM Tự mở HTML report
echo Opening HTML report in browser...
start "" "reports\html\report.html"

pause
