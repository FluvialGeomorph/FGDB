# Local analysis package and platform bindings

- Status: draft logical model; exact first-slice binding in `network-package-v0.1.md`
- Updated: 2026-08-29
- Governing decisions: ADR-0015 and ADR-0016

## Design answer

The historical Stream Geodatabase is a good ArcGIS desktop location for
network-scope scientific metadata. It is already the workspace where analysts
derive and edit the synthetic network, classify Streams and Reaches, establish
topology, choose a mouth, and develop common stationing.

The `.gdb` format is not the canonical cross-platform contract. It is one
physical binding of a platform-neutral **local analysis package** defined by
`fluvgeo` scientific data contracts and the FGDB exchange profile.

## Local ownership by analytical scale

| Local workspace | Scientific content authored there |
|---|---|
| Network workspace (historical Stream Geodatabase family) | Network Scope metadata; one time-specific Network Observation per editable geodatabase; segment geometry and topology; Stream/Reach classifications; mouth; reusable paths; longitudinal frame definitions; package manifest. |
| Reach–Survey Event workspace | Hydro DEM, Cutlines, Flowline and points, Cross Sections and later derived features; event-specific calibration results and provenance; package manifest entries. |

Stable UUIDs relate records across workspaces. Filesystem paths, geodatabase
`OBJECTID`s, and feature-class names are locators or aliases, not relationship
keys. The package/export operation inventories the referenced local workspaces
and produces a self-consistent submission manifest.

For one independently processed Stream, the historical term **Stream
Geodatabase** remains accurate. For a connected Study Area network containing
several Streams, the same physical role is more precisely a **Study Area
Network Geodatabase**. Both implement the logical Network Workspace owned by
one Network Scope. Discontinuous Streams use separate Stream Geodatabases and
separate scopes.

The editable ArcGIS unit is intentionally narrower than the logical Network
Workspace: one time-specific geodatabase contains one Network Observation and
one `stream_network` feature class. Several observation geodatabases may
participate in the same logical scope and submission package by carrying the
same `network_scope_id`. This preserves the historical manual edit model while
allowing the enterprise binding to consolidate all accepted segments in one
feature class keyed by `network_observation_id`.

## Separation of concerns

The earlier brainstorming list mixed three categories. This contract separates
them:

1. **Scientific entities** have durable identity and scientific meaning, such
   as Network Scope, Network Observation, and Reference Frame.
2. **Relationship records** state membership, ordering, use, or calibration
   between entities. A relationship row is not another geomorphic object.
3. **Package records** describe a transport snapshot submitted to FGDB. They
   are operational records, not scientific entities.

Study Area, Stream, Reach, Survey Event, and Flowline remain the hierarchy and
feature entities defined elsewhere. The Network Workspace references their
stable IDs; it does not create a second competing definition of them. Display
names may be copied as snapshots for usability but never act as foreign keys.

## Candidate object-relational model

```text
Study Area
  └─< Network Scope >─< Scope-Stream membership >─ Stream
          ├─< Network Observation ─< Stream Network Segment
          │          └─< Network-Event Use >─ Reach Survey Event
          └─< Reference Frame ──1 Reference Mouth
                    ├─< Reach Assignment ──1 selected Base Flowline
                    │          └─< Comparison Flowline Calibration
                    └─< Reference Path >─< ordered Path-Reach membership
```

`─<` means one-to-many and `>─<` means many-to-many through an explicit
relationship table.

### Identifier and common-field convention

- Every entity uses a stable UUID generated before enterprise submission. In
  a file geodatabase this is an Esri GUID field, not `OBJECTID`.
- Foreign keys use those UUIDs across local geodatabases and package bindings.
- Every locally governed entity has `created_at`, `created_by`, `modified_at`,
  `modified_by`, and controlled `lifecycle_status` fields.
- Scientific reviewable objects additionally have `review_status`,
  `reviewed_at`, and `reviewed_by`.
