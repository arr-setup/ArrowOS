Clear-Host
Set-Location machine

Write-Output "Removing environment..."
Remove-Item -Path '.venv' -Force -Recurse
Write-Output "Removing storage..."
Remove-Item -Path 'disks' -Force -Recurse

Set-Location ..
$answer = Read-Host "Setup the machine again ? (O/N)"

if ($answer -eq "Y" -or $answer -eq "y") {
    .\machine\cmd\update
    .\machine\cmd\setup
} else {
    Write-Host "The machine has been reset to its primary state."
}