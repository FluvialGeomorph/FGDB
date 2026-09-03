# Platform type crosswalk and conformance specification

## Purpose

Define how FGDB records and verifies the representation of governed data across
R, `sf`, GDAL/OGR, Esri file geodatabase, OGC GeoPackage, ArcGIS Feature
Services, PostgreSQL/PostGIS, and Esri SDE. This specification implements
ADR-0021.

The crosswalk is part of the physical schema. It shall ultimately be maintained
as version-controlled machine-readable tables that R can load as data frames.
Markdown may explain the contract but shall not be the only executable source
of accepted mappings.

## Separation of concerns

The framework distinguishes four contracts:

| Contract | Governs |
|---|---|
| Logical field type | Scientific meaning, valid values, units, precision, nullability, and identity role independent of storage |
| Physical platform binding | Exact field or geometry representation and creation options on one platform |
| Boundary transform | Approved conversion between two bindings, including loss, tolerance, and recovery rules |
| Conformance evidence | A value-bearing test of one boundary or operational round trip under identified software versions |

No physical platform binding is the canonical scientific definition.

## Version identities

The registry keeps these versions independent:

| Version | Changes when |
|---|---|
| Logical schema version | A relation, field, ownership rule, or scientific invariant changes |
| Logical type version | A reusable value, unit, precision, null, or encoding rule changes |
| Platform profile version | A material platform, driver, library, service, database, option, or capability combination changes |
| Binding version | A logical-to-physical representation changes |
| Transform version | A directional conversion implementation or rule changes |
| Adapter version | Executable read, write, validation, or service behavior changes |
| Conformance-suite version | Test values, assertions, tolerances, or required paths change |
| Migration version | A source-to-destination contract migration changes |

Versions are immutable after acceptance. New records use explicit
`supersedes_id` links. A data instance retains the versions under which it was
created, validated, transformed, and loaded.

## Required crosswalk relations

All repeated values are normalized into child relations. Version lists, option
maps, capability results, migration steps, conformance paths, and assertion
differences shall not be stored as opaque JSON, delimited text, or list columns.

### `platform_profile`

One row identifies one material runtime profile. Profiles are more specific
than product names but exclude secrets and environment-specific endpoints.

| Field | Required | Meaning |
|---|---:|---|
| `platform_profile_id` | yes | Immutable profile identifier |
| `platform_family` | yes | R, GDAL/OGR, OpenFileGDB, GeoPackage, PostgreSQL/PostGIS, FeatureService, SDE, or mosaic dataset |
| `platform_version` | yes | Product, standard, API, or format version |
| `capability_contract_id` | yes | Required capability-probe specification |
| `support_status` | yes | `candidate`, `unverified`, `accepted-read`, `accepted-write`, `deprecated`, `blocked`, `unsupported`, or `retired` |
| `supersedes_id` | conditional | Earlier profile replaced by this profile |
| `accepted_at` | conditional | Acceptance date/time |
| `notes` | conditional | Scope and known limitations |

### `platform_profile_component`

One row identifies one material component and version in a platform profile.

| Field | Required | Meaning |
|---|---:|---|
| `platform_profile_id` | yes | Parent profile |
| `component_role` | yes | Runtime, driver, library, database extension, server, client, or standard |
| `component_name` | yes | Stable component name |
| `component_version` | yes | Observed version |

### `platform_profile_option`

One row identifies one non-secret material option in a platform profile.

| Field | Required | Meaning |
|---|---:|---|
| `platform_profile_id` | yes | Parent profile |
| `option_scope` | yes | Dataset, layer, field, geometry, raster, connection, or service |
| `option_name` | yes | Stable option name |
| `option_value` | yes | Canonical non-secret value |

### `capability_observation`

One row represents one execution of the capability probes against a platform
profile candidate or accepted profile.

| Field | Required | Meaning |
|---|---:|---|
| `capability_observation_id` | yes | Observation identity |
| `platform_profile_id` | yes | Profile evaluated |
| `probe_contract_id` | yes | Versioned probe suite |
| `drift_from_profile` | yes | Whether observed behavior differs from the accepted profile |
| `executed_at` | yes | UTC execution time |
| `execution_class` | yes | Deterministic local, open integration, or licensed ArcGIS integration |

