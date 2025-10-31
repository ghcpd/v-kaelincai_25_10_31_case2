# Run script for Project A (Faulty Implementation) - Windows PowerShell

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Running Project A - Faulty Implementation" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_original\Scripts\Activate.ps1"

# Clear previous logs
if (Test-Path "log_original.txt") { Remove-Item "log_original.txt" }
if (Test-Path "time_original.txt") { Remove-Item "time_original.txt" }

# Start timing
$startTime = Get-Date

Write-Host "Running tests with pytest...`n" -ForegroundColor Yellow

# Run tests and capture output
pytest test_original.py -v --tb=short --json-report --json-report-file=test_results_original.json 2>&1 | Tee-Object -FilePath log_original.txt

# End timing
$endTime = Get-Date
$executionTime = ($endTime - $startTime).TotalSeconds

# Generate timing report
@"
=========================================
Project A - Performance Report
=========================================

Execution Time: $executionTime seconds
Timestamp: $(Get-Date)

Test Results Summary:
See log_original.txt for detailed output
See test_results_original.json for structured results

"@ | Out-File -FilePath time_original.txt -Encoding UTF8

# Display summary
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "Execution Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Total execution time: $executionTime seconds" -ForegroundColor Yellow
Write-Host "Results saved to:" -ForegroundColor Green
Write-Host "  - log_original.txt"
Write-Host "  - time_original.txt"
Write-Host "  - test_results_original.json"
Write-Host "=========================================" -ForegroundColor Cyan
