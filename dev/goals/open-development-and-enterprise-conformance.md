# Open development and enterprise conformance requirements

## Status and authority

- Status: accepted design baseline
- Date: 2026-09-02
- Governing decisions: ADR-0001, ADR-0015, ADR-0018, ADR-0019, and ADR-0020

This document converts the accepted local-first, geodatabase-first, and
service-mediated architecture into testable project goals and design
requirements. It defines required outcomes, not an implementation claim.

## Goals

### G1. License-independent normal development

A contributor can develop and test scientific functions, local relational
outputs, FGDB validation, and Feature Service client behavior without an
ArcGIS Pro license, an ArcPy installation, or access to the USACE network.

### G2. One open scientific implementation

`fluvgeo` remains the canonical implementation of scientific derivation,
topology, calibration, reconstruction, and scientific validation. ArcGIS Pro,
Shiny, direct R, and future QGIS experiences use the same functions and
relations rather than maintaining different scientific implementations.

### G3. Direct relational interchange

Accepted scientific outputs are feature classes and tables whose object
meaning is stable across file geodatabase, GeoPackage, PostgreSQL/PostGIS, and
enterprise SDE bindings. Storage adapters may differ, but they do not introduce
a second scientific schema or an unrelated serialization model.

### G4. Service-mediated enterprise use

User-facing FGDB and Shiny tools read and write through governed ArcGIS Portal
Feature Services using the R-ArcGIS package ecosystem. Viewer applications use
read-only service access. ArcGIS Pro is not required for routine application
access to an already provisioned FGDB deployment.

### G5. A narrow licensed administration boundary

ArcPy and licensed ArcGIS execution are limited to enterprise provisioning,
SDE/geodatabase configuration, mosaic datasets, registered data stores,
referenced service publication, and conformance checks that supported web GIS
interfaces cannot perform.

### G6. Evidence-based cross-platform conformance

Tests begin with provenance-documented outputs governed through `fluvgeodata`.
The project verifies scientific, relational, storage, service, and licensed
ArcGIS behavior at the layer capable of making each claim; no single storage
driver is treated as an oracle for the entire system.

### G7. Progressive removal of proprietary client dependencies

New scientific and routine data-management capabilities default to open R and
GDAL implementations. Proprietary dependencies must be isolated, justified by
a specific unsupported platform operation, and replaceable without changing
the scientific or logical data contracts.

### G8. Demonstrated cross-platform type fidelity

Every supported R, file geodatabase, GeoPackage, Feature Service,
PostgreSQL/PostGIS, SDE, and raster boundary has an explicit, versioned type
crosswalk and value-bearing conformance evidence. Successful I/O alone never
establishes scientific equivalence.

### G9. Controlled adaptation to platform change

New platform, driver, library, service, database, and format versions can be
discovered and evaluated without silently changing accepted contracts. Unknown
or drifted profiles fail safely, while immutable historical profiles preserve
the interpretation and migration path of existing scientific data.

### G10. Interpretable results across scientific change

Every accepted result identifies its scientific method, logical schema,
producing software, and storage profile. Feature-specific dimensions remain
typed wide relations, while an in-database metric catalog preserves meaning
across releases. Analysts explicitly approve historical correction, backfill,
or reanalysis; a software upgrade never initiates it automatically.

## Component requirements

### Scientific producer

- **REQ-SCI-001:** `fluvgeo` shall own all reusable scientific calculations,
  geospatial derivation, topology, calibration, reconstruction, and scientific
  validation.
- **REQ-SCI-002:** Scientific functions shall accept and return R data frames,
  tibbles, `sf`, or raster objects with explicit schemas and invariants.
- **REQ-SCI-003:** A scientific operation shall complete locally without an
  FGDB connection and shall not require ArcGIS Pro when an open implementation
  exists.
- **REQ-SCI-004:** Loading data into FGDB shall never trigger scientific
  derivation, reconstruction, snapping, segmentation, calibration, or base-
  event selection as a hidden side effect.
- **REQ-SCI-005:** Client wrappers shall not contain independent scientific
  implementations.
