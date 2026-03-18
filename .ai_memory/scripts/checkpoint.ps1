# CM-OS Checkpoint (Windows PowerShell)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Saving Checkpoint ===" -ForegroundColor Yellow
python "$scriptDir/scan_repo.py"
python "$scriptDir/git_context.py"
python "$scriptDir/memory_pack.py"
python "$scriptDir/save_session_state.py"
python "$scriptDir/episode_log.py" "Checkpoint saved"
Write-Host "=== Checkpoint Complete ===" -ForegroundColor Green
