param(
  [Parameter(Mandatory=$true)][string]$RunId,
  [string]$Propy = 'C:/Program Files/ArcGIS/Pro/bin/Python/Scripts/propy.bat'
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Propy)) {
  throw 'ArcGIS Pro Python launcher not found. Supply -Propy with its actual installed path.'
}
& $Propy (Join-Path $PSScriptRoot 'arcgis.py') --run $RunId
if ($LASTEXITCODE -ne 0) { throw "Runner incomplete (exit $LASTEXITCODE). Preserve results; use a new run ID after resolving the error." }
Write-Output 'Review completion.json and checks.json. A completed run can contain scientific failures.'
