Clear-Host
Set-Location machine

Write-Output "Welcome to ArrowBit !"
.venv\scripts\activate
Write-Output "..."
python -m main

Set-Location ..