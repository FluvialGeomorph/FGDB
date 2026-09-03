# Scientific contract reference data

- Status: draft for design review
- Updated: 2026-09-02
- Scope: reusable identifiers referenced by scientific-result contracts

## Purpose

This specification defines the small reference layer needed before concrete
feature contracts can instantiate ADR-0023. These relations describe governed
dataset types, measurement units, value domains, and null semantics. They are
not observations, derived features, or another level of the Study Area → Stream
→ Reach → Survey Event hierarchy.

## `dataset_type`

One row represents one stable kind of governed dataset, such as Flowline,
Flowline Points, L1 Cross-section Dimensions, hydro-modified DEM, or Stream
Network segments.

| Field | Required | Contract |
|---|---:|---|
| `dataset_type_id` | yes | Immutable identifier. |
| `dataset_type_code` | yes | Unique stable uppercase code; never a display label. |
| `preferred_label` | yes | Analyst-facing name. |
| `definition` | yes | Scientific or operational meaning of one dataset of this type. |
| `representation_kind` | yes | `FEATURE_CLASS`, `TABLE`, `RASTER_DATASET`, or `MOSAIC_DATASET_ITEM`. |
| `feature_concept_id` | no | Qualified ontology concept when the dataset represents features of one governed type. |
| `lifecycle_status` | yes | `DRAFT`, `ACTIVE`, `DEPRECATED`, or `RETIRED`. |
| `replaced_by_dataset_type_id` | no | Explicit successor when meaning changes. |

A dataset type is not a physical table name. A
`dataset_schema_contract` binds it to one versioned logical relation, and
platform bindings map that relation to file geodatabase, GeoPackage,
PostgreSQL/SDE, and Feature Service representations.

## `measurement_unit`

One row represents one governed unit used by a metric, parameter, coordinate,
or tolerance.

| Field | Required | Contract |
|---|---:|---|
| `unit_id` | yes | Immutable identifier. |
| `unit_code` | yes | Unique canonical code. |
| `preferred_label` | yes | Human-readable label. |
| `symbol` | yes | Display symbol. |
| `quantity_kind_id` | yes | Length, area, elevation, slope, ratio, or another governed quantity kind. |
| `ucum_code` | no | UCUM mapping when valid for the unit. |
| `qudt_iri` | no | QUDT mapping when adopted by the USACE ontology framework. |
| `lifecycle_status` | yes | Governed lifecycle state. |

Conversions require separately tested conversion rules. Sharing a quantity kind
does not by itself authorize conversion, and horizontal length units do not
define vertical datum or elevation units.

## `value_domain` and `value_domain_member`

`value_domain` defines one reusable enumeration or bounded numeric rule.
`value_domain_member` contains one row per permissible enumerated value. The
domain is the semantic source even when an Esri coded-value domain mirrors it
for editing.

Minimum `value_domain` fields are `value_domain_id`, `domain_code`,
`definition`, `domain_kind`, `version`, `lifecycle_status`, and
`supersedes_value_domain_id`.

Minimum `value_domain_member` fields are `value_domain_id`, `member_code`,
`preferred_label`, `definition`, `sort_order`, `lifecycle_status`, and
`replaced_by_member_code`.

## `null_semantics`

One row defines why a governed field may be null. Null remains the stored value;
sentinel numbers and strings are prohibited.

| Code | Meaning |
|---|---|
| `NOT_ALLOWED` | Every accepted row must have a value. |
| `UNKNOWN` | The value exists conceptually but available evidence does not establish it. |
| `NOT_OBSERVED` | The workflow did not observe or collect the value. |
| `NOT_CALCULATED` | Applicable calculation was not performed. |
| `NOT_APPLICABLE` | The concept does not apply to this row. |
| `SOURCE_UNAVAILABLE` | Calculation or verification could not proceed because its required source was unavailable. |

The physical schema may need a companion reason field when more than one null
meaning is valid for the same column. A nullable field without a declared null
contract is incomplete.

## Initial instantiated dataset type

The first concrete row is:

| `dataset_type_code` | `preferred_label` | `representation_kind` | Definition |
|---|---|---|---|
| `FLOWLINE` | Flowline | `FEATURE_CLASS` | One Survey Event-specific polyline representing the likely flow path through one governed Reach; it is not asserted to be a surveyed thalweg. |

Its detailed contract is maintained in `flowline-feature-contract.md`.
