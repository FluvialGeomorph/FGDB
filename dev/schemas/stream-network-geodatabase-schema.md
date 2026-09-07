# Stream Network Geodatabase schema

- Status: accepted first-slice schema
- Updated: 2026-09-05
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
| `stream_network_node` | point feature class | One exact endpoint location in one Observation, shared by incident segments. | when connectivity assigned | loader support pending |
| `stream_network_connection` | table | One downstream segment relationship, or one observed outlet row. | when connectivity assigned | loader support pending |
| `stream_network_source` | table | One source feature contributing evidence to one segment. | conditional | required when lineage exists |
| `stream_network_operation` | table | One applied operation that produced or classified a segment. | conditional | required when an operation occurred |
| `stream_network_direction_evidence` | table | One candidate's DEM endpoint assessment and optional applied-operation link. | required when DEM direction is assessed | method evidence; loader support pending |
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

## Candidate node and connectivity extension (2026-09-05)

fluvgeo's `connect_stream_network()` assigns node UUIDs and derives all
downstream relationships with hydroloom. Preparation enables it explicitly with
`connect = TRUE` after normalization, optional consolidation, DEM orientation,
and geometry assessment. The prior seven-table return is unchanged by default;
the option appends the following two relations. These are working candidate
outputs, not an enterprise migration or an acceptance result.

### `stream_network_node`

Fields: `node_id` UUID primary key, `stream_network_observation_id` UUID FK,
`in_degree`/`out_degree` nonnegative integers, `node_topology` code, and POINT
`Shape` in the segment CRS. Segment `upstream_node_id`/`downstream_node_id`
reference this table in the same Observation. Shared IDs require exact endpoint
coincidence for this method; it does not use the tolerance to snap or cluster.
Existing segment node UUIDs are reused only when consistent with endpoint
sharing: multiple IDs at one location, or one ID at multiple locations, fail.
New UUIDs identify previously unidentified candidate endpoints. They do not
establish physical node identity across Observations or independent reruns that
discard the node FKs. Store the returned nodes and segment FKs together.

Counts use downstream flow: in-degree is the count arriving from upstream;
out-degree is the count leaving downstream. `node_topology` is derived from
those counts: `UPSTREAM_BOUNDARY` (in = 0), `DOWNSTREAM_BOUNDARY` (out = 0),
`CONTINUATION` (1/1), `CONFLUENCE` (>1/1), `DIVERGENCE` (1/>1), or
`COMPLEX_JUNCTION` (>1/>1). Boundary labels describe the observed extent,
not physical headwaters or a river mouth. No segment role is inferred.

### `stream_network_connection`

Fields: `stream_network_observation_id` UUID FK,
`stream_network_segment_id` upstream segment UUID FK,
nullable `downstream_segment_id` downstream segment UUID FK, and `node_id`
UUID FK. Both segments belong to the same Observation. `node_id` equals the
upstream segment's downstream node and, when present, the downstream segment's
upstream node. Each unique segment/downstream-segment pair occurs once. Each
observed outlet has exactly one row with a null downstream segment; no sentinel
ID is persisted. Diversions repeat the upstream segment ID for every connection.
This is not a unique-feature table. Row order follows hydroloom's hydrologic
ordering, but positions are not persistent identities.

The implementation reverses only a computational copy for sfnetworks' directed
graph, and supplies its node relationships to hydroloom's non-dendritic
`add_toids()` and `sort_network()`. All storage geometry and source relationships
are preserved. No custom hydrologic relationship algorithm is introduced in FGDB.

### Assignment and deferral

Every segment must have confirmed direction. Ambiguous geometry or directed
cycles block node/connectivity assignment. Preparation also blocks assignment
for endpoint near misses inside its existing observation tolerance. It returns
empty typed relations and one linked `CONNECTIVITY_DIRECTION_UNRESOLVED`,
`CONNECTIVITY_GEOMETRY_UNRESOLVED`, or `CONNECTIVITY_DIRECTED_CYCLE` finding.
Unexpected dependency/input errors propagate rather than masquerading as review.
There is no partial graph assignment. VALIDATE_ONLY always returns empty
node/connection tables. Disconnected components, multiple outlets, and directed
acyclic diversions are representable, not automatically scientifically accepted.

