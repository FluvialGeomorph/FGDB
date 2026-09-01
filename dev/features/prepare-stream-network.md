# Prepare Stream Network capability

- Status: revised producer API proposal
- Updated: 2026-09-01
- Scientific owner: `fluvgeo`
- Clients: ArcGIS Pro, Shiny, direct R, future QGIS
- Local database: Study Area/Stream Geodatabase
- Enterprise loader: `FGDB`

## Outcome

An analyst or application supplies terrain-derived linework, a retained legacy
`stream_network`, or governed Reach Flowlines. `fluvgeo` creates and maintains
the Stream Network feature class and its related object-relational tables. All
candidate repairs, validation findings, and analyst decisions are reviewable as
feature-class or table rows before the Stream Network Observation is accepted.

FGDB access is not required to derive, review, accept, or retain the Stream
Network locally.

## Ownership

`fluvgeo` owns every operation that creates, changes, classifies, relates,
measures, or scientifically validates terrain-derived features. FGDB begins at
the enterprise boundary: it checks enterprise identity and authorization,
stages approved local relations, performs controlled create/correction loads,
records load audit, and publishes enterprise content.

Client wrappers own parameter collection, layer selection, editing interaction,
progress, and display. They do not implement separate topology or database
logic.

## R and geodatabase representation

Every public function consumes or returns a data frame/tibble or `sf` object.
Column names correspond directly to
`dev/schemas/stream-network-geodatabase-schema.md`. When one operation produces
several relations, its R return value is a strictly named list of those data
frames/`sf` objects.

The same relations are written to the Study Area/Stream Geodatabase. There is
no separate serialization model between R, the analyst's geodatabase, and the
enterprise loader.

## `fluvgeo` producer functions

### Create the configuration tables

```r
create_stream_network_configuration(
  stream_network_configuration_id,
  study_area_id,
  configuration_name,
  configuration_mode = c("STREAM", "STUDY_AREA_NETWORK"),
  streams,
  description = NA_character_,
  actor,
  created_at = Sys.time()
)
```

Returns `stream_network_configuration` and
`stream_network_configuration_stream` data frames. `streams` contains governed
`stream_id` and reviewable `stream_name` columns. The function checks UUIDs,
membership uniqueness, and one-versus-multiple Stream cardinality without
performing enterprise identity matching.

### Create the time-specific observation table

```r
create_stream_network_observation(
  stream_network_observation_id,
  stream_network_configuration_id,
  observation_year,
  observation_month = NA_integer_,
  observation_day = NA_integer_,
  evidence_class,
  coverage_status,
  source_terrain_id = NA_character_,
  source_terrain_label = NA_character_,
  source_terrain_fingerprint = NA_character_,
  derivation_method_id,
  method_version = NA_character_,
  threshold_value = NA_real_,
  threshold_unit = NA_character_,
  topology_tolerance,
  topology_tolerance_unit,
  native_horizontal_crs,
  native_vertical_datum = NA_character_,
  horizontal_unit,
  vertical_unit = NA_character_,
  cell_size = NA_real_,
  provenance_completeness,
  actor,
  created_at = Sys.time()
)
```

Returns one `stream_network_observation` row, derives date precision, and
checks all evidence-class conditional fields.

### Prepare retained or newly edited features

```r
prepare_stream_network_from_features(
  stream_network,
  configuration,
  configuration_streams,
  observation,
  actor,
  review_mode = c("CREATE_REVIEW_FEATURES", "VALIDATE_ONLY")
)
```

The input is projected `sf` linework. The function checks geometry and CRS,
explodes multipart lines, identifies confluence/Stream/Reach splits, evaluates
direction and endpoint coincidence, and assigns candidate segment/node UUIDs.
It returns:

- candidate `stream_network` segments;
- `stream_network_source` lineage rows;
- proposed `stream_network_review` features; and
- validation run/issue tables.

The source data is never modified in place.

### Reconstruct from Reach Flowlines

```r
reconstruct_stream_network_from_flowlines(
  flowlines,
  configuration,
  configuration_streams,
  observation,
  actor,
  review_mode = c("CREATE_REVIEW_FEATURES", "VALIDATE_ONLY")
)
```

