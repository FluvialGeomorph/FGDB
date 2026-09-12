# WESM for archived terrain-source discovery

## Finding and evidence boundary (2026-09-12)

**Verified:** WESM includes older collections and can support forensic source
discovery now. It is not a complete historical catalog or proof that an archived
FG DEM used a particular collection. No FG source association or metadata assertion
was changed during this review. This is research evidence and a proposed workflow,
not an implemented discovery tool.

Read the public [WESM CSV](https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/metadata/WESM.csv)
in memory on 2026-09-12: 3,278 records. Examples include `WA_PSLC_2000`
(-1694; collection 2000-12-01 to 2001-01-30) and `NE_LINCOLN_2003`
(-1480; 2003-11-01 to 2003-12-01). These examples establish historical coverage,
not its earliest valid date, completeness or FG archive match rate. Dictionary
date ranges are not evidence of continuous coverage back to their lower bounds.

**Verified candidate, not verified lineage:** `NE_NIROC_PAPIOCO_2010`, work-unit
ID -1481, has collection dates 2010-04-16 to 2010-04-28. A live read-only query of
the [USGS lidar index layer 24](https://index.nationalmap.gov/arcgis/rest/services/3DEPElevationIndex/MapServer/24)
with `where=workunit = 'NE_NIROC_PAPIOCO_2010'`, `returnGeometry=false`
returned that record, `vert_crs=6360`, `geoid=GEOID09`, a legacy LPC location and
a metadata location; `sourcedem_link` was empty. Candidate selection used its
name/date, not a tested footprint intersection or source-file comparison. Do not
copy these reference values onto the FG DEM: derivation may have transformed them.
The linked point-cloud files and project metadata were not inspected in this probe.

## Access options

- **Verified download:** [USGS spatial metadata documentation](https://www.usgs.gov/3d-elevation-program/3dep-spatial-metadata)
  publishes GeoPackage and CSV, with near-daily updates as projects are published.
- **Verified service:** [3DEP Elevation Index](https://index.nationalmap.gov/arcgis/rest/services/3DEPElevationIndex/MapServer)
  exposes queryable lidar and source-DEM index layers. Layer 24 includes WESM-style
  work-unit/project IDs, dates, CRS, geoid, product status and links, and supports
  JSON/GeoJSON and pagination. The query above succeeded without an ArcGIS license.
  This is an available discovery interface, not proof of complete field/record
  parity, synchronized refresh or immutable history relative to WESM downloads.
- **Proposed FG approach:** support a dated local GeoPackage snapshot for offline
  spatial searching and reproducible review; optionally use the service for online
  discovery. Pin the consulted records and retrieval context. Do not make an online
  service mandatory for archive staging or local analysis.

## Historical gaps and later enrichment

The [WESM dictionary](https://www.usgs.gov/ngp-standards-and-specifications/wesm-data-dictionary-general-attributes)
explicitly accommodates legacy data and missing source DEMs. Product update fields
do not supply a complete pre-March-2023 revision history. Work-unit reports beginning
in July 2020 are not a lower acquisition-date cutoff for the catalog.

**Unknown:** no commitment or timetable to recover every missing historical
collection was found in the reviewed official documentation. Near-daily publication
does not promise retrospective completeness. Coverage of Cole Creek 2006/2010/2016
or the wider FG archive remains unverified. A name-only search cannot establish
absence, and no catalog match does not mean a source never existed.

For gaps, use the [US Interagency Elevation Inventory](https://coast.noaa.gov/digitalcoast/tools/inventory.html),
state/local/provider catalogs and retained project evidence as complementary sources.
USIEI is a multi-agency inventory with a map service and downloadable GeoPackage;
its inclusion does not itself prove exact source availability or FG lineage.

**Proposed workflow:** find candidates by location and acquisition period; compare
source names, metadata, processing history, grid/CRS and any retained input records;
ask the analyst only for unresolved choices. Keep candidate, analyst-confirmed,
rejected and unresolved interpretations distinct, with supporting evidence. These
are review concepts, not newly approved database enums or confidence scores.

Give the local source record its own stable identity even when no external ID is
known. Later evidence may add or revise an external link through attributed review,
retaining the previous assertion and catalog snapshot. Catalog updates must not
automatically replace accepted lineage, change Survey Event dates or reprocess DEMs.
One derivative may use several collections. Preserve the distinction between
identifying a collection, identifying the exact input edition and reconstructing
the processing that produced the retained artifact.

## Completed footprint and metadata test (2026-09-12)

**Verified local evidence:** at fluvgeodata commit
`25b562d9cbfca4f841aad097e246981322466f5f`, the `GDB_Items.Documentation`
record for `y2010_R1.gdb / dem_2010_ft_50` records copying
`LittlePapillionCreek_2010_ft`, clipping to `dem_2010_ft_1000`, then clipping to
`dem_2010_ft_50`. The five retained process entries do not establish the acquisition
provider or reconstruct the earlier DEM-production steps. Local paths/accounts are
omitted. The retained flowline and DEM use NAD83 / UTM zone 14N.

**Verified spatial rejection of the published work unit:** its service footprint
does not intersect Cole Creek R1 or the retained DEM rectangle. The footprint has
a self-intersection; a repaired in-memory diagnostic copy remains about 12,777 m
from the flowline. The original `NE_PapioCo_footprint2.shp` in the linked public
metadata directory is valid and independently confirms non-overlap, about 12,817 m
away. The small difference between footprints does not affect that conclusion.
No source geometry was overwritten. Rectangle containment here tests catalog
location, not DEM quality, valid-cell occupancy or completeness of a masked raster.

**Verified report content, not FG lineage:** the public
[NIROC LiDAR Mapping Report](https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/metadata/legacy/NE_NIROC-PAPIOCO_2010/Nebraska_Iowa_Regional_Orthophotography_Consortium__NIROC__LiDAR_Mapping_Report.pdf)
describes Merrick's broader NIROC project around Omaha/Lincoln. Page 3 gives
2010-04-16 through 2010-04-28 acquisition; page 24 declares Nebraska State Plane,
NAD83, NAVD88/Geoid09 and USFeet. Page 39 describes a four-foot DTM from ground
points and breaklines. Pages 3, 24 and 39 were visually checked after extraction.
These are source-project declarations, not proof that the retained FG raster used
that project or preserved its vertical reference. The broader NIROC project remains
a possible lead; work unit -1481 is not a supported spatial association.

**Verified alternate spatial candidate:** a read-only layer-24 query intersecting
the DEM's geographic bounding envelope
`-96.037062194,41.260749618,-96.030348246,41.278300154` (EPSG:4326)
returned `NE_Eastern_UA_2016`, work-unit 59026. Its valid footprint covers both
the flowline and DEM rectangle. Dates are 2016-12-08 through 2017-02-03;
catalog fields report `vert_crs=6360` and `geoid=GEOID12B`. This establishes an
available spatial candidate, not the source of the retained 2016 FG DEM, an
additional independent survey, or comparability with other FG terrain. Its metadata
has not yet been inspected. No other collection was returned by this query; this
does not exhaust source-DEM, USIEI, state, local or restricted holdings.

The comparison is reproducible with
[the read-only R probe](../../../fluvgeo/dev/scripts/cole-creek-source-footprint-probe.R):
run from the workspace root and supply the public-download directory. It compares
both 2010 footprints and the spatial response with retained FG geometry, reports
source validity separately from diagnostic repair, and checks all source FileGDB
file hashes before/after. The rerun passed with sources unchanged (GDAL 3.12.1,
GEOS 3.14.1, PROJ 9.7.1). It is an investigation script, not a production adapter.

Local public downloads are retained, untracked, under
`fluvgeo/dev/outputs/terrain-development/papio-source-v1/`. SHA-256 snapshots:

- `niroc-mapping-report.pdf`: `D85BC1C38BF4CC953DFBEDB987A8903B6EB7F7D716104BDCBC57B09A5C0AFA27`
- `papio-2010.geojson`: `E3BC8CAE7616F734408E67564761AB5864C3E2350ED4836E0B4AA748A16A85C5`
- `cole-creek-spatial-candidates.geojson`: `3E771D9D320AE5E035F11E3AD599B1D59B9FE90AB46085FABF961D167DB9A553`

To reacquire, use the linked metadata directory for the PDF and four shapefile
components. Query layer 24 with `f=geojson`, `outSR=4326`, `returnGeometry=true`
and the work-unit predicate above for the 2010 footprint. For spatial candidates,
use `where=1=1`, the envelope above, `geometryType=esriGeometryEnvelope`,
`inSR=4326` and `spatialRel=esriSpatialRelIntersects`. Retain work-unit/ID,
collection dates, vertical CRS/geoid and metadata-link fields. Remote responses
may change; the probe reports the supplied snapshot rather than asserting timeless
candidate counts. No LiDAR payloads were downloaded or FG metadata populated.

## Next bounded step

Use these findings to ground the accepted
[survey-opportunity report](../features/survey-discovery-opportunities.md).
Keep the 2010 lineage and 2004/2006 ambiguity unresolved until additional provider
or analyst evidence is available. Evaluate historical match coverage by actual
project, not a national age cutoff. A broader-project report is not a substitute
for a defensible acquisition/asset association.
Follow the [scientific traceability roadmap](../goals/scientific-traceability-roadmap.md)
for shared-backend ownership and provenance requirements. This document does not
select a new client library or change the enterprise retention model.
