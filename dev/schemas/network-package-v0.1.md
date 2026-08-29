# Network Package Contract v0.1

- Status: draft for design review
- Contract version: `0.1.0`
- Updated: 2026-08-29
- Governing decisions: ADR-0014 through ADR-0017

## Purpose and boundary

This contract defines the minimum platform-neutral package for one reviewed,
time-specific Network Observation. It is the shared handoff between:

- scientific constructors, derivation, reconstruction, and validation owned by
  `fluvgeo`;
- ArcGIS Pro, Shiny, direct R, and future QGIS producer clients; and
- FGDB package validation, identity reconciliation, and enterprise loading.

The contract does not define longitudinal reference frames, Flowline
calibration, cross-time segment correspondence, enterprise publication, or a
processing-run history. Those capabilities reference the stable identities
created here but are not prerequisites for retaining a network.

One package contains exactly one Network Scope snapshot and exactly one Network
Observation. One editable ArcGIS geodatabase implements exactly one such
observation under ADR-0016.

## Required package contents

| Object | Physical kind | Rows | Requirement |
|---|---|---:|---|
| `fg_network_scope` | nonspatial table | exactly 1 | always |
| `fg_network_scope_stream` | nonspatial table | 1..N | always |
| `fg_network_observation` | nonspatial table | exactly 1 | always |
| `stream_network` | 2D polyline feature class/layer | 1..N | always |
| `fg_network_segment_source` | nonspatial table | 0..N | required for reconstructed observations; otherwise optional |
| `manifest.json` | UTF-8 JSON document | one | required for an immutable submission package; absent while the workspace is merely being edited |

`NETWORK_NOT_RETAINED` does not create an empty Network Observation package.
It is a completeness state on the applicable legacy Reach package. A Network
Observation exists only when at least one governed segment geometry exists.

## Logical and physical type mapping

The logical types are normative. Platform bindings may use different physical
types only if round-trip validation preserves the logical value exactly.

| Logical type | ArcGIS file geodatabase | R / `sf` | GeoPackage | Rules |
|---|---|---|---|---|
| `uuid` | `GUID` | length-one character per row | `TEXT(36)` | RFC 9562 textual form when serialized: lowercase hexadecimal with hyphens and no braces. |
| `string(n)` | `TEXT(n)` | character | `TEXT` | UTF-8; trim outer whitespace; empty strings normalize to null unless a field explicitly permits empty. |
| `enum(n)` | `TEXT(n)` with coded-value domain where available | factor or character | `TEXT` plus validation | Stored value is the uppercase contract code, not its display label. |
| `int16` | `SHORT` | integer | `INTEGER` | Whole number in the declared range. |
| `int32` | `LONG` | integer | `INTEGER` | Whole number in the declared range. |
| `float64` | `DOUBLE` | double | `REAL` | Finite unless the field is null; NaN and infinity are invalid. |
| `boolean` | `SHORT` domain `0,1` | logical | `INTEGER` `0,1` | Null only where explicitly allowed. |
| `datetime_utc` | `DATE` | `POSIXct`, timezone UTC | ISO-8601 text or datetime | ArcGIS values are interpreted as UTC; serialized form uses `YYYY-MM-DDTHH:MM:SS.sssZ`. |
| `json` | `TEXT(65535)` | character or parsed list | `TEXT` | Valid UTF-8 JSON object; `{}` represents no additional parameters. |
| `polyline_2d` | `POLYLINE`, Z disabled, M disabled | `LINESTRING` | `LINESTRING` | One nonempty, valid, singlepart line per row in the declared layer CRS. |

File geodatabases do not enforce primary or foreign keys. Producer and FGDB
validators enforce all keys, relationships, conditional requirements, and
domains in this contract. `OBJECTID`, `Shape_Length`, and similar storage
fields are binding-generated and never package identity.

## Common fields

The following fields appear wherever identified below as **common lifecycle
fields**:

| Field | Logical type | Null | Rule |
|---|---|---:|---|
| `created_at` | `datetime_utc` | no | Time the local identity was created. |
| `created_by` | `string(255)` | no | Stable actor or process identifier; not necessarily a display name. |
| `modified_at` | `datetime_utc` | no | At or after `created_at`. |
| `modified_by` | `string(255)` | no | Stable actor or process identifier. |
| `lifecycle_status` | `enum(16)` | no | `ACTIVE` or `RETIRED`; a submission package contains only active rows. |