`flowlines` is projected `sf` with governed `flowline_id`, `survey_event_id`,
`stream_id`, `reach_id`, and temporal evidence. The function rejects an
unexplained mixture of incompatible terrain times, preserves source lineage,
and creates review features for proposed splitting, snapping, reversal,
assembly, or classification. It never smooths source Flowlines or represents
the result as the unavailable historical network.

### Future terrain derivation

```r
derive_stream_network_from_terrain(
  terrain,
  configuration,
  configuration_streams,
  observation,
  outlet,
  initiation_threshold,
  threshold_unit,
  analysis_corridor = NULL,
  actor
)
```

This is the open-source terrain-to-network boundary. Method-specific algorithms
require separate scientific specifications. The function produces candidate
segments and review feature classes; it never automatically accepts them.

### Apply analyst decisions

```r
apply_stream_network_reviews(
  stream_network,
  review_features,
  actor
)
```

Every review feature has `PENDING`, `ACCEPT`, or `REJECT` status. The function
applies accepted decisions atomically to copies of the data, writes applied
operations to `stream_network_operation`, preserves rejected rows as local QA
evidence, regenerates identities when segment grain changes, and reruns
scientific validation. Required pending/rejected repairs remain blocking.

### Validate and accept

```r
validate_stream_network(
  configuration,
  configuration_streams,
  observation,
  stream_network,
  sources = NULL,
  operations = NULL,
  level = c("WORKING", "ACCEPTANCE")
)

accept_stream_network(
  geodatabase,
  reviewer,
  review_notes = NA_character_
)
```

Validation returns `stream_network_validation_run` and
`stream_network_validation_issue` tables. Acceptance writes the final review
status into the observation and segment rows only when no blocking issue or
pending required review remains.

### Write and read the local geodatabase

```r
write_stream_network_geodatabase(
  relations,
  dsn,
  format = c("FILE_GEODATABASE", "GEOPACKAGE"),
  mode = c("CREATE", "UPDATE"),
  overwrite = FALSE
)

read_stream_network_geodatabase(dsn, validate = TRUE)
```

Every member of `relations` is written as its corresponding feature class or
table. Updates preserve stable IDs and enforce the one-active-observation local
editing rule. Round-trip tests compare the resulting relations to their source
R data frames/`sf` objects.

## FGDB loader functions

```r
inspect_stream_network_geodatabase(dsn)

validate_stream_network_load(
  dsn,
  connection,
  operation = c("CREATE_NEW_OBSERVATION", "REPLACE_CORRECTED_OBSERVATION")
)

reconcile_stream_network_identities(dsn, connection, decisions)

load_stream_network_geodatabase(
  dsn,
  connection,
  operation = c("CREATE_NEW_OBSERVATION", "REPLACE_CORRECTED_OBSERVATION")
)
```

FGDB verifies schema/version, calls `fluvgeo::validate_stream_network()`, checks
governed hierarchy identities, requires explicit reconciliation, transforms
geometry according to the governed CRS registry, stages the corresponding
relations, and commits the complete operation atomically. It never splits,
snaps, orients, classifies, reconstructs, or recalibrates geometry.

## Analyst workflow

```text
Create/select Stream Network Configuration tables
  -> create a time-specific Stream Network Observation row
  -> derive, retain, or reconstruct candidate stream_network features
  -> inspect proposed feature-class/table rows
  -> record accept/reject decisions
  -> apply accepted operations and validate
  -> accept the Stream Network Observation in the local geodatabase
  -> optionally invoke FGDB to validate, stage, and load those relations
```

## Implementation sequence

1. Accept or revise the exact Stream Network Geodatabase schema.
2. Add direct representative Stream Geodatabases to `fluvgeodata` where the
   existing evidence set does not cover a required case.
3. Implement constructors and retained-feature normalization in `fluvgeo`.
4. Implement review feature classes, topology validation, and acceptance.
5. Implement reviewed Flowline reconstruction and lineage.
6. Implement file-geodatabase and open relational read/write conformance.
7. Implement FGDB schema inspection, enterprise identity checks, staging, and
   transactional load.
8. Specify automated terrain-to-stream-network derivation separately.
