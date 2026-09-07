# GeoPackage raster qualification: open-source findings

Date: 2026-09-07. Evidence class: executed experimental implementation evidence,
not an accepted storage profile. Owner: FGDB. Scope: analytical raster exchange,
not whole-File-Geodatabase equivalence.

## Conclusion

The tested Float32 and signed Int16 numerical GeoPackages are useful candidates
for the licensed ArcGIS experiment. All nine successfully created candidates
preserved the tested cells, NoData masks, grids and CRS in the open-source reads.
Two boundaries prevent claiming unrestricted interchangeability: the selected
writer rejected Float64, and QGIS export lost explicit band units. The existing
folder/GeoTIFF migration design remains in force.

## Verified observations

The portable payload contains four synthetic controls and six full retained Cole
Creek rasters, approximately 14 MB. Its [manifest](payload/manifest.json) records
source hashes, extraction checks, numerical oracles, grid/CRS/type expectations,
creation options and the Float64 creation error. No source archive was changed.
Git attributes preserve checksummed payload/results bytes across platforms.

Harness verification: seven automated tests passed (numerical/mask corruption,
grid shift, path containment, exact simulated return, overwrite refusal, altered
artifact refusal and incomplete-run refusal). Python syntax and both PowerShell
launchers were checked. Simulated returns are not licensed ArcGIS evidence.
A fresh checkout from the Git index with Windows line-ending conversion enabled
preserved all 29 payload hashes and all three runtime/manifest identities.

| Executed lane | PASS | FAIL | ERROR | Evidence |
| --- | ---: | ---: | ---: | --- |
| QGIS LTR 3.44.14 + GDAL 3.13.3 | 72 | 2 | 7 | [Checks](results/open-ltr-verified/checks.json), [runtime](results/open-ltr-verified/runtime.json) |
| QGIS 4.2.2 + GDAL 3.13.3 | 72 | 2 | 7 | [Checks](results/open-current-verified/checks.json), [runtime](results/open-current-verified/runtime.json) |
| R 4.6.0, terra 1.9.46, sf 1.1.2, GDAL 3.12.1 | 9 | 0 | 1 | [Checks](results/open-r-final/checks.json), [runtime](results/open-r-final/runtime.json) |

Counts are route observations, not independent datasets or statistical estimates.
The QGIS lanes share GDAL/PROJ libraries. R uses another installed GDAL version
but is still not an independent Esri implementation.

- **Numerical preservation:** nine candidates passed GDAL reading, translation
  back to GeoTIFF, native QGIS block reading and QGIS raster calculator multiplication
  by two. All valid cells and NoData masks were compared, not just statistics or
  visual appearance. All ten GeoTIFF controls passed.
- **Metadata loss:** both QGIS versions' tested `QgsRasterFileWriter` export path
  lost explicit `m` and `ft` band units on the Float32 synthetic fixtures. Their
  cells, grid, masks, type and horizontal CRS passed. This describes the tested
  export path, not every possible QGIS export configuration.
- **Unsupported representation:** GDAL rejected the Float64 GeoPackage creation
  with the selected options. Its absent candidate explains all seven ERROR rows
  in each QGIS/GDAL lane and the one R ERROR, not seven unrelated defects.
  Its GeoTIFF/oracle remain available for ArcGIS's own creation routes.
- **Container behavior:** nine candidates passed GDAL's GeoPackage structural
  checker and relocation without sidecars. An additional mixed-container test
  appended two numerical rasters and a synthetic line layer, preserved the raster
  data, resolved named QGIS raster layers, and verified vector attributes, SQLite
  integrity and foreign keys. This is not a full FGDB schema test.
- **Environment boundary:** the default OSGeo4W PROJ database was incompatible
  with its installed library. Tested subprocesses explicitly used sf's database;
  runtime records include its SHA-256 and metadata. No installation or global
  configuration was changed. Results qualify this recorded combination, not the
  broken default environment.

The payload uses GeoPackage 1.3, TIFF tiles for floating-point coverage and PNG
for integer coverage, with no requested resampling or pixel cast. Grid comparisons
allow only 32 scaled double-precision epsilons, not a scientific shift tolerance.
The [GDAL driver documentation](https://gdal.org/en/stable/drivers/raster/gpkg.html)
describes numerical coverage representations. Structural checks are not OGC
certification or proof of scientific fidelity.

## Inferred implications, not accepted changes

- A useful interoperability profile will likely require allowed pixel types and
  metadata checks, rather than treating `.gpkg` as one uniform capability.
- Horizontal CRS preservation alone cannot preserve terrain meaning: band units
  and vertical reference need separate checks.
- These results justify licensed testing; they do not establish ArcGIS support
  for the numerical gridded coverages supplied here.

## Unknown / deferred

ArcGIS reading, numerical fidelity, writing, File GDB round trips, Catalog discovery
and saved-project relocation remain **unexecuted**. Its runner has only been
statically checked here. Manual review supplements array comparisons; successful
display is not numerical acceptance.

Original Cole Creek vertical datum and units are not independently established.
Synthetic feet/metre cases test preservation, not datum transformation. Rotated
grids, arbitrary non-default scale/offset, multiband rasters, large-terrain performance,
all pyramid levels, concurrency, attachments, domains, relationships and complete
event-container equivalence are not qualified.

## Authorized next phase

The user approved committing evidence here, running and committing licensed tests
on the on-network workstation without Codex, then returning for independent review.
Follow the [standalone handoff](README.md). The ArcGIS runner attempts seven routes
per case and retains failures and exports; it does not alter production workflows.
Esri's documented [Add Raster to GeoPackage](https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/add-raster-to-geopackage.htm)
path is tested with `TILED`. Documentation is not evidence of lossless numerical
support. Any revised storage decision requires review of returned files, not merely
a completed execution.