- **REQ-SCI-006:** Feature-specific dimension outputs shall remain typed wide
  relations unless a separate accepted decision changes their canonical
  representation.
- **REQ-SCI-007:** Every dimension field shall bind to a stable
  `dimension_metric_definition` and an applicable versioned scientific method
  contract.
- **REQ-SCI-008:** Software release, scientific method, output schema, and
  platform profile shall have independent identities and version lifecycles.
- **REQ-SCI-009:** New software shall not automatically rerun or mutate prior
  Survey Event results. Update tooling shall produce an analyst-reviewable,
  tabular dependency and action plan.
- **REQ-SCI-010:** Batch reprocessing with validated idempotent replacement
  shall remain an accepted strategy for aligning historical results when the
  analyst determines it is scientifically appropriate.

### Local relational storage

- **REQ-LOC-001:** Producer tooling shall write analyst-reviewable feature
  classes and tables that implement the accepted logical relations for the
  applicable Study Area/Stream or Reach–Survey Event geodatabase.
- **REQ-LOC-002:** The local relations shall match their enterprise scientific
  counterparts as closely as practical. Differences shall be limited to
  documented storage-engine fields, enterprise authorization and audit,
  administration, and deliberate local editing aids.
- **REQ-LOC-003:** The file-geodatabase vector binding shall use GDAL
  OpenFileGDB where its installed capabilities satisfy the contract. Code and
  tests shall request and verify the intended driver rather than assume that a
  `.gdb` suffix selects a particular implementation.
- **REQ-LOC-004:** Storage code shall detect required GDAL driver capabilities
  and fail with an actionable message when they are unavailable.
- **REQ-LOC-005:** File-geodatabase round trips shall preserve, within the
  documented binding, relation and field names, supported field types,
  geometry type and dimensionality, CRS, stable identifiers, null semantics,
  row meaning, and relationship keys.
- **REQ-LOC-006:** GeoPackage may implement the same logical relations for
  Shiny, direct R, and future QGIS clients. A GeoPackage binding shall not
  change object identity, ownership, or scientific meaning.
- **REQ-LOC-007:** Local write operations shall use temporary or staged output
  and verification where necessary to avoid presenting a partial relational
  dataset as complete.
- **REQ-LOC-008:** Each governed local database shall carry relational artifact,
  producer-component, and dataset manifest tables sufficient to bind every
  output to its scientific and schema contracts. Metric-level bindings are
  required only when one wide table contains mixed calculation provenance.

### Raster interchange

- **REQ-RAS-001:** Scientific raster products shall have an open, testable
  local representation. GeoTIFF or Cloud Optimized GeoTIFF is the default
  interchange binding unless a later accepted raster decision selects another
  open format.
- **REQ-RAS-002:** Raster conformance shall verify CRS, horizontal and vertical
  reference metadata, extent, resolution, alignment, dimensions, data type,
  NoData semantics, and representative values.
- **REQ-RAS-003:** Lack of GDAL file-geodatabase raster creation shall not
  block scientific processing or ordinary local tests.
- **REQ-RAS-004:** Loading accepted `hydro_dem` and REM products into enterprise
  mosaic datasets is an FGDB administrative/deployment operation, not a
  scientific derivation step.

### Platform type fidelity

- **REQ-TYP-001:** Each governed field shall declare a canonical logical type
  independently from its R or storage representation.
- **REQ-TYP-002:** Each supported platform binding shall explicitly define the
  physical type, subtype, width, precision, scale, nullability, default,
  constraint, read/write R representation, and material creation options.
- **REQ-TYP-003:** Geometry bindings shall explicitly define geometry family,
  multipart rules, XY/Z/M dimensionality, null and empty behavior, CRS, axis
  order, precision grid, tolerance, and curve handling.
- **REQ-TYP-004:** Raster bindings shall explicitly define pixel type, NoData
  and NaN behavior, bands, grid alignment, extent, resolution, CRS, vertical
  reference, units, compression, and enterprise mosaic dataset item mapping.
