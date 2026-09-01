# Stream Network Geodatabase schema

- Status: proposed exact first-slice schema
- Updated: 2026-09-01
- Governing decision: ADR-0019
- Scientific implementation owner: `fluvgeo`
- Database loading owner: `FGDB`

## Purpose

This schema stores a configured, time-specific Stream Network as feature
classes and related tables in a Study Area/Stream Geodatabase. R data frames
and `sf` objects use the same relation and field names. FGDB maps approved local
rows to closely corresponding enterprise SDE relations.

One editable geodatabase contains one active `stream_network_observation` and
one `stream_network` feature class. Separate geodatabases for other terrain
times reuse the same `stream_network_configuration_id` when they represent the
same intended Study Area/Stream configuration.

## Relation inventory

| Relation | Kind | Row meaning | Local | Enterprise |
|---|---|---|---:|---:|
| `stream_network_configuration` | table | One Study Area-owned definition of the Streams intended to participate in a connected or independently analyzed Stream Network. | required | required |
| `stream_network_configuration_stream` | table | One Stream participating in one configuration. | required | required |
| `stream_network_observation` | table | One time-specific realization of the configured Stream Network. | required | required |
| `stream_network` | polyline feature class | One directed topology segment in one Stream Network Observation. | required | required |
| `stream_network_source` | table | One source feature contributing evidence to one segment. | conditional | required when lineage exists |
| `stream_network_operation` | table | One applied operation that produced or classified a segment. | conditional | required when an operation occurred |
| `stream_network_review` | polyline feature class | One spatial proposal presented to an analyst and its decision. | required when proposals occur | local editing aid; accepted operations load through `stream_network_operation` |
| `stream_network_validation_run` | table | One execution of the Stream Network validator. | required | final accepted run referenced by enterprise load audit |
| `stream_network_validation_issue` | table | One issue found during a validation run and its disposition. | conditional | final accepted issues referenced by enterprise load audit |

Binding-managed `OBJECTID`, `GlobalID`, `Shape_Length`, and similar fields are
not scientific identifiers or foreign keys.

## Common rules

- Scientific identifiers are immutable UUIDs stored as Esri `GUID` locally and
  in SDE, and as canonical UUID text in open relational bindings.
- Timestamps are UTC. Actor fields store stable actor/process identifiers.
- Controlled codes are stored values, with file-geodatabase coded-value domains
  supplied as editing aids.
- All polyline geometry is valid, nonempty, 2D, and stored in the scientifically
  appropriate projected analysis CRS locally.
- File geodatabases do not enforce all relational constraints; `fluvgeo`
  validation and FGDB preflight enforce them before enterprise loading.

## `stream_network_configuration`

**One row means:** one durable analyst-defined configuration governing which
Stream or connected Streams are analyzed and compared together across terrain
times.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `stream_network_configuration_id` | UUID | no | Primary key; reused across terrain times for the same configuration. |
| `study_area_id` | UUID | no | FK to the owning Study Area. |
| `configuration_name` | text(255) | no | Human-readable name unique within Study Area after normalization. |
| `configuration_mode` | enum | no | `STREAM` or `STUDY_AREA_NETWORK`. |
| `description` | text(2000) | yes | Scientific purpose or extent qualification. |
| `created_at`, `created_by` | lifecycle | no | Creation provenance. |
| `modified_at`, `modified_by` | lifecycle | no | Current local modification provenance. |
| `lifecycle_status` | enum | no | `ACTIVE` or `RETIRED`. |

A `STREAM` configuration has exactly one membership. A `STUDY_AREA_NETWORK`
configuration has at least two memberships and one intentionally common
topology/stationing context.

## `stream_network_configuration_stream`

**One row means:** one governed Stream participating in one Stream Network
Configuration.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `stream_network_configuration_id` | UUID | no | FK to configuration. |
| `stream_id` | UUID | no | FK to Stream. |
| `stream_name` | text(255) | no | Reviewable display snapshot; not identity. |
| `membership_role` | enum | no | `SUBJECT` in the first schema version. |
| `created_at`, `created_by` | lifecycle | no | Membership provenance. |

