# ADR-0001: ArcGIS Enterprise system and repository boundary

- Status: accepted
- Date: 2026-08-25

## Context

`FluvialGeomorph-toolbox` analyses currently produce independent local
file-geodatabase datasets for individual reach survey events. FGDB needs to
consolidate those outputs, preserve their spatial and temporal relationships,
and make them consistently available to client applications. The initiative
also needs a durable home for its design specification and for operational
database tooling.

## Decision

- The USACE cloud-hosted ArcGIS Enterprise suite will provide the operational
  system of record for geospatial content derived using
  `FluvialGeomorph-toolbox` tools.
- The enterprise geodatabase will use PostgreSQL as its database platform and
  Esri SDE-managed database objects.
- Vector and tabular content will be stored in enterprise feature classes and
  related database objects.
- DEM and REM raster content will be managed through enterprise mosaic
  datasets.
- Client applications will access published content through a defined series
  of ArcGIS Feature Layer services and any additional raster-capable service
  types required by the eventual mosaic dataset design.
- The FGDB repository will initially own both:
  1. design records and specifications for the database; and
  2. an ArcGIS toolbox and supporting functions for database creation, loading,
     and management.
- `FluvialGeomorph-toolbox` retains ownership of the scientific derivation
  workflows that produce source content. FGDB owns the contract and operations
  that validate and load that content into the enterprise system.
- The documentation and operational tooling may be separated later through a
  new decision if the combined ownership boundary becomes unwieldy.

## Consequences

- Schema design must account for Esri geodatabase behavior as well as
  PostgreSQL storage; a generic PostGIS-only design is not sufficient.
- Idempotent ingestion, provenance, validation, and reconciliation are core
  product behavior rather than one-time migration utilities.
- The design must explicitly cover both vector/tabular feature content and
  raster content managed through enterprise mosaic datasets.
- Published-service contracts are part of the system design and must be
  versioned alongside database schema contracts.
- Environment provisioning, database administration, ArcGIS Server
  publication, permissions, and credentials cross organizational and security
  boundaries. Repository automation must keep sensitive and
  environment-specific values out of version control.
- Local file geodatabases remain processing and migration inputs; they are not
  the authoritative consolidated source after successful loading and
  verification.
- Reports, maps, exports, and other non-database artifacts are not assigned a
  storage design by this decision and require explicit treatment if they are to
  be included in FGDB's authoritative scope.
