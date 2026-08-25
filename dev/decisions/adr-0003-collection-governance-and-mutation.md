# ADR-0003: Collection-scoped governance and mutation semantics

- Status: accepted
- Date: 2026-08-25

## Context

FGDB receives content from two workflows that share much of the `{fluvgeo}`
scientific backend but serve different audiences and purposes:

- experienced GIS analysts create rigorously reviewed, customer-facing
  reach-survey-event datasets with the desktop `FluvialGeomorph-toolbox`; and
- general USACE users create smaller, informative analyses in browser-based
  Shiny applications.

Treating the source merely as provenance would not express the different
visibility, QA, and correction policies. A single append-only revision model
would also retain desktop-derived geometry known to be wrong, while forcing
desktop replacement semantics onto interactive Shiny records would make
ordinary self-service editing unnecessarily cumbersome.

## Decision

- `collection` is the top-level FGDB domain object and policy boundary.
- The initial model has distinct desktop and Shiny collections. Their exact
  physical representation and naming are deferred to the logical schema.
- The desktop collection is expert-produced and authoritative. It follows a
  rigorous QA workflow before publication.
- The Shiny collection is general-user-produced and informative. Valid saved
  content may be visible immediately under its applicable authorization rules.
- Desktop loading is idempotent at the reach-survey-event unit:
  - an identical repeat is a no-op;
  - a corrected input replaces all active records belonging to that
    reach-survey-event as one logically atomic operation; and
  - erroneous superseded feature geometry and attributes are not retained as
    queryable production history.
- Replacement audit metadata may record who replaced what, when, why, and from
  which load manifest without preserving the erroneous feature records in the
  active data model.
- Shiny content uses in-place editing under stable entity identifiers, with
  updated attribution and timestamps. Detailed concurrency and audit behavior
  remain to be designed.
- Study areas have immutable identifiers and globally unique, human-readable
  names governed by a tiered naming convention. Global uniqueness spans the
  collections so a dropdown selection is unambiguous.
- Both collections record `{fluvgeo}` and originating-application versions.
  Shared calculation code does not erase collection-specific authority or QA
  meaning.

## Consequences

- Collection identity participates in governance, validation, service
  publication, and authorization, not just lineage.
- The database and loader need an explicit ownership key that identifies every
  row and raster item belonging to a desktop reach-survey-event replacement
  unit.
- Desktop replacement must stage and validate a complete candidate before
  removing active records. Failure must leave or restore the prior consistent
  state.
- Coordinating feature-class replacement with mosaic-dataset items may require
  staged publication, compensating actions, and reconciliation because all
  Esri operations may not share one PostgreSQL transaction.
- Load manifests and operational backups remain necessary, but neither should
  expose known-bad geometry as a valid historical observation.
- Shiny editing requires authorization and concurrency rules even though it
  does not require the desktop QA lifecycle.
- The naming convention must be formalized before study-area creation tools or
  dropdown contracts can be finalized.

