# ADR-0025: Reach–Survey–Event folders and external GeoTIFF terrain

- Status: accepted migration design; storage binding and adapters pending.
- Date: 2026-09-07
- Reaffirmed by the user: 2026-09-08 after review of the completed experiment.
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

## Qualification follow-up (2026-09-07)

The user subsequently authorized a [two-computer raster qualification experiment](../experiments/geopackage-raster/README.md)
to test whether a narrower GeoPackage analytical-raster profile could simplify
interoperability. [Open-source findings](../experiments/geopackage-raster/OPEN-SOURCE-FINDINGS.md)
are recorded; licensed ArcGIS execution and independent return-side review remain
pending. This investigation does not supersede the accepted folder design or
qualify a production write path. The folder-profile probe above remains separate.

## Returned evidence (2026-09-08)

[Completed analysis](../experiments/geopackage-raster/FINAL-FINDINGS.md) of ArcGIS
Pro 3.6 run `arcgis-pro-01` confirms numerical reading of nine supplied GeoPackages,
but its tested creation path converted all ten rasters to Byte image tiles with
changed values and NoData masks. This supports retaining this ADR, not a blanket
claim that Esri cannot read GeoPackage rasters. Provisional CRS false failures,
conversion-path errors and one auxiliary-file integrity discrepancy are explicitly
qualified in the analysis. No new production profile is accepted by this result.

The user accepted these findings and confirmed this storage decision. Continue
with GeoPackage vectors/tables, external GeoTIFF terrain and linked metadata in
event folders; do not pursue single-container equivalence as a migration gate.
The next contract work is the versioned folder manifest and its validation under
[the existing requirements](../schemas/local-project-folder-requirements.md).
Exact serialization, adapters and production qualification remain pending.
