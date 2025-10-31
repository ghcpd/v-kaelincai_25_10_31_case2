# Run script for Project B (Optimized Implementation) - Windows PowerShell

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Running Project B - Optimized Implementation" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_optimized\Scripts\Activate.ps1"

# Clear previous logs
if (Test-Path "log_optimized.txt") { Remove-Item "log_optimized.txt" }
if (Test-Path "time_optimized.txt") { Remove-Item "time_optimized.txt" }

# Start timing
$startTime = Get-Date

Write-Host "Running tests with pytest...`n" -ForegroundColor Yellow

# Run tests and capture output
pytest test_optimized.py -v --tb=short --json-report --json-report-file=test_results_optimized.json 2>&1 | Tee-Object -FilePath log_optimized.txt

# End timing
$endTime = Get-Date
$executionTime = ($endTime - $startTime).TotalSeconds

# Generate timing report
@"
=========================================
Project B - Performance Report
=========================================

Execution Time: $executionTime seconds
Timestamp: $(Get-Date)

Test Results Summary:
See log_optimized.txt for detailed output
See test_results_optimized.json for structured results

"@ | Out-File -FilePath time_optimized.txt -Encoding UTF8

# Display summary
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "Execution Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Total execution time: $executionTime seconds" -ForegroundColor Yellow
Write-Host "Results saved to:" -ForegroundColor Green
Write-Host "  - log_optimized.txt"
Write-Host "  - time_optimized.txt"
Write-Host "  - test_results_optimized.json"
Write-Host "=========================================" -ForegroundColor Cyan