Reviewable objects additionally use:

| Field | Logical type | Null | Rule |
|---|---|---:|---|
| `review_status` | `enum(24)` | no | `DRAFT`, `READY_FOR_REVIEW`, `ACCEPTED`, or `REJECTED`. |
| `reviewed_at` | `datetime_utc` | conditional | Required only for `ACCEPTED` or `REJECTED`. |
| `reviewed_by` | `string(255)` | conditional | Required only for `ACCEPTED` or `REJECTED`. |
| `review_notes` | `string(2000)` | yes | Material qualifications or rejection explanation. |

Only an `ACCEPTED` Network Observation may be exported as a submission
package. Draft workspaces can contain draft segments and unresolved values as
described below.

## `fg_network_scope`

**One row means:** the intended connected network-analysis and stationing
scope for this observation. This is a portable snapshot of a durable scope,
not a new scope for every terrain time.

| Field | Logical type | Null | Rule |
|---|---|---:|---|
| `network_scope_id` | `uuid` | no | Primary key; generated locally for a new scope or copied exactly from an existing governed scope. |
| `study_area_id` | `uuid` | no | Referenced Study Area identity. |
| `study_area_name` | `string(255)` | no | Display snapshot; never a relationship key. |
| `scope_mode` | `enum(32)` | no | `STREAM` or `STUDY_AREA_NETWORK`. |
| `scope_label` | `string(255)` | no | Human-readable label unique after normalization within the Study Area. |
| `contract_version` | `string(20)` | no | Exactly `0.1.0` for this contract. |
| common lifecycle fields |  |  | Required. |

Rules:

1. The table contains exactly one active row and no retired rows in a package.
2. `STREAM` describes one independently derived Stream network.
3. `STUDY_AREA_NETWORK` describes a connected, intentionally common topology
   containing two or more Stream memberships. A one-Stream scope uses
   `STREAM`.
4. Scope identity persists across terrain times. A material change to scope
   mode or intended Stream membership creates a new scope ID.
5. Scope snapshots carrying the same ID must agree on Study Area, mode, and
   membership during multi-package assembly.

## `fg_network_scope_stream`

**One row means:** one durable Stream participates in the package's Network
Scope. It is a relationship record, not another Stream definition.

| Field | Logical type | Null | Rule |
|---|---|---:|---|
| `network_scope_id` | `uuid` | no | FK to the package's one scope. |
| `stream_id` | `uuid` | no | Referenced durable Stream identity. |
| `stream_name` | `string(255)` | no | Display snapshot; never a relationship key. |
| `membership_role` | `enum(16)` | no | `SUBJECT` in v0.1. |
| `created_at` | `datetime_utc` | no | Membership creation time. |
| `created_by` | `string(255)` | no | Membership creator identifier. |

Primary key: (`network_scope_id`, `stream_id`).

Rules:

1. Every row references the one packaged scope.
2. `STREAM` has exactly one membership.
3. `STUDY_AREA_NETWORK` has at least two memberships.
4. Every accepted segment's `stream_id` appears in this table.
5. A Stream identity must belong to the scope's Study Area. The producer
   validates known local context; FGDB revalidates authoritative ownership.

## `fg_network_observation`

**One row means:** one current, time-specific analytical network realization
supported by terrain evidence or reconstructed from terrain-derived Reach
Flowlines. Observation time describes the terrain evidence; creation and
review times describe later processing.