- **REQ-TYP-005:** Constraint bindings shall distinguish native enforcement,
  emulation, application validation, documentation-only behavior, and lack of
  support for keys, uniqueness, domains, defaults, relationships, and indexes.
- **REQ-TYP-006:** Storage and service adapters shall prohibit silent coercion,
  truncation, precision loss, identifier mutation, geometry-dimensionality
  loss, and unapproved constraint loss.
- **REQ-TYP-007:** Known lossy mappings require a field-specific approved
  transform, scientific justification, tolerance or recovery rule, and
  provenance. Otherwise the binding is unsupported.
- **REQ-TYP-008:** Round-trip tests shall contain values selected to expose
  numeric, text, date/time, UUID, missing-value, geometry, CRS, and constraint
  conversion failures.
- **REQ-TYP-009:** Every conformance result shall identify the logical schema,
  crosswalk, platforms, transformation path, software and driver versions,
  creation options, evidence source, and execution class.
- **REQ-TYP-010:** The crosswalk and conformance records shall be maintained as
  machine-readable relations loadable as R data frames; narrative documentation
  alone is insufficient.
- **REQ-TYP-011:** Platform-generated fields shall be explicitly classified and
  shall not substitute for governed scientific identity.
- **REQ-TYP-012:** The term **mosaic dataset** shall identify the Esri
  geodatabase data type used to manage enterprise raster collections. The terms
  *raster mosaic* and *mosaicking* shall be reserved for a combined raster image
  and the operation that creates or dynamically renders one.

### FGDB R client and service access

- **REQ-SVC-001:** FGDB user-facing R tooling shall use the supported
  `{arcgis}` ecosystem, currently principally `{arcgislayers}` and
  `{arcgisutils}`, for Portal authentication and Feature Service operations.
- **REQ-SVC-002:** FGDB shall wrap third-party service calls behind versioned
  FGDB contracts so package changes or REST details do not leak into the
  scientific schema.
- **REQ-SVC-003:** Viewer applications shall use query-only authorization.
  Controlled FGDB and Shiny writers shall use separately authorized edit
  capabilities appropriate to their collection and operation.
- **REQ-SVC-004:** Before any enterprise write, FGDB shall validate the
  scientific relations, reconcile governed identities, validate service schema
  compatibility, and establish the intended create, edit, or correction unit.
- **REQ-SVC-005:** After a write, FGDB shall verify the committed service state
  and record sufficient load evidence to reconcile it with the local source.
- **REQ-SVC-006:** Desktop correction shall preserve idempotent replacement of
  one governed unit. Shiny editing shall preserve stable identities and its
  accepted collection-specific mutation policy.
- **REQ-SVC-007:** A partial multi-relation service edit shall not be reported
  as a successful load. Transaction, compensation, staging, or rollback
  behavior shall be specified before the enterprise loader is production-ready.
- **REQ-SVC-008:** Applications shall not connect directly to PostgreSQL RDS or
  modify SDE system tables.
- **REQ-SVC-009:** Service URLs, tokens, client secrets, connection files, and
  environment-specific identifiers shall remain outside version control.
- **REQ-SVC-010:** Every populated derived-dataset slot shall identify exactly
  one valid, retained current edition. Default services shall expose only rows
  belonging to current editions.
- **REQ-SVC-011:** Invalidating an edition shall remove its known-bad scientific
  rows and raster items from production while retaining sufficient metadata to
  explain the correction. Valid noncurrent content shall be retained only under
  an approved scientific policy and excluded from default services.

### Enterprise administration

- **REQ-ADM-001:** FGDB admin-facing tooling shall reproducibly scaffold and
  configure a new FGDB enterprise instance from versioned schema and service
  specifications.
- **REQ-ADM-002:** ArcPy may be used only for an identified administration or
  conformance operation that is not adequately exposed by the supported R and
  web GIS interfaces.
- **REQ-ADM-003:** ArcPy code shall remain a thin infrastructure adapter and
  shall not define an independent logical schema or scientific algorithm.
