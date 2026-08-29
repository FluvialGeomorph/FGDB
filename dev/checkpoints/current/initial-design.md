# Checkpoint: Initial FGDB design

- Updated: 2026-08-29
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
  editable in place as the Area of Interest changes.
- Accepted required Survey Event year with optional month/day and derived date
  precision/labels. The contemporaneous report-only base-event assumption was
  later superseded by ADR-0014.
- Required per-source-CRS horizontal/vertical transformations and conformance
  to the Enterprise `hydro_dem` mosaic parameters.
- Corrected the terrain boundary to retain Cutlines and their material
  hydro-modification method/parameters as important assumption records.
- Drafted the next catalog entries for Stream, Reach, and the synthetic stream
  network, exposing their unresolved geometry, boundary, persistence, and
  ownership contracts.
- Accepted mandatory hierarchy identity with level-specific geometry
  cardinality: required Study Area AOI, optional Stream/Reach polygons, and an
  optional Survey Event DEM/analysis AOI that may be derived from the hydro DEM
  footprint.
- Clarified that Study Area means an area being evaluated and does not imply a
  remediation project exists.
- Accepted analyst-driven segmentation of the synthetic network into Streams
  and Reaches according to investigation objectives.
- Verified that USGS now maintains 3DHP while NHD, WBD, and NHDPlus HR are
  legacy products; accepted configurable national-service name suggestions
  with analyst confirmation and retained external-name provenance in ADR-0006.
- Evaluated the current semantic-standards landscape and proposed a distinct
  FG ontology layer linking external standards, the feature catalog, the
  physical GIS schema, and a future RDF/knowledge-graph projection.
- Drafted ADR-0007, a semantic interoperability architecture, an initial
  kernel crosswalk, competency questions, and a non-normative `dev/ontology/`
  scaffold for team review.
- Identified OGC HY_Features as the primary hydrographic conceptual alignment;
  proposed GeoSPARQL, OWL, SKOS, PROV-O, SOSA/SSN, DCAT, and SHACL for
  complementary concerns, with Geoconnex as an integration candidate.
- Reclassified hydrOntology and the USGS Surface Water Ontology as informative
  prior art rather than maintained normative foundations.
- Accepted Geoconnex as the standard external hydrologic reference-feature
  interface and `hydrogeofetch` as the supported R client in ADR-0008.
- Verified that current `fluvgeo` calls use NLDI processing operations rather
  than direct Geoconnex reference queries, and separated the package migration
  from the new external-identifier discovery contract.
- Established `usace-ukg-ontologies` as the authority for future namespace,
  ontology promotion, versioning, named graphs, and semantic validation.
- Applied `dev/ontology/ontology-guidance.md`: full OWL/SHACL/RML development is outside the
  implementation critical path; the present focus is immutable identity,
  controlled concepts, provenance, kernel HY_Features mappings, and an
  ontology-ready relational schema.
- Clarified the Survey Event model after operational review: one Reach has many
  Survey Events; each Survey Event has one current derived result set and one
  current derivation-provenance record. Reprocessing replaces incorrect
  content and provenance rather than creating a persistent one-to-many
  processing-run hierarchy.
- Allowed sparse legacy Survey Events populated from required year and the best
  available evidence, explicitly recording unknown/not-retained clearinghouse
  metadata, point clouds, intermediates, and acquisition footprints instead of
  fabricating provenance.
- Updated `fluvgeo` to import `get_raindrop_trace()` and
  `get_split_catchment()` from `hydrogeofetch` 2.0.1, replaced the dependency
  in its reproducible lockfile, and verified the existing watershed return
  contract against the live service.
- Moved ontology design guidance from the repository root into the durable
  `dev/ontology/` route and registered that route in `AGENTS.md`.
- Accepted project-defined Stream and Reach extent in ADR-0009: only stored
  FGDB geometry directly asserts extent; national geometry, segmentation, and
  route measures remain contextual and do not govern FGDB identity.
- Established that no national linear referencing system is required. Local
  stationing references a specific version-aware FGDB Flowline representation.
- Recorded the historical terrain and research-data infrastructure gap that
  motivates centralized, multi-time-period FGDB terrain and geometry.
- Accepted ADR-0010: the optional `Stream Geodatabase` (legacy
  `Site Geodatabase`) is a local preprocessing workspace, not an FGDB entity
  or load package. Its Stream-scale DEM and drainage intermediates remain
  excluded from persistence; ADR-0014 later superseded ADR-0010's exclusion of
  the reviewed synthetic network.
