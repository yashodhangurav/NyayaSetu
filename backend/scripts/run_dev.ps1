# Windows PowerShell counterpart of scripts/run_dev.sh.
# Activates the first usable virtual environment and launches the backend API.

$ErrorActionPreference = "Stop"

$backendDir = Split-Path -Parent $PSScriptRoot
Set-Location $backendDir

$venvCandidates = @(
    (Join-Path (Split-Path -Parent $backendDir) "venv"),
    (Join-Path $backendDir ".venv"),
    (Join-Path $backendDir "venv")
)

foreach ($candidate in $venvCandidates) {
    $activate = Join-Path $candidate "Scripts/Activate.ps1"
    if (Test-Path $activate) {
        Write-Host "Activating virtual environment from $candidate..."
        . $activate
        break
    }
}

Write-Host "Starting NyayaSetu FastAPI Server on http://localhost:8000 ..."
python run.py
