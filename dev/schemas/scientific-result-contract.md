# Scientific result, metric, and dataset-edition contract

- Status: accepted logical design; physical names and Esri bindings remain draft
- Updated: 2026-09-02
- Governing decision: ADR-0023

## Purpose

This contract makes results produced across changing FluvialGeomorph software
and methods interpretable without converting feature-specific dimensions to a
long measurement store. It defines durable metric definitions, versioned
scientific method and output-schema contracts, exact producing-software
provenance, accepted dataset editions, and analyst-controlled updates.

Platform type and format fidelity remain governed separately by
`platform-type-crosswalk.md`.

## Relationship model

```text
Dataset Type 1 ---- N Dimension Metric Definition
      |                         |
      |                         N
      |                         |
      +---- N Scientific Method Contract 1 ---- N Method Contract Metric
      |
      +---- N Dataset Schema Contract 1 ---- N Dataset Schema Field

Software Environment 1 ---- N Environment Release N ---- 1 Software Release
                                                        |
                                                        N
                                                        |
                                                   Software Component

Survey Event 1 ---- N Derived Dataset
Derived Dataset 1 ---- N Derived Dataset Edition
                           |       |       |       |
                           |       |       |       +---- Platform Profile
                           |       |       +------------ Software Environment
                           |       +-------------------- Dataset Schema Contract
                           +---------------------------- Scientific Method Contract

Derived Dataset Edition 1 ---- N wide feature/dimension rows
```

`derived_dataset` is a stable semantic slot. An edition is an accepted
realization, not a raw tool execution. Wide scientific rows always identify the
edition that governs their interpretation.

## Core relations

### `dimension_metric_definition`

One row represents one stable scientific metric concept.

| Field | Required | Contract |
|---|---:|---|
| `metric_definition_id` | yes | Immutable identifier; never derived from a field alias. |
| `dataset_type_id` | yes | Dataset or feature family to which the metric applies. |
| `canonical_field_name` | yes | Stable FGDB wide-table field name. |
| `preferred_label` | yes | Human-readable metric name. |
| `definition` | yes | Scientific meaning independent of one software release. |
| `logical_type_id` | yes | Reference to `logical_field_type` in the governed type registry. |
| `canonical_unit_id` | conditional | Required for quantities; null only for dimensionless or nonnumeric values. |
| `ontology_concept_id` | no | Qualified FG/USACE ontology concept reference when established. |
| `value_domain_id` | no | Governed coded-value or numeric-domain reference when applicable. |
| `lifecycle_status` | yes | `DRAFT`, `ACTIVE`, `DEPRECATED`, or `RETIRED`. |
| `replaced_by_metric_definition_id` | no | Explicit successor when scientific meaning changes rather than merely implementation. |

Candidate uniqueness is (`dataset_type_id`, `canonical_field_name`). A material
change in scientific meaning creates a new metric identity. Correcting wording
without changing meaning preserves identity and requires governed audit.

### `scientific_method_contract`

One row represents an immutable, versioned scientific contract for producing a
dataset type or coherent feature family.

| Field | Required | Contract |
|---|---:|---|
| `scientific_method_contract_id` | yes | Immutable identifier. |
| `dataset_type_id` | yes | Governed output to which the contract applies. |
| `contract_version` | yes | Human-readable version unique within the dataset type. |
| `method_name` | yes | Stable method family name. |
| `method_definition` | yes | Inputs, operations, assumptions, and output meaning. |
| `effective_status` | yes | `DRAFT`, `ACCEPTED`, `DEPRECATED`, or `RETIRED`. |
| `supersedes_contract_id` | no | Prior contract when this is its successor. |
| `change_class` | yes | `INITIAL`, `ADDITIVE`, `EQUIVALENT_METHOD`, `MATERIAL_METHOD`, or `DEFECT_CORRECTION`. |
| `change_rationale` | yes | Scientific explanation of the version boundary. |

The contract is software-independent: more than one conforming software release
may implement the same method contract. An implementation-only software change
therefore creates a new software release and conformance claim, not an
artificially new scientific contract.