### `capability_observation_result`

One row represents one observed capability or material default.

| Field | Required | Meaning |
|---|---:|---|
| `capability_observation_id` | yes | Parent observation |
| `capability_id` | yes | Stable capability or default identifier |
| `expected_value` | conditional | Accepted-profile value when comparing drift |
| `observed_value` | yes | Canonical observed value |
| `result` | yes | Pass, fail, changed, unsupported, or not applicable |

### `logical_field_type`

One row represents one reusable canonical logical type.

| Field | Required | Meaning |
|---|---:|---|
| `logical_type_id` | yes | Immutable identifier such as `uuid`, `int32_count`, `float64_measure`, `text_code`, `date_partial`, or `datetime_utc` |
| `logical_type_version` | yes | Immutable rule version |
| `value_kind` | yes | Boolean, signed integer, real, decimal, text, UUID, date, datetime, binary, or another accepted kind |
| `units_policy` | yes | Unitless, fixed unit, per-field unit, or controlled vocabulary |
| `precision_rule` | yes | Exact range or accepted precision/tolerance rule |
| `null_rule` | yes | Whether missing is prohibited, allowed, qualified, or structurally inapplicable |
| `encoding_rule` | conditional | Unicode normalization, date/time, UUID, or binary encoding rule |
| `description` | yes | Scientific and operational meaning |
| `status` | yes | Proposed, accepted, deprecated, or superseded |
| `supersedes_id` | conditional | Earlier logical type version |

### `field_binding`

One row represents one field's physical representation on one platform for one
schema version. Reusable defaults may be inherited from a logical type, but the
resolved field binding must be inspectable.

| Field | Required | Meaning |
|---|---:|---|
| `field_binding_id` | yes | Immutable binding identity |
| `binding_version` | yes | Immutable binding version |
| `schema_id` | yes | Owning logical/physical schema identifier |
| `schema_version` | yes | Contract version |
| `relation_name` | yes | Feature class or table |
| `field_name` | yes | Canonical field name |
| `logical_type_id` | yes | Canonical logical type |
| `platform_profile_id` | yes | Exact R, OGR, FileGDB, GeoPackage, FeatureService, PostgreSQL, or SDE profile |
| `physical_type` | yes | Exact platform type |
| `subtype` | conditional | OGR, Esri, PostgreSQL, or application subtype |
| `width` | conditional | Maximum length or storage width |
| `precision` | conditional | Numeric precision |
| `scale` | conditional | Numeric scale |
| `nullable` | yes | Physical nullability |
| `default_expression` | conditional | Platform default or generated-value rule |
| `domain_or_constraint` | conditional | Domain, check, range, code list, or application validation identifier |
| `creation_options` | conditional | Exact driver or platform options needed to create the binding |
| `read_representation` | yes | Expected R class and attributes after reading |
| `write_representation` | yes | Required R class and attributes before writing |
| `loss_class` | yes | `lossless`, `tolerance_bounded`, `qualified_loss`, `unsupported`, or `unverified` |
| `notes` | conditional | Known platform behavior and restrictions |
| `supersedes_id` | conditional | Earlier binding replaced by this version |

### `geometry_binding`

One row represents the geometry contract for one feature class on one platform.

