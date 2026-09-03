# FGDB initiative brief

## Status and source

This is an initial working brief derived from
[`FG-Tech-Manual/DB-migration.qmd`](../../../FG-Tech-Manual/DB-migration.qmd),
reviewed beginning 2026-08-25 and updated through 2026-09-02. It records
user-provided direction, not a completed
system design. The technical-manual chapter remains authoritative for its own
published content; accepted FGDB decisions and contracts will live in this
repository.

## Purpose

Develop the FluvialGeomorph Database (FGDB) initiative to consolidate
independently maintained, site-oriented analysis datasets into a coherent
ArcGIS Enterprise geodatabase that supports multiple study areas and
observations through time. FGDB will be the single authoritative enterprise
data source for accepted geospatial content produced by ArcGIS Pro, Shiny,
direct-R, and future QGIS clients using canonical `fluvgeo` contracts.

The initiative also externalizes a design problem that had become too large to
hold reliably in one developer's working memory while maintaining continuous
production operations. Versioned evidence, crosswalks, decisions, schemas, and
review records will make interacting scientific, technical, operational,
historical, and deployment requirements collectively tractable.

## Initial repository scope

This repository has two initial responsibilities:

1. Document the FGDB design process and maintain its specifications.
2. Provide an R package for schema validation, service-mediated data access,
   repeatable loading, and subsequent database management, plus licensed
   administrative adapters for enterprise setup and configuration where
   supported web GIS interfaces are insufficient.
3. Assemble and preserve relevant historical requirements, schema prototypes,
   production examples, and workflow evidence so fragmented prior work can be
   evaluated through one unified design process.

These responsibilities may be separated into different repositories later if
their size, release cycles, access boundaries, or maintenance needs make the
combined repository impractical.

## Domain hierarchy

The starting domain model has `Collection` as its top-level object and policy
boundary. Beneath each collection, it continues through study area, stream,
reach, survey event, and FG feature content.

```text
Collection
└── Study Area
    └── Stream
        └── Reach
            └── Survey Event
                └── FG Features
```

A reach-survey-event geodatabase represents derived conditions for one reach
at one point in time. Its feature content can include terrain, hydrography,
flowline, cross-section, bankfull, bankline, valley, and related derived
datasets.

## Desired outcomes

- Establish stable identities and relationships for study areas, streams,
  reaches, survey events, and their derived FG features.
- Require a Study Area AOI polygon while allowing Stream, Reach, and Survey
  Event polygons to be absent when no defensible or retained extent exists.
- Support repeat observations of a reach without conflating survey events.
- Compose separately derived Reach/Survey Event content into reproducible
  Stream- and Study Area-scale queries while retaining direct ownership and
  provenance.
- Govern a common project longitudinal coordinate measured upstream from a
  selected Stream mouth or connected Study Area/watershed outlet so separately
  processed Reaches and tributaries can participate in the same analysis.
- Enable idempotent loading of locally processed artifacts into a central
  database system.
- Publish database feature classes to client applications through a defined
  set of ArcGIS Feature Layer services.
- Store reach-survey-event hydro-modified DEM and REM raster content through
  enterprise mosaic datasets; do not retain source terrain or watershed
  preparation products.
- Preserve accepted Stream and Reach segmentation and each reviewed,
  time-specific synthetic stream network without retaining the local Stream
  Geodatabase, its Stream-scale DEM, or drainage/construction intermediates.
- Allow new work to use the new model while legacy project data is migrated
  incrementally without stopping current work.
- Maintain a clear crosswalk from legacy project folders and reach-survey-event
  file geodatabases to the FGDB model.
- Align terminology with the FG User Manual, including the transition from
  `Site` to `Stream` where applicable.
- Prevent differences between desktop and browser derivation implementations
  from being misinterpreted as fluvial change, using canonical contracts,
  validation, and method/version provenance.
