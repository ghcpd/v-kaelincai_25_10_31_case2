# Setup script for Project A (Faulty Implementation) - Windows PowerShell

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setting up Project A - Faulty Implementation" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
python -m venv venv_original

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_original\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements_original.txt

Write-Host "`nSetup complete for Project A!" -ForegroundColor Green
Write-Host "Environment: venv_original" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