| Field | Required | Meaning |
|---|---:|---|
| `geometry_binding_id` | yes | Immutable binding identity |
| `binding_version` | yes | Immutable binding version |
| `schema_id` | yes | Owning schema |
| `schema_version` | yes | Owning schema version |
| `relation_name` | yes | Bound feature class |
| `platform_profile_id` | yes | Exact platform profile |
| `geometry_family` | yes | Point, multipoint, polyline, polygon, or accepted collection |
| `multipart_rule` | yes | Required, allowed, or prohibited |
| `dimension` | yes | XY, XYZ, XYM, or XYZM |
| `geometry_nullable` | yes | Whether null geometry is allowed |
| `empty_geometry_rule` | yes | Allowed representation and round-trip expectation |
| `crs_contract_id` | yes | Governed horizontal/vertical CRS and transformation contract |
| `axis_order_rule` | yes | Coordinate order expected by the adapter |
| `xy_resolution` | conditional | XY coordinate precision grid resolution |
| `z_resolution` | conditional | Z coordinate precision grid resolution |
| `m_resolution` | conditional | M coordinate precision grid resolution |
| `xy_tolerance` | conditional | XY platform tolerance |
| `z_tolerance` | conditional | Z platform tolerance |
| `m_tolerance` | conditional | M platform tolerance |
| `curve_rule` | yes | Preserve, densify under tolerance, prohibit, or unsupported |
| `loss_class` | yes | Same controlled values as `field_binding` |
| `creation_options` | conditional | Driver and layer options |

### `constraint_binding`

One row represents how one logical constraint is handled on one platform.

| Field | Required | Meaning |
|---|---:|---|
| `constraint_binding_id` | yes | Immutable binding identity |
| `binding_version` | yes | Immutable binding version |
| `constraint_id` | yes | Stable logical constraint identifier |
| `relation_name` | yes | Owning relation |
| `constraint_kind` | yes | Primary key, foreign key, unique, check, domain, index, relationship, or generated value |
| `platform_profile_id` | yes | Exact physical platform profile |
| `implementation` | yes | Native, trigger, application validation, emulated, documented only, or unsupported |
| `physical_name` | conditional | Platform object name |
| `validation_query_or_rule` | yes | Executable verification reference |
| `loss_class` | yes | Fidelity classification |
| `supersedes_id` | conditional | Earlier constraint binding |

### `raster_binding`

One row represents one governed raster product's binding on one platform. A
raster artifact and an enterprise mosaic dataset item are different objects and
must have distinct bindings.

| Field | Required | Meaning |
|---|---:|---|
| `raster_binding_id` | yes | Immutable binding identity |
| `binding_version` | yes | Immutable binding version |
| `raster_contract_id` | yes | Governed raster product contract |
| `platform_profile_id` | yes | Exact R raster, GDAL raster, GeoTIFF/COG, SDE raster item, or mosaic dataset profile |
| `pixel_type` | yes | Exact numeric representation |
| `nodata_rule` | yes | Sentinel, mask, NaN, or prohibited |
| `band_rule` | yes | Count, order, names, and interpretation |
| `grid_rule` | yes | Dimensions, resolution, origin/alignment, and extent |
| `crs_contract_id` | yes | Horizontal and vertical reference contract |
| `units` | yes | Cell-value units |
| `compression` | conditional | Compression and material options |
| `item_mapping` | conditional | Mosaic dataset item fields, identity, and source lifecycle mapping |
| `loss_class` | yes | Fidelity classification |
| `supersedes_id` | conditional | Earlier raster binding |

### `boundary_transform`

One row represents one approved directional conversion between two platform
bindings.

| Field | Required | Meaning |
|---|---:|---|
| `transform_id` | yes | Stable transform identifier |
| `transform_version` | yes | Immutable directional transform version |
| `source_binding_id` | yes | Directional source binding |
| `destination_binding_id` | yes | Directional destination binding |
| `implementation_id` | yes | Owning R/GDAL/ArcGIS adapter |
| `implementation_version` | yes | Exact adapter version |
| `precondition_contract_id` | yes | Required source properties and supported range |
| `conversion_rule` | yes | Explicit type, value, geometry, CRS, or constraint conversion |
| `loss_class` | yes | Fidelity classification |
| `tolerance_or_recovery_rule` | conditional | Accepted error bound or reversible encoding |
| `approval_reference` | conditional | Required for `qualified_loss` |
| `supersedes_id` | conditional | Earlier directional transform |

### `compatibility_matrix`

One row represents one directional support claim for one logical schema and
execution lane.

