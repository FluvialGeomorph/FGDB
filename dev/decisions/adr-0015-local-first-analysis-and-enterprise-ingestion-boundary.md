# ADR-0015: Local-first analysis and enterprise ingestion boundary

- Status: accepted
- Date: 2026-08-29
- Clarified by: ADR-0018 and ADR-0019

## Context

FluvialGeomorph scientific tools must remain fully useful in local desktop,
Shiny, direct-R, and future QGIS workflows. Enterprise consolidation adds
cross-project access and management but must not remove local analytical
capability or cause database loading to initiate scientific operations.

The historical desktop workflow stores scientific geometry in Stream and
Reach–Survey Event file geodatabases. The forward-looking workflow adds the
related scientific metadata, topology, QA, and review relations needed to make
those geodatabases self-describing and directly loadable into FGDB.

## Decision

1. Analysts can complete, review, accept, and retain scientific analysis in
   local geodatabases without an FGDB connection.
2. `fluvgeo` is the long-term owner of scientific calculations, geospatial
   derivation, reconstruction, topology, classification, calibration, and
   scientific validation.
3. ArcGIS Pro, Shiny, direct R, and future QGIS clients invoke the same
   `fluvgeo` functions. Client wrappers own interaction and platform plumbing,
   not independent scientific implementations.
4. Producer tools write derived feature classes and all scientific metadata
   needed to interpret them into the applicable Study Area/Stream or
   Reach–Survey Event geodatabase.
5. Every scientific operation is explicitly user initiated. Data arrival or an
   FGDB load never triggers derivation, reconstruction, recalibration, or a
   change of scientific default.
6. FGDB tools inspect analyst-approved geodatabases, call the canonical
   scientific validators, reconcile identities explicitly, transform according
   to governed CRS rules, stage relations, load create/correction units
   transactionally, verify results, record load audit, and publish content.
7. FGDB tools do not split, snap, orient, classify, reconstruct, derive, select
   a base event, or calibrate features as a hidden effect of loading.
8. Local geodatabase relations match the enterprise scientific relations as
   closely as practical. FGDB-specific authorization, load audit, rollback,
   SDE management, and publication relations remain enterprise concerns.
9. Legacy migration tools may collect missing historical metadata and invoke
   explicitly selected `fluvgeo` reconstruction functions. Controlled unknown
   and not-retained states distinguish migration accommodation from the target
   producer schema.
10. New analyses enabled by consolidated enterprise data remain scientific
    functions in `fluvgeo` or another explicitly governed analysis package.
    FGDB supplies governed data access and persistence.

## Handoff

```text
Analyst
  |
  v
ArcGIS Pro / Shiny / direct R / future QGIS
  | calls
  v
fluvgeo scientific functions
  |
  v
Study Area/Stream and Reach–Survey Event geodatabase relations
  |
  | optional analyst-initiated FGDB load
  v
inspect -> scientific validation -> identity reconciliation
  -> transform -> stage -> transactional load -> verify -> publish
```

## Consequences

- Local projects remain scientifically complete when never loaded into FGDB.
- Producer and enterprise tooling share one object-relational scientific
  schema instead of translating through an unrelated delivery abstraction.
- Legacy data requires explicit migration handling when required tables or
  identities were never recorded.
- Cross-repository schema and function changes require coordinated versions and
  conformance tests driven by direct outputs in `fluvgeodata`.

## Tool placement

- **Prepare Stream Network**, **Create Longitudinal Reference Frame**, and all
  feature derivation/calibration operations are producer capabilities backed by
  `fluvgeo`.
- **Load Stream Network Geodatabase**, **Load Reach–Survey Event
  Geodatabase**, reconciliation, and enterprise publication are FGDB
  capabilities.
- The migration workflow may orchestrate both sides visibly, but the load step
  never absorbs scientific logic.