| Field | Logical type | Null | Rule |
|---|---|---:|---|
| `network_observation_id` | `uuid` | no | Primary key. |
| `network_scope_id` | `uuid` | no | FK to the package's one scope. |
| `observation_year` | `int16` | no | Four-digit year from 1000 through 9999; never fabricated. |
| `observation_month` | `int16` | yes | 1 through 12 when known. |
| `observation_day` | `int16` | yes | Valid calendar day; requires month. |
| `date_precision` | `enum(8)` | no | `YEAR`, `MONTH`, or `DAY`, exactly matching populated components. |
| `evidence_class` | `enum(48)` | no | See evidence domain below. |
| `coverage_status` | `enum(24)` | no | `FULL_SCOPE`, `PARTIAL_SCOPE`, `KNOWN_GAPS`, or `UNKNOWN_LEGACY`. |
| `source_terrain_id` | `uuid` | yes | Governed terrain/dataset identity when one exists. |
| `source_terrain_label` | `string(255)` | yes | Nonidentity evidence label when useful. |
| `source_terrain_fingerprint` | `string(64)` | yes | Lowercase SHA-256 hex digest when retained evidence permits it. |
| `derivation_method_id` | `string(255)` | no | Stable method identifier; `LEGACY_UNKNOWN` is allowed only for legacy retained evidence. |
| `method_version` | `string(64)` | conditional | Required unless method is `LEGACY_UNKNOWN`. |
| `threshold_value` | `float64` | conditional | Positive initiation threshold when material to the method and known. |
| `threshold_unit` | `enum(24)` | conditional | `SQUARE_METER`, `SQUARE_FOOT`, `CELL_COUNT`, or `LEGACY_UNKNOWN`; required with threshold. |
| `parameters_json` | `json` | no | Remaining material parameters; `{}` is valid. |
| `native_horizontal_crs` | `string(255)` | conditional | Stable CRS authority identifier when available, otherwise an unambiguous local identifier. Required for new derivations/reconstructions. |
| `native_vertical_datum` | `string(255)` | conditional | Required for new terrain derivations; nullable for Flowline reconstruction when no elevation is used. |
| `horizontal_unit` | `enum(24)` | conditional | `METER`, `US_SURVEY_FOOT`, `INTERNATIONAL_FOOT`, or another future controlled code. Required for new work. |
| `vertical_unit` | `enum(24)` | conditional | Same initial unit vocabulary; required when vertical datum is populated. |
| `cell_size` | `float64` | conditional | Positive terrain cell size in `horizontal_unit`; required for new terrain derivation. |
| `provenance_completeness` | `enum(24)` | no | `COMPLETE`, `PARTIAL_LEGACY`, or `MINIMAL_LEGACY`. |
| common lifecycle fields |  |  | Required. |
| reviewable-object fields |  |  | Required as governed above. |

### Evidence domain

| Code | Meaning | Additional requirement |
|---|---|---|
| `DIRECT_TERRAIN_DERIVATION` | Network created under the current contract from terrain evidence. | Complete method, version, material parameters, CRS, units, cell size, and provenance. |
| `SOURCE_NETWORK_RETAINED` | A previously derived and edited network survives and is being registered. | Retain known source evidence; controlled legacy unknowns are allowed. |
| `RECONSTRUCTED_FROM_REACH_FLOWLINES` | Original network is absent and a new analytical network was assembled from governed Reach Flowlines. | `fg_network_segment_source` is complete for every segment; method/version and reconstruction QA are required. |

Rules:

1. The table contains exactly one row and it references the packaged scope.
2. A new terrain-observation occurrence creates a new observation ID. A
   correction to the same intended occurrence retains the ID and replaces the
   complete active segment set after review.
3. Date is not unique. Distinct observations can share a date.
4. `FULL_SCOPE` asserts that all intended subject paths in the scope are
   represented. `PARTIAL_SCOPE` asserts an intentionally limited subset.
   `KNOWN_GAPS` asserts missing geometry within intended paths.
   `UNKNOWN_LEGACY` makes no completeness assertion.
5. `RECONSTRUCTED_FROM_REACH_FLOWLINES` is a new reconstruction made later
   from historical evidence. It never claims that the original source network
   geometry survived.

## `stream_network`

**One row means:** one directed topology edge belonging to the package's one
Network Observation.

| Field | Logical type | Null | Rule |
|---|---|---:|---|
| `network_segment_id` | `uuid` | no | Primary scientific identity. |
| `network_observation_id` | `uuid` | no | FK to the one packaged observation. |
| `stream_id` | `uuid` | conditional | Required for `ACCEPTED`; must be a scope membership. |
| `reach_id` | `uuid` | yes | Optional classified Reach; when present it must belong to `stream_id`. |
| `downstream_node_id` | `uuid` | conditional | Required for `ACCEPTED`; logical downstream endpoint identity. |
| `upstream_node_id` | `uuid` | conditional | Required for `ACCEPTED`; logical upstream endpoint identity. |
| `segment_role` | `enum(24)` | no | `MAINSTEM`, `TRIBUTARY`, `CONNECTOR`, `ARTIFICIAL`, or `UNRESOLVED`. |
| `direction_status` | `enum(16)` | no | `CONFIRMED` or `UNRESOLVED`; accepted segments require `CONFIRMED`. |
| `direction_method` | `enum(32)` | conditional | `TERRAIN_ELEVATION`, `FLOW_ACCUMULATION`, `SOURCE_RETAINED`, `ANALYST_CONFIRMED`, or `LEGACY_UNKNOWN`; required when confirmed. |
| `source_feature_key` | `string(255)` | yes | Convenience traceability only; not identity and not a substitute for the lineage table. |
| common lifecycle fields |  |  | Required. |
| reviewable-object fields |  |  | Required. |
| `Shape` | `polyline_2d` | no | Directed from downstream endpoint to upstream endpoint. |

