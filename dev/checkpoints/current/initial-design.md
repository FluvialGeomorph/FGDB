# FGDB initial design checkpoint

- Updated: 2026-09-02
- State: active design; no enterprise loader implementation yet

## Initiative boundary

FGDB has two purposes:

1. maintain the FGDB design, relational specifications, semantic alignment,
   migration rules, and operating guidance; and
2. provide an R package for validating, reconciling, loading, and managing
   FluvialGeomorph content in an Esri Enterprise SDE geodatabase.

ArcGIS Enterprise is the consolidated source for published FluvialGeomorph
feature layers and raster content managed through mosaic datasets. Desktop and
browser analysis remain useful independently of enterprise loading.

## Accepted architecture

- `fluvgeo` owns scientific calculations and geospatial derivation,
  reconstruction, topology, classification, calibration, scientific
  validation, review operations, and local-geodatabase serialization.
- ArcGIS Pro, Shiny, direct R, and future QGIS clients collect parameters and
  provide interaction around the same `fluvgeo` functions.
- FGDB calls the `fluvgeo` scientific validator and adds enterprise-state
  validation, explicit identity reconciliation, relational mapping, staging,
  transactional load/correction, audit, and publication.
- Every scientific operation is analyst initiated. Loading never derives,
  reconstructs, recalibrates, or changes a scientific default as a side effect.
- FGDB is an R package using `testthat`. Shared test evidence comes from direct,
  provenance-documented producer outputs in `fluvgeodata`.
- R APIs use data frames/tibbles and `sf`. Persistent local scientific content is
  stored as relational tables and feature classes in a file geodatabase or
  GeoPackage.
- The enterprise deployment uses a registered PostgreSQL RDS/SDE data source in
  USACE ArcGIS Enterprise. FGDB and Shiny R clients use authenticated Portal
  Feature Services through the `{arcgis}` ecosystem; viewers receive read-only
  access.
- Licensed ArcPy is confined to admin-facing provisioning, SDE and mosaic
  dataset configuration, registered-data-store setup, service publication, and
  ArcGIS conformance that supported web GIS interfaces cannot perform.
- Deterministic R, GDAL, mocked-service, and isolated PostgreSQL/PostGIS tests
  form the normal off-network development loop. A separate licensed integration
  lane verifies deployed ArcGIS behavior.
- Every cross-platform field, geometry, constraint, CRS, and raster mapping
  requires a machine-readable type crosswalk and value-bearing conformance
  evidence. Readability or a successful conversion is not proof of scientific
  fidelity.
- **Mosaic dataset** is the required term for the Esri enterprise geodatabase
  raster-management data type; it is distinct from a combined raster mosaic or
  the operation of mosaicking.

Governing records include ADR-0004, ADR-0015, ADR-0017, ADR-0018, ADR-0019,
ADR-0020, ADR-0021, ADR-0022, and ADR-0023. Detailed open-development and enterprise-conformance goals,
requirements, evidence layers, and release gates are maintained in
`dev/goals/open-development-and-enterprise-conformance.md`.

## Governed scientific model

- Collections separate authoritative desktop content from informative Shiny
  content and carry different QA/mutation policies.
- The required hierarchy is Study Area → Stream → Reach → Survey Event.
- Study Area has one multipart-capable AOI polygon. Stream and Reach polygons
  are optional because stored project geometry defines their extent.
- One Reach has many Survey Events. Year is required; month/day are optional.
- Each Survey Event may own several durable derived-dataset slots by feature
  family and role. Every populated slot has exactly one current accepted
  edition with scientific-method, schema, software, platform, and source
  provenance. A correction replaces incorrect current content rather than
  preserving known-bad scientific rows as alternative results.
- Dimension results remain canonical typed wide tables. The in-database
  `dimension_metric_definition` catalog defines their scientific meaning, and
  a long observation representation is deferred to a separate interoperability
  decision.
- The governed terrain artifact is the hydro-modified DEM. Cutlines and their
  material interpolation assumptions are retained. Source point clouds,
  acquisition wrangling, and temporary terrain intermediates are outside FGDB.
- Local analysis uses the scientifically appropriate horizontal/vertical CRS;
  consolidated enterprise geometry is transformed according to the governed
  source-CRS transformation registry.

Detailed hierarchy and feature rules are in the feature catalog, conceptual
model, and kernel relational model.

## Stream Network and longitudinal reference model

- A Stream Network Configuration belongs to one Study Area and contains either
  one independently analyzed Stream or a connected set of Streams.
- Each terrain time may produce a distinct reviewed Stream Network Observation. A
  correction to the same intended observation retains its identity and
  replaces its active segment set.