- Names are display snapshots and aliases; IDs establish relationships.

### `fg_network_scope` — scientific entity

**One row represents:** one intended connected network-analysis and stationing
scope. The ArcGIS binding recommends exactly one active scope row per editable
Network Observation geodatabase. The same stable scope row may be carried as a
metadata snapshot in several time-specific geodatabases; package assembly
reconciles those snapshots by `network_scope_id` and rejects conflicts.

| Field | Required | Meaning |
|---|---:|---|
| `network_scope_id` | yes | UUID primary key. |
| `study_area_id` | yes | Stable referenced Study Area identity. |
| `study_area_name` | yes | Display snapshot; not a foreign key. |
| `scope_mode` | yes | `STREAM` or `STUDY_AREA_NETWORK`. |
| `scope_label` | yes | Human-readable local label. |
| `contract_version` | yes | Version of the `fluvgeo` Network Scope contract. |
| common lifecycle fields | yes | Local creation/modification and status. |

The mouth does not belong on this row because different Reference Frames in
the same scope may intentionally use different mouths.

### `fg_network_scope_stream` — relationship table

**One row represents:** membership of one durable Stream in one Network Scope.
It does not represent a second Stream object.

| Field | Required | Meaning |
|---|---:|---|
| `network_scope_id` | yes | FK to `fg_network_scope`. |
| `stream_id` | yes | Stable Stream identity. |
| `stream_name` | yes | Display snapshot. |
| `membership_role` | yes | Initially `SUBJECT`; permits later controlled roles if justified. |

Primary key: (`network_scope_id`, `stream_id`). A `STREAM` scope has exactly
one row; a `STUDY_AREA_NETWORK` scope has the reviewed connected set.

### `fg_network_observation` — scientific entity

**One row represents:** one reviewed synthetic-network realization derived
from terrain at one observation time. It is not a Survey Event and not a
processing-run history.

| Field | Required | Meaning |
|---|---:|---|
| `network_observation_id` | yes | UUID primary key. |
| `network_scope_id` | yes | FK to the one scope. |
| `observation_year` | yes | Terrain-observation year. |
| `observation_month`, `observation_day` | no | Known date components. |
| `date_precision` | yes | `YEAR`, `MONTH`, or `DAY`. |
| `source_terrain_id` | no | Stable source/hydro-DEM reference when known. |
| `derivation_method_id`, `method_version` | yes | Controlled scientific method and version; legacy unknown is explicit. |
| `threshold_value`, `threshold_unit` | conditional | Stream-initiation threshold when known/required by method. |
| `parameters_json` | yes | Canonically serialized remaining material parameters. |
| `native_horizontal_crs`, `native_vertical_datum`, `cell_size` | yes for new work | Terrain/derivation spatial context. |
| `provenance_completeness` | yes | Complete, partial legacy, or controlled not-retained state. |
| common lifecycle/review fields | yes | Current local observation and review state. |

A new terrain time creates a new row. Correcting the same intended observation
retains this ID and replaces its current segment set after review.

The ArcGIS editing binding contains exactly one active observation row per
time-specific geodatabase. This is a physical safety constraint, not an
enterprise cardinality rule.

### `stream_network` — scientific feature class

**One row represents:** one directed polyline segment in exactly one Network
Observation. In an editable local ArcGIS geodatabase, every row in the feature
class must reference the geodatabase's one active observation. Separate terrain
times use separate geodatabases rather than an observation-filtered editing
layer. The enterprise binding may place segments from many observations in one
physical feature class because `network_observation_id` remains mandatory.