- **REQ-ADM-004:** Administrative operations shall run only in an approved,
  appropriately licensed environment and shall obtain restricted configuration
  and credentials at runtime.
- **REQ-ADM-005:** Provisioning shall verify the resulting SDE objects,
  registered-data-store state, mosaic datasets, Portal items, service
  capabilities, and permissions against the versioned contracts.

### Compatibility evolution

- **REQ-EVO-001:** Logical schemas, logical types, platform profiles, bindings,
  transforms, adapters, conformance suites, and migrations shall have distinct
  immutable version identities.
- **REQ-EVO-002:** Platform profiles shall record material product, format,
  driver, library, database/service, option, and capability information without
  storing sensitive environment configuration.
- **REQ-EVO-003:** Runtime capability probes shall supplement version checks and
  detect material default or behavior drift.
- **REQ-EVO-004:** FGDB shall maintain a directional compatibility matrix
  joining logical schema, source and destination profiles, transform, adapter,
  conformance suite, execution lane, and support status.
- **REQ-EVO-005:** A new or materially changed platform profile shall begin as
  `unverified` and shall not write governed production data until explicitly
  accepted from applicable conformance evidence.
- **REQ-EVO-006:** Drift or failed conformance shall block affected writes. Any
  continued read-only recovery shall use an explicit qualified profile.
- **REQ-EVO-007:** Accepted compatibility records shall be superseded, not
  rewritten, so prior data provenance remains interpretable.
- **REQ-EVO-008:** Schema and binding changes shall use explicit migrations with
  source and destination versions, preconditions, transforms, loss class,
  validation, recovery, and approval.
- **REQ-EVO-009:** Each environment shall declare one accepted write profile per
  applicable contract; multiple accepted read profiles may support historical
  data and migrations.
- **REQ-EVO-010:** Platform and dependency upgrades shall follow the governed
  observe, diff, classify, test, review, accept, migrate, and release workflow.
- **REQ-EVO-011:** Conformance tests shall be selectable by affected logical
  type, feature family, platform boundary, capability, and execution lane.
- **REQ-EVO-012:** Deprecation and retirement shall define a support window,
  affected-data inventory, migration or recovery path, and approval.

## Verification requirements

- **REQ-TST-001:** R packages shall use `testthat` and standard R package
  checks for deterministic unit and integration tests.
- **REQ-TST-002:** Shared geospatial test inputs shall be direct,
  provenance-documented producer outputs governed through `fluvgeodata`.
- **REQ-TST-003:** Local tests may copy real outputs to temporary storage or
  make a minimal in-memory mutation beside an assertion; they shall not commit
  invented geospatial datasets as substitute evidence.
- **REQ-TST-004:** Every supported vector storage binding shall have a
  write-read-validate round-trip test driven by the same logical relations.
- **REQ-TST-005:** FGDB shall test relational constraints, replacement,
  transactions, rollback or compensation, and hierarchy-aware queries against
  an ephemeral or otherwise isolated PostgreSQL/PostGIS environment before the
  enterprise loader is considered complete.
- **REQ-TST-006:** Feature Service request construction, pagination, batching,
  error handling, retry safety, and response validation shall be testable
  offline with controlled HTTP responses.
- **REQ-TST-007:** Live Portal tests shall run only in an approved integration
  environment and shall use nonproduction test services and identities.
- **REQ-TST-008:** A licensed ArcGIS conformance lane shall verify only claims
  that require ArcGIS, including SDE registration, Esri-managed schema
  behavior, mosaic datasets, publication, permissions, and round-trip client
  compatibility.
- **REQ-TST-009:** External-service unavailability shall be reported separately
  from deterministic code regressions. Tests shall not silently convert an
  unavailable required service into a pass.
- **REQ-TST-010:** Each conformance result shall identify the data evidence,
  schema version, package versions, storage driver and version, execution
  environment, and whether the result is deterministic, mocked, or live.

## Development and release gates

### Gate A: Scientific contract

- Producer relations and invariants are accepted.
- `fluvgeo` implements the scientific constructor and validator.
- Tests pass against direct `fluvgeodata` evidence.
- Logical types and scientific invariants have immutable version identities.

