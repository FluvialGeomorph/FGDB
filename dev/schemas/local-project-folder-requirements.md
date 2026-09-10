# Local project folder and raster metadata requirements

Status: accepted design requirements under ADR-0025; exact manifest schema,
filenames, serialization, binding identifier and APIs remain proposed/unimplemented.
This is not an extension to `FLUVGEO_NETWORK_GPKG_1`.

The initial [fluvgeo intake inventory](../../../fluvgeo/dev/schemas/terrain-intake-manifest.md)
now implements selected-file snapshot/inspection and report integration. Its local
case/artifact labels are not governed identities; it does not fulfill the complete
event manifest, shared-asset or cross-client requirements below. FGDB's binding and
ingestion contract remain pending; no enterprise schema is changed by that slice.

## Delivery boundary

The user-directed [two-branch migration architecture](../../../FG-architecture/dev/decisions/adr-0005-analyst-staged-archive-migration.md)
places these target deliveries under the **GPKG** branch. The separate **FileGDB**
branch is analyst-configured migration staging: selected clean copies from the
untouched archive plus reconstructed Study Area/Stream FileGDBs. The new FGDB
desktop/archive intake accepts the qualified GPKG representation, not raw or
staged FileGDBs. Conversion and enterprise acceptance remain separate operations.
The observed `FG-filedata` tree is a prototype, not the exact binding. Define
Study Area/Stream staging content, event placement/date precision, readiness
criteria and the source/target crosswalk before implementing a general converter.

The [legacy staging review draft](legacy-project-staging-contract.md) proposes
those source-side records and review gates, grounded in Copperas Creek. Its
filenames, catalog homes and physical binding are not yet accepted requirements.

Use a folder for each Reach–Survey–Event delivery, with vector/table GeoPackages,
external GeoTIFF rasters, machine-readable metadata and reviewable reports.
Maintain analogous intake folders before scientific identities are resolved.
Copy/validate the complete delivery, not just its GeoPackage. A zip may transport
it but does not change the logical contract or authorize unsafe extraction paths.

Study/Stream-scale source terrain may be shared by several events. Preserve its
actual extent and lineage in a declared project-level asset store; associate it
explicitly rather than clipping, copying, or guessing ownership merely to fit
the event hierarchy. Record shared dependencies in the delivery inventory.

## Metadata that must survive physical separation

| Area | Required content |
| --- | --- |
| Identity and linkage | Stable artifact ID and revision, role (source DEM, hydro-DEM, REM, etc.), owning/context identities or explicit unresolved intake case; association to the applicable terrain edition and derived products. |
| Location and integrity | Package-root-relative path, declared format/layer or band, size, checksum algorithm/value, required companions and shared dependencies; no workstation drive path as the only locator. |
| Spatial reference | Retained original CRS representation, interpreted horizontal CRS/authority where known, axis interpretation and horizontal units; separately identified vertical reference, vertical units and coordinate epoch where applicable. |
| Grid and values | Extent, dimensions, resolution, origin/geotransform, rotation if present, pixel interpretation, band roles, pixel type, scale/offset, NoData encoding and mask semantics. |
| Provenance | Source artifact references/checksums, survey date and precision, derivation/conditioning steps, parameters, software/driver versions, creation/compression options and approved transformations. |
| Evidence and review | What was observed, inferred, analyst-confirmed or unknown; validation result and tested clients, unresolved conflicts and acceptance recorded separately. |

GeoTIFF should carry its own georeferencing; separation from a GeoPackage does
not mean the raster must lose its CRS. The package metadata retains provenance,
meaning and links that clients may not expose. Preserve the source definition as
evidence and compare it semantically, not by WKT string equality alone.
Do not make GeoPackage metadata-extension tables or a client's private project
file the only copy of essential metadata; retain a portable, machine-readable
record with the delivery. GeoTIFF tags alone are not the complete study record.

Do not silently prefer a manifest, embedded tag or sidecar when they disagree.
Report the conflict and require a documented resolution before dependent work.
Test a GeoTIFF reopened without incidental workstation sidecars; if a companion
is genuinely necessary, declare, copy and checksum it. A world file alone is not
a CRS or provenance record. GDAL can prioritize auxiliary metadata over internal
GeoTIFF tags, which makes stale sidecars a concrete risk.
[GDAL georeferencing behavior](https://gdal.org/en/stable/drivers/raster/gtiff.html#georeferencing).

## Required qualification for the implementing workflow

- Validate path resolution within the declared root, unique identities and all
  referenced files before processing; detect missing, substituted and stale assets.
- Reopen the copied folder in a new location and resolve all declared links.
- Compare native grid, semantic CRS, vertical meaning, pixel type, values and
  NoData masks through intended R/GDAL, QGIS and ArcGIS clients. Record versions
  and read/write direction; a map that looks correct is not conformance evidence.
- Keep format conversion separate from reprojection, resampling, unit conversion
  and scientific conditioning. Require explicit approval/provenance for changes;
  do not silently reduce precision or use lossy imagery encoding for terrain.
- Preserve unknown metadata during inventory, but prevent claims of readiness
  for operations requiring that metadata. Never manufacture a datum or date.
- Stage new outputs, validate the entire referenced set, then publish its manifest
  as complete. Recover/flag partial writes rather than presenting partial success.
- Show artifact availability, associations, discrepancies and readiness in the
  Terrain Development report; use the same structured assessment for selective
  Shiny prompts. Completeness is not scientific acceptance or FGDB load approval.