- Support an open-source canonical processing backend so ArcGIS Pro is an
  optional expert editing client, future QGIS integration is feasible, and
  ArcGIS Enterprise is the required Esri dependency only at the enterprise
  deployment and service boundary.
- Maintain versioned field, geometry, constraint, CRS, and raster type
  crosswalks with value-bearing round-trip tests so file geodatabase,
  GeoPackage, Feature Service, PostgreSQL/PostGIS, and SDE conversions cannot
  silently change scientific meaning.
- Preserve local-first capability across ArcGIS Pro, Shiny, direct R, and
  future QGIS clients: all computable scientific operations live in
  `fluvgeo`, complete without FGDB, and write object-relational geodatabase
  feature classes and tables that FGDB can load.
- Let previous and future customers discover and inspect derived geometry for
  delivered analyses, including repeat survey events used to assess change
  through time.
- Let authenticated USACE Shiny users save a small-area self-service analysis,
  find it again by map or study-area selection, and resume or review it in a
  later session.
- Support small and unnamed streams without requiring national geometry,
  segmentation, or linear referencing; FGDB-stored geometry and stable IDs
  govern project extent and identity.
- Provide centralized, standards-ready access to governed high-resolution,
  multi-time-period terrain analysis products and derived fluvial geometry that
  historically lacked a durable shared digital representation.
- Support empirical analysis of fluvial geomorphic process over decades by
  preserving comparable observations across spatial scales, time periods, and
  historic manual or modern remote-sensing methods.
- Make design evidence and dependencies traceable enough that the team can
  review decisions from its scientific, technical, operational, program, and
  documentation perspectives without relying on one person's memory.
- Define a maintained FluvialGeomorph ontology module that connects scientific
  terminology, the logical feature catalog, the physical GIS model, and future
  USACE knowledge graphs through versioned, evidence-backed mappings.
- Align with current OGC and W3C semantic standards where meanings genuinely
  agree while preserving explicit FG extensions for specialized fluvial
  geomorphology concepts.
- Use Geoconnex as the standard external hydrologic reference-feature
  interface and `hydrogeofetch` as the supported R client.
- Align any future normative ontology module with the namespace, candidate,
  versioning, validation, and publication framework in
  `usace-ukg-ontologies`, without making full ontology implementation a
  prerequisite for the FGDB schema.

## Constraints and principles

- The legacy `/FluvialGeomorph/Projects/` structure remains operational during
  migration.
- Migration is stepwise and pay-as-you-go; it must not require a big-bang
  conversion.
- Local derivation workflows remain part of the starting operating model.
- The normative desktop derivation unit is one Reach and one Survey Event.
  Legacy multi-Reach vectorization is not a target processing capability;
  FGDB hierarchy queries provide Stream- and Study Area-scale composition.
- Database loads must be safely repeatable.
- The desktop collection uses idempotent reach-survey-event replacement:
  corrected loads remove and replace the prior active records rather than
  preserving known-bad feature data as queryable history.
- The Shiny collection permits valid content to be visible immediately and
  uses in-place editing under stable identities.
- Study-area names are globally unique, human-readable values governed by a
  two-level district-code and descriptive-name convention; immutable IDs
  provide unambiguous identity.
- Stream and Reach names should use analyst-confirmed suggestions from current
  national hydrography services where available, while FGDB IDs and
  investigation-specific segmentation remain authoritative.
- Viewer access to Feature Services is read-only. Creation, correction,
  replacement, and retirement occur only through controlled, authenticated
  FGDB or application-mediated workflows using separately authorized edit
  capabilities.
- Reports, maps, and export files remain outside FGDB's authoritative database
  scope initially; FGDB makes their associated derived geometry accessible but
  does not replace the delivered report archive.
- Folder structure should express the domain model but must not substitute for
  explicit database identity and integrity rules.
- Existing repositories retain ownership of their established capabilities
  unless an explicit cross-repository decision changes an ownership boundary.
