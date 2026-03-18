# CM-OS Memory Boot (Windows PowerShell)
# Usage: powershell -File .ai_memory/scripts/memory.ps1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$memDir = Split-Path -Parent $scriptDir
$rootDir = Split-Path -Parent $memDir

Write-Host "=== CM-OS Memory Boot ===" -ForegroundColor Cyan

# Step 1: Scan repo
Write-Host "Scanning repository..."
python "$scriptDir/scan_repo.py"

# Step 2: Git context
Write-Host "Extracting git context..."
python "$scriptDir/git_context.py"

# Step 3: Reset session
Write-Host "Starting new session..."
python "$scriptDir/session_memory.py" start

# Step 4: Generate MEMORY_PACK
Write-Host "Generating MEMORY_PACK..."
python "$scriptDir/memory_pack.py"

Write-Host "=== CM-OS Ready ===" -ForegroundColor Green
