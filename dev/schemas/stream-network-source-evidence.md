# Stream Network source-evidence audit

- Status: current implementation evidence
- Audited: 2026-09-01
- Source: direct file-geodatabase outputs retained by `fluvgeodata`

## Purpose

This audit identifies which real FluvialGeomorph outputs can drive the first
`fluvgeo` Stream Network implementation. It does not create substitute test
data. Tests consume these direct outputs and compare the resulting data frames,
`sf` features, geodatabase tables, and feature classes to the accepted Stream
Network Geodatabase schema.

## Retained Stream Network evidence

| Geodatabase | `stream_network` rows | Legacy fields | Geometry | CRS | Case supported |
|---|---:|---|---|---|---|
| `AntelopeCreek_2013.gdb` | 1 | `arcid`, `grid_code`, `from_node`, `to_node`, `ReachName` | nonempty, valid multipart polyline | EPSG:26914 | single retained network feature with source topology attributes |
| `testing_data.gdb` | 99 | `arcid`, `grid_code`, `from_node`, `to_node`, `ReachName` | nonempty, valid multipart polylines | EPSG:26915 | multi-segment topology; 99 distinct source feature keys and no duplicate node pairs or self-loops |
| `y2006_R1.gdb` | 1 | `ReachName` | nonempty, valid multipart polyline | EPSG:26914 | incomplete legacy provenance with no retained source node keys |

All three geodatabases also contain a `flowline` feature class. GDAL reports
the Esri polyline features as `MULTILINESTRING`; each audited row currently has
one line part. The new normalization operation must nevertheless handle true
multipart source rows explicitly.

## Flowline-only reconstruction evidence

| Geodatabase | `flowline` rows | Geometry | CRS | Case supported |
|---|---:|---|---|---|
| `AntelopeCreek_2017.gdb` | 1 | nonempty multipart polyline | EPSG:26914 | missing retained Stream Network |
| `y2010_R1.gdb` | 1 | nonempty multipart polyline | EPSG:26914 | missing retained Stream Network |
| `y2016_R1.gdb` | 1 | nonempty multipart polyline | EPSG:26914 | missing retained Stream Network |

These files support the later, explicitly qualified reconstruction path. They
do not support claiming that a reconstructed feature is the unavailable
historical Stream Network.

## Legacy-to-governed interpretation

| Legacy value | Governed treatment |
|---|---|
| `arcid` | `stream_network_source.source_feature_key`; never scientific identity |
| `from_node`, `to_node` | source-node keys on `stream_network_source`; evidence for topology review, not governed node UUIDs |
| `grid_code` | `stream_network_source.source_class_code` |
| `ReachName` | `stream_network_source.source_reach_name`; reviewable label requiring explicit Stream/Reach identity reconciliation |
| `OBJECTID`, `Shape_Length` | storage-managed values; neither identity nor relationship keys |
| source geometry and CRS | retained as lineage evidence and normalized only through an explicit scientific operation |

The audit therefore grounds every retained legacy value in a named source
feature relationship. It does not introduce a generic attribute store.

## Coverage decision

No additional data are required before implementing configuration and
observation constructors, retained-feature normalization, or initial
validation in `fluvgeo`. The existing evidence covers:

- single-feature and multi-segment retained networks;
- complete and incomplete legacy topology attributes;
- Flowline-only legacy projects;
- distinct projected CRSs; and
- source labels that cannot be treated as governed identities.

The current workspace contains no separate surviving Site/Stream Geodatabase
and no direct output containing the newly accepted relations. Add evidence to
`fluvgeodata` only when a real surviving Stream Geodatabase is located or a
normal producer workflow creates the new relations. Do not manufacture a
replacement geodatabase merely to satisfy tests.

## First implementation sequence

Implementation proceeds in these independently verifiable steps:

1. **Implemented 2026-09-01:** construct and validate
   `stream_network_configuration` and `stream_network_configuration_stream`
   data frames.
2. **Implemented 2026-09-01:** construct and validate one
   `stream_network_observation` row.
3. **Implemented 2026-09-03:** normalize a retained legacy `stream_network`
   `sf` object into candidate governed segments plus `stream_network_source`
   rows;
4. **Implemented 2026-09-03:** require a separate per-source-feature mapping of
   governed Stream and optional Reach identities rather than inferring them
   from legacy names;
5. **Implemented 2026-09-03:** preserve legacy source attributes according to
   the table above and explicitly handle missing attributes; and
6. **Implemented 2026-09-03:** return working validation-run and
   validation-issue tables that keep direction, nodes, and segment role
   unresolved pending later review.

Initial retained-source assessment and linked pending INSPECT features were
implemented on 2026-09-04. Tests use the 99-row retained network and controlled
in-memory edits of its geometry to exercise duplicates, joins, gaps, and interior
intersections. The 2026-09-05 coverage investigation corrected the initial DEM
test pairing: the retained `dem_1m.tif` does not cover the full 99-row network.
The earlier statement that all 53 unresolved cases lacked elevations was wrong.

Verified containing-cell sampling results are:

| Segment outcome | Count |
| --- | ---: |
| At least one endpoint outside the DEM extent | 46 |
| Additional segments with an in-extent NoData endpoint | 4 |
| Both endpoints available but equal | 3 |
| Direction supported (13 KEEP, 33 REVERSE) | 46 |

Both inputs use EPSG:26915. Network northings span 4704420.6–4707430.2 m;
DEM northings span 4705024.8–4706911.8 m: the network extends about 604 m south
and 518 m north of this raster. The three equal cases (legacy `arcid` 1126,
1268, 1278) are sub-metre segments whose endpoints share one 1 m raster cell.
Equal values are therefore a resolution limitation, not missing elevations.
The cause of the in-extent NoData cells is not established.

The full pair is now a negative coverage test. Positive preparation tests use
an explicitly selected 49-segment subset with both endpoint values available;
this is not evidence of successful preparation of the entire original network.
Tests also cover repeat-run stability and controlled flat/missing DEM values.
The original derivation DEM has not been found in `fluvgeodata`. The user
confirmed that it may need recovery from archives and should then be retained
in `fluvgeodata` with provenance for a complete-network test. The user is not
currently connected to the agency file system containing those archives and
directed that recovery and the data-package update be deferred. Exact source
identity remains unknown; a modern replacement DEM would not verify historical
derivation. Continue with the available coverage and subset evidence meanwhile.
Full topology validation, actionable repair proposals, analyst review application,
Flowline reconstruction, geodatabase writing, and enterprise loading remain later.
