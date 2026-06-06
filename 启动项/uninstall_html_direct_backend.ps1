# -*- coding: utf-8 -*-
$ErrorActionPreference = "Stop"

$RunPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$Name = "CESBackendAutoStart"

if (Get-ItemProperty -Path $RunPath -Name $Name -ErrorAction SilentlyContinue) {
  Remove-ItemProperty -Path $RunPath -Name $Name
}

Unregister-ScheduledTask -TaskName $Name -Confirm:$false -ErrorAction SilentlyContinue

Write-Host "CES backend autostart removed."
