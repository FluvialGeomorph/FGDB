# Checkpoint: Initial FGDB design

- Updated: 2026-08-27
- Status: active

## Objective

Turn the database-migration problem statement into an agreed FGDB design and
an implementable, staged work plan.

## Current state

FGDB contains the `{reproducibleai}` base agentic-context profile and initial
design records. The system-of-record technology, high-level data flow,
repository responsibilities, and ownership boundary have been selected. The
two initial write use cases and read-only service boundary are established.
Collection-scoped authority and mutation semantics are established. The full
logical and physical schemas and operating model have not yet been designed.

## Completed

- Inspected the FGDB repository, branch, worktree, and remote.
- Read the database-migration problem statement.
- Reviewed current FluvialGeomorph capability ownership and dependency records.
- Scaffolded and validated agentic-context standard 0.1 with the `base` profile.
- Recorded the initial scope, desired outcomes, constraints, and unknowns in
  `dev/goals/initiative-brief.md`.
- Accepted ArcGIS Enterprise backed by PostgreSQL/SDE as the authoritative
  system for derived feature content and DEM/REM mosaic datasets.
- Assigned FGDB ownership of the schema/specification and the database setup,
  loading, and management toolbox, while retaining derivation ownership in
  `FluvialGeomorph-toolbox`.
- Recorded the decision in ADR-0001 and the current system context under
  `dev/architecture/`.
- Defined the experienced desktop analyst's legacy/future geodatabase loading
  workflow and the authenticated Shiny user's save-and-restore workflow.
- Accepted controlled desktop and application-mediated writes with read-only
  client Feature Layer services in ADR-0002.
- Inspected `ohwm2`; verified that its current user geometry and derived
  outputs live in Shiny session state and that it has no database persistence
  implementation.
- Accepted `collection` as the top-level data and governance boundary, with an
  authoritative desktop collection and an informative Shiny collection.
- Accepted globally unique tiered study-area names alongside immutable IDs.
- Defined desktop reach-survey-event replacement and Shiny in-place editing in
  ADR-0003 and the initial conceptual data-model contract.
- Verified that both current workflows call exported `{fluvgeo}` functions,
  although their exact call surfaces differ.
- Accepted strict adherence to the full collection-to-survey-event hierarchy
  for desktop and Shiny records; clients may automate but not bypass levels.
- Compared the ArcPy and R flowline implementations and confirmed they are not
  behaviorally equivalent.
- Accepted canonical open-source feature derivation in `fluvgeo` through
  ADR-0004, with contract-level parity and scientific-review gates.
- Defined the transition sequence: complete the coherent R pipeline using
  Shiny as an early proving ground, then perform a coordinated desktop overhaul
  that retains ArcGIS Pro as an optional editing client and enables future QGIS
  adapters.
- Established FGDB as the synthesis location for fragmented historical design
  artifacts, production examples, requirements, and accepted specifications.
- Parsed and compared the target file-geodatabase prototype and the Papillion
  R1 2016 wild-caught L1/L2/L3 output schema.
- Recorded the XML assessment, initial dataset dispositions, limitations, and
  design implications under `dev/schemas/`.
- Recorded the project's origin, architecture evolution, database motivation,
  and reason for an evidence-driven AI-assisted design process.
- Recorded the stated historic team roles and a working, non-formal review map
  spanning technical, scientific/program, production, and documentation
  perspectives.
- Defined the feature-catalog record contract and began the catalog in Level 1
  workflow order with study-area identity/location and terrain inputs.
- Used the initial catalog draft to distinguish terrain workflow artifacts and
  expose the source-terrain versus governed-raster boundary for resolution.
- Accepted one governed polygon per Study Area and codified the Study Area
  extent-type domain as Small Reach, Long Reach, or Watershed.
- Restricted FGDB terrain scope to the hydro-modified DEM for each
  reach-survey-event; LiDAR acquisition, source terrain, watershed products,
  and hillshades remain outside database persistence scope.
- Accepted local scientifically appropriate analysis coordinate references and
  Web Mercator Enterprise storage, with native horizontal and vertical
  reference metadata retained.
- Established Survey Event temporal identity, subsequently refined to require
  year while permitting unknown month/day and deriving the display label from
  known precision.
- Recorded these foundation choices in ADR-0005 and revised the feature catalog
  to contain governed objects only.
- Accepted a two-level Study Area name comprising a controlled three-letter
  USACE district code and descriptive name.
- Accepted multipart-capable, analyst-defined Study Area polygons that are
  editable in place as general project scope changes.
- Accepted required Survey Event year with optional month/day, derived date
  precision/labels, and report-only default base-event selection.
- Required per-source-CRS horizontal/vertical transformations and conformance
  to the Enterprise `hydro_dem` mosaic parameters.
- Corrected the terrain boundary to retain Cutlines and their material
  hydro-modification method/parameters as important assumption records.
- Drafted the next catalog entries for Stream, Reach, and the synthetic stream
  network, exposing their unresolved geometry, boundary, persistence, and
  ownership contracts.

## Remaining

1. Resolve the Stream geometry, Reach/boundary normalization, and synthetic
   stream-network persistence/ownership questions in the new catalog slice.
2. Specify the per-source-CRS transformation registry and complete `hydro_dem`
   mosaic-item contract.
3. Complete the Study Area string grammar and Survey Event tie/partial-date
   ordering rules.
4. Prepare separately scoped cross-repository implementation planning for
   accepted ADR-0004; treat flowline as a later paired-implementation contract
   pilot rather than the first catalog entry.
5. Formalize required metadata for collection, study area, stream, reach,
   survey event, and feature content.
6. Specify immutable identifier formats and the remaining Study Area name,
   rename, alias, and reuse rules.
7. Formalize temporal semantics, spatial semantics, provenance, and integrity
   constraints.
8. Complete the L1/L2/L3 feature-class and mosaic-dataset source-to-target
   disposition and field crosswalks.
9. Design ingestion, reconciliation, error handling, and rollback behavior.
10. Define Feature Layer and raster-service boundaries and client contracts.
11. Define environment, security, deployment, and operational requirements with
   the USACE hosting stakeholders.
12. Define the legacy inventory and migration crosswalk.
13. Record accepted decisions, schemas, workflows, and a staged
   delivery plan in their durable routes.
14. Add FGDB to the organization repository catalog and capability map through
   a separately reviewed cross-repository change when its role is accepted.

## Evidence and verification

- Source brief: `../FG-Tech-Manual/DB-migration.qmd` from the workspace root.
- Organization evidence: `FG-architecture/dev/architecture/` and
  `FG-architecture/repositories.yml`.
- `validate_agentic_context("FGDB")` returned `valid = TRUE` with no findings.
- Repository inspection found no existing Enterprise/SDE database-loading
  implementation in `FluvialGeomorph-toolbox`; its current tools produce local
  geodatabase content.

## Next safe action

Review the draft Stream, Reach, and synthetic stream-network catalog entries
and resolve their geometry, boundary normalization, persistence, and ownership
questions. Then define the transformation registry and complete hydro DEM
mosaic contract. Do not cut over the production desktop workflow until the
coherent replacement pipeline is ready.

## Blockers or decisions

Implementation authorization is still required before changing `fluvgeo`, the
desktop toolbox, Shiny clients, or `FG-architecture`. The Study Area name
separator, descriptive-component normalization, rename/alias behavior, and
name reuse policy remain to be defined.