- One editable Study Area/Stream Geodatabase contains one active Stream Network
  Observation and one `stream_network` feature class. Observations for other
  terrain times may share the same durable Stream Network Configuration ID
  across separate geodatabases.
- Stream Network segments are directed topology edges classified to a Stream and,
  optionally, a Reach. Logical node identities and endpoint geometry establish
  connectivity.
- Retained historical networks and explicit reconstruction from governed Reach
  Flowlines are supported evidence classes. Missing network evidence remains a
  qualified legacy completeness state.
- Longitudinal stationing is project-defined. A Reference Frame explicitly
  selects base-event Flowlines; comparison-event measures remain calibrated to
  those selected geometries. Alternative frames may coexist.

The accepted object-relational schema is in
`dev/schemas/stream-network-geodatabase-schema.md`; the producer API is
`dev/features/prepare-stream-network.md`.

## Semantic interoperability

- OGC HY_Features is the primary hydrologic conceptual alignment.
- GeoSPARQL, SKOS, PROV-O, SOSA/SSN, DCAT, and SHACL address complementary
  spatial, vocabulary, provenance, observation, catalog, and validation needs.
- Geoconnex is the standard external hydrologic reference interface and
  `hydrogeofetch` is the supported R client.
- `usace-ukg-ontologies` governs future namespace, promotion, versioning,
  knowledge-graph, and semantic-validation decisions.
- National reference features inform names and external references; they do not
  define FGDB Stream/Reach identity, project extent, or stationing.

## Repository implementation state

FGDB is scaffolded as an R package with:

- `DESCRIPTION`, `NAMESPACE`, roxygen package documentation, and R project
  configuration;
- `testthat` edition 3;
- `fluvgeodata` and `sf` development dependencies; and
- initial source-data tests covering retained-network and Flowline-
  only legacy file geodatabases.

Verification:

- `devtools::test()` passes 27 assertions against six direct geodatabase
  outputs from `fluvgeodata`.
- `devtools::check(args = "--no-manual")` completes with zero errors, warnings,
  or notes under R 4.6.1 with Windows-compatible locale settings.

## Current implementation boundary

The Stream Network Geodatabase schema and producer API are accepted. Direct
legacy evidence and the first separately reviewed `fluvgeo` implementation
slice are recorded in `dev/schemas/stream-network-source-evidence.md`.

The Configuration, Configuration–Stream membership, and Observation
constructors are implemented in `fluvgeo`. Retained-feature normalization now
creates candidate `stream_network` segments, `stream_network_source` lineage,
and working validation results from a separate per-source-feature Stream/Reach
mapping. Focused tests use direct retained evidence, including missing legacy
attributes and an in-memory multipart case. Initial retained-source assessment
and linked pending INSPECT features are implemented (2026-09-04), covering
duplicates, self-intersections, closed segments, interior intersections, and
endpoint near misses. Direction remains unresolved. The next step is analyst
inspection to choose concrete repair and direction-evidence behavior; applying
reviews, node assignment, full topology validation, and acceptance remain later.

The first ADR-0023 instantiation is now drafted. `FLOWLINE` is the first
`dataset_type`; `scientific-reference-data.md` defines the supporting reference
relations; and `flowline-feature-contract.md` specifies Flowline identity,
minimal fields, XY geometry, source lineage, legacy disposition, two observed
method contracts, and a worked Dataset Edition example. Scientific method is
explicitly production metadata on an edition, not a hierarchy object or a
synonym for a feature class. Flowline Points is the next feature-catalog slice
after review of this draft.

Do not begin the FGDB enterprise loader until the producer relations and
scientific validator are implemented and stable in `fluvgeo`.

## Later design work

1. Complete remaining hierarchy identity, uniqueness, rename/alias, and
   resegmentation rules.
2. Populate the canonical logical-type and platform-binding crosswalk for the
   accepted hierarchy and Stream Network schemas and implement its first
   OpenFileGDB/GeoPackage boundary tests, capability probes, and compatibility
   profiles.
3. Specify the source-CRS transformation registry and `hydro_dem` mosaic
   dataset item contract.
4. Review and accept the Flowline contract, then specify Flowline Points and
   continue the L1/L2/L3 dataset types, wide fields, metric definitions, and
   initial scientific/schema contracts from direct producer and manual
   evidence.
5. Specify enterprise ingestion, reconciliation, rollback, and load audit.
6. Specify Feature Layer, raster service, query, authorization, deployment, and
   operational contracts.
7. Complete legacy inventory and migration crosswalks.
8. Finalize longitudinal-frame calibration, QA, and materialized measure
   contracts.

Cross-repository changes to `fluvgeo`, desktop/Shiny clients,
`FG-architecture`, or `usace-ukg-ontologies` require their own reviewed scope.