### Edge and endpoint rules

1. Every row is nonempty, valid, and singlepart with at least two distinct
   coordinates. Z and M values are not part of the network contract.
2. Edges are split at every retained confluence, Stream boundary, Reach
   boundary, and explicit gap boundary. Interior edge crossings without a
   common node are allowed only when they are true nonconnecting crossings;
   otherwise they fail validation.
3. Geometry coordinate order is downstream to upstream. The first coordinate
   realizes `downstream_node_id`; the last realizes `upstream_node_id`.
4. A shared logical node ID requires endpoint coordinates to coincide within
   the package's declared topology tolerance. Coincident endpoints intended to
   connect must share a node ID.
5. `downstream_node_id` and `upstream_node_id` cannot be equal on one edge.
6. Node IDs are logical endpoint identities in v0.1. No governed node table or
   point feature class is persisted; node geometry is derived from edge
   endpoints. A later contract can add node representations without changing
   segment identity.
7. Accepted networks contain no duplicate edge identity or duplicate geometry
   with the same classified role. Directed cycles fail v0.1 submission
   validation unless a later contract defines an explicit reviewed exception.
8. Multipart source features are deterministically exploded before identity is
   assigned. Splitting, snapping, reversal, or other geometry changes are
   recorded by method parameters and lineage rather than hidden.

## `fg_network_segment_source`

**One row means:** one source feature contributed evidence to one packaged
network segment. Several packaged segments may derive from one source feature,
and one assembled segment may cite several source features.

| Field | Logical type | Null | Rule |
|---|---|---:|---|
| `network_segment_source_id` | `uuid` | no | Primary key. |
| `network_segment_id` | `uuid` | no | FK to `stream_network`. |
| `source_object_type` | `enum(32)` | no | `STREAM_NETWORK_FEATURE` or `FLOWLINE`. |
| `source_object_id` | `uuid` | conditional | Required for `FLOWLINE`; optional for legacy network features lacking durable IDs. |
| `source_dataset_ref` | `string(255)` | yes | Package-local dataset/item identifier or reviewed nonpath label. |
| `source_feature_key` | `string(255)` | conditional | Required when `source_object_id` is null; never promoted to governed identity. |
| `relation_code` | `enum(24)` | no | `COPIED_FROM`, `SPLIT_FROM`, `ASSEMBLED_FROM`, or `GEOMETRY_GUIDE`. |
| `geometry_modified` | `boolean` | no | Whether packaged geometry differs from the cited source portion. |
| `modification_json` | `json` | no | Material operations and parameters; `{}` when unmodified. |

Rules:

1. Every reconstructed segment has at least one lineage row with
   `source_object_type = FLOWLINE` and a non-null governed `source_object_id`.
2. A lineage row must resolve to an included package item or to an explicitly
   governed external identity declared by the manifest.
3. Filesystem paths, `OBJECTID`, and layer names may appear only as qualified
   evidence in `source_dataset_ref` or `source_feature_key`; they never act as
   foreign keys.
4. Endpoint snapping, splitting, reversal, or assembly sets
   `geometry_modified = 1` and records its method/tolerance in
   `modification_json`.

## Identity creation and reconciliation

1. New local identities use cryptographically random UUID version 4 values
   conforming to RFC 9562. Existing governed non-nil UUIDs are accepted without
   rewriting solely because they were minted under an earlier compatible UUID
   specification.
2. A producer referencing an existing FGDB Study Area, Stream, Reach, Scope,
   Survey Event, or Flowline must use that object's existing immutable UUID,
   obtained through a governed context export or connected selection.