Primary key: (`stream_network_configuration_id`, `stream_id`). Every Stream
belongs to the configuration's Study Area.

## `stream_network_observation`

**One row means:** one reviewed, time-specific Stream Network realization
supported by terrain evidence or reconstructed from governed Reach Flowlines.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `stream_network_observation_id` | UUID | no | Primary key. |
| `stream_network_configuration_id` | UUID | no | FK to configuration. |
| `observation_year` | short integer | no | Four-digit terrain-evidence year. |
| `observation_month` | short integer | yes | 1–12 when known. |
| `observation_day` | short integer | yes | Valid day; requires month. |
| `date_precision` | enum | no | `YEAR`, `MONTH`, or `DAY`. |
| `evidence_class` | enum | no | `DIRECT_TERRAIN_DERIVATION`, `SOURCE_NETWORK_RETAINED`, or `RECONSTRUCTED_FROM_REACH_FLOWLINES`. |
| `coverage_status` | enum | no | `FULL_CONFIGURATION`, `PARTIAL_CONFIGURATION`, `KNOWN_GAPS`, or `UNKNOWN_LEGACY`. |
| `source_terrain_id` | UUID | yes | Governed hydro DEM/terrain identity when available. |
| `source_terrain_label` | text(255) | yes | Reviewable nonidentity label. |
| `source_terrain_fingerprint` | text(64) | yes | Content hash when retained evidence permits it. |
| `derivation_method_id` | text(255) | no | Stable scientific method identifier. |
| `method_version` | text(64) | conditional | Required unless controlled legacy unknown. |
| `threshold_value` | double | conditional | Positive stream-initiation threshold when material. |
| `threshold_unit` | enum | conditional | Unit accompanying threshold. |
| `topology_tolerance` | double | no | Positive endpoint/snap tolerance used for this observation. |
| `topology_tolerance_unit` | enum | no | Same unit as the local horizontal CRS. |
| `native_horizontal_crs` | text(255) | conditional | Required for new work. |
| `native_vertical_datum` | text(255) | conditional | Required when terrain elevation is material. |
| `horizontal_unit` | enum | conditional | Required for new work. |
| `vertical_unit` | enum | conditional | Required with vertical datum. |
| `cell_size` | double | conditional | Positive terrain cell size for direct derivation. |
| `provenance_completeness` | enum | no | `COMPLETE`, `PARTIAL_LEGACY`, or `MINIMAL_LEGACY`. |
| `review_status` | enum | no | `DRAFT`, `READY_FOR_REVIEW`, `ACCEPTED`, or `REJECTED`. |
| `reviewed_at`, `reviewed_by` | lifecycle | conditional | Required for accepted/rejected observations. |
| `review_notes` | text(2000) | yes | Scientific qualification. |
| common lifecycle fields | lifecycle | no | Creation/modification/status provenance. |

Method-specific attributes that materially affect interpretation require
explicit schema fields in a versioned method-specific related table. A generic
unattached variable store is not part of this schema.

## `stream_network` feature class

**One row means:** one directed topology segment belonging to one Stream
Network Observation.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `stream_network_segment_id` | UUID | no | Primary scientific identity. |
| `stream_network_observation_id` | UUID | no | FK to observation; identical across the editable feature class. |
| `stream_id` | UUID | conditional | Required for accepted rows; Stream must participate in configuration. |
| `reach_id` | UUID | yes | Optional classified Reach belonging to `stream_id`. |
| `downstream_node_id` | UUID | conditional | Required for accepted rows. |
| `upstream_node_id` | UUID | conditional | Required for accepted rows. |
| `segment_role` | enum | no | `MAINSTEM`, `TRIBUTARY`, `CONNECTOR`, `ARTIFICIAL`, or `UNRESOLVED`. |
| `direction_status` | enum | no | `CONFIRMED` or `UNRESOLVED`. |
| `direction_method` | enum | conditional | `TERRAIN_ELEVATION`, `FLOW_ACCUMULATION`, `SOURCE_RETAINED`, `ANALYST_CONFIRMED`, or `LEGACY_UNKNOWN`. |
| `source_feature_key` | text(255) | yes | Traceability only; not identity. |
| `review_status` | enum | no | Row review state. |
| common lifecycle fields | lifecycle | no | Creation/modification/status provenance. |
| `Shape` | 2D polyline | no | Coordinate order is downstream to upstream. |

