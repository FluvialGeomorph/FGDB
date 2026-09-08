# GeoPackage raster interoperability: completed return analysis

Reviewed 2026-09-08. Evidence: FGDB commit `9181522`, run `arcgis-pro-01`,
ArcGIS Pro 3.6 build 59527, Python 3.13.7. Experiment baseline: `8f89841`.

## Outcome

**Do not treat GeoPackage as an interchangeable analytical-raster replacement
for File GDB across these workflows. Retain the accepted event-folder design:
GeoPackage vectors/tables, GeoTIFF terrain and explicitly linked metadata.**

This is not a finding that ArcGIS cannot read GeoPackage rasters. It read all nine
supplied numerical GeoPackages with exact cells, masks, grids and pixel types.
However, its tested creation tool produced 8-bit image tiles instead of preserving
the analytical terrain. The experiment therefore distinguishes useful read support
from a reliable bidirectional scientific storage workflow.

Analysis of the returned run is complete. It does not certify every possible
ArcGIS configuration, the complete folder profile, or whole-File-GDB equivalence.
No production adapter, schema or accepted storage decision was changed.

**Subsequent human decision, 2026-09-08:** the user accepted these findings and
reaffirmed the folder/GeoTIFF design in
[ADR-0025](../../decisions/adr-0025-folder-deliverables-and-geotiff-terrain.md).
The experimental observations below remain unchanged; implementation of the
versioned folder binding is the next development step, not completed by this report.

## Verified results

The original [ArcGIS checks](results/arcgis-pro-01/checks.json) remain unchanged:
0 PASS, 39 FAIL, 31 ERROR. Those totals alone are misleading. The separate
[return analysis](results/arcgis-pro-01/return-analysis.json) reconciles recorded
CRS definitions and independently reads all 20 exported datasets with GDAL 3.13.3
/ PROJ 9.5.0, with auxiliary metadata disabled.

| Path | Evidence-based interpretation |
| --- | --- |
| GeoTIFF control → ArcGIS | All 10 preserve exact valid values, masks, grids, types and band count. Returned horizontal CRS definitions are semantically equivalent. |
| GDAL numerical GeoPackage → ArcGIS array | All 9 available candidates preserve the same properties. Float64 candidate was never created and is not an ArcGIS read-support test. |
| GeoTIFF → File GDB | All 10 returned rasters independently preserve exact cells, masks, grids, types and horizontal CRS, including Float64. GDAL does not expose the explicit band units on 3 synthetic cases. |
| File GDB → ArcGIS GeoPackage (`AddRasterToGeoPackage`, `TILED`) | All 10 become single-band Byte rasters in PNG tiles. All 10 change valid values and lose the expected NoData masks. Grids and horizontal CRS survive. |
| GeoPackage → TIFF / File GDB using `CopyRaster` | All 30 attempts fail parameter validation (`000732`) for the supplied string paths, including ArcGIS-created GeoPackages. This path was not qualified. |

The independent export comparisons yield **7 PASS and 13 FAIL**: seven File GDB
rasters pass every checked property, three fail only explicit band-unit exposure,
and all ten ArcGIS-created GeoPackages fail numerical/type/mask preservation.
An empty source unit on a retained raster is not proof of correct physical units.

### The creation failure is scientifically consequential

All ten ArcGIS GeoPackages declare `gpkg_contents.data_type = tiles`, contain PNG
tiles, and lack the gridded-coverage extension in their recorded extension lists.
GDAL reads their pixels as Byte; it finds no NoData cells in any of them. For example,
the synthetic metre control ranges from -6 to 6.125, while its generated GeoPackage
ranges from 0 to 255. The Cole Creek `cole_2006_0` control ranges approximately
1015.290–1082.347; its generated GeoPackage ranges 126–255. These are not minor
floating-point differences or alternative CRS spellings.

**Inference:** the tested tool produces a display-oriented raster pyramid, not a
lossless analytical terrain copy. This is consistent with Esri's description of
[Add Raster to GeoPackage](https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/add-raster-to-geopackage.htm)
as loading a raster pyramid. The precise rendering/scaling operation was not isolated;
do not generalize this result to every possible Esri raster writer or option.

### The provisional CRS test was not a reliable horizontal-CRS gate

Every one of the 39 completed ArcPy inspections reported `crs_arcpy_equal = false`,
including the unchanged GeoTIFF controls. All 39 recorded horizontal CRS definitions
compare equivalent using GDAL/PROJ after parsing the WKT portion of Esri's export.
The remaining semicolon-delimited coordinate-domain/precision settings are not
silently claimed equivalent. Returned dataset CRS checks agree with the WKT review.

Thus 29 original FAIL rows have no demonstrated numerical/grid/type/horizontal-CRS
failure. Their original statuses are preserved, not retroactively rewritten.
Esri [documents SpatialReference equality](https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/spatialreference.htm),
so the finding is not that the operator is unsupported: this experiment's comparison
was too broad to serve as its scientific horizontal-CRS acceptance gate. The exact
ArcPy property responsible remains unisolated without the licensed runtime.

## Integrity exception and handling

All 29 original payload hashes match. Of 790 returned artifact checksums, **789
match**. The exception is `cole_2006_0/arcgis_created.gpkg.aux.xml`; its containing
GeoPackage matches exactly. The strict `inspect_return.py` correctly stops at this
discrepancy and has not been weakened. No strict-success review was produced.

The discrepant sidecar is already present in the returned Git commit, not a local
review edit. Its cause is unknown; it contains auxiliary metadata and statistics.
The supplementary [analysis script](analyze_return.py) reports expected/observed
hashes, disables GDAL auxiliary metadata use, and reads the primary datasets without
consulting that sidecar. It verifies all recorded artifacts are unchanged after
inspection. This is diagnostic evidence with an explicit integrity qualification,
not acceptance of the altered sidecar. Nine other ArcGIS GeoPackages independently
demonstrate the same numerical failure without any associated hash discrepancy.

## Unknowns and limits

- No operator notes were included: Catalog discovery, interactive Identify and
  saved-project relocation remain undocumented, not silently passed.
- `CopyRaster` rejected string paths which `arcpy.Raster` could read. A Raster
  object or explicit layer may behave differently, but neither was tested. These
  errors cannot establish a blanket inability to export numerical GeoPackages.
- The cause of the sidecar change and exact ArcPy equality difference remain unknown.
- GDAL's missing File GDB band-unit exposure does not establish whether equivalent
  information exists elsewhere in Esri metadata. Original vertical references also
  remain unknown; no datum transformation or vertical-accuracy claim is made.
- The open-source Float64 writer limitation and QGIS export unit losses remain
  documented in the [first-phase findings](OPEN-SOURCE-FINDINGS.md).

## Recommended next development step

Proceed with the already accepted folder profile, not another broad interchangeability
investigation: implement and test the event manifest linking GeoPackage vectors/tables,
GeoTIFF rasters, their CRS/units/vertical-reference provenance, checksums and relative
paths. Test relocation and missing/conflicting assets. This is a recommendation,
not implementation or approval of a new binding in this analysis.

Keep numerical GeoPackage reading as a potentially useful qualified capability;
do not require it for ArcGIS interoperability. A narrowly targeted licensed follow-up
using Raster/layer inputs could resolve `CopyRaster` behavior if that capability
becomes necessary. It is not required to reject the tested lossy creation route or
to continue the folder-based migration.
