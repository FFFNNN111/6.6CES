# -*- coding: utf-8 -*-
$ErrorActionPreference = "Stop"

$AppDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ProjectDir = (Resolve-Path (Join-Path $AppDir "..")).Path
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$BackendFile = (Get-ChildItem -Path $AppDir -Recurse -Filter "proxy.py" -File | Select-Object -First 1).FullName
$Port = "8088"
$HealthUrl = "http://127.0.0.1:$Port/api/health"

$env:PORT = $Port
$env:DEEPSEEK_URL = "https://api.deepseek.com"
$env:DEEPSEEK_RETRIES = "5"
$env:DEEPSEEK_TIMEOUT = "25"

function Test-CesHealth {
  try {
    $resp = Invoke-RestMethod -Uri $HealthUrl -TimeoutSec 3
    return [bool]$resp.ok
  } catch {
    return $false
  }
}

if (-not (Test-Path $PythonExe)) {
  exit 1
}

if (-not $BackendFile -or -not (Test-Path $BackendFile)) {
  exit 1
}

if (Test-CesHealth) {
  exit 0
}

Start-Process -FilePath $PythonExe -ArgumentList @($BackendFile) -WorkingDirectory (Split-Path -Parent $BackendFile) -WindowStyle Hidden

for ($i = 0; $i -lt 60; $i++) {
  if (Test-CesHealth) {
    exit 0
  }
  Start-Sleep -Seconds 1
}

exit 1
