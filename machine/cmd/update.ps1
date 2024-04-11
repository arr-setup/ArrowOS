Clear-Host
Set-Location machine

Remove-Item -Path ".venv" -Recurse

Write-Output "Setting a new venv..."
python -m venv .venv
.venv\scripts\activate

Write-Output "Upgrading pip..."
python -m pip install -q --upgrade pip

Write-Output "Installing modules..."
python -m pip install -q adrv cryptography requests bcrypt

Set-Location ..