### Gate B: Local persistence contract

- Accepted feature classes and tables round-trip through the required local
  binding.
- Raster products round-trip through the accepted open raster binding.
- Any binding loss or storage-specific mapping is documented and tested.
- Field, geometry, raster, and constraint bindings have accepted crosswalk rows
  and value-bearing boundary tests.
- The runtime platform profile passes capability probes and is an accepted
  write profile for the local contract.

### Gate C: FGDB client contract

- FGDB validates and maps approved local relations without scientific changes.
- Offline service tests cover request, response, failure, retry, and partial-
  load behavior.
- PostgreSQL/PostGIS tests prove relational and replacement semantics.
- Service, database, adapter, and transform profiles are represented in the
  directional compatibility matrix.

### Gate D: Licensed enterprise conformance

- Admin tooling provisions the schema and services in a nonproduction USACE
  environment.
- Controlled loads, queries, corrections, permissions, mosaic datasets, and audit
  evidence pass against the deployed contract.

### Gate E: Production readiness

- Deployment, secrets, backup, recovery, monitoring, drift detection, and
  operational ownership are approved.
- No production write path depends on an untested scientific or storage
  translation.

## Success criteria

This architecture succeeds when all of the following are demonstrated:

1. A contributor without ArcGIS Pro can run the deterministic `{fluvgeo}` and
   `{FGDB}` development suites from real project evidence.
2. An accepted set of local Stream or Reach–Survey Event relations can be
   written and read through its supported open vector binding without changing
   scientific identity or row meaning.
3. Accepted raster products can be produced and validated without writing a
   file-geodatabase raster.
4. The FGDB R client can validate, submit, verify, and reconcile a controlled
   Feature Service load in a nonproduction enterprise environment.
5. A correction can replace exactly one governed desktop unit without leaving
   known-bad or partial rows queryable as current data.
6. A Shiny user can create or edit permitted informative-collection content
   under a stable identity without receiving unrestricted access to
   authoritative content.
7. Read-only viewers can query the supported FGDB hierarchy and derived
   geometry exclusively through Portal services.
8. Admin tooling can reproduce and verify the SDE schema, mosaic datasets,
   registered data store, services, and capability assignments in a licensed
   integration environment.
9. The same scientific relations and identifiers can be traced from direct
   producer evidence through local storage, enterprise loading, and service
   query results.
10. ArcGIS-specific failures are isolated to the licensed conformance lane and
    do not prevent ordinary open-source development.
11. File geodatabase, GeoPackage, Feature Service, PostgreSQL/PostGIS, SDE, and
    raster conversions either preserve each accepted scientific contract or
    fail before data is accepted or published.
12. A platform or dependency upgrade can be evaluated as a new profile, with
    affected tests selected and executed, without changing prior accepted
    contracts or the scientific interpretation of existing data.
13. A result produced by any supported historical or current workflow can be
    resolved from its dataset edition to the exact metric definitions,
    scientific method, logical schema, software environment, source manifest,
    and platform profile that govern its interpretation.
14. An analyst can review a tabular update plan and explicitly choose reuse,
    backfill, reprocessing, correction, exclusion, or unresolved review for
    each affected historical result; installing newer software performs none
    of those actions by itself.

## Non-goals

- Reimplement or emulate SDE system behavior in R or GDAL.
- Treat GDAL success as proof of ArcGIS Enterprise compatibility.
- Treat successful conversion or readability as proof that scientific field,
  geometry, constraint, or raster semantics survived.
- Make ArcGIS Pro-free enterprise administration an immediate requirement.
- Duplicate `fluvgeo` scientific behavior in FGDB, ArcPy, Shiny, or client
  wrappers.
- Give viewers, analysts, or applications general-purpose edit access to the
  enterprise database.
- Require local scientific geodatabases to contain enterprise-only
  authorization, load-audit, rollback, or service-publication relations.
- Promise indefinite read or write support for every historical platform
  version without an approved support and migration policy.
