# ADR-0002: Controlled write paths and read-only client services

- Status: accepted
- Date: 2026-08-25
- Superseded in part by: ADR-0020

## Context

FGDB must support both large, professionally produced desktop datasets and
small self-service analyses created in USACE Shiny applications. Customers and
other clients need convenient access to derived geometry, but unrestricted
editing through published services would bypass validation, provenance,
idempotency, and lifecycle controls.

## Decision

- Client-facing ArcGIS Feature Layer services are read-only.
- Desktop data enters FGDB through an FGDB-owned ArcGIS Pro toolbox workflow
  that performs controlled preflight, loading, verification, and load-manifest
  recording.
- Shiny data enters FGDB through an authenticated application-mediated
  workflow that enforces the same shared schema and provenance contracts while
  allowing use-case-specific validation.
- End users do not receive a general-purpose feature-editing path to the
  authoritative datasets.
- Every stored analysis records its origin workflow and lifecycle/validation
  state so different production and review paths remain explicit.
- The exact integration mechanism for each controlled writer—database
  connection, geoprocessing service, feature service, API, or another
  approved interface—will be selected after security, transaction, and hosting
  requirements are known.

## Consequences

- FGDB requires at least two ingestion adapters but one coherent identity,
  provenance, and lifecycle model.
- Shiny persistence is a cross-repository change: FGDB owns the persistence
  contract and `ohwm2` owns integration with its reactive workflow.
- Service publication must separate read contracts from privileged write
  operations.
- A user's ability to view a record does not imply authority to modify,
  publish, or retire it.
- Collection-specific authority, visibility, and mutation semantics are defined
  by ADR-0003; detailed authorization rules remain required before physical
  schema and service design can be finalized.