- The target is the USACE private-cloud ArcGIS Enterprise deployment, currently
  hosted in AWS GovCloud IL4, with an Esri enterprise geodatabase in PostgreSQL
  RDS registered with ArcGIS Enterprise and exposed to applications through
  Portal Feature Services.
- Credentials, connection files, server names, and other environment-specific
  or sensitive configuration must remain outside version control.
- Historical artifacts are evidence, not automatically authoritative
  specifications. Their accepted meaning must be captured in maintained goals,
  architecture, decisions, schemas, features, and workflows.
- FGDB governs loaded analysis objects, not the analyst's local LiDAR search,
  acquisition, point-cloud cleaning, source DEM, watershed-product, or
  hillshade workflow. Cutline geometry is retained as a governed record of
  terrain inadequacy and hydro-modification assumptions.
- The `Stream Geodatabase` (legacy `Site Geodatabase`) is the local database of
  record for Stream Network feature classes and related scientific metadata;
  it is not an FGDB hierarchy entity or retained enterprise object. Its Stream-scale DEM and
  drainage/construction intermediates are not retained in FGDB. Its reviewed
  synthetic network is retained as a governed, time-specific Network
  Observation. Projects requiring complete process reconstruction retain the
  remaining materials locally; FGDB requires traceability for its retained
  network and Reach/Survey Event results.
- Desktop analysis may use an appropriate local projected horizontal and
  vertical reference. Governed spatial content is transformed to Web Mercator
  (EPSG:3857) for consolidated Enterprise storage, with native analysis and
  vertical-reference metadata retained.
- Survey acquisition and feature derivation remain conceptually distinct.
  Each Survey Event owns typed derived-dataset slots with one current accepted
  edition per populated slot; reprocessing updates those editions without
  creating a second Survey Event or persistent processing-run hierarchy.
- Co-location in FGDB does not establish scientific comparability. Queries and
  analyses must retain observation/derivation method, units/datums, spatial
  and temporal scope, quality, and provenance, and must explicitly select
  Survey Events when composing results across Reaches.
- Project `distance_to_mouth_km` values require an explicit reference
  frame/version, mouth, selected Stream paths, Reach assignments, and Flowline
  calibrations. The numeric measure is not identity and is not accepted solely
  because it exists in a legacy feature class.
- Successful storage or conversion does not establish interoperability. Every
  supported platform binding must demonstrate its declared data-type,
  missing-value, geometry, CRS, constraint, and raster fidelity under a
  versioned crosswalk and conformance test.
- **Mosaic dataset** means the Esri geodatabase data type used to catalog,
  manage, process, and serve raster collections. It does not mean a traditional
  combined raster mosaic or the operation of mosaicking rasters.

## Success criteria

The measurable open-development, storage, service, administration, and
enterprise-conformance criteria are defined in
`open-development-and-enterprise-conformance.md`. Feature-specific criteria
remain in the applicable schema, feature, and workflow contracts.

## Explicitly unresolved

- The authoritative source for each metadata and feature field.
- Exact feature-class, table, relationship, domain, subtype, topology, mosaic
  dataset, and indexing designs.
- Exact Feature Service grouping, layer composition, batching, editing
  transactions, permissions, and client contract versions.
- The exact division between R-based administration, supported Portal
  administration APIs, and licensed ArcPy adapters for FGDB setup.
- Ownership, editing concurrency, sharing, and retention rules for self-service
  Shiny analyses.
- Customer authorization and service-partitioning requirements.
- Canonical identifiers, naming rules, versioning, and survey-event semantics.
- The relationship between filesystem organization and database organization.
- Integration contracts with `FluvialGeomorph-toolbox`, `fluvgeo`, `ohwm2`,
  manuals, and future consumers.
- Persistent ontology namespace ownership, publication infrastructure,
  semantic versioning policy, and the approved external-alignment profile.
