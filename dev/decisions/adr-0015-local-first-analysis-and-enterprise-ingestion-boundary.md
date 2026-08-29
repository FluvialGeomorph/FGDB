# ADR-0015: Local-first analysis and enterprise ingestion boundary

- Status: accepted
- Date: 2026-08-29
- Refines: ADR-0010 decision 2 by permitting a forward-looking Stream/Network
  Geodatabase to participate in a versioned local exchange package while
  retaining that it is not an FGDB hierarchy entity or enterprise object

## Context

FGDB consolidates independently produced analyses, but consolidation must not
make ArcGIS Enterprise a prerequisite for performing fundamental
FluvialGeomorph analysis. The project was intentionally designed as a toolbox
of standardized, composable operations: analysts select inputs, order,
parameters, editing steps, and scientific purpose in a local workspace.

The emerging network and longitudinal-reference model needs more explicit
topology, observation, base-Flowline, calibration, and provenance metadata
than historical file geodatabases retained. If FGDB tools become responsible
for creating that scientific metadata, database ingestion could gradually
absorb analysis behavior and erode the standalone desktop/open-source
workflow.

ADR-0001 assigns scientific derivation to producer repositories and database
validation/loading to FGDB. ADR-0004 assigns canonical reusable scientific and
geospatial derivation contracts to `fluvgeo`, with ArcGIS Pro orchestration in
`FluvialGeomorph-toolbox`. This decision defines a concrete handoff between
those boundaries.

## Decision

1. **Local-first capability is an invariant.** Fundamental feature derivation,
   topology construction, longitudinal-reference creation, calibration,
   editing, QA, visualization, and reporting remain usable without an FGDB
   connection or ArcGIS Enterprise deployment.
2. “Local-first” describes independence from FGDB and enterprise persistence,
   not necessarily execution on a desktop filesystem. A user-initiated Shiny
   analysis in an application-managed workspace is a local-first client when
   it can complete the scientific workflow without first loading to FGDB.
3. `fluvgeo` is the long-term home for all computable scientific analysis and
   geospatial derivation functions and their data contracts. It does not
   depend on ArcPy, FGDB, a particular UI, or an enterprise connection.
4. `FluvialGeomorph-toolbox` owns the ArcGIS Pro user experience, editing, and
   local geodatabase I/O, but its target scientific tools are thin wrappers
   around `fluvgeo` functions rather than independent ArcPy scientific
   implementations. Existing ArcPy functions are replaced incrementally under
   explicit parity/method-change review.
5. Shiny applications call `fluvgeo` directly through application
   orchestration. A future QGIS toolbox supplies QGIS-facing wrappers around
   the same `fluvgeo` functions and contracts.
6. Producer tools write both derived features and the scientific metadata
   required to interpret them into the analyst's local workspace. This
   includes, as applicable, network-observation identity, source/method
   metadata, reviewed topology and classification, base-Flowline selection,
   calibration parameters/results, and analyst QA disposition.
7. FGDB owns a versioned **exchange/load-package profile** that describes how
   locally produced scientific content and metadata are presented for
   ingestion. The profile references canonical `fluvgeo` contracts without
   transferring scientific ownership to FGDB. The local package is not a
   replica of the normalized SDE schema: it may use a deliberately simpler,
   partially denormalized file-geodatabase/manifest representation that the
   loader maps to enterprise relations.
8. FGDB tools remain lightweight database-boundary tools. They inventory,
   validate, map local identities to governed enterprise identities, transform
   representations where specified, stage, load idempotently, reconcile,
   audit, and publish. They do not decide to run or perform scientific
   derivation or calibration as a side effect of loading.
9. Loading into FGDB is optional from the perspective of local analysis. No
   existing or future fundamental analysis capability may be removed from the
   local workflow merely because an enterprise equivalent or downstream query
   exists.
10. Legacy migration adapters in FGDB may collect metadata that historical
   producers failed to retain. Such behavior is an explicit migration
   accommodation, uses controlled unknown/not-retained states, and is not the
   target producer contract.
11. New analyses made possible by consolidated enterprise data are additive.
   Their scientific logic belongs in `fluvgeo` or an appropriate analysis
   client; FGDB may provide governed data access and persistence but does not
   become the scientific algorithm owner.
