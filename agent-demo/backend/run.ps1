# Agent Demo Backend Startup Script (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Intelligent Personal Agent - Backend   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "WARNING: .env file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and configure your Azure OpenAI settings." -ForegroundColor Yellow
    Write-Host ""
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Please edit it with your credentials." -ForegroundColor Green
}

# Run the application
Write-Host ""
Write-Host "Starting the backend server..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
