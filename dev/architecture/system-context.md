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
| R clients for enterprise validation, loading, reconciliation, and governed access through Portal Feature Services | `FGDB`, using `{arcgis}` / `{arcgislayers}` / `{arcgisutils}` | accepted target boundary in ADR-0020 |
| Licensed enterprise schema, SDE, mosaic dataset, registered-data-store, and service administration | FGDB admin tooling, using ArcPy where required | accepted target boundary in ADR-0020 |
| All computable scientific analysis and geospatial derivation functions | `fluvgeo` | accepted target boundary in ADR-0004 and ADR-0015 |
| ArcGIS Pro analyst experience, editing, and local geodatabase I/O | `FluvialGeomorph-toolbox` wrappers around `fluvgeo` | accepted target boundary in ADR-0015 |
| Shiny and future QGIS analyst experiences | Client-specific wrappers/orchestration around `fluvgeo` | accepted target boundary in ADR-0015 |
| PostgreSQL RDS/SDE and ArcGIS Enterprise hosting operations | USACE private cloud, currently AWS GovCloud IL4 | accepted external operational boundary; environment-specific details remain external |
| Client-specific application behavior | Applicable client repository | to be defined per integration |

The current organization boundary assigns shared R calculations to `fluvgeo`,
ArcGIS orchestration to `FluvialGeomorph-toolbox`, and Shiny orchestration to
`ohwm2`. ADR-0004 accepts a target boundary in which reusable geospatial
feature derivation also has one canonical implementation in `fluvgeo`.
Implementation and the corresponding authoritative `FG-architecture` update
remain separately scoped cross-repository work.

FGDB is the repository home for R tools that validate, load, reconcile, and
manage enterprise records through authenticated Portal Feature Services, and
for admin tooling that provisions and configures the SDE-backed deployment.
ArcPy is limited to licensed administrative operations for which supported web
GIS interfaces are insufficient. ADR-0015 requires that analyst-facing network
documentation and longitudinal-reference creation remain local producer
capabilities in `FluvialGeomorph-toolbox`, calling canonical `fluvgeo`
algorithms, while FGDB loads analyst-approved geodatabase relations. The existing
`FluvialGeomorph-toolbox` remains the production derivation client during
transition and does not become the owner of enterprise loading logic.

## Intended data flow

```text
Desktop path:                          Self-service path:
Local terrain and survey inputs        Authenticated Shiny user
              |                                  |
              v                                  v
Study Area/Stream Geodatabase           Shiny relational inputs + outputs
(feature classes and tables)                       |
       |                 |                        v
       |                 v             App-mediated FGDB load
       |      FluvialGeomorph-toolbox             |
       |                 |                        |
       |                 v                        |
       |      Local features + scientific         |
       |      metadata tables                     |
       |                 |                        |
       +-----------------+------------------------+
                         v
             FGDB R validation + governed loading
                         |
                         v
        authenticated Portal Feature Services
                         |
                         v
     PostgreSQL RDS / Esri enterprise geodatabase
              |                          |
              v                          v
     SDE feature classes        hydro DEM/REM mosaic datasets

FGDB admin tooling --licensed ArcPy where required--> SDE, mosaic dataset,
registered-data-store, and service configuration
```

## Authority and lifecycle

- Local file geodatabases are production and migration inputs.
- The Stream Geodatabase (legacy `Site Geodatabase`) is the local database of
  record for Stream Network feature classes and related scientific metadata;
  it is not an FGDB hierarchy entity or enterprise object. Its Stream-scale DEM and
  construction intermediates remain excluded from enterprise persistence. Its
  reviewed synthetic network crosses the loading boundary as a governed,
  time-specific Stream Network Observation; Reach/Survey Event results and metadata
  join it through stable object and relationship identities.
- Analysts retain local inputs and preprocessing workspaces when complete
  process reconstruction is required. FGDB governs traceability of retained
  results rather than archiving every input and intermediate.
- A successful load alone is insufficient to establish authority; the loading
  workflow must verify the committed database state and retain enough
  provenance to reconcile it with its source.
- After successful loading and verification, ArcGIS Enterprise is the
  authoritative consolidated data source for the loaded content.
- Viewer access to published services is read-only. Privileged edit-capable
  services are used only by authenticated FGDB and application-mediated
  workflows and remain subject to FGDB governance.
- Records retain their origin workflow and lifecycle state; co-location in the
  enterprise geodatabase does not imply identical review or publication status.
- `collection` is the top-level domain and policy boundary separating the
  authoritative desktop source from the informative Shiny source.
- Both source paths use the `{fluvgeo}` scientific backend for portions of
  their derivation. Application and `fluvgeo` versions are part of provenance.
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

## Enterprise access and administration boundary

- Portal Feature Services are the application-facing contract for FGDB vector
  feature classes and tables. Read-only viewers and privileged writers receive
  capabilities appropriate to their roles.
- FGDB and Shiny R clients use the `{arcgis}` ecosystem, principally
  `{arcgislayers}` and `{arcgisutils}`, rather than requiring ArcGIS Pro for
  ordinary reads and controlled writes.
- PostgreSQL RDS is registered with ArcGIS Enterprise as the SDE-backed data
  source. Applications do not connect directly to RDS or alter SDE system
  tables.
- FGDB admin tooling scaffolds and configures deployments. ArcPy executes only
  the licensed SDE, mosaic dataset, registered-data-store, and service
  administration that supported web GIS interfaces cannot provide.
- Off-network development uses deterministic R and GDAL tests. A separate
  licensed USACE integration lane verifies the deployed ArcGIS contracts.

See ADR-0020 for the governing decision.

## Open architecture questions

- Canonical entity identifiers and natural-key rules.
- Physical enforcement of collection ownership and globally unique tiered
  study-area names.
- Partial/unknown legacy survey dates and revision/correction behavior.
- Physical representation and service exposure of Stream Network Configurations, versioned
  synthetic networks, and frame-relative base-event calibration.
- Source-to-target feature-class crosswalk and geometry constraints.
- Enterprise geodatabase dataset organization and naming conventions.
- Mosaic dataset design, raster item identity, footprints, overviews, and
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