3. A newly created offline object keeps its locally generated UUID when first
   accepted by FGDB. FGDB does not replace it merely because it was created
   offline.
4. If a submission proposes a new object whose governed unique name already
   exists, loading fails with an identity conflict. No name or geometry match
   silently rewrites package foreign keys.
5. An analyst-facing rebind/reconciliation operation may explicitly replace a
   proposed local reference with a selected governed UUID, update every
   dependent reference atomically, revalidate, and create a new package
   fingerprint.
6. `OBJECTID`, filenames, paths, labels, and geometry proximity never resolve
   identity automatically.

The v0.1 Network Package references Study Area, Stream, and optional Reach
objects but does not reproduce their full hierarchy tables. A separately
versioned context snapshot or connected client supplies their governed IDs and
display labels.

## Working-workspace validation

A producer validator returns structured issues with at least:

- `issue_code`;
- `severity` = `ERROR`, `WARNING`, or `INFO`;
- affected object/table and stable ID when available;
- human-readable message; and
- optional machine-readable details.

Working validation permits `DRAFT`, nullable segment classification and node
IDs, `UNRESOLVED` roles/direction, and incomplete review fields. It still
rejects unreadable tables, invalid UUID syntax, duplicate primary IDs, orphaned
foreign keys, null/empty geometry, invalid geometry type, invalid date
components, and values outside controlled domains.

## Submission validation

An immutable submission package passes only when:

1. all required objects, row counts, fields, logical types, and domains match
   contract `0.1.0`;
2. the one scope and observation are `ACTIVE` and the observation is
   `ACCEPTED`;
3. all segments are `ACTIVE`, `ACCEPTED`, classified to a member Stream, have
   confirmed direction, and have both logical endpoint IDs;
4. every optional Reach belongs to the segment's Stream;
5. UUIDs are unique in their required scope and every FK resolves;
6. edge splitting, endpoint/node consistency, direction, duplicate, crossing,
   cycle, and connectivity checks pass;
7. the declared coverage status agrees with connected components, explicit
   gaps, and intended scope;
8. evidence-class conditional provenance is complete;
9. reconstructed observations have complete governed Flowline lineage and
   recorded geometry modifications;
10. layer CRS is defined and agrees with observation spatial context;
11. every manifest item count, content fingerprint, locator, and schema
    fingerprint matches the packaged content; and
12. no absolute path, parent traversal, credential, token, or secret is stored
    in the manifest or scientific tables.

Submission result is `PASS`, `PASS_WITH_WARNINGS`, or `FAIL`:

- `FAIL` contains at least one error and cannot load.
- `PASS_WITH_WARNINGS` may load into an allowed qualified legacy state but
  cannot be silently presented as complete network evidence.
- `PASS` satisfies all requirements for its declared evidence and coverage
  class. `PASS` does not upgrade partial or reconstructed evidence into direct,
  full-scope evidence.

## Topology tolerance

`manifest.json` declares one positive `topology_tolerance` and unit for the
package. It controls endpoint coincidence and candidate snapping validation;
it is not a general geometry simplification tolerance.

- Unit must be the layer's horizontal unit.
- New derivations and reconstructions require an explicit value selected or
  confirmed by the analyst-facing workflow.
- Legacy retained networks may use a documented migration default, which must
  be visible in provenance and may produce warnings.
- A producer may propose repairs inside the tolerance, but geometry is changed
  only through an explicit invoked preparation/reconstruction operation.
- The package records the resolved tolerance, method version, issue results,
  and whether any endpoint changed.

No universal numeric tolerance is specified in v0.1 because appropriate
values depend on source resolution and native CRS units. Tool specifications
must define defensible presets and require the resolved value in the package.

## Canonical submission package

The submission is a directory or archive with this logical layout:

```text
fg-network-package/
  manifest.json
  data/
    network.gdb/       # ArcGIS binding
    # or network.gpkg  # open binding
```

Exactly one data-container binding is authoritative in one package. Additional
renders or convenience exports are excluded from the content fingerprint.

`manifest.json` is the canonical package manifest. Optional mirror tables in a
geodatabase are read-only conveniences generated from the JSON and are not an
independent source of truth.

### Required manifest properties