### `method_contract_metric`

One row states how one metric participates in one scientific method contract.
This is an optional child relation, not the definition of a scientific method.
A method contract may produce a geometry-only dataset such as Flowline and
therefore have no metric rows. Conversely, the same stable metric definition
may participate in several method contracts as implementations evolve.

| Field | Required | Contract |
|---|---:|---|
| `scientific_method_contract_id` | yes | Parent contract. |
| `metric_definition_id` | yes | Parent metric definition. |
| `population_requirement` | yes | `REQUIRED`, `CONDITIONAL`, `OPTIONAL`, or `NOT_PRODUCED`. |
| `calculation_definition` | conditional | Metric-specific calculation or governed specification reference. |
| `dependency_set_id` | no | Normalized dependency-graph reference used by update planning. |
| `expected_unit_id` | conditional | Must be convertible to the metric's canonical unit. |
| `null_semantics_id` | yes | Governed meaning of null/not-calculated/not-applicable. |

The primary key is (`scientific_method_contract_id`,
`metric_definition_id`). Free-text dependency lists or serialized objects are
not permitted.

### `dataset_schema_contract` and `dataset_schema_field`

The schema contract versions the logical wide-table representation separately
from scientific meaning. One schema-field row binds an ordered physical field
to a metric definition or to another governed identity/provenance attribute.

Minimum `dataset_schema_contract` fields are
`dataset_schema_contract_id`, `dataset_type_id`, `schema_version`, `status`, and
`supersedes_schema_contract_id`.

Minimum `dataset_schema_field` fields are `dataset_schema_contract_id`,
`field_ordinal`, `field_name`, `logical_type_id`, `nullable`,
`metric_definition_id` (nullable for non-metric fields), `value_domain_id`, and
`unit_id`.

Schema aliases and source-to-canonical field mappings belong in normalized
binding relations; they do not change metric identity.

### Software release and environment relations

`software_component` identifies a stable producer or runtime component such as
`fluvgeo`, `FluvialGeomorph-toolbox`, an R application, R itself, GDAL, or a
material geospatial library. `software_release` identifies one immutable
version/build of a component. `software_environment` identifies the
reproducible combination used for one or more accepted results, and
`software_environment_release` provides its normalized membership and role.

Minimum component fields are `software_component_id`, `component_name`,
`component_type`, and `source_authority`. Minimum release fields are
`software_release_id`, `software_component_id`, `version_label`,
`source_reference`, and `release_fingerprint`. Minimum environment fields are
`software_environment_id`, `environment_fingerprint`, `recorded_at`, and
`evidence_reference`.

`software_environment_release` has the composite key
(`software_environment_id`, `software_release_id`, `component_role`). A
`software_method_implementation` relation binds the material producing release
to the scientific method contract it claims to implement, together with
conformance status, evidence, reviewer, and acceptance date. Unknown legacy
values are explicit; they are never inferred from the load date.

### `derived_dataset`

One row represents the durable semantic slot for a governed product.

| Field | Required | Contract |
|---|---:|---|
| `derived_dataset_id` | yes | Immutable identifier. |
| `survey_event_id` | yes | Owning Survey Event. |
| `dataset_type_id` | yes | Governed feature, table, raster, or metric-family type. |
| `role_code` | yes | Governed semantic role within the Survey Event. |
| `current_dataset_edition_id` | conditional | Exactly one accepted current edition when populated. |

Candidate uniqueness is (`survey_event_id`, `dataset_type_id`, `role_code`).
The slot survives accepted correction or reanalysis; its current edition may
change.

### `derived_dataset_edition`

One row represents one analyst-accepted realization of a derived-dataset slot.

