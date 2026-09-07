# ADR-0025: Reach–Survey–Event folders and external GeoTIFF terrain

- Status: accepted migration design; storage binding and adapters pending.
- Date: 2026-09-07
- Refines ADR-0024: supersedes GeoPackage as the target terrain payload container,
  not its vector/table choice, archive reconstruction or preservation decisions.

Adopt the user-directed [cross-repository decision and evidence](../../../FG-architecture/dev/decisions/adr-0004-folder-based-spatial-deliverables.md):
each Reach–Survey–Event delivery is a folder of GeoPackage vector/table content,
GeoTIFF raster files, metadata and related documents. Do not require Esri to
consume numerical terrain stored in a GeoPackage. Some Esri raster-tile support
exists; reliable analytical coverage exchange and metadata preservation cannot
be assumed from it. No prediction about future vendor support is a dependency.

The folder is the unit of local integrity checking and delivery, not an automatic
FGDB acceptance unit. A `.gpkg` alone does not supply the event's full evidence.
Use the [folder/metadata requirements](../schemas/local-project-folder-requirements.md)
for the next binding design. This reinforces REQ-RAS-001's GeoTIFF default and
does not alter enterprise raster retention or mosaic administration.

Earlier Cole Creek raster-GeoPackage experiments remain historical qualification
evidence for GDAL paths only. Their outputs do not establish this folder profile
or licensed ArcGIS interoperability. The next storage probe must test external
GeoTIFF payloads, metadata links, folder relocation and missing/conflicting assets.
