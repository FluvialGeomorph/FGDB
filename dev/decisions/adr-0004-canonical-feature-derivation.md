# ADR-0004: Canonical reusable feature derivation in fluvgeo

- Status: accepted
- Date: 2026-08-25
- Clarified by: ADR-0018

## Context

The ecosystem's original division of labor assigned early geospatial feature
creation to Esri Python tools in `FluvialGeomorph-toolbox` and fluvial
geomorphic calculations to the `{fluvgeo}` R package. Browser-based clients
cannot rely on desktop ArcPy processing, so reusable open-source feature
derivation has also developed in `{fluvgeo}`.

This has created parallel implementations that can produce conceptually
similar features without one shared behavioral contract. For example:

- `_05a_Flowline.py` dissolves an edited stream network by `ReachName`, applies
  Esri PAEK line smoothing, and can emit one feature per reach name.
- `fluvgeo::flowline()` requires one already drawn line, assigns `ReachName`,
  checks its CRS against a DEM, and orients it upstream using endpoint
  elevations. It does not dissolve a network or apply PAEK smoothing.

These are complementary partial pipelines, not equivalent implementations.
Uncontrolled differences in derivation could be misinterpreted as physical
change when FGDB is analyzed across survey events or collections.

The current organization boundary assigns shared R calculations to `fluvgeo`
and ArcGIS geoprocessing orchestration to `FluvialGeomorph-toolbox`.
`fluvgeo`'s maintained architecture already prefers open-source implementations
when they satisfy scientific and operational requirements, while recognizing
that current coverage is partial.

The divergence increased over time because the original desktop workflow
automated the feasible stages and relied on manual editing elsewhere. Later
production experience revealed opportunities to reorder stages, automate
manual interventions, and catch recurring errors. Shiny development began
with that accumulated knowledge and required a portable backend, so its
`fluvgeo`-based workflow adopted the streamlined order rather than reproducing
the older desktop sequence.

## Decision

- `fluvgeo` becomes the canonical owner of reusable geospatial feature
  derivation and fluvial geomorphic calculation contracts used by both desktop
  and browser clients.
- `FluvialGeomorph-toolbox` continues to own ArcGIS Pro orchestration,
  geodatabase I/O, symbology, messages, and other desktop-specific integration.
  It calls canonical `{fluvgeo}` functions rather than maintaining an
  independent scientific derivation implementation where migration is viable.
- Shiny applications continue to own interactive and reactive orchestration
  while calling the same canonical `{fluvgeo}` contracts.
- The canonical end-to-end feature workflow is completed in `fluvgeo` first,
  using Shiny requirements and use as an early proving ground while keeping the
  R functions independent of Shiny session state.
- During that buildout, the production desktop workflow remains supported and
  is not repeatedly interrupted by partial cutovers. Individual open-source
  capabilities are still designed and verified incrementally.
- After the canonical pipeline covers the required workflow and passes
  scientific review, contract tests, representative comparison, performance
  assessment, and integration verification, the desktop toolbox is overhauled
  in a coordinated migration to call the R pipeline for all viable derivation
  and calculation stages.
- In the target architecture, ArcGIS Pro is an optional expert editing and
  workflow client rather than the required geospatial processing engine.
  Equivalent adapters such as a future QGIS toolbox can call the same backend.
- ArcGIS Enterprise remains the required Esri component for enterprise
  database deployment and service delivery. Esri desktop licensing is no
  longer intended to be an initial requirement for running the canonical
  analysis backend.
- Exact numeric or vertex-for-vertex reproduction is not assumed to be the
  correct acceptance criterion. Where an open-source algorithm differs from an
  Esri algorithm such as PAEK smoothing, maintainers must define scientifically
  acceptable invariants and tolerances and explicitly approve any methodology
  change.
- FGDB records derivation engine/method and version provenance so legacy and
  canonical outputs can be interpreted correctly over time.

## Consequences

- Reusable scientific/spatial logic has one implementation and test authority,
  reducing desktop/browser drift.
- The ArcGIS toolbox remains valuable as the expert desktop workflow rather
  than becoming the owner of duplicate algorithms.
- `fluvgeo` needs new feature-level input/output schemas, deterministic tests
  driven by representative direct producer outputs governed through
  `fluvgeodata`, scientific acceptance criteria, and release discipline.
- Desktop migration requires an explicit R invocation and geodatabase adapter
  strategy for each tool.
- The streamlined workflow order, automation boundaries, and remaining manual
  review points must be specified before desktop cutover.
- QGIS support becomes a client-adapter project rather than a second scientific
  implementation.
- Some ArcPy capabilities may remain temporarily or permanently when no
  replacement satisfies scientific, performance, licensing, or operational
  requirements; exceptions must be documented rather than silently duplicated.
- Legacy FGDB loads require method/version provenance, even when their outputs
  predate the canonical implementation.

## Approval and scope

This direction was accepted for FGDB design on 2026-08-25. It changes
capability boundaries across `fluvgeo`,
`FluvialGeomorph-toolbox`, Shiny clients, FGDB, documentation, and
`FG-architecture`. Implementing those changes remains separately scoped
cross-repository work and must follow the organization cross-repository
workflow, including updates to the authoritative owning repositories.
