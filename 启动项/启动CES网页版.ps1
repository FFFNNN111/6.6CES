# -*- coding: utf-8 -*-
$ErrorActionPreference = "Stop"

$AppDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ProjectDir = (Resolve-Path (Join-Path $AppDir "..")).Path
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$BackendFile = (Get-ChildItem -Path $AppDir -Recurse -Filter "proxy.py" -File | Select-Object -First 1).FullName
$Port = "8088"
$LocalUrl = "http://127.0.0.1:$Port"

if (-not (Test-Path $PythonExe)) {
  Write-Host "Python venv not found: $PythonExe"
  Read-Host "Press Enter to exit"
  exit 1
}

if (-not $BackendFile -or -not (Test-Path $BackendFile)) {
  Write-Host "Backend proxy.py not found under: $AppDir"
  Read-Host "Press Enter to exit"
  exit 1
}

$env:PORT = $Port
$env:DEEPSEEK_URL = "https://api.deepseek.com"
$env:DEEPSEEK_RETRIES = "5"
$env:DEEPSEEK_TIMEOUT = "25"

function Test-CesHealth {
  try {
    $resp = Invoke-RestMethod -Uri "$LocalUrl/api/health" -TimeoutSec 3
    return [bool]$resp.ok
  } catch {
    return $false
  }
}

if (-not (Test-CesHealth)) {
  Write-Host "Starting CES backend..."
  Start-Process -FilePath $PythonExe -ArgumentList @($BackendFile) -WorkingDirectory (Split-Path -Parent $BackendFile) -WindowStyle Minimized
}

$ready = $false
for ($i = 0; $i -lt 60; $i++) {
  if (Test-CesHealth) {
    $ready = $true
    break
  }
  Start-Sleep -Seconds 1
}

if (-not $ready) {
  Write-Host "Backend startup failed. Local model or port 8088 is not ready."
  Read-Host "Press Enter to exit"
  exit 1
}

$lanIps = @()
try {
  $lanIps = Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
    Select-Object -ExpandProperty IPAddress -Unique
} catch {
  $lanIps = @()
}

Write-Host ""
Write-Host "CES web app is ready."
Write-Host "Local URL: $LocalUrl"
foreach ($ip in $lanIps) {
  Write-Host "Phone URL on same Wi-Fi: http://$ip`:$Port"
}
Write-Host ""
Write-Host "If phone cannot open it, check same Wi-Fi and Windows Firewall port 8088."

Start-Process $LocalUrl