| Field | Required | Meaning |
|---|---:|---|
| `compatibility_claim_id` | yes | Immutable support-claim identity |
| `logical_schema_id` | yes | Schema identity under test |
| `logical_schema_version` | yes | Schema under test |
| `source_platform_profile_id` | yes | Exact source profile |
| `destination_platform_profile_id` | yes | Exact destination profile |
| `transform_id` | yes | Approved directional conversion |
| `transform_version` | yes | Approved transform version |
| `adapter_id` | yes | Executable implementation identity |
| `adapter_version` | yes | Executable implementation version |
| `conformance_suite_version` | yes | Required evidence contract |
| `execution_lane` | yes | Local, open integration, mocked service, or licensed ArcGIS |
| `support_status` | yes | `unverified`, `accepted-read`, `accepted-write`, `deprecated`, `blocked`, `unsupported`, or `retired` |
| `latest_conformance_result_id` | conditional | Most recent applicable evidence |
| `supersedes_id` | conditional | Earlier support claim |

### `contract_migration`

One row represents an explicit migration between schema, binding, or platform
profile versions.

| Field | Required | Meaning |
|---|---:|---|
| `migration_id` | yes | Immutable migration identity |
| `migration_version` | yes | Immutable migration version |
| `source_schema_id` | yes | Required source schema |
| `source_schema_version` | yes | Required source schema version |
| `destination_schema_id` | yes | Resulting schema |
| `destination_schema_version` | yes | Resulting schema version |
| `precondition_contract_id` | yes | Executable required-source-state contract |
| `loss_class` | yes | Expected fidelity classification |
| `validation_contract_id` | yes | Post-migration verification |
| `reversibility` | yes | Reversible, compensatable, restore-from-source, or irreversible |
| `recovery_rule` | yes | Required failure and rollback behavior |
| `approval_reference` | conditional | Required for qualified loss or irreversible change |
| `supersedes_id` | conditional | Earlier migration version |

### `contract_migration_binding`

One row binds a required source or destination platform binding to a migration.

| Field | Required | Meaning |
|---|---:|---|
| `migration_id` | yes | Parent migration identity |
| `migration_version` | yes | Parent migration version |
| `binding_role` | yes | Source or destination |
| `binding_kind` | yes | Field, geometry, constraint, raster, or platform profile |
| `binding_id` | yes | Exact required binding identity |
| `binding_version` | yes | Exact required binding version |

### `contract_migration_step`

One row represents one ordered executable migration step.

| Field | Required | Meaning |
|---|---:|---|
| `migration_id` | yes | Parent migration identity |
| `migration_version` | yes | Parent migration version |
| `step_order` | yes | Positive integer execution order |
| `transform_id` | yes | Exact transform identity |
| `transform_version` | yes | Exact transform version |
| `validation_contract_id` | yes | Step-level postcondition |

### `conformance_result`

One row represents one executed boundary or round-trip assertion group.

| Field | Required | Meaning |
|---|---:|---|
| `conformance_result_id` | yes | Result identity |
| `test_contract_id` | yes | Test specification identity |
| `test_contract_version` | yes | Exact test specification version |
| `schema_id` | yes | Logical schema identity under test |
| `schema_version` | yes | Logical schema under test |
| `crosswalk_id` | yes | Platform crosswalk identity under test |
| `crosswalk_version` | yes | Platform crosswalk under test |
| `evidence_id` | yes | `fluvgeodata` or other governed source evidence |
| `execution_class` | yes | Deterministic local, mocked service, live open integration, or licensed ArcGIS integration |
| `result` | yes | Pass, fail, blocked, or not applicable |
| `summary` | conditional | Human-readable result summary; detailed differences are assertion rows |
| `executed_at` | yes | UTC execution time |

### `conformance_path_step`

One row identifies one ordered boundary step exercised by a conformance result.

| Field | Required | Meaning |
|---|---:|---|
| `conformance_result_id` | yes | Parent result |
| `step_order` | yes | Positive integer path order |
| `platform_profile_id` | yes | Exact runtime profile at this step |
| `capability_observation_id` | yes | Runtime probe result |
| `binding_id` | conditional | Exact field, geometry, constraint, or raster binding identity |
| `binding_version` | conditional | Exact binding version |
| `transform_id` | conditional | Directional transform used to enter this step |
| `transform_version` | conditional | Exact transform version |
| `adapter_id` | yes | Executable adapter identity |
| `adapter_version` | yes | Exact adapter version |

