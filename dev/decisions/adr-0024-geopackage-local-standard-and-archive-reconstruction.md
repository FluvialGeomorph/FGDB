# ADR-0024: GeoPackage local storage and forensic archive preparation

- Status: direction accepted by the user; general migration adapters and the
  standardized directory contract are not yet implemented.
- Date: 2026-09-06
- Supersedes: ADR-0019's immediate File GDB local binding preference (items 7/9),
  not its object-relational scientific model.
- Complements: ADR-0015, ADR-0017 and ADR-0021 through ADR-0023.

**2026-09-07 refinement:** [ADR-0025](adr-0025-folder-deliverables-and-geotiff-terrain.md)
supersedes this record's terrain-container direction with external GeoTIFFs in
Reach–Survey–Event folders. The raster-GeoPackage experiments below are retained
as historical evidence, not the selected cross-client delivery profile.

## Context and decision

The user establishes two linked requirements:

1. The evolving Terrain Development report also guides **forensic reconstruction
   of archived analyses for FGDB loading**. An analyst other than the original
   maker must recover structural intent from surviving evidence, propose missing
   Study Area/Stream/Reach/Survey Event relationships and record their decisions.
2. **OGC GeoPackage is the target local project spatial-data storage standard**,
   replacing ESRI File GDB for new production and prepared archive data. Archive
   candidates must enter a standardized local directory structure and qualified
   GeoPackage bindings before they are eligible for the new FGDB loading path.

These are complementary uses of the same scientific preparation workflow, not
an opaque file conversion performed by the enterprise loader. Local work remains
useful without FGDB. Reports and supporting documents remain documents; this
decision concerns the geospatial data and their related project tables, including
terrain, rather than encoding HTML or ordinary documents as spatial layers.

Original archives remain preserved evidence. Migration creates separately
identified candidates; it does not rewrite originals or silently remove their
File GDB read compatibility. Do not require invented hierarchy merely to inventory
an archive: unresolved candidates need an intake location before they can be
assigned governed parent identities.

Observed source facts, proposed interpretations, supplied analyst confirmations,
rejected alternatives and unknowns must remain distinguishable. Confirmation of
an interpretation does not itself reconcile UUIDs, approve scientific repairs,
qualify a conversion or authorize an enterprise load. A directory/year/name is
evidence, not a foreign key. Preserve rationale and source references, especially
when the original analyst is unavailable.

The decision changes local storage direction, not FGDB's enterprise SDE/Feature
Service boundary or mosaic dataset management. Type and CRS conformance remain
governed by ADR-0021. Do not rewrite previous ADRs as if this direction had always
been the implemented binding.

## Historical evidence inspected

Verified in local fluvgeo history (commit messages and relevant code/test diffs):

| Date / commit | Observed change |
| --- | --- |
| 2022-11-07 / `5cf0264` | A slope/sinuosity fix addressed non-metre linear units. |
| 2022-11-15 / `c884327` | `arc2sp()` attempted Unicode cleanup of CRS WKT. |
| 2022-12-19 / `0164569` | It switched from an EPSG/WKID-derived CRS to source WKT and commented out that cleanup. |
| 2022-12-19 / `e5d09e1` | `sp2arc()` copied a retained feature's ArcGIS `shapeinfo` to preserve CRS. |
| 2022-12-21 / `61d2520` | Another revision targeted feature-dataset handling; the explicit `shape_info` write argument was commented out and tests changed again. |
| 2023-08 / `d755a60`, `9c9b270` | Changes moved CRS/unit handling toward `sf::st_crs()` and `units_gdal`. |
| 2025-01-04 / `e0446d1` | Raster-read tests added explicit EPSG assertions; the change was in tests, not a new reader implementation. |

Inference: metadata representation and unit assumptions across boundaries were
recurrent problems, not a single filename-format issue. The user's account of a
GeoPackage migration and rollback is accepted historical context, but this
inspection did **not** locate an explicit rollback commit. Message searches in
the local fluvgeo, fluvgeodata and Toolbox histories did not identify that event;
do not present the listed ArcGIS/CRS fixes as proof of the precise rollback cause.