| Property | Type | Rule |
|---|---|---|
| `package_id` | uuid | New immutable export-snapshot identity. |
| `package_profile` | string | `FGDB_NETWORK_PACKAGE`. |
| `package_version` | string | `0.1.0`. |
| `created_at`, `created_by` | datetime/string | Export actor/process and UTC time. |
| `source_application`, `source_application_version` | string | Calling client and version. |
| `fluvgeo_version` | string | Scientific contract implementation version. |
| `operation` | enum | `CREATE_NEW_OBSERVATION` or `REPLACE_CORRECTED_OBSERVATION`. |
| `submission_context` | enum | `CURRENT_PRODUCTION` or `LEGACY_MIGRATION`; this does not alter create/replace semantics. |
| `network_scope_id` | uuid | Must equal the scope table value. |
| `network_observation_id` | uuid | Must equal the observation table value. |
| `container_format` | enum | `FILE_GEODATABASE` or `GEOPACKAGE`. |
| `topology_tolerance`, `topology_tolerance_unit` | number/enum | Positive resolved endpoint tolerance and horizontal unit. |
| `validation_result` | enum | `PASS` or `PASS_WITH_WARNINGS`; failed packages are not exported. |
| `validation_issues` | array | Structured warnings and informational results; no suppressed errors. |
| `items` | array | One entry per required/conditional table or feature layer. |
| `external_references` | array | Governed hierarchy/Flowline UUIDs referenced but not reproduced. |
| `package_fingerprint` | string | Lowercase SHA-256 digest calculated by the package profile. |

Each `items` entry contains:

- stable `package_item_id` UUID;
- `object_name` and `object_kind`;
- POSIX-style relative `locator` with no drive, leading slash, URI scheme, or
  `..` segment;
- row/feature count;
- geometry type and CRS for spatial items;
- schema fingerprint;
- content fingerprint; and
- byte size when the binding exposes a stable file representation.

Each `external_references` entry contains:

- `object_type` and stable `object_id`;
- `reference_state` = `GOVERNED_EXISTING` or
  `PROPOSED_IN_COMPANION_PACKAGE`;
- optional `display_name` snapshot;
- `parent_object_id` when needed to validate a proposed hierarchy reference;
  and
- `companion_package_id` and `companion_package_item_id` when
  `reference_state = PROPOSED_IN_COMPANION_PACKAGE`.

Every nonpackaged Study Area, Stream, Reach, Survey Event, Flowline, or terrain
UUID used by a table appears once in this array. A standalone Network Package
can load only when its references are already governed. References proposed
locally must be submitted and validated as part of a transactionally assembled
companion package set; display snapshots never contain enough authority to
create hierarchy objects silently.

### Deterministic fingerprints

Fingerprints describe normalized logical content rather than unstable file
geodatabase bytes:

1. A schema descriptor lists fields in contract order using logical field
   name, logical type, nullability, primary/FK role, enum values, and, for a
   spatial item, `polyline_2d` plus a canonical CRS identifier. Its RFC 8785
   JSON Canonicalization Scheme UTF-8 serialization receives a SHA-256 schema
   fingerprint.
2. Rows are sorted by their declared primary key; composite-key components use
   contract order. UUIDs use lowercase canonical strings, timestamps use UTC
   ISO-8601, strings use Unicode NFC, null remains JSON null, enums use stored
   codes, and embedded JSON is parsed before canonicalization.
3. Geometry is encoded as lowercase hexadecimal little-endian OGC 2D WKB,
   preserving the meaningful downstream-to-upstream coordinate order. CRS is
   carried by the schema descriptor rather than repeated in each row.
4. Each normalized row is a JSON array in contract field order. The RFC 8785
   canonical JSON array of all sorted rows receives the SHA-256 content
   fingerprint.
5. `package_fingerprint` is SHA-256 over the RFC 8785 canonical manifest after
   removing only the `package_fingerprint` property. It therefore identifies
   an export snapshot, while item content fingerprints identify repeatable
   scientific content across different exports.

For an authority-defined CRS, the canonical identifier is `AUTHORITY:CODE`
(for example `EPSG:26915`). A CRS without an authority code uses a profile
fixture containing normalized WKT2 and its SHA-256 identifier. Executable
fixtures must verify that ArcGIS and GeoPackage bindings normalize to the same
logical hashes before implementation is declared conformant.

## Correction and idempotency

1. `CREATE_NEW_OBSERVATION` requires a new observation ID not already governed.
2. `REPLACE_CORRECTED_OBSERVATION` names the exact existing observation ID and
   contains its complete replacement segment set, not a row-level patch.
