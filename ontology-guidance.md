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
   * Survey/acquisition event
   * Analysis/processing event
   * Source and derived datasets
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
* Survey/acquisition
* Analysis/processing run
* Flowline
* Cross Section
* derived geomorphic feature
* source dataset
* derived dataset

For each entity document:

> What properties may change while this remains the same entity, and what change creates a new entity?

## Reach modeling

Do not assume that Reach is simply a persistent physical child of Stream.

Treat Reach as a potentially study- or analysis-specific segmentation of a persistent hydrologic feature unless evidence supports a stronger identity model.

Ensure the schema can represent different reach segmentations of the same stream across studies or analysis versions without corrupting stream identity.

## Survey versus analysis provenance

Do not overload one `SurveyEvent` concept to mean all of:

* field or remote-sensing acquisition;
* source dataset creation;
* analysis execution;
* generation of derived features.

Model enough separation to preserve lineage such as:

acquisition/observation
→ source dataset
→ analysis/processing activity
→ derived dataset/features

The implementation does not need to use PROV-O now, but it should remain compatible with a future provenance mapping.

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
