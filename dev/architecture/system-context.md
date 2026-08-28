# FGDB system context

## Status

This document records the intended architecture established so far. Detailed
components and interfaces remain under design.

## Ownership boundary

| Capability | Owner | Status |
|---|---|---|
| Scientific and geospatial derivation workflows | `FluvialGeomorph-toolbox` and its established dependencies | verified existing boundary |
| FGDB conceptual and physical schema specifications | `FGDB` | accepted intended boundary |
| Validation and idempotent loading into the enterprise geodatabase | `FGDB` | accepted intended boundary |
| FGDB database setup and management toolbox | `FGDB` | accepted intended boundary |
| PostgreSQL/SDE and ArcGIS Enterprise hosting operations | USACE cloud environment | accepted external operational boundary; details unknown |
| Client-specific application behavior | Applicable client repository | to be defined per integration |

The current organization boundary assigns shared R calculations to `fluvgeo`,
ArcGIS orchestration to `FluvialGeomorph-toolbox`, and Shiny orchestration to
`ohwm2`. ADR-0004 accepts a target boundary in which reusable geospatial
feature derivation also has one canonical implementation in `fluvgeo`.
Implementation and the corresponding authoritative `FG-architecture` update
remain separately scoped cross-repository work.

## Intended data flow

```text
Desktop path:                          Self-service path:
Local terrain and survey inputs        Authenticated Shiny user
              |                                  |
              v                                  v
Optional Stream Geodatabase            Shiny inputs + derived outputs
(local segmentation/preprocessing)                |
              |                                  v
              v                       App-mediated FGDB submission
FluvialGeomorph-toolbox derivation                |
              |                                  |
              v                                  |
Reach-survey-event file geodatabase               |
              |                                  |
              v                                  |
FGDB validation + idempotent loading <------------+
              |
              v
PostgreSQL / Esri enterprise geodatabase
      |                       |
      v                       v
SDE feature classes     hydro DEM/REM mosaic datasets
      |                       |
      +-----------+-----------+
                  v
       ArcGIS Enterprise services
                  |
                  v
          Authorized clients
```

## Authority and lifecycle

- Local file geodatabases are production and migration inputs.
- The optional Stream Geodatabase (legacy `Site Geodatabase`) is a local
  preprocessing workspace, not an FGDB entity or load package. Its Stream-scale
  DEM, pre-segmentation synthetic network, and construction intermediates are
  excluded. Only separately governed downstream content in an accepted
  reach-survey-event package crosses the FGDB loading boundary.
- Analysts retain local inputs and preprocessing workspaces when complete
  process reconstruction is required. FGDB governs traceability of retained
  results rather than archiving every input and intermediate.
- A successful load alone is insufficient to establish authority; the loading
  workflow must verify the committed database state and retain enough
  provenance to reconcile it with its source.
- After successful loading and verification, ArcGIS Enterprise is the
  authoritative consolidated data source for the loaded content.
- Published client services are read-only. Privileged writes are mediated by
  FGDB-controlled desktop or application workflows.
- Records retain their origin workflow and lifecycle state; co-location in the
  enterprise geodatabase does not imply identical review or publication status.
- `collection` is the top-level domain and policy boundary separating the
  authoritative desktop source from the informative Shiny source.
- Both source paths use the `{fluvgeo}` scientific backend for portions of
  their derivation. Application and package versions are part of provenance.
- The schema specification and service contracts in this repository describe
  intended behavior. The deployed database and services provide operational
  evidence and must be checked for drift.

## External reference-feature and naming assistance

Geoconnex is the standard interface for discovering external hydrologic
reference features during hierarchy creation or migration. R clients use
`hydrogeofetch`; current USGS 3D Hydrography Program references are preferred
where Geoconnex coverage supports the needed feature. Product-specific
services may supplement specialized attributes or processing, but they do not
replace the governed external-reference contract. This is an advisory
read-only dependency:

- an analyst confirms, overrides, or marks a candidate unavailable/unnamed;
- FGDB stores the selected source, external ID, supplied label, service version
  or retrieval date, and disposition;
- service geometry and watershed units do not define FGDB hierarchy or AOIs;
- live external values never replace FGDB immutable IDs; and
- temporary service unavailability must have an explicit manual/deferred
  fallback and must not corrupt an established hierarchy.

The current `fluvgeo::pt_watershed_area()` NLDI processing calls are not direct
Geoconnex reference queries. Dependency migration to `hydrogeofetch` and new
Geoconnex identifier discovery are separately testable changes.

## Security boundary

The repository may define configuration schemas and deployment procedures, but
must not contain credentials, tokens, private connection files, sensitive
hostnames, or production data. Authentication, authorization, infrastructure
approval, backup, and disaster recovery requirements remain to be elicited
with the USACE hosting stakeholders.

## Open architecture questions

- Canonical entity identifiers and natural-key rules.
- Physical enforcement of collection ownership and globally unique tiered
  study-area names.
- Partial/unknown legacy survey dates, base-event representation, and
  revision/correction behavior.
- Source-to-target feature-class crosswalk and geometry constraints.
- Enterprise geodatabase dataset organization and naming conventions.
- Mosaic-dataset design, raster item identity, footprints, overviews, and
  source-file lifecycle.
- Transaction boundaries, load manifests, idempotency keys, and rollback.
- Feature service grouping, query/edit permissions, versioning, and publishing
  workflow.
- Development, test, staging, and production environment topology.
- Drift detection, monitoring, backup, recovery, and operational ownership.
- Shiny save/restore payload, authentication delegation, in-place edit
  concurrency, sharing, and retention semantics.
- Cross-repository implementation planning and organization-architecture update
  for canonical open-source feature derivation accepted by ADR-0004.