3. `submission_context = LEGACY_MIGRATION` uses the same create/replace
   semantics but permits the controlled legacy provenance states defined here.
4. Re-exporting identical scientific content creates a new `package_id` but
   identical item content fingerprints. FGDB recognizes the already accepted
   content as an idempotent no-op.
5. Changed content for an existing observation requires explicit correction;
   loading never infers replacement from date, name, path, or proximity.
6. FGDB stages and validates the complete package before atomically creating or
   replacing the observation's active segment set.

## ArcGIS file-geodatabase binding

1. Table and feature-class names are exactly those specified in Required
   package contents.
2. IDs and FKs use Esri `GUID` fields. Adding Esri-managed `GlobalID` fields is
   permitted for platform behavior, but `GlobalID` is not the contract ID
   unless it is explicitly the same governed UUID and round trips unchanged.
3. `stream_network` is a simple 2D polyline feature class in the analyst's
   appropriate projected CRS. It is not stored in EPSG:3857 locally.
4. Coded-value domains should mirror contract enums, but validation may not
   assume domains survived format conversion.
5. Native geodatabase relationship classes and topology datasets are optional
   editing aids. The package contract is enforced from UUID fields and geometry
   rules so that it remains portable.
6. The ArcGIS client prevents mixed observation IDs in one editable feature
   class and writes the one scope/observation metadata rows before acceptance.
7. Absolute source paths may be shown transiently in the client but are not
   written into governed package fields or the canonical manifest.

## Open `sf` / GeoPackage binding

1. `fluvgeo` constructors return data frames and `sf` objects using the logical
   names and values in this contract.
2. UUIDs serialize as canonical strings; timestamps use UTC; enums serialize
   as contract codes rather than R factor ordinals.
3. `stream_network` uses one 2D `LINESTRING` geometry column and one declared
   projected CRS.
4. A GeoPackage writer uses the same object names and produces the same
   manifest properties and validation results as the ArcGIS binding.
5. Direct file-geodatabase writing is not required of `fluvgeo`. An ArcGIS Pro
   wrapper may translate validated `fluvgeo` objects into the ArcGIS binding
   without owning a second scientific schema.

## Version compatibility

- Producers write exactly one declared package version.
- A loader advertises supported package versions and rejects an unsupported
  major/minor version before staging.
- Additive fields require a new minor version; changed meaning, cardinality,
  identity, geometry, or required behavior requires a new major version.
- Patch versions may clarify validation or fix fixtures without changing valid
  data shape.
- Unknown fields are rejected in v0.1 submission packages unless a later
  profile explicitly permits extensions. This prevents silent semantic drift
  during the initial implementation.

## Normative external references

- [RFC 9562, Universally Unique IDentifiers
  (UUIDs)](https://www.rfc-editor.org/rfc/rfc9562.html) governs UUID syntax and
  version 4 generation. It supersedes RFC 4122.
- [RFC 8785, JSON Canonicalization Scheme
  (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html) governs deterministic JSON
  serialization for schema, item-content, and package fingerprints.

## Contract fixtures required before implementation

The contract becomes implementation-ready after the repository contains and
validates these small, noncustomer fixtures:

1. a minimal valid one-Stream direct-derivation package;
2. a valid connected multi-Stream package with a confluence;
3. a valid reviewed reconstruction with one Flowline split into several edges;
4. a partial/known-gap legacy package producing the intended warnings;
5. an invalid mixed-observation package;
6. an invalid hierarchy/Reach mapping package;
7. invalid endpoint-node, direction, cycle, and unsplit-confluence examples;
8. a correction package and an identical-content idempotent resubmission; and
9. equivalent ArcGIS and GeoPackage bindings that normalize to the same
   logical objects and item fingerprints.

## Decisions deferred beyond v0.1

- governed node feature/table representations;
- cross-time segment correspondence;
- longitudinal Reference Frames, mouths, paths, Reach assignments, and
  Flowline calibrations;
- network-to-Reach-Survey-Event association packaging;
- universal or method-specific automatic tolerance selection;
- raster and Hydro DEM inclusion;
- enterprise physical table names, indexes, service views, and publication
  policy beyond the required normalized mapping; and
- optional extension fields and aggregate archive canonicalization after
  executable fixtures establish deterministic behavior.
