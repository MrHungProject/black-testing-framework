# BLACK TESTING FRAMEWORK - Demo runner (PowerShell)
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " BLACK TESTING FRAMEWORK - DEMO RUN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Install dependencies
Write-Host "[1/3] Installing dependencies..." -ForegroundColor Yellow
pip install pytest pytest-html openpyxl pydantic pydantic-settings PyYAML pyserial | Out-Null
Write-Host "Done." -ForegroundColor Green
Write-Host ""

# Run tests
Write-Host "[2/3] Running demo tests..." -ForegroundColor Yellow
Write-Host ""
pytest tests/demo/ -v --tb=short

Write-Host ""
Write-Host "[3/3] Reports:" -ForegroundColor Yellow
Write-Host "  HTML  : reports\html\report.html" -ForegroundColor Green
Write-Host "  Excel : reports\excel\test_results.xlsx" -ForegroundColor Green
Write-Host "  Log   : reports\logs\" -ForegroundColor Green
Write-Host ""

# Open report
Start-Process "reports\html\report.html"
