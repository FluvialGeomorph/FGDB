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
| ArcGIS Pro tools for enterprise package validation, loading, and database reconciliation | `FGDB` | accepted intended boundary |
| All computable scientific analysis and geospatial derivation functions | `fluvgeo` | accepted target boundary in ADR-0004 and ADR-0015 |
| ArcGIS Pro analyst experience, editing, and local geodatabase I/O | `FluvialGeomorph-toolbox` wrappers around `fluvgeo` | accepted target boundary in ADR-0015 |
| Shiny and future QGIS analyst experiences | Client-specific wrappers/orchestration around `fluvgeo` | accepted target boundary in ADR-0015 |
| PostgreSQL/SDE and ArcGIS Enterprise hosting operations | USACE cloud environment | accepted external operational boundary; details unknown |
| Client-specific application behavior | Applicable client repository | to be defined per integration |

The current organization boundary assigns shared R calculations to `fluvgeo`,
ArcGIS orchestration to `FluvialGeomorph-toolbox`, and Shiny orchestration to
`ohwm2`. ADR-0004 accepts a target boundary in which reusable geospatial
feature derivation also has one canonical implementation in `fluvgeo`.
Implementation and the corresponding authoritative `FG-architecture` update
remain separately scoped cross-repository work.

FGDB is the repository home for ArcGIS tools that validate, load, reconcile,
and manage enterprise records. ADR-0015 requires that analyst-facing network
documentation and longitudinal-reference creation remain local producer
capabilities in `FluvialGeomorph-toolbox`, calling canonical `fluvgeo`
algorithms, while FGDB consumes a versioned exchange package. The existing
`FluvialGeomorph-toolbox` remains the production derivation client during
transition and does not become the owner of enterprise loading logic.

## Intended data flow

```text
Desktop path:                          Self-service path:
Local terrain and survey inputs        Authenticated Shiny user
              |                                  |
              v                                  v
Optional Stream Geodatabase            Shiny inputs + derived outputs
(local segmentation/preprocessing)                |
       |                 |                        v
       |                 v             App-mediated FGDB submission
       |      FluvialGeomorph-toolbox             |
       |                 |                        |
       |                 v                        |
       |      Local features + scientific         |
       |      metadata/load package               |
       |                 |                        |
       +-----------------+------------------------+
                         v
            FGDB validation + governed loading
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
  Network Workspace, not an FGDB hierarchy entity or enterprise object. Under
  ADR-0015, a forward-looking version may store network scientific metadata
  and participate in a local exchange package. Its Stream-scale DEM and
  construction intermediates remain excluded from enterprise persistence. Its
  reviewed synthetic network crosses the loading boundary as a governed,
  time-specific Network Observation; Reach/Survey Event results and metadata
  join it through stable package identities.
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

## Scientific query boundary

The normative producer writes one Reach/Survey Event result at a time. FGDB
provides multi-Reach capability after loading through hierarchy-aware queries,
views, and services:

- Reach results retain one direct Survey Event owner;
- Stream and Study Area selection traverses explicit parent keys;
- broader-scope results do not duplicate or reassign authoritative geometry;
- temporal selection across Reaches is explicit rather than inferred from a
  shared year label; and
- method, datum/unit, validation, and provenance remain visible so clients can
  assess comparability.

A Stream or connected-watershed longitudinal profile is a composed query
product. ADR-0013 establishes a governed project longitudinal reference frame:
one project-defined Stream or Study Area/watershed mouth at zero kilometers,
selected Stream paths and Reach intervals, and Survey Event Flowline
calibrations. Existing `km_to_mouth` attributes are legacy evidence until
bound to and validated against such a frame. Temporal Survey Event selection
remains explicit. See `dev/schemas/longitudinal-reference-model.md` and
`dev/features/multiscale-scientific-query.md`.

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
- Partial/unknown legacy survey dates and revision/correction behavior.
- Physical representation and service exposure of Network Scopes, versioned
  synthetic networks, and frame-relative base-event calibration.
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