- Recorded the initial, subsequently superseded conclusion that Stream and
  Reach records alone captured accepted segmentation. Full local process
  reconstruction still requires analyst retention outside FGDB.
- Accepted ADR-0011: the manually added legacy `boundary` feature class is
  excluded and is not mapped automatically to Study Area, Stream, Reach, or
  Survey Event geometry.
- Drafted `dev/schemas/kernel-relational-model.md` as the next design slice,
  translating accepted hierarchy and current-result semantics into proposed
  relations, cardinalities, integrity invariants, identity-change rules, and
  uniqueness constraints for review.
- Accepted ADR-0012: the normative derivation/load unit is one Reach and one
  Survey Event; the legacy ArcPy dissolve-by-`ReachName` behavior is
  non-normative residue rather than a `{fluvgeo}` parity requirement.
- Accepted one current Flowline per populated Survey Event and assigned
  multi-Reach/Stream scale-up to hierarchy-aware FGDB queries rather than
  multi-Reach producer execution or duplicated authoritative geometry.
- Drafted `dev/features/multiscale-scientific-query.md`, including Stream
  longitudinal-profile composition, explicit cross-Reach temporal selection,
  and method/provenance safeguards for historic manual and modern
  remote-sensing observations.
- Verified that the ArcPy Flowline-points tool uses a manually supplied
  `km_to_mouth` offset while the current R implementation starts local measures
  at zero. This exposes the need for a governed Reach-order/topology and
  Stream-scale station-alignment contract.
- Accepted ADR-0013: FGDB governs a project longitudinal reference frame owned
  by one Study Area and scoped either to one Stream or to a connected Study
  Area/watershed network. One explicit mouth is zero kilometers and distance
  increases upstream along selected paths.
- Drafted `dev/schemas/longitudinal-reference-model.md` with Network Scope,
  frame, mouth, reusable network path, Reach assignment, explicit base
  Flowline, comparison calibration, identity, validation, and legacy-migration
  contracts.
- Clarified that the Stream Geodatabase remains excluded while its reviewed
  calibration output is governed. Legacy `km_to_mouth` is not identity and is
  canonical only after explicit frame binding and validation.
- Accepted ADR-0014: retain each reviewed synthetic network as a governed,
  time-specific Network Observation within a Study-Area-owned Network Scope.
  One connected Study Area may use one multi-Stream scope; a discontinuous
  Study Area may use separate single-Stream scopes in the same physical
  enterprise feature class.
- Established an N:M association between Network Observations and applicable
  Reach Survey Events, explicit Stream/Reach classification of network
  segments, and explicit reviewed correspondence between segments at
  different terrain times.
- Corrected base-event semantics: a longitudinal reference frame selects one
  base Flowline per participating Reach assignment and may select a compatible
  base Network Observation. Base status is frame-relative, alternative base
  choices may coexist, and changing the base creates a different frame rather
  than mutating a global Survey Event flag.
- Drafted `dev/schemas/synthetic-network-model.md` and updated the kernel,
  longitudinal-reference, feature-catalog, ontology, architecture, migration,
  and scientific-query specifications to reflect ADR-0014.
- Reduced ADR-0014 to an immediately implementable legacy-import slice. The
  initially proposed FGDB **Register Synthetic Network** tool hid normalized
  writes behind one guided dialog and required only Network Scope, scope
  membership, Network Observation, and the enterprise segment feature class.
  Proposed ADR-0015 subsequently limits that richer FGDB behavior to legacy
  migration and recommends a producer package plus lightweight loader for new
  work.
- Documented whole-network, Reach-fragment batch, correction-replacement, and
  disconnected-Stream import behavior in
  `dev/workflows/import-synthetic-network.md`.
- Verified that the Papillion R1 2016 XML contains no `stream_network`
  feature-class definition; the term occurs only in Flowline lineage pointing
  to a Stream-Geodatabase path. Legacy Reach results therefore remain loadable
  with explicit `NETWORK_NOT_RETAINED` completeness rather than fabricated
  network geometry.
- Confirmed the implementation boundary: FGDB owns the ArcGIS Pro tools and
  database-write orchestration for network registration, reference-frame
  creation, loading, and reconciliation; reusable scientific topology and
  calibration algorithms belong in `fluvgeo` and are called by those tools.