Successful preparation records one `ASSIGN_NETWORK_NODES` operation per segment
after existing operations (sequence 3 after consolidation and direction, 2 after
direction only). It records method `EXACT_ENDPOINT_CONNECTIVITY_1` and dependency
versions, actor, and UTC time. Target/tolerance/classification fields are null;
multi-source operations have null source FK. Assignment alone does not set
`geometry_modified`. `SEGMENT_REVIEW_REQUIRED` remains for role and acceptance
review; its message no longer requests already assigned node identities.

## `stream_network_source`

**One row means:** one source feature contributing evidence to one Stream
Network segment.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `stream_network_source_id` | UUID | no | Primary key. |
| `stream_network_segment_id` | UUID | no | FK to the governed segment. |
| `source_object_type` | enum | no | Controlled source-feature class, including retained Stream Network and governed Flowline. |
| `source_object_id` | UUID | yes | Governed source identity when one exists. |
| `source_dataset_name` | text(255) | yes | Reviewable source feature-class name. |
| `source_feature_key` | text(255) | conditional | Source-stable feature key such as legacy `arcid`; not governed identity. |
| `source_from_node_key` | text(255) | yes | Retained source `from_node` value when present. |
| `source_to_node_key` | text(255) | yes | Retained source `to_node` value when present. |
| `source_class_code` | text(255) | yes | Retained source classification such as legacy `grid_code`. |
| `source_reach_name` | text(255) | yes | Retained legacy `ReachName` display value; not identity. |
| `relation_code` | enum | no | How the source supports the governed segment. |
| `geometry_modified` | boolean | no | Whether governed geometry differs from the source geometry. |

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

The role-classification extension adds nullable `segment_role` text to this
table. `CLASSIFY_SEGMENT_ROLE` operations carry the supplied MAINSTEM, TRIBUTARY,
CONNECTOR, or ARTIFICIAL value in that field; other operation codes leave it
null. Each changed classification appends the next sequence for that segment,
with explicit actor, UTC time, and decision notes. Source FK is null for a
multi-source segment. Reapplying the same role is a no-op. Geometry, source
lineage, inspection decisions, and previous validation records are unchanged.
An accepted segment must be explicitly reopened before its role is changed.

The pair (`stream_network_segment_id`, `operation_sequence`) is unique.

### Logical-link consolidation (2026-09-05)

fluvgeo preparation optionally concatenates exact-endpoint degree-two
continuations before direction assessment (`consolidate = TRUE`). Stream/Reach
identity transitions and explicit protected endpoints are retained. This uses
sfnetworks; FGDB does not reimplement the graph transformation. See fluvgeo's
`dev/decisions/ADR-0001-network-processing-libraries.md` for the accepted
sfnetworks/hydroloom ownership decision.

Each merged link receives a new candidate segment UUID and one sequence-1
`CONSOLIDATE_SEGMENTS` operation. All normalized source-part rows retain their
source relationship UUIDs and source attributes, reference the resulting link,
and set `geometry_modified = TRUE`. A merged segment's scalar
`source_feature_key` is null; original keys remain in `stream_network_source`.
Whole-link operations/reviews use a null source FK when several sources
contribute. Single-segment issues then have null related relation/object fields;
their affected segment FK retrieves every source. Pair findings retain their
second-segment relationship. No field is added to the relational tables.

Consolidation records method `LOGICAL_LINKS_1` and library versions in notes.
Its tolerance fields record the near-miss protection distance, not snapping.
Direction follows at sequence 2 for merged links, sequence 1 otherwise.
Without a DEM only consolidation operations are recorded. VALIDATE_ONLY
preserves raw normalized segmentation and records no applied operations.
Logical-link direction evidence samples the merged geometry before orientation;
raw endpoint coverage is checked first so missing source values cannot be hidden.

### Automatic DEM direction operations (2026-09-05)

Preparation with a source DEM records `REVERSE_DIRECTION` for reversed lines
and `CONFIRM_DIRECTION` for lines already ordered downstream to upstream.
Each supported candidate receives one direction operation for this preparation
run (sequence 1 unless preceded by consolidation); direction preserves the
candidate segment ID. `performed_by` is the caller's actor/process,
not an invented human reviewer. Tolerance, target-node, and classification
`stream_id`/`reach_id` fields are null for this method. `performed_at` is UTC.
Reversed sources set `geometry_modified = TRUE`; existing true values survive.

`stream_network_direction_evidence` is a method-specific table with one row per
candidate assessed against the supplied DEM. Its fields are:

- `stream_network_segment_id`: primary key and segment FK for this preparation;
- nullable `stream_network_operation_id`: FK when the result was applied;
- `start_elevation`, `end_elevation`: original endpoint values, nullable doubles;
- `start_sample_status`, `end_sample_status`: `AVAILABLE`,
  `OUTSIDE_DEM_EXTENT`, or `DEM_NODATA` (the generic primitive also uses
  `NOT_SAMPLED` for unsupported multipart geometry);
- nullable `elevation_unit`: observation vertical unit, unknown when not supplied;
- `action`: `KEEP`, `REVERSE`, or `UNRESOLVED`;
- `reason_code`: `DEM_ENDPOINT_ORDER`, `EQUAL_ENDPOINT_ELEVATION`,
  `ENDPOINT_OUTSIDE_DEM`, or `ENDPOINT_DEM_NODATA` (outside-extent takes
  precedence when both coverage failures occur; the generic primitive also reports
  `MULTIPART_GEOMETRY`, which network normalization handles first);
- `method`: `DEM_ENDPOINTS_1`;
- `dem_band`: sampled single-band name; and
- nullable `dem_source`: raster file reference, not a content fingerprint.

The caller supplies the appropriate source DEM; spatial agreement alone does
not verify its historical derivation provenance. Values retain the DEM's native
vertical units, which the caller must describe correctly in the observation.
This endpoint rule does not imply a monotonic profile or accepted topology.
No threshold, interpolation, or profile-based fallback is applied.

Without a DEM direction evidence is empty (consolidation can still record
operations). VALIDATE_ONLY populates evidence but
leaves operation links null and does not apply direction changes. Automatic
direction assignment does not accept the observation or resolve node/role checks.
Automatic preparation requires finite elevation coverage at every candidate
endpoint; it errors before returning corrections if any coverage is missing.
VALIDATE_ONLY instead reports `DEM_COVERAGE_INCOMPLETE` issues with the endpoint
diagnostics above. Incomplete input coverage is not a direction repair task.
Equal finite values still produce `DIRECTION_UNRESOLVED`.

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

### Initial retained-source inspection representation (2026-09-04)

The implemented preparation slice also emits inspection requests, identified by
`operation_code = INSPECT`. `Shape` is the unchanged affected candidate segment.
These rows carry `stream_network_segment_id`, `stream_network_source_id`, and
`stream_network_validation_issue_id`; the issue's related-object fields identify
the other segment for pair findings. `reason_code` equals the issue code.

Reserved proposal fields are `proposed_tolerance_value` (double),
`proposed_tolerance_unit` (text), `proposed_node_id`, `proposed_stream_id`, and
`proposed_reach_id` (UUID text); all are null for INSPECT. Decision fields are
`decision`, `decision_at` (UTC timestamp), `decision_by`, and `decision_notes`.
Generated decisions are PENDING. An INSPECT row does not specify a repair, and
accepting it cannot authorize geometry changes or Network Observation acceptance.

Initial reason codes are `DIRECTION_UNRESOLVED`, `DUPLICATE_GEOMETRY`,
`SELF_INTERSECTION`, `CLOSED_SEGMENT`, `INTERIOR_INTERSECTION`, and
`ENDPOINT_NEAR_MISS`. Findings are unresolved blocking issues, not automatic
proof of invalid hydrology; crossing and gap interpretation belongs to review.
After successful DEM direction assignment, `SEGMENT_REVIEW_REQUIRED` replaces
the direction finding to retain the unresolved node/role checks.

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

### Implemented retained-network validation (2026-09-05)

`fluvgeo::validate_stream_network()` implements read-only WORKING/ACCEPTANCE
checks for SOURCE_NETWORK_RETAINED. Each call returns a new run and current
issue table, with PASS or REVIEW_REQUIRED; it neither replaces old evidence
nor changes observation/segment review status. PASS alone is not acceptance
or load authorization. Acceptance is a separate explicit transition.

Checks reuse constructor metadata rules, shared preparation geometry checks,
and hydroloom-backed connectivity. Current node locations/counts/labels and all
connection pairs (including outlet nulls and diversion rows) must match the
recomputed result. Checks also cover Configuration/Observation/Stream membership,
optional supplied Reach-Stream mappings, explicit roles/direction methods,
per-segment source coverage, source/operation FKs, operation order/provenance,
and agreement of the latest explicit role operation with the current role.
Unknown Reach membership is reported, not inferred or looked up in enterprise.
Exact matching CRS display names from geodatabase reads are supported alongside
reparsable CRS metadata; other disagreement is blocking.