| Field | Required | Meaning |
|---|---:|---|
| `network_segment_id` | yes | UUID primary scientific identifier; `OBJECTID` remains Esri-internal. |
| `network_observation_id` | yes | FK to `fg_network_observation`. |
| `stream_id` | yes before accepted review | Classified Stream; must belong to scope membership. |
| `reach_id` | no | Classified Reach after segmentation. |
| `downstream_node_id`, `upstream_node_id` | yes before accepted review | Stable logical endpoint identifiers. Package v0.1 derives node geometry from endpoints and persists no node feature class. |
| `segment_role` | yes | Main stem, tributary, connector, artificial, unresolved, or another controlled value. |
| `direction_status` | yes | Confirmed downstream-to-upstream orientation or controlled unresolved state. |
| `source_feature_key` | no | Legacy/local traceability only; never identity. |
| `review_status` | yes | Draft, reviewed, accepted, or rejected. |
| `Shape` | yes | Polyline geometry in the workspace CRS. |

Observation-level date, threshold, method, and provenance are not repeated on
every segment. Service/export views may denormalize them later.

### `fg_network_event_use` — relationship table

**One row represents:** a documented role played by one Network Observation
for one Reach-owned Survey Event.

| Field | Required | Meaning |
|---|---:|---|
| `network_observation_id` | yes | FK to the network observation. |
| `survey_event_id` | yes | Stable Reach Survey Event identity from a Reach workspace. |
| `relationship_role` | yes | `TOPOLOGY_SOURCE`, `STATIONING_SOURCE`, `DERIVATION_CONTEXT`, or `COMPARISON_TARGET`. |
| `notes` | no | Reviewed qualification. |

Primary key: (`network_observation_id`, `survey_event_id`,
`relationship_role`). This bridges scales without making the network a child
of one Reach.

### `fg_reference_frame` — scientific entity

**One row represents:** one analyst-created, base-realization-specific
longitudinal coordinate definition for a Network Scope.

| Field | Required | Meaning |
|---|---:|---|
| `reference_frame_id` | yes | UUID primary key. |
| `network_scope_id` | yes | FK to scope. |
| `base_network_observation_id` | no | Selected topology realization when applicable. |
| `frame_label` | yes | Human-readable analysis label. |
| `base_selection_preset` | no | For example `LATEST_VALIDATED_EVENT`; provenance only. |
| `measure_unit` | yes | `KILOMETER`. |
| `measure_direction` | yes | `INCREASES_UPSTREAM`. |
| `method_id`, `method_version` | yes | Stationing/calibration contract. |
| common lifecycle/review fields | yes | Analyst-created and accepted state. |

Changing the base selection, mouth, scope, or path semantics creates a new
frame ID. Loading a newer Survey Event changes nothing automatically.

### `fg_reference_mouth` — one-to-one spatial representation

**One feature row represents:** the zero-measure mouth point for one Reference
Frame. It is a spatial representation belonging to the frame, not an
independent network entity.

| Field | Required | Meaning |
|---|---:|---|
| `reference_frame_id` | yes | PK/FK; enforces one mouth per frame. |
| `mouth_meaning` | yes | Stream downstream limit or connected-network outlet. |
| `selection_method` | yes | Analyst selected, derived candidate then confirmed, or controlled method. |
| `Shape` | yes | Point geometry in workspace CRS. |

### `fg_reach_assignment` — frame relationship with embedded base selection

**One row represents:** one Reach's interval and selected base Flowline in one
Reference Frame.

| Field | Required | Meaning |
|---|---:|---|
| `reach_assignment_id` | yes | UUID primary key. |
| `reference_frame_id` | yes | FK to frame. |
| `stream_id`, `reach_id` | yes | Stable hierarchy references. |
| `base_survey_event_id` | yes | Explicit selected base event for this Reach. |
| `base_flowline_id` | yes | Explicit selected base Flowline. |
| `downstream_measure_km`, `upstream_measure_km` | yes | Governed interval on the base realization. |
| `topology_role` | yes | Terminal, main stem, tributary, shared downstream, or controlled role. |
| `validation_status` | yes | Interval/topology validation result. |

Unique key: (`reference_frame_id`, `reach_id`). Embedding the one-to-one base
selection here is a deliberate local simplification; the enterprise schema may
normalize it into a separate base-selection relation.

