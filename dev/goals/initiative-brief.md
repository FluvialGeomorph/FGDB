# FGDB initiative brief

## Status and source

This is an initial working brief derived from
[`FG-Tech-Manual/DB-migration.qmd`](../../../FG-Tech-Manual/DB-migration.qmd),
reviewed on 2026-08-25. It records user-provided direction, not a completed
system design. The technical-manual chapter remains authoritative for its own
published content; accepted FGDB decisions and contracts will live in this
repository.

## Purpose

Develop the FluvialGeomorph Database (FGDB) initiative to consolidate
independently maintained, site-oriented analysis datasets into a coherent
ArcGIS Enterprise geodatabase that supports multiple study areas and
observations through time. FGDB will be the single authoritative data source
for geospatial content derived using the `FluvialGeomorph-toolbox` tools.

The initiative also externalizes a design problem that had become too large to
hold reliably in one developer's working memory while maintaining continuous
production operations. Versioned evidence, crosswalks, decisions, schemas, and
review records will make interacting scientific, technical, operational,
historical, and deployment requirements collectively tractable.

## Initial repository scope

This repository has two initial responsibilities:

1. Document the FGDB design process and maintain its specifications.
2. Contain an ArcGIS toolbox and supporting functions for database setup,
   repeatable data loading, and subsequent database management.
3. Assemble and preserve relevant historical requirements, schema prototypes,
   production examples, and workflow evidence so fragmented prior work can be
   evaluated through one unified design process.

These responsibilities may be separated into different repositories later if
their size, release cycles, access boundaries, or maintenance needs make the
combined repository impractical.

## Domain hierarchy

The starting domain model has `Collection` as its top-level object and policy
boundary. Beneath each collection, it continues through study area, stream,
reach, survey event, and FG feature content.

```text
Collection
└── Study Area
    └── Stream
        └── Reach
            └── Survey Event
                └── FG Features
```

A reach-survey-event geodatabase represents derived conditions for one reach
at one point in time. Its feature content can include terrain, hydrography,
flowline, cross-section, bankfull, bankline, valley, and related derived
datasets.

## Desired outcomes

- Establish stable identities and relationships for study areas, streams,
  reaches, survey events, and their derived FG features.
- Support repeat observations of a reach without conflating survey events.
- Enable idempotent loading of locally processed artifacts into a central
  database system.
- Publish database feature classes to client applications through a defined
  set of ArcGIS Feature Layer services.
- Store DEM and REM raster content through enterprise mosaic datasets.
- Allow new work to use the new model while legacy project data is migrated
  incrementally without stopping current work.
- Maintain a clear crosswalk from legacy project folders and reach-survey-event
  file geodatabases to the FGDB model.
- Align terminology with the FG User Manual, including the transition from
  `Site` to `Stream` where applicable.
- Prevent differences between desktop and browser derivation implementations
  from being misinterpreted as fluvial change, using canonical contracts,
  validation, and method/version provenance.
- Support an open-source canonical processing backend so ArcGIS Pro is an
  optional expert editing client, future QGIS integration is feasible, and
  ArcGIS Enterprise is the required Esri dependency only at the enterprise
  deployment and service boundary.
- Let previous and future customers discover and inspect derived geometry for
  delivered analyses, including repeat survey events used to assess change
  through time.
- Let authenticated USACE Shiny users save a small-area self-service analysis,
  find it again by map or study-area selection, and resume or review it in a
  later session.
- Make design evidence and dependencies traceable enough that the team can
  review decisions from its scientific, technical, operational, program, and
  documentation perspectives without relying on one person's memory.

## Constraints and principles

- The legacy `/FluvialGeomorph/Projects/` structure remains operational during
  migration.
- Migration is stepwise and pay-as-you-go; it must not require a big-bang
  conversion.
- Local derivation workflows remain part of the starting operating model.
- Database loads must be safely repeatable.
- The desktop collection uses idempotent reach-survey-event replacement:
  corrected loads remove and replace the prior active records rather than
  preserving known-bad feature data as queryable history.
- The Shiny collection permits valid content to be visible immediately and
  uses in-place editing under stable identities.
- Study-area names are globally unique, human-readable values governed by a
  tiered naming convention; immutable IDs provide unambiguous identity.
- Client-facing Feature Layer services are read-only. Creation, correction,
  replacement, and retirement occur only through controlled FGDB write
  workflows.
- Reports, maps, and export files remain outside FGDB's authoritative database
  scope initially; FGDB makes their associated derived geometry accessible but
  does not replace the delivered report archive.
- Folder structure should express the domain model but must not substitute for
  explicit database identity and integrity rules.
- Existing repositories retain ownership of their established capabilities
  unless an explicit cross-repository decision changes an ownership boundary.
- The target is the USACE cloud-hosted ArcGIS Enterprise suite, with an Esri
  enterprise geodatabase backed by PostgreSQL and managed through ArcGIS SDE
  capabilities.
- Credentials, connection files, server names, and other environment-specific
  or sensitive configuration must remain outside version control.
- Historical artifacts are evidence, not automatically authoritative
  specifications. Their accepted meaning must be captured in maintained goals,
  architecture, decisions, schemas, features, and workflows.

## Open success criteria

Measurable success criteria will be defined during design. At minimum they
need to address data integrity, repeatable ingestion, provenance, migration
traceability, query usefulness, and operational recovery.

## Explicitly unresolved

- The authoritative source for each metadata and feature field.
- Exact feature-class, table, relationship, domain, subtype, topology, mosaic,
  and indexing designs.
- ArcGIS service boundaries, editing rules, permissions, and client contracts.
- The implementation form of the FGDB setup and data-management toolbox.
- Ownership, editing concurrency, sharing, and retention rules for self-service
  Shiny analyses.
- Customer authorization and service-partitioning requirements.
- Canonical identifiers, naming rules, versioning, and survey-event semantics.
- The relationship between filesystem organization and database organization.
- Integration contracts with `FluvialGeomorph-toolbox`, `fluvgeo`, `ohwm2`,
  manuals, and future consumers.
