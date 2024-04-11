Clear-Host
Set-Location machine

if (Test-Path '.venv' -PathType Container) {
    $answer = Read-Host "Remove the existing venv ? (Y/N - Recommended if you want an up-to-date machine) "

    if ($answer -eq "Y" -or $answer -eq "y") {
        Set-Location ..
        .\machine\cmd\update
        Set-Location machine
    } else {
        Write-Host "The venv has been conserved. Please setup the machine again before submitting a bug report if you have a problem"
        .venv\scripts\activate
    }
} else {
    Write-Output "Setting venv..."
    python -m venv .venv
    .venv\scripts\activate

    Write-Output "Installing modules..."
    python -m pip install -q --upgrade pip
    python -m pip install -q adrv cryptography requests bcrypt
}

Write-Output "Starting machine..."
python -m setup
python -m main

Set-Location ..