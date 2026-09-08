# GeoPackage raster qualification: two-computer experiment

Status: experimental evidence, not a storage adapter or approved compatibility
profile. Start with the [completed return analysis](FINAL-FINDINGS.md), with
[open-source findings](OPEN-SOURCE-FINDINGS.md) retained as the first-phase record.
The tested creation route is not lossless; existing folder/GeoTIFF decisions remain
in force. The procedures below preserve the original experiment for reproduction.

## What travels in this repository

- `payload/`: exact GeoTIFF controls, candidate GeoPackages, numerical oracles and
  a versioned manifest with SHA-256 hashes. About 14 MB; no Git LFS required.
  Locally generated GeoPackage statistics sidecars are ignored, not part of the
  portable payload; standalone relocation is tested without them.
- `results/open-*/`: compact observations and runtime records from this computer.
- `arcgis.py` and `run-arcgis.ps1`: licensed on-network runner; needs ArcGIS Pro
  Python (3.9+) and its bundled NumPy, **not Codex, R, QGIS or internet at runtime**.
- `inspect_return.py`: independent GDAL inspection when ArcGIS outputs return.

Four synthetic cases exercise Float32/metres, Float32/feet, signed Int16,
Float64 precision, negative/fractional values, valid zeros and internal/boundary
NoData. CRS codes are 26914 and 2276. These are artificial grids, not actual sites;
no real vertical datum or physical terrain validity is asserted.