ACCEPTANCE additionally requires current INSPECT decisions covering every
candidate, all ACCEPT, with unique review UUIDs and explicit reviewer/time/notes.
Accepted inspection geometry must match current geometry, and its timestamp
must not predate the candidate's modified time, including role changes.
Pending/rejected/foreign/stale reviews block; accepting INSPECT does not apply
repairs. Rejected/retired observations or candidates need an explicit reopen.
Observation `review_notes` must qualify partial/unknown coverage, incomplete
provenance, or multiple observed outlets. These notes do not upgrade provenance
or imply complete geographic coverage. No acknowledgement is invented by the
validator or the role-classification function.

This is bounded local validation, not verification of historical DEM identity,
whole-line downhill profiles, undeclared Stream/Reach splits, complete original
source retention, scientific correctness of supplied roles, or enterprise
hierarchy membership. Those remain analyst/loader responsibilities. Malformed
required tables/UUIDs raise input errors; assessed inconsistencies return
blocking ERROR issues. Earlier PASS flags cannot override current findings.

## Local acceptance and GeoPackage binding (2026-09-05)

`fluvgeo::accept_stream_network()` consumes the named relation list. It requires
explicit inspection decisions and reruns ACCEPTANCE validation; no decisions or
scientific qualifications are inferred. Only DRAFT/READY_FOR_REVIEW observations
can transition. Success appends the passing run, marks Observation and segments
ACCEPTED, and records observation reviewer/time/notes plus modification provenance.
Segment `modified_at`/`modified_by` remain the provenance of the inspected
scientific state; changing review status alone does not invalidate inspections.
Acceptance cannot predate inspections, operations, or current modifications.
Failure exposes current findings and appended history in a structured error;
input relations and disk files remain untouched. Prior issues are historical
evidence, not silently marked resolved. The new current run assesses readiness.

The initial disk binding supports only new `.gpkg` files, with one Configuration
and one Observation. Every supplied relation is an ordinary spatial layer or
attribute table. UUIDs remain canonical text. Binding-managed FIDs do not become
scientific identifiers. `fluvgeo_network_fields` records binding version
`FLUVGEO_NETWORK_GPKG_1`, relation, field, position, kind, and geometry_type
(POINT/LINESTRING or NONE for scalar fields). Supported kinds are
character, integer, double, logical, date, datetime, and geometry. Timestamps are
UTC ISO-8601 text with nine fractional digits (restored as POSIXct); dates are
ISO date text; booleans are nullable 0/1 (restored as logical). This avoids driver
timestamp precision loss. Nonfinite values other than NA, unsupported R classes,
and reserved/ambiguous field names fail. Incidental R vector names and data-frame
row names are not persisted identities. Nonspatial reads return tibbles.

Container checks always verify supported relations, primary keys and evidence
references, including historical issue/run and review/issue links. Drafts may
retain scientific findings. Accepted-state save/read additionally reruns current
ACCEPTANCE checks and requires the recorded acceptance run and reviewer/time;
later recorded modifications/inspections invalidate that acceptance. These are
consistency checks, not a cryptographic signature or tamper-proof audit.
Default reads attach fresh validation results without replacing saved history;
`validate = FALSE` is an inspection escape hatch, never acceptance authority.
Reach-classified bundles still require supplied Reach-Stream mappings.

Writes stage a sibling file, compare exact field values/types and geometry/CRS
after reload, then publish with a non-replacing hard link. Existing destinations
are never modified. Unsupported hard-link filesystems fail safely; callers must
use a supported local filesystem. The implementation adds no R dependencies and
uses sf/GDAL for both spatial and attribute tables. It is not an in-place GIS
editing transaction. FILE_GEODATABASE, UPDATE/overwrite, explicit reopening, and
FGDB enterprise loading remain deferred. The file-geodatabase GUID/domain rules
above remain the target contract, not a claim about this open binding.

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

## Deferred schema refinements

These refinements do not block the accepted first implementation slice:

1. Add explicitly modeled derivation-method attributes when direct producer
   evidence demonstrates that threshold, tolerance, CRS, units, and cell size
   are insufficient.
2. Decide which accepted review and validation records require long-term
   enterprise retention when the enterprise load-audit contract is specified.

Direct legacy evidence supporting this schema is cataloged in
`dev/schemas/stream-network-source-evidence.md`.
