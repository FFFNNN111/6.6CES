# -*- coding: utf-8 -*-
$ErrorActionPreference = "Stop"

$ServiceScript = Join-Path $PSScriptRoot "ces_backend_daemon.ps1"
$TaskName = "CESBackendAutoStart"
$RunPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"

if (-not (Test-Path $ServiceScript)) {
  Write-Host "Backend service script not found: $ServiceScript"
  exit 1
}

$Command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ServiceScript`""

New-ItemProperty -Path $RunPath -Name $TaskName -Value $Command -PropertyType String -Force | Out-Null

Start-Process -FilePath "powershell.exe" -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", $ServiceScript) -WindowStyle Hidden

Write-Host "CES backend autostart registry entry installed and started: $TaskName"