| Field | Required | Contract |
|---|---:|---|
| `dataset_edition_id` | yes | Immutable identifier. |
| `derived_dataset_id` | yes | Stable parent slot. |
| `edition_sequence` | yes | Monotonic display/order value unique within the slot; not scientific identity. |
| `scientific_method_contract_id` | conditional | Method governing interpretation; nullable only for qualified unresolved legacy evidence. |
| `dataset_schema_contract_id` | yes | Logical wide schema used by the edition. |
| `software_environment_id` | conditional | Required when known; null is permitted for qualified unresolved legacy evidence. |
| `platform_profile_id` | yes | Accepted storage/runtime profile used to create or ingest the representation. |
| `source_manifest_id` | yes | Local artifact/load-manifest evidence. |
| `content_fingerprint` | yes | Deterministic fingerprint under a declared normalization contract. |
| `method_evidence_status` | yes | `DOCUMENTED`, `INFERRED_REVIEWED`, or `UNKNOWN`. |
| `software_evidence_status` | yes | `DOCUMENTED`, `PARTIAL`, or `UNKNOWN`. |
| `validity_status` | yes | `VALID` or `INVALIDATED`; current status is not duplicated here. |
| `content_retention` | yes | `RETAINED` or `METADATA_ONLY`. |
| `accepted_by` | yes | Authorized approving identity under collection policy; authoritative desktop acceptance requires an analyst/reviewer. |
| `accepted_at` | yes | Acceptance timestamp. |
| `supersedes_dataset_edition_id` | no | Prior edition when replacement lineage applies. |
| `disposition_reason_id` | conditional | Required for supersession or invalidation. |

An edition is never created for a failed or rejected processing attempt. A
populated dataset slot's `current_dataset_edition_id` is the sole current-status
authority and must reference a `VALID`, `RETAINED` child edition. An
`INVALIDATED` edition must have `METADATA_ONLY` retention in production;
known-bad scientific feature rows and raster items are removed. Acceptance
facts and contract bindings are immutable; a later validity or retention change
is governed and audited.

An unresolved legacy edition may be accepted for preservation with a null
scientific-method or software-environment reference only when the corresponding
evidence status is `UNKNOWN`, the source artifact and schema are validated, and
the edition is excluded from scientific comparisons that require the missing
contract. FGDB never creates a fictional software version or silently infers a
method from load date. A later reviewed identification may populate a formerly
null reference and advance its evidence status only through an audited
provenance-enrichment operation; an existing non-null contract binding is never
silently overwritten.

All wide derived feature and dimension rows carry `dataset_edition_id`. Current
service views join through `derived_dataset.current_dataset_edition_id`; they
do not rely on dates, maximum sequence values, or a mutable boolean copied to
every scientific row.

`METADATA_ONLY` is the default for a valid edition after replacement unless an
approved scientific retention need exists. `RETAINED` noncurrent content may be
held in a governed historical relation, archive, or research service rather
than the current production feature classes. Its physical binding must preserve
the edition ID and must not weaken current-table uniqueness or default-service
filtering.

`dataset_edition_metric_contract` provides metric-level overrides only when a
wide edition contains mixed scientific provenance, such as a separately
approved backfill. Its key is (`dataset_edition_id`, `metric_definition_id`)
and it records the applicable scientific method contract, producing software
environment, source edition/input reference, and acceptance evidence. In the
ordinary case, every metric inherits the edition-level contracts and no
override rows are written.

## Scientific compatibility

Platform fidelity and scientific comparability are different claims. A
`scientific_compatibility_claim` relation records reviewed compatibility
between two scientific contracts at dataset, feature, or metric scope.

Minimum fields are:

- `scientific_compatibility_claim_id`;
- source and target `scientific_method_contract_id`;
- optional `metric_definition_id` for metric-scoped claims;
- `comparison_purpose_id`;
- `compatibility_status`: `EQUIVALENT`, `TOLERANCE_COMPATIBLE`,
  `TRANSFORMABLE`, `INCOMPATIBLE`, or `UNKNOWN`;
- normalized tolerance and transformation references when applicable;
- evidence and reviewer references; and
- acceptance and supersession metadata.

Compatibility is directional when a transformation is involved. An absent
claim evaluates to `UNKNOWN`, never implicitly compatible.

## Analyst-controlled update protocol

When a new Survey Event or software release is introduced:

