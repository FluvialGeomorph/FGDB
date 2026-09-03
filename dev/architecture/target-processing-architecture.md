# Target feature-processing architecture

## Purpose

Define the accepted long-term processing direction on which FGDB data
consistency depends. This is a target architecture, not a claim about current
implementation completeness.

## Functional division of labor

| Component | Target responsibility |
|---|---|
| `{fluvgeo}` | Canonical, client-independent implementation of all computable scientific analysis and geospatial derivation functions, validation contracts, and reusable reporting logic |
| Shiny applications | Local-first browser interaction, small-area self-service orchestration, presentation, relational data creation, and optional FGDB save/restore integration |
| ArcGIS Pro toolbox | Optional expert editing experience, desktop orchestration, and geodatabase adapters that call canonical R functions |
| Future QGIS toolbox | Optional open-source desktop editing and orchestration adapter calling the same canonical R functions |
| FGDB user-facing tooling | R service clients built on `{arcgis}`, principally `{arcgislayers}` and `{arcgisutils}`, for validation, controlled ingestion, replacement/edit policies, reconciliation, and governed data access |
| FGDB admin-facing tooling | Repeatable SDE schema, mosaic dataset, registered-data-store, and service configuration; ArcPy is used where licensed ArcGIS administration is required |
| FGDB compatibility infrastructure | Versioned logical types, platform profiles, bindings, transforms, migrations, capability probes, compatibility matrix, and conformance harness |
| ArcGIS Enterprise | USACE private-cloud deployment, Portal, registered PostgreSQL RDS/SDE data source, authoritative data services, authorization, and scalable client delivery |

This direction refines, but does not silently rewrite, the current
`FG-architecture` records. The organization catalog must be updated through a
separately scoped cross-repository change when implementation planning begins.

## Target flow

```text
                           +---------------------+
Shiny application --------|                     |
                           |                     |
ArcGIS Pro adapter --------|      fluvgeo        |---> local feature classes + tables
                           | all scientific      |               |
Future QGIS adapter -------| processing and      |               v optional
                           | validation          |       FGDB service loader
Batch/other client --------|                     |               |
                           +---------------------+               v
                                                   Portal Feature Services
                                                     /              \
                                                    v                v
                                      authorized FGDB/Shiny      read-only viewers
                                              writes
```

Client adapters may collect inputs, support editing, display progress, and
translate native formats. They do not independently redefine reusable feature
derivation or scientific calculation behavior.

## Transition strategy

### Phase 1: Preserve production and inventory divergence

- Keep the working ArcGIS desktop production workflow available.
- Inventory every automated and manual step, its inputs/outputs, ordering,
  failure modes, and downstream consumers.
- Map ArcPy stages to existing, partial, or missing `{fluvgeo}` capabilities.

### Phase 2: Complete the canonical open-source pipeline

- Implement missing capabilities in `{fluvgeo}` as client-independent
  functions with explicit schemas and scientific invariants.
- Use Shiny workflows to exercise the streamlined order and error handling.
- Build representative, provenance-documented test evidence from direct
  producer outputs and record method/version provenance from the start.
- Avoid partial production cutovers that would repeatedly disrupt analysts.

### Phase 3: Validate the coherent replacement workflow

- Verify individual feature contracts and the complete workflow.
- Evaluate scientific validity, error detection, topology, downstream metric
  sensitivity, performance at desktop scales, and operational recovery.
- Document intentional differences from legacy Esri algorithms and their
  implications for longitudinal analysis.

### Phase 4: Coordinated ArcGIS Pro cutover

- Refactor the toolbox into an editing/orchestration and format-adapter layer.
- Call canonical `{fluvgeo}` functions for every scientific processing stage;
  retain only client-specific editing, UI, and format-I/O behavior in the
  ArcGIS adapter.
- Preserve an explicit rollback path during transition.
- Retire duplicate ArcPy derivations only after production acceptance.

### Phase 5: Additional clients

- Implement QGIS or other clients against the same versioned contracts without
  duplicating scientific logic.

## FGDB dependency

FGDB can begin schema and migration design before this transition completes,
but it must:

- identify the derivation method and version for legacy and future content;
- avoid assuming legacy desktop and current Shiny feature geometries are
  methodologically equivalent;
- support collection-specific governance while preserving shared hierarchy;
- define feature contracts jointly with the canonical `fluvgeo` outputs; and
- distinguish actual geomorphic change from processing-method changes.

Local-first analysis produces complete local feature classes, tables, and scientific metadata
before the optional FGDB boundary. FGDB loading must not be embedded inside a
`fluvgeo` scientific function or required to complete a Shiny, ArcGIS Pro,
direct-R, or future QGIS analysis.

FGDB application access crosses the enterprise boundary through authenticated
Portal services. Ordinary R loading and querying do not require ArcGIS Pro.
Licensed ArcPy administration is isolated to provisioning and configuration
that supported web GIS interfaces cannot perform. See ADR-0020.