Segments split at retained confluences, Stream boundaries, Reach boundaries,
and explicit gap boundaries. Shared node IDs require coincident endpoints
within the observation's topology tolerance. Accepted first-version networks
cannot contain unexplained cycles, duplicate edges, unresolved direction, or
unclassified Stream membership.

## `stream_network_source`

**One row means:** one source feature contributing evidence to one Stream
Network segment.

Fields: `stream_network_source_id` PK, `stream_network_segment_id` FK,
`source_object_type`, nullable governed `source_object_id`, nullable
`source_dataset_name`, conditional `source_feature_key`, `relation_code`, and
`geometry_modified`.

Reconstructed segments require at least one governed Flowline source. Local
paths and `OBJECTID` values may be traceability labels but never relationship
keys.

## `stream_network_operation`

**One row means:** one applied, ordered operation that produced or classified a
Stream Network segment.

Fields: `stream_network_operation_id` PK, `stream_network_segment_id` FK,
nullable `stream_network_source_id` FK, `operation_sequence`, `operation_code`,
nullable `tolerance_value`/`tolerance_unit`, nullable `target_node_id`, nullable
classification Stream/Reach IDs, `operation_notes`, `performed_at`, and
`performed_by`.

The pair (`stream_network_segment_id`, `operation_sequence`) is unique.

## `stream_network_review` feature class

**One row means:** one spatial repair or classification result presented to an
analyst for an explicit decision.

Fields: `stream_network_review_id` PK, `stream_network_observation_id` FK,
nullable source segment/source IDs, `operation_code`, `reason_code`, proposed
tolerance/node/Stream/Reach values, `decision` (`PENDING`, `ACCEPT`, or
`REJECT`), decision actor/time/notes, and proposed 2D `Shape`.

The source geometry remains visible in `stream_network` or the selected source
feature class. Accepted proposals create or update governed segment rows and
create `stream_network_operation` lineage. Rejected proposals remain local QA
evidence and do not become governed Stream Network geometry.

## Validation tables

`stream_network_validation_run` contains one row per validation execution:
run ID, observation ID, validation level, result, model/validator versions,
actor, and time.

`stream_network_validation_issue` contains one row per issue: issue ID, run ID,
issue code, severity, affected relation/object ID, related relation/object ID,
message, analyst disposition, disposition actor/time, and notes.

An accepted observation requires a current acceptance-level run with no
unresolved error. FGDB reruns the same `fluvgeo` validation immediately before
staging and records the load validation in its enterprise audit relations.

## Local-to-enterprise mapping

The local and enterprise schemas preserve the same scientific table names,
keys, row meanings, controlled codes, and relationships. FGDB may add:

- enterprise Collection ownership and publication state;
- SDE/ArcGIS managed fields and indexes;
- load job, reconciliation, authorization, and rollback audit tables;
- approved transformation fields required for enterprise storage; and
- service-oriented views that do not change authoritative relations.

FGDB reads the analyst-approved Study Area/Stream Geodatabase directly,
validates its relations, transforms geometry according to the governed CRS
registry, stages all affected rows, and commits the complete create/correction
unit atomically.

## Physical conformance

`fluvgeo` tests use direct producer outputs from `fluvgeodata` and verify that R
data frames/`sf`, file-geodatabase tables/feature classes, and open relational
bindings preserve the same scientific values and geometry. Invalid-state tests
make temporary R modifications to direct outputs beside the relevant
`testthat` assertions.

## Remaining schema questions

1. Identify any derivation-method attributes beyond threshold, tolerance, CRS,
   units, and cell size required in the first schema version.
2. Decide which accepted review/validation records require long-term enterprise
   retention versus remaining local QA evidence.