Six complete retained rasters were extracted from fluvgeodata's Cole Creek
2006/2010/2016 GDBs. The manifest identifies the original layer names and source
file checksums. Source files were unchanged; extracted cells, masks, CRS and grid
were checked against the GDAL source reader. These inputs originate in the
public CC0 [fluvgeodata](https://github.com/FluvialGeomorph/fluvgeodata) repository.
Their vertical datum/units are not independently established by filenames.
This is not a whole-project conversion: other archived vectors/tables are outside
this raster experiment. The mixed-container case uses a synthetic vector only.

## On-network procedure: no agent required

1. After the originating commit is pushed, clone **FGDB** onto the licensed
   workstation (or pull it in an existing clean clone). Check out the same
   experiment revision; preserve the payload unchanged. A separate fluvgeodata
   clone is **not needed** to execute the supplied test payload.
2. Open ArcGIS Pro and establish the normal approved license/sign-in. Do not
   install packages, change production environments or enable extra extensions.
3. Open PowerShell at the FGDB repository root and run:

   ```powershell
   .\dev\experiments\geopackage-raster\run-arcgis.ps1 -RunId arcgis-pro-01
   ```

   For a non-default ArcGIS installation, add `-Propy 'actual/path/propy.bat'`.
   Run IDs must be new. Never delete a failing result to make a run look clean.
   A launcher/license error is an environment failure, not a format failure.
4. Read `results/arcgis-pro-01/completion.json` and `checks.json` in the experiment
   directory. Completion means all attempted routes were recorded, **not** that
   they passed. The Float64 GPKG candidate is intentionally absent because the
   open-source writer rejected it; its GeoTIFF control still exercises Esri's
   File GDB -> GeoPackage route. Missing-candidate errors are expected for that lane.
5. In ArcGIS Pro, use **disposable copies** of the test files to inspect discovery:
   can Catalog find numerical GPKG layers without entering a path manually?
   Can Identify show fractional/negative values and distinguish zero from NoData?
   Can a saved project reopen after moving the disposable folder? Record the
   exact case IDs, actions, failures and visible metadata in
   `results/arcgis-pro-01/operator-notes.md`. Do not infer success from symbology.
   Avoid screenshots containing unrelated agency material.
6. Close ArcGIS Pro and the Python process before staging data (release GDB locks).
   Review the **entire result directory**, including generated geodatabase metadata,
   for local paths or institution-restricted information. Use only these supplied
   public/synthetic inputs; no agency archives, credentials or private project data.
   Follow agency transfer policy before sending any results off-network.
7. Commit the completed result directory and operator notes, then push using the
   organization's normal authorized Git workflow. Inspect the staged file list:

   ```powershell
   git status --short
   git add dev/experiments/geopackage-raster/results/arcgis-pro-01
   git diff --cached --stat
   git commit -m "Record ArcGIS Pro raster interoperability experiment"
   git push
   ```

   Do not stage `scratch/`, `input-copy/`, locks or unrelated work. These are
   ignored. Result rasters and GDB files are needed for independent inspection.
   If a result is too large for the approved Git host, stop and arrange an approved
   artifact-transfer route; do not upload it elsewhere or discard it silently.

## What the ArcGIS runner does

For each case it tests the GeoTIFF control, reads the GDAL-created GPKG, exports
that GPKG to TIFF and File GDB, creates a File GDB raster from the TIFF, creates
an Esri GPKG from that File GDB, then copies the Esri GPKG back to File GDB.
All writes are under a new result directory. Inputs are copied first because
ArcGIS may generate statistics/auxiliary files on read. No Spatial Analyst license
is required for the selected conversion/array operations.

The array comparison uses two different NoData replacements to identify the
mask without confusing valid zeros with missing cells. ArcPy CRS equality is
recorded as provisional; returned WKT and raster files support independent review.
Band units and vertical interpretation are not certified by the ArcPy array pass.
The licensed runner was executed in returned run `arcgis-pro-01`; its provisional
CRS gate and string-path conversion limitations are analyzed in the final findings.
Record unexpected errors rather than improvising a silent conversion workaround.

## Return to this computer

Pull the reviewed ArcGIS commit. Keep its raw results unchanged. Run the
independent inspection with the same isolated open-source environment:

```powershell
$env:FG_PROJ_DATA = 'directory containing the qualified proj.db'
& "$env:LOCALAPPDATA/Programs/OSGeo4W/bin/python-qgis-ltr.bat" `
  dev/experiments/geopackage-raster/inspect_return.py --run arcgis-pro-01
```

The reviewer verifies payload identity and returned artifact checksums, then
compares every exported TIFF/GPKG/File GDB raster against the original oracle.
Commit the independent review and update the findings only after reconciling
ArcGIS observations with these results. A changed metadata field or unsupported
route is a finding, not permission to weaken the expected values.

For `arcgis-pro-01`, strict review stopped on one auxiliary-file hash discrepancy.
The separate `analyze_return.py --run arcgis-pro-01` generated `return-analysis.json`
with auxiliary metadata disabled, explicit integrity qualifications and WKT
reconciliation. It refuses to overwrite its output and does not replace strict
review or alter raw observations. See the final findings before interpreting it.

## Reproduce the open-source phase

No package download or installation occurs. Use a coherent GDAL/PROJ environment.
The workstation's OSGeo4W default PROJ database is incompatible with its library;
the qualified local invocation explicitly selects the database bundled with R's
sf package **for the subprocess only**. Runtime files record its hash/metadata.

```powershell
$rInstall = (Get-ItemProperty 'HKCU:\SOFTWARE\R-core\R').InstallPath
.\dev\experiments\geopackage-raster\run-open.ps1 -RunId open-ltr-repeat `
  -ProjData (Join-Path $rInstall 'library/sf/proj')
# Add -Qgis qgis to exercise the installed current QGIS instead of LTR.
$env:LC_ALL = 'C'; $env:LANG = 'C'
& (Join-Path $rInstall 'bin/x64/Rscript.exe') --vanilla `
  dev/experiments/geopackage-raster/r_readback.R `
  dev/experiments/geopackage-raster open-r-repeat
```

`--prepare` / `-PrepareFrom` is only for rebuilding a **new, separate experiment
copy without a payload directory**, using fluvgeodata `inst/extdata`. Never rebuild
the committed payload between machines; hashes and identical inputs are essential.

Python tests (in the OSGeo4W Python environment; no licensed runtime):

```powershell
python -m unittest discover -s dev/experiments/geopackage-raster -p "test_*.py"
```

The return-review tests also require GDAL and the same process-local
`FG_PROJ_DATA` setting described above. They simulate returned artifacts under
ignored scratch storage; they are not ArcGIS execution evidence.

## Interpretation boundaries

Exact valid-cell values and masks are required for storage translations. Grid
comparison permits only 32 scaled floating-point epsilons, reported explicitly;
it is not a scientific resampling tolerance. QGIS calculation is multiplication
by two against the independent array oracle, not a hydrological-method test.
Structural validation does not establish numerical fidelity or OGC certification.
Several clients share GDAL/PROJ; their agreement is not independent Esri evidence.
Unknown original metadata stays unknown. No new storage decision follows
automatically from a completed script.

API references: [GeoPackage GDAL driver](https://gdal.org/en/stable/drivers/raster/gpkg.html),
[RasterToNumPyArray](https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/rastertonumpyarray-function.htm),
[Add Raster to GeoPackage](https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/add-raster-to-geopackage.htm),
[Copy Raster](https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/copy-raster.htm).
