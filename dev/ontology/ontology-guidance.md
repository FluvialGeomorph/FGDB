# Ontology design guidance

Continue FGDB development with the following semantic-interoperability constraints.

## Immediate objective

Prioritize a stable, production-ready FGDB logical/physical schema that can ingest and roll up outputs from the FluvialGeomorph toolbox. Do not make development of a full fluvial geomorphology ontology a prerequisite for FGDB implementation.

## Semantic scope for this phase

1. Continue using `dev/schemas/ontology-crosswalk.md` as the primary semantic design artifact.
2. Complete OGC HY_Features crosswalks only for FGDB kernel entities where the mapping affects schema design or persistent identity.
3. Focus especially on:

   * Stream
   * Reach
   * Synthetic Network
   * Flowline
   * Flowline location/stationing
   * Cross Section
   * Study Area
   * Survey Event
   * Current derivation provenance
   * Known source references and retained derived datasets
4. Treat HY_Features as a conceptual interoperability model. Do not reproduce the HY_Features UML/database structure inside FGDB unless a specific requirement justifies it.
5. Preserve the distinction between persistent real-world hydrologic entities and their geometric/data representations.

## Defer full ontology implementation

Do not require development of:

* a full `fluvial_geomorphology` OWL ontology;
* BFO alignment;
* SWEET/ENVO integration;
* SHACL;
* R2RML/RDF generation;
* formal process-form ontology relationships;
* comprehensive ontology treatment of riffles, pools, bars, bankfull features, valley features, or later L2/L3 geomorphic products.

These should remain future semantic-projection work unless an immediate FGDB schema decision depends on them.

## Govern geomorphic terminology now

For geomorphic feature types such as riffle, pool, bankfull polygon, bankline, valley bottom, bars, and future L2/L3 features:

* use stable controlled concept identifiers rather than uncontrolled strings;
* maintain preferred label;
* maintain definition;
* maintain authoritative source/citation;
* maintain vocabulary/version information;
* maintain lifecycle/status such as proposed, accepted, deprecated;
* preserve aliases/synonyms where useful.

Design this controlled vocabulary so it can later be mapped to SKOS/OWL without changing existing FGDB records.

## Persistent identity

Do not use ArcGIS `OBJECTID`, geometry, display name, database location, or project-specific numbering as persistent identity.

Define stable identifiers and explicit identity rules for at least:

* Stream
* Reach
* Survey Event
* Current derivation-provenance record
* Flowline
* Cross Section
* derived geomorphic feature
* source dataset, when retained or externally identifiable
* derived dataset

For each entity document:

> What properties may change while this remains the same entity, and what change creates a new entity?

## Reach modeling

Do not assume that Reach is simply a persistent physical child of Stream.

Treat Reach as a potentially study- or analysis-specific segmentation of a persistent hydrologic feature unless evidence supports a stronger identity model.

Ensure the schema can represent different reach segmentations of the same stream across studies or analysis versions without corrupting stream identity.

## Project-defined extent and referencing

Do not align FGDB Stream or Reach extent to national feature geometry,
segmentation, route measures, or watershed boundaries. When present, the
entity's own stored FGDB geometry is its only direct extent assertion.

Do not require a national linear referencing system. Local stationing may use
a specific stored FGDB Flowline, but must retain its reference Flowline ID,
origin, direction, units, method, and Survey Event or representation scope.
HY_Features river-referencing concepts are candidate semantic mappings, not a
requirement to adopt an external route or treat local measures as globally
comparable.

## Stream entity versus preprocessing workspace

Do not model the local `Stream Geodatabase` (legacy `Site Geodatabase`) as a
domain class or confuse it with the persistent FGDB Stream. It is an optional
desktop workspace used to derive/edit a synthetic network and establish Reach
segmentation. Its Stream-scale DEM, pre-segmentation network, and construction
intermediates are outside FGDB persistence scope.

The synthetic network may be described in the semantic crosswalk as a
derivation-stage representation, but the current physical model does not
assign it persistent FGDB identity. Durable Stream/Reach identities and any
separately governed downstream features carry the accepted result of the
analyst's segmentation decision. Full reconstruction remains dependent on
local retention outside FGDB.

## Survey Event versus derivation provenance

Preserve the conceptual distinction between:

* field or remote-sensing acquisition;
* known source data or source references;
* derivation of the current accepted content; and
* the current derived features and rasters.

Do not require those distinctions to become separate levels in the persistent
domain hierarchy. The operational FGDB relationship is:

Reach
→ many Survey Events
→ one current derivation-provenance record per populated Survey Event
→ one current accepted derived result set

Reprocessing an existing Survey Event replaces incorrect current content and
updates its current derivation provenance; it does not create another Survey
Event or a persistent one-to-many processing-run hierarchy. Optional execution
or load-attempt history is operational audit data, not authoritative domain
content.

Legacy Survey Events may have no retained point clouds, intermediate products,
tile footprints, clearinghouse URI, or complete acquisition metadata. Record
those facts as unknown or not retained rather than fabricating source dataset
instances. The implementation does not need to use PROV-O now, but the current
derivation record should remain compatible with a future provenance mapping.

## Required provenance

FGDB should be able to answer, for any important derived feature:

* what source data produced it;
* when those data were acquired;
* what analysis/tool generated it;
* which FluvialGeomorph toolbox/software version was used;
* which relevant parameters/configuration were used;
* when processing occurred;
* which study/reach/context it belongs to.

## Ontology-ready database design

Design FGDB so a future RDF/OWL semantic projection can be added without redesigning the enterprise schema.

Prefer:

* persistent IDs;
* explicit foreign-key relationships;
* normalized reference/concept tables;
* controlled vocabularies;
* documented cardinalities;
* explicit provenance;
* clear separation of entities from representations.

Avoid:

* semantic meaning encoded only in field names;
* magic strings;
* undocumented coded values;
* conflating concepts because they currently share geometry;
* table structures that require ontology concepts to correspond one-to-one with database tables.

## Deliverables for the current development phase

Prioritize:

1. finalized FGDB kernel entity model;
2. identity rules for kernel entities;
3. HY_Features crosswalk for relevant kernel concepts;
4. revised Survey/Analysis provenance model;
5. governed geomorphic feature-type vocabulary;
6. relational/cardinality rules;
7. enterprise geodatabase implementation;
8. ingestion and validation workflows.

Keep full `fluvial_geomorphology` ontology development explicitly out of the critical path.

When architectural questions arise, use this decision rule:

> Formalize only enough semantics now to prevent a bad FGDB schema or loss of future interoperability. Defer semantics that can be added later through controlled vocabulary mappings or an RDF/OWL projection without changing the underlying database.
