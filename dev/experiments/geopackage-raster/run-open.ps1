param(
  [Parameter(Mandatory=$true)][string]$RunId,
  [string]$OSGeoRoot = "$env:LOCALAPPDATA/Programs/OSGeo4W",
  [ValidateSet('qgis-ltr','qgis')][string]$Qgis = 'qgis-ltr',
  [Parameter(Mandatory=$true)][string]$ProjData,
  [string]$PrepareFrom
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath (Join-Path $ProjData 'proj.db'))) { throw 'PROJ database directory missing' }
$oldProj = $env:FG_PROJ_DATA
try {
  $env:FG_PROJ_DATA = (Resolve-Path -LiteralPath $ProjData).Path
  $launcher = Join-Path $OSGeoRoot "bin/python-$Qgis.bat"
  $runArguments = @((Join-Path $PSScriptRoot 'open_source.py'), '--run', $RunId)
  if ($PrepareFrom) { $runArguments += @('--prepare', (Resolve-Path -LiteralPath $PrepareFrom).Path) }
  & $launcher @runArguments
  if ($LASTEXITCODE -ne 0) { throw "Experiment runner failed: $LASTEXITCODE" }
} finally { $env:FG_PROJ_DATA = $oldProj }