### `fg_reference_path` and `fg_path_reach` — entity plus relationship

`fg_reference_path` has one row per named main-stem or tributary-to-mouth path:

| Field | Required | Meaning |
|---|---:|---|
| `reference_path_id` | yes | UUID primary key. |
| `reference_frame_id` | yes | FK to frame. |
| `path_name`, `path_role` | yes | Human label and controlled main-stem/tributary role. |

`fg_path_reach` has one row per ordered Reach assignment used by a path:

| Field | Required | Meaning |
|---|---:|---|
| `reference_path_id` | yes | FK to path. |
| `reach_assignment_id` | yes | FK to the reusable Reach assignment. |
| `path_sequence` | yes | Downstream-to-upstream integer order. |

This N:M relationship permits several tributary paths to reuse one shared
downstream Reach assignment without duplicating its calibration.

### `fg_flowline_calibration` — scientific relationship/result

**One row represents:** calibration of one non-base Survey Event Flowline to
the selected base Flowline for the same Reach and Reference Frame.

| Field | Required | Meaning |
|---|---:|---|
| `flowline_calibration_id` | yes | UUID primary key. |
| `reference_frame_id`, `reach_assignment_id` | yes | Frame and applicable Reach interval. |
| `comparison_survey_event_id`, `comparison_flowline_id` | yes | Flowline being calibrated. |
| `method_id`, `method_version` | yes | Calibration algorithm/contract. |
| `control_points_ref` | conditional | Stable reference to local calibration-point evidence. |
| `search_tolerance`, `tolerance_unit` | conditional | Material matching parameter. |
| `residual_summary_json` | no | Error/fit evidence where available. |
| `validation_status` | yes | Staged, passed, failed, or accepted result. |
| common lifecycle/review fields | yes | Analyst-run and reviewed operation. |

Unique key: (`reference_frame_id`, `comparison_flowline_id`). Base Flowlines do
not receive a comparison-calibration row; their selection is recorded on the
Reach assignment.

## Reach–Survey Event output augmentation

The Stream/Network Geodatabase does not absorb event-specific geometry. The
existing Reach–Survey Event workspace adds stable identity and qualified
station fields to its own outputs:

| Existing object | Added logical fields |
|---|---|
| `flowline` | `flowline_id`, `survey_event_id`, method/version and review provenance. |
| `flowline_points` | `flowline_point_id`, `flowline_id`, local uncalibrated measure, `reference_frame_id`, nullable `flowline_calibration_id` for comparison events, and frame-specific `km_to_mouth`. |
| downstream derived features | Stable feature ID plus traceability to `reference_frame_id` and calibration when `km_to_mouth` is materialized. |

Thus the Stream/Network workspace stores the cross-Reach definition and
calibration registry, while each Reach–Survey Event workspace retains its own
derived geometry and point values.

## Submission package records — operational, not scientific

A package is an immutable export snapshot assembled after analysis. These
records do not belong in the scientific entity graph:

### `fg_package_manifest`

One row/document represents one submission snapshot with:

- `package_id`, `package_profile_version`, and `created_at/by`;
- source application and `fluvgeo` versions;
- `network_scope_id` and included Study Area identity;
- requested operation (`CREATE_NEW_OBSERVATION` or
  `REPLACE_CORRECTED_OBSERVATION`) and submission context (current production
  or legacy migration);
- overall content fingerprint and validation result; and
- completeness status.

### `fg_package_item`

One row per included feature class, table, raster, or referenced Reach
workspace records:

- `package_item_id`, `package_id`, and scientific object type;
- stable dataset/object identity;
- relative package locator rather than original absolute path;
- record count, item fingerprint, CRS/format, and completeness state.

Canonical `manifest.json` is required by package v0.1. Equivalent geodatabase
tables may be generated as read-only conveniences for ArcGIS inspection but
are not a second source of truth. Export creates the manifest; routine
scientific editing does not continually mutate a fictitious "current package."

## Deliberate differences from the enterprise model

