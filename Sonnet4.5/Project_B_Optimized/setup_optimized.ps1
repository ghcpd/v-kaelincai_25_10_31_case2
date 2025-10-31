# Setup script for Project B (Optimized Implementation) - Windows PowerShell

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setting up Project B - Optimized Implementation" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
python -m venv venv_optimized

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_optimized\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements_optimized.txt

Write-Host "`nSetup complete for Project B!" -ForegroundColor Green
Write-Host "Environment: venv_optimized" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