12. Every scientific operation remains explicitly user initiated. A producer
    tool may automate calculations after invocation, but neither data arrival
    nor an FGDB loader triggers analysis, recalibration, or changes to a
    scientific default.

## Handoff

```text
Analyst
  |
  v
FG-toolbox / Shiny / future QGIS client
  | calls
  v
fluvgeo scientific contracts
  |
  v
Local features + local scientific metadata + package manifest
  |
  | optional analyst-initiated submission
  v
FGDB inventory -> validate -> map -> stage -> load -> verify -> publish
  |
  v
Enterprise feature classes, mosaics, services, and additive queries
```

## Metadata ownership examples

| Metadata or operation | Primary author/owner | FGDB responsibility |
|---|---|---|
| Network derivation method, threshold, terrain time, and source evidence | Producer tool / analyst using canonical contract | Validate and load; never infer silently. |
| Network topology, Stream/Reach classification, mouth, and paths | Analyst-facing producer workflow | Validate hierarchy/topology and map identities. |
| Base Flowline choice and comparison calibration | Analyst-facing producer workflow calling `fluvgeo` | Validate references and load accepted results. |
| Local QA/review disposition | Analyst-facing producer workflow | Enforce publication requirements and retain provenance. |
| Package schema version, source-stable IDs, and content manifest | Producer adapter following FGDB exchange profile | Validate compatibility and use for idempotency. |
| Enterprise IDs, collection ownership, load transaction, publication state, and reconciliation log | FGDB | Create and govern. |
| Enterprise-spanning scientific analysis | `fluvgeo` plus an appropriate user-facing client | Supply governed inputs and optionally persist explicitly submitted results. |

Exact identity federation between offline packages and existing enterprise
hierarchy records remains a logical-schema decision.

## Consequences

### Benefits

- Protects the standalone desktop and open-source workflows from enterprise
  coupling and capability erosion.
- Captures scientific metadata at the point where the analyst and producing
  tool actually know it, reducing inference during loading.
- Keeps FGDB loaders smaller, more deterministic, and easier to secure and
  test.
- Supports offline work, delayed submission, reproducible local projects, and
  future non-Esri clients.
- Gives the same local package value even when a project is never loaded into
  FGDB.
- Preserves the distinction between automation within an invoked tool and
  autonomous scientific processing triggered by database state.

### Costs and risks

- Producer repositories must adopt new local metadata tables/manifests and
  versioned package-writing behavior.
- Package compatibility must be coordinated across FGDB, `fluvgeo`, desktop,
  and browser releases.
- Analysts may see additional metadata/review steps during production rather
  than only at load time; defaults and inheritance should minimize repetition.
- Offline identity creation and later reconciliation require explicit conflict
  rules.
- Some validation is necessarily duplicated: immediate producer feedback and
  authoritative FGDB ingress enforcement.
- Legacy artifacts still require a more capable migration path because they
  predate the package contract.

## Alternatives considered

### FGDB performs scientific preparation during loading

This minimizes producer changes and makes legacy ingestion convenient, but it
mixes scientific derivation with database operations, requires enterprise
access for complete processing, risks silent behavior changes, and encourages
local capability erosion. Retain only as an explicit legacy migration adapter.

### Producers write directly to enterprise tables

This avoids an intermediate package but tightly couples analysis tools to the
physical SDE schema, credentials, connectivity, transactions, and deployment
version. It weakens offline use and makes schema evolution harder.

### Local package plus lightweight FGDB loader

This adds a contract and coordination cost but best preserves local autonomy,
scientific ownership, portability, and an enforceable enterprise boundary. It
is the recommended alternative.

## Approval and follow-up

This boundary was accepted with the Shiny-local-first and `fluvgeo` ownership
clarifications on 2026-08-29. It refines the tool placement described after
ADR-0014:

- split **Register Synthetic Network** into a producer-side **Prepare/Document
  Synthetic Network Package** capability and an FGDB-side **Load Synthetic
  Network Package** capability;
- place **Create Longitudinal Reference Frame** and Flowline calibration in
  the analyst-facing producer workflow, backed by `fluvgeo`;
- retain FGDB legacy migration tools for incomplete historical artifacts; and
- plan the required cross-repository contract changes separately before
  modifying `fluvgeo`, `FluvialGeomorph-toolbox`, Shiny clients, or
  `FG-architecture`.