## Conformance before migration acceptance

GeoPackage's open specification is a reason to standardize, not proof that every
adapter is lossless. OGC defines a gridded-coverage extension for terrain and a
WKT CRS extension. Current GDAL documentation describes Float32 TIFF coverage
tiles and separate NoData behavior; ordinary image tiles are not an equivalent
scientific DEM encoding. Sources: [OGC coverage guidance](https://www.geopackage.org/guidance/extensions/tiled_gridded_coverage_data.html),
[GDAL raster binding](https://gdal.org/en/stable/drivers/raster/gpkg.html),
[GDAL vector/CRS binding](https://gdal.org/en/stable/drivers/vector/gpkg.html).

Qualify each supported path with explicit source/destination types, creation
options and versions. Compare geometry dimensions/order, values/nulls, identity,
constraints, semantic CRS, horizontal and vertical references, units, raster
grid alignment, pixel values and NoData masks. Retain original CRS definitions.
String differences in WKT need interpretation; equal CRS labels alone are not
enough. Never relabel a CRS as a substitute for a required transformation.
Do not silently cast Float64 terrain to Float32 or infer feet/datum from a name.

Unknown source metadata must remain unknown after conversion. The qualification
must separate faithful preservation of an unknown from independent verification
of the scientific reference. Physical standardization does not manufacture lost
provenance or make periods scientifically comparable.

## First bounded experiment and its limits

Reproducer: `fluvgeo/dev/scripts/cole-creek-geopackage-probe.R`, run from fluvgeo
with a new output directory. It copies only each event's flowline and two retained
rasters from `y2006_R1.gdb`, `y2010_R1.gdb`, `y2016_R1.gdb`, not the whole archive.

Observed failures during development:

- A terra GeoPackage write path changed some NoData cells to zeros despite CRS
  and grid checks passing. Explicit sentinel selection did not resolve that path.
- Direct `sf::gdal_utils("translate")` from OpenFileGDB attempted additional
  dataset content and produced table/transaction warnings; a direct VRT translate
  exposed a multidimensional group rather than the desired raster.
- `terra::sds()` display names repeated the GDB basename for both rasters;
  explicit GDAL subdataset identifiers were required to distinguish layers.

The successful narrow path uses `terra::vrt()` to isolate the raster, then GDAL
translation to a new, single-raster GeoPackage with TIFF tiles. Flowlines have a
separate GeoPackage with the WKT CRS extension. No reprojection, resampling or
pixel-type cast is requested. Temporary VRTs are not delivery dependencies.

On R 4.6.0, sf 1.1-2, terra 1.9-46, GDAL 3.12.1, PROJ 9.7.1 and GEOS 3.14.1,
the final probe passed 51 assertions with no conversion warnings. Comparisons
include exact vector geometry/attributes, exact finite raster values and NoData
masks, pixel types, dimensions and resolution, and semantic CRS. Raster checks
also reopen a copy of the `.gpkg` alone, without sidecars. Extent comparison uses
an explicit experimental bound of 32 scaled double-precision machine epsilons;
the measured differences and tolerance are retained in `conformance.csv`, not
reported as bitwise-identical extents. This is a candidate tolerance for review,
not a newly approved universal scientific transform. Source checksums were
unchanged. Runtime and creation options are retained with the probe output.

Not established: general File GDB conversion, remaining feature layers, domains,
attachments, arbitrary datatypes/CRSs, true vertical references, licensed ArcGIS
round trips, enterprise loading, production-scale performance or a fully qualified
project storage profile. Failed experimental copies are not eligible inputs.

## Next boundary

The report now has a first reconstruction ledger and visual structure/time view;
these are report inputs, not a persisted hierarchy editor. Design and qualify the
project-context/intake GeoPackage relations and directory contract next, then
exercise a complete archived Reach–Survey Event dataset. Keep preparation,
conversion conformance, analyst decisions and FGDB load acceptance separate.
No archive-wide migration or customer deployment follows automatically from this ADR.