1. Inventory the scientific method, schema, software, and platform contracts
   represented by the current editions in scope.
2. Resolve the scientific questions, feature families, and metrics to be
   compared or updated.
3. Use normalized dependency records and compatibility claims to build a
   tabular update plan with one row per proposed action.
4. Classify each action as `REUSE`, `BACKFILL`, `REPROCESS`, `CORRECT`,
   `EXCLUDE`, or `REVIEW_UNKNOWN`.
5. Present the plan and its reasons to the analyst. No action executes merely
   because a newer release exists.
6. Run selected `{fluvgeo}` scientific operations locally and write normal wide
   feature classes/tables with their contract manifest.
7. Stage and validate complete candidate replacement units in FGDB.
8. On acceptance, create the edition metadata, load its rows, change the
   current-edition pointer atomically where the platform permits, and apply the
   approved retention/disposition policy to the prior edition.
9. If the prior result is a defect correction, remove known-bad scientific rows
   and retain only invalidation/audit metadata. If it is a valid reanalysis,
   retain or remove noncurrent content according to the approved scientific
   retention need.

Adding a metric does not automatically require full historical reprocessing.
The update plan may backfill that metric from retained governed inputs when its
dependencies and contract allow it. Batch reprocessing and idempotent
replacement remain valid whenever they are simpler or scientifically safer.

## Worked lifecycle example

Assume Reach R1 has 2016 and 2028 Survey Events and both contain the governed
L1 cross-section-dimensions dataset type.

1. The metric catalog contains one row each for fields such as width, depth,
   and area. These rows are reused across Survey Events and software releases.
2. The 2016 Survey Event owns derived-dataset slot D2016-L1. Its accepted
   edition E2016-1 points to the schema observed in the legacy geodatabase. If
   its exact producing software is unknown, that reference remains null with
   `software_evidence_status = UNKNOWN`.
3. The 2028 Survey Event owns a different slot, D2028-L1. Edition E2028-1
   records the current `{fluvgeo}` environment and scientific method contract.
4. The two editions are not presumed comparable. The applicable dataset- or
   metric-scoped compatibility claims determine which change analyses are
   allowed.
5. If the analyst elects to rerun 2016 with the 2028 method, the local tools
   create ordinary wide output and FGDB stages E2016-2. Acceptance changes
   D2016-L1's current pointer from E2016-1 to E2016-2. E2016-1 becomes
   metadata-only by default or is retained outside current production content
   under an approved scientific need.
6. If E2016-1 was known to be wrong rather than merely methodologically older,
   it is marked `INVALIDATED` and its scientific rows are removed. Its minimal
   edition metadata remains to explain the correction.

The 2028 Survey Event never changes the 2016 Survey Event identity, and loading
2028 never initiates the 2016 rerun.

## Local geodatabase binding

The local output remains compact and reviewable. It carries the contract
references needed to load its wide feature classes; it does not copy the
complete enterprise registries.

The minimum relational manifest is:

- `artifact_manifest`: one row identifying the local geodatabase, Survey Event,
  creation time, and manifest contract;
- `artifact_software_component`: one row per material producer component;
- `dataset_manifest`: one row per governed feature class, table, or raster,
  naming its dataset type, role, scientific method contract, schema contract,
  source CRS, and content fingerprint; and
- `dataset_metric_binding`: one row per metric only when a wide table contains
  metrics produced under different scientific contracts or separate backfill
  provenance.

Ordinary tables produced wholly under one scientific contract inherit their
metric provenance from `dataset_manifest` and the enterprise contract
registries. This avoids gratuitous field-level metadata repetition.

## Deferred physical decisions

- exact enterprise and file-geodatabase field lengths and Esri aliases;
- the initial dataset-type and metric-definition contents for L1/L2/L3;
- normalized dependency graph relations and update-plan table fields;
- retention approval roles and duration for valid noncurrent content;
- whether selected noncurrent editions are published through separate research
  services; and
- physical transaction/compensation behavior across feature classes and mosaic
  dataset items.