- Clarified that the governed reference frame does not make stationing
  independent of Flowline geometry. Comparison-event `km_to_mouth` values
  remain calibrated to explicitly selected base-event Flowlines. The normal
  operational preset is `LATEST_VALIDATED_EVENT`, offered only after an
  analyst initiates frame creation; resolved IDs are stored.
- Reaffirmed the foundational analyst-control invariant: loading or publishing
  a newer Survey Event never creates a frame, recalibrates previous Flowlines,
  or changes a current/default frame. The analyst chooses the base and
  comparison events, initiates the tool, reviews and accepts results, and
  explicitly designates a default when desired.
- Accepted ADR-0015 to protect a local-first analysis boundary.
  Analyst-facing tools write derived features and scientific metadata to a
  local file-geodatabase exchange package; FGDB tools validate, map, load,
  reconcile, and publish without absorbing scientific derivation. Legacy FGDB
  migration adapters may collect missing historical metadata as an explicit
  exception.
- Corrected provisional tool placement: **Create Longitudinal Reference
  Frame** belongs in the producer workflow (`FluvialGeomorph-toolbox` calling
  `fluvgeo`), while FGDB owns the corresponding package loader. The earlier
  FGDB **Register Synthetic Network** concept becomes a legacy migration tool
  plus a future lightweight package loader.
- Defined Shiny as a local-first platform when user-initiated analysis can
  complete in application-managed state without first persisting to FGDB.
- Strengthened the target ownership boundary: `fluvgeo` is the long-term home
  for all computable scientific analysis and geospatial derivation functions;
  ArcGIS Pro and future QGIS toolboxes are wrappers/adapters, and Shiny calls
  the same contracts through application orchestration.
- Established the Stream Geodatabase as the ArcGIS binding of a logical local
  Network Workspace for network observations, topology, classifications,
  frames, and package metadata. A connected multi-Stream scope may use a Study
  Area Network Geodatabase; platform-neutral contracts also support Shiny,
  direct R, and future GeoPackage/QGIS bindings. Drafted
  `dev/schemas/local-analysis-package.md`.

## Remaining

1. Review and finalize the proposed kernel identity-change, uniqueness, and
   cardinality rules, especially project-scoped Stream identity, Reach
   resegmentation, stable current-result slots, and Cross Section
   keys/alignment.
2. Specify the per-source-CRS transformation registry and complete `hydro_dem`
   mosaic-item contract.
3. Complete the Study Area string grammar and Survey Event tie/partial-date
   ordering rules.
4. Prepare separately scoped cross-repository implementation planning for
   accepted ADR-0004; treat flowline as a later paired-implementation contract
   pilot rather than the first catalog entry.
5. Formalize required metadata for Collection, Study Area, Stream, Reach,
   Survey Event, optional hierarchy geometries, and feature content.
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
15. Review and finalize the logical/physical synthetic-network and project
    longitudinal-reference contracts, including node/edge topology,
    cross-time segment correspondence, base-Flowline realization, QA
    tolerances, measure materialization, and manual-survey calibration.
16. Define query/service contracts for Study Area-, Stream-, Reach-, and
    Survey Event-scale selection, including explicit cross-Reach temporal
    selection and observation-method compatibility behavior.

## Evidence and verification

- Source brief: `../FG-Tech-Manual/DB-migration.qmd` from the workspace root.
- Organization evidence: `FG-architecture/dev/architecture/` and
  `FG-architecture/repositories.yml`.
- `validate_agentic_context("FGDB")` returned `valid = TRUE` with no findings.
- Repository inspection found no existing Enterprise/SDE database-loading
  implementation in `FluvialGeomorph-toolbox`; its current tools produce local
  geodatabase content.

## Next safe action

Review the platform-neutral package and ArcGIS Stream/Network Geodatabase
binding proposed in `dev/schemas/local-analysis-package.md`. Then separately
specify (1) its exact local fields/tables and cross-workspace identity rules,
(2) the lightweight FGDB package-loader contract, and (3) the more permissive
legacy migration adapter in `dev/workflows/import-synthetic-network.md`. Do not
design the FGDB loader to absorb scientific analysis.

## Blockers or decisions

Implementation authorization is still required before changing `fluvgeo`, the
desktop toolbox, Shiny clients, or `FG-architecture`. The Study Area name
separator, descriptive-component normalization, rename/alias behavior, and
name reuse policy remain to be defined. A future FluvialGeomorph ontology
namespace requires sponsorship and approval through `usace-ukg-ontologies`;
no public semantic identifiers should be minted locally.
