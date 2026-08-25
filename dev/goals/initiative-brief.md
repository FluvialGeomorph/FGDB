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
system that supports multiple study areas and observations through time.

## Domain hierarchy

The starting domain model is:

```text
Study Area
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
- Allow new work to use the new model while legacy project data is migrated
  incrementally without stopping current work.
- Maintain a clear crosswalk from legacy project folders and reach-survey-event
  file geodatabases to the FGDB model.
- Align terminology with the FG User Manual, including the transition from
  `Site` to `Stream` where applicable.

## Constraints and principles

- The legacy `/FluvialGeomorph/Projects/` structure remains operational during
  migration.
- Migration is stepwise and pay-as-you-go; it must not require a big-bang
  conversion.
- Local derivation workflows remain part of the starting operating model.
- Database loads must be safely repeatable.
- Folder structure should express the domain model but must not substitute for
  explicit database identity and integrity rules.
- Existing repositories retain ownership of their established capabilities
  unless an explicit cross-repository decision changes an ownership boundary.

## Open success criteria

Measurable success criteria will be defined during design. At minimum they
need to address data integrity, repeatable ingestion, provenance, migration
traceability, query usefulness, and operational recovery.

## Explicitly unresolved

- Which data classes FGDB will store directly versus reference externally.
- The authoritative source for each metadata and feature field.
- Database technology, spatial extensions, hosting, and access model.
- Whether this repository will be an R package, another type of software
  project, or a combination of code and declarative contracts.
- Canonical identifiers, naming rules, versioning, and survey-event semantics.
- The relationship between filesystem organization and database organization.
- Integration contracts with `FluvialGeomorph-toolbox`, `fluvgeo`, `ohwm2`,
  manuals, and future consumers.