Material options are inherited through the related `platform_profile_option`
rows rather than copied into an opaque result value.

### `conformance_assertion_result`

One row represents one value, schema, constraint, geometry, raster, or
scientific-invariant assertion.

| Field | Required | Meaning |
|---|---:|---|
| `conformance_result_id` | yes | Parent result |
| `assertion_id` | yes | Versioned assertion identity |
| `relation_name` | conditional | Relation under test |
| `field_or_property_name` | conditional | Field, geometry, raster, or constraint property |
| `expected_value` | conditional | Canonical expected value |
| `observed_value` | conditional | Canonical observed value |
| `tolerance_rule_id` | conditional | Accepted comparison tolerance |
| `result` | yes | Pass, fail, blocked, or not applicable |
| `difference_class` | conditional | Classified difference |

## Compatibility support states

| State | Meaning | Write behavior |
|---|---|---|
| `candidate` | Profile was discovered but not fully characterized | Prohibited |
| `unverified` | Binding exists but required evidence is incomplete | Prohibited |
| `accepted-read` | Approved for the specified read/recovery scope | Prohibited |
| `accepted-write` | Approved environment write profile | Permitted for contracted paths |
| `deprecated` | Still supported during a declared migration window | New use restricted by policy |
| `blocked` | Drift or failure invalidated an earlier claim | Prohibited |
| `unsupported` | Cannot satisfy the contract | Prohibited |
| `retired` | Support window ended | Prohibited except approved recovery |

One environment has one declared `accepted-write` profile for each applicable
contract. Multiple `accepted-read` profiles may coexist to support historical
data and migrations.

Environment-specific paths, hosts, credentials, and tokens are not stored in
any compatibility relation.

## Fidelity classes

| Class | Meaning | Release treatment |
|---|---|---|
| `lossless` | All contracted values and properties survive exactly | Allowed when tests pass |
| `tolerance_bounded` | Numeric or geometric change remains within an accepted scientific tolerance | Allowed only with explicit tolerance tests |
| `qualified_loss` | A documented property is lost or transformed without changing approved scientific use | Requires field-specific approval and provenance |
| `unsupported` | The platform cannot represent the contract | Binding prohibited |
| `unverified` | Representation may exist but lacks sufficient evidence | Binding not production-ready |

Readable is not a fidelity class. A conversion that completes without an error
remains `unverified` until its contracted properties are compared.

## Minimum boundary-value profile

Each applicable logical type shall be tested with ordinary and boundary values:

- missing values and qualified unknowns;
- zero, negative, positive, minimum, and maximum accepted numeric values;
- floating-point values chosen to expose precision and scale changes;
- `NaN`, positive infinity, and negative infinity when the source can contain
  them, with explicit rejection when the contract prohibits them;
- empty, one-character, maximum accepted length, Unicode, and normalization-
  sensitive text;
- lower-, upper-, and mixed-case stable UUID text plus the physical GUID
  binding where adopted;
- leap-day dates, unknown month/day encodings where allowed, UTC datetimes, and
  daylight-saving boundaries where local time enters an interface;
- single and multipart geometries, repeated vertices, orientation-sensitive
  lines, polygon holes, null/empty geometry where allowed, and Z/M values where
  contracted;
- coordinates near the accepted spatial domain and values sensitive to
  resolution, tolerance, axis order, and datum transformation.

## Required test paths

The matrix is expanded per relation and feature family. The minimum paths are:

| Path | Execution lane | Purpose |
|---|---|---|
| R/`sf` -> OpenFileGDB -> R/`sf` | deterministic local | File geodatabase write/read fidelity |
| R/`sf` -> GeoPackage -> R/`sf` | deterministic local | Native open-storage fidelity |
| FileGDB -> R/`sf` -> GeoPackage -> R/`sf` | deterministic local | Migration from retained Esri output into open storage |
| GeoPackage -> R/`sf` -> OpenFileGDB -> R/`sf` | deterministic local | Return to the desktop Esri interchange binding |
| R relations -> PostgreSQL/PostGIS -> R relations | isolated open integration | Relational types, constraints, transactions, and queries |
| R relations -> mocked Feature Service -> R relations | deterministic offline | Esri JSON, request, response, error, and pagination contracts |
| Accepted local relations -> live Feature Service -> SDE -> Feature Service -> R | licensed integration | Operational enterprise round trip |
| Open raster artifact -> mosaic dataset item -> raster-capable service read | licensed integration | Raster identity, metadata, values, rendering inputs, and lifecycle |

Additional direct boundaries are required whenever an operational workflow
bypasses one of these intermediate representations.

## Comparison layers

Every round trip compares all applicable layers:

1. Dataset inventory and relation identity.
2. Field inventory, order policy, canonical names, aliases, and physical names.
3. R classes and exact physical field types.
4. Nullability, missing-value counts, and qualified-unknown encodings.
5. Exact categorical, text, date, identifier, and integer values.
6. Floating-point values under field-specific absolute, relative, or unit-aware
   tolerances.
7. Geometry family, feature count, multipart status, validity, emptiness,
   XY/Z/M dimensionality, CRS, coordinate precision, and topology invariants.
8. Keys, uniqueness, relationships, domains, defaults, and indexes according to
   each platform's enforcement class.
9. Scientific invariants owned by the applicable `fluvgeo` validator.
10. Platform-generated fields, which are classified and excluded from governed
    identity comparisons unless explicitly contracted.

## Initial high-risk mappings

The following mappings must remain `unverified` until a feature-specific
crosswalk and boundary test accepts them:

- R double values used for integers, especially values beyond exact IEEE-754
  integer range;
- 64-bit integer and object-ID behavior across older and newer ArcGIS clients;
- UUID/GUID/GlobalID representations and case normalization;
- `Date`, `POSIXct`, time zone, and partial Survey Event date representation;
- logical values represented as integer or text codes;
- `NA`, `NaN`, infinity, database `NULL`, raster NoData, and masks;
- text width, Unicode normalization, empty string versus null, field aliases,
  and field-name case;
- XY/Z/M dimensionality, geometry collections, true curves, empty geometries,
  coordinate resolution, and geodatabase tolerance;
- CRS WKT dialect, EPSG/WKID aliases, axis order, vertical CRS, and datum
  transformations;
- coded and range domains, defaults, relationship classes, foreign keys,
  unique constraints, and indexes;
- raster pixel type, scale/offset, NoData, compression, statistics, overviews,
  footprints, and mosaic dataset item properties.

## Evidence basis

- [GDAL OpenFileGDB driver](https://gdal.org/en/stable/drivers/vector/openfilegdb.html)
  documents versioned write support, creation options, coordinate precision,
  domains, relationships, and 64-bit integer behavior.
- [OGC GeoPackage Encoding Standard](https://www.ogc.org/standards/geopackage/)
  governs the open GeoPackage encoding and integrity requirements.
- [ArcGIS field data types](https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/overview/arcgis-field-data-types.htm)
  defines ArcGIS-visible field types and compatibility constraints.
- [Esri mosaic datasets](https://pro.arcgis.com/en/pro-app/latest/help/data/imagery/mosaic-datasets.htm)
  defines the enterprise raster-management dataset meant by this project.

## Unresolved work

1. Select the machine-readable file format and R loader for these relations.
2. Define canonical logical types used by the hierarchy and Stream Network
   schemas before filling their platform binding rows.
3. Extract observed field and geometry types from direct `fluvgeodata` file
   geodatabases and compare them with the XML workspace evidence.
4. Establish the GeoPackage profile and determine which geodatabase constraints
   require application validation or extensions.
5. Establish the ArcGIS Enterprise/SDE and Feature Service profiles in a
   licensed nonproduction environment.
6. Define field-specific scientific tolerances with the owning `fluvgeo`
   validators.
7. Specify the `hydro_dem` and REM mosaic dataset item contract separately from
   open raster artifact bindings.