The local model remains smaller because it:

- embeds Study Area/name snapshots on scope and Stream names on memberships
  instead of copying complete enterprise hierarchy tables;
- embeds the one base-Flowline selection on each Reach assignment instead of
  creating a separate one-to-one table;
- keeps current derivation/provenance fields on Network Observation and
  calibration rows instead of creating enterprise audit/load relations;
- contains no Enterprise Collection, publication, service, SDE, load-job,
  reconciliation, or authorization objects; and
- generates package manifest records only at export time.

The first network-persistence release always needs `fg_network_scope`,
`fg_network_scope_stream`, `fg_network_observation`, and `stream_network`.
It conditionally needs `fg_network_segment_source` for reconstructed legacy
observations. Exact v0.1 fields, domains, types, topology rules, validation,
identity reconciliation, and serialization are specified in
`dev/schemas/network-package-v0.1.md`.
`fg_network_event_use` is added when Reach packages are linked. Reference
Frame, mouth, Reach assignment, path, and calibration objects are a second
analyst-facing capability rather than prerequisites for initially retaining a
network.

## Platform bindings

| Client | Local-first binding |
|---|---|
| ArcGIS Pro | One editable Stream/Study Area Network file geodatabase per Network Observation, plus Reach–Survey Event geodatabases and a package manifest, written by `FluvialGeomorph-toolbox` wrappers around `fluvgeo`. |
| Shiny | User/application-scoped `sf`/tabular objects and durable application workspace or export package produced from the same `fluvgeo` contracts; no FGDB load is required to complete analysis. |
| QGIS | Future QGIS wrappers around `fluvgeo`, with an open local container such as GeoPackage plus the same logical manifest. |
| Direct R | `sf`/data-frame domain objects returned and validated by `fluvgeo`, with package read/write helpers independent of any GUI. |

The bindings may differ physically but must preserve the same stable identity,
scientific meaning, required provenance, controlled values, and validation
behavior. Cross-platform parity concerns scientific contracts, not identical
storage-engine fields or byte representation.

## Function ownership

`fluvgeo` should eventually provide:

- platform-neutral constructors and validators for Network Scope, Network
  Observation, topology, reference frame, and calibration objects;
- open-source replacements for scientific/geospatial ArcPy derivation stages;
- package manifest construction, validation, and platform-neutral
  serialization helpers where appropriate; and
- explicit method/version identifiers and scientific QA results.

Client adapters remain responsible for UI, interactive editing, platform
layer selection, and format-specific I/O:

- `FluvialGeomorph-toolbox` translates ArcGIS Pro parameters and file
  geodatabase features to/from `fluvgeo` contracts;
- Shiny applications translate reactive/user state to/from those contracts;
- a QGIS toolbox translates QGIS layers and user interaction to/from them; and
- FGDB translates a validated exchange package into normalized Enterprise
  rows, mosaics, and services without rerunning the analysis.

## Boundary tests

The architecture passes only if:

1. an analyst can complete and retain the full analysis without FGDB access;
2. the same scientific function and contract can be invoked from ArcGIS Pro,
   Shiny, direct R, and a future QGIS adapter;
3. the local result contains enough metadata to understand and validate it
   before enterprise submission;
4. the FGDB loader can ingest a valid package without deriving topology,
   selecting a base event, or recalibrating a Flowline; and
5. adding FGDB support does not remove or degrade a local analytical
   capability.

## Open questions

1. Review and accept/revise draft Network Package Contract v0.1 field names,
   domains, conditional requirements, and validation behavior.
2. Build the required conformance fixtures and verify deterministic logical
   fingerprints across ArcGIS and GeoPackage bindings.
3. Define the separate hierarchy/context snapshot used to supply governed IDs
   to offline producers; package v0.1 already defines conflict and explicit
   rebind behavior.
4. Specify the first `fluvgeo` constructors, validators, reconstruction
   functions, and serialization interface against package v0.1.
