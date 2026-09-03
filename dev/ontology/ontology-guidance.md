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
   * Accepted dataset-edition provenance
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
* Derived Dataset and accepted Dataset Edition
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

Do not require a national linear referencing system. FGDB uses a governed
project longitudinal reference frame anchored to a project-defined Stream or
Study Area/watershed mouth. Reach path/interval assignments and Flowline
calibrations relate Survey Event representations to that frame. Materialized
positions must retain frame/version, reference Flowline, direction, units,
method, and representation scope. HY_Features river-referencing concepts are
candidate semantic mappings, not a requirement to adopt an external route or
treat project measures as globally comparable.

The reference frame, Stream path, Reach assignment, Flowline calibration, and
materialized hydro-location are distinct semantic resources. Do not encode
their meanings only in a numeric `km_to_mouth` attribute. The numeric position
is not an identifier and may repeat on separate tributaries.

Reach-owned representations may be composed for Stream- or Study Area-scale
analysis, but semantic projection must preserve each feature's direct Survey
Event owner and provenance. A composed Stream longitudinal profile is a query
or analysis result, not evidence that its Reach Flowlines share identity.
Cross-Reach station alignment and temporal selection must be explicit.

Keep the kernel observation-method neutral. Historic manual surveys and modern
remote-sensing derivations may instantiate common feature concepts only when
their method, measurement definition, units/datums, quality, temporal scope,
and provenance remain available for fitness and comparability assessment.

## Stream entity versus Stream Geodatabase

Do not model the local `Stream Geodatabase` (legacy `Site Geodatabase`) as a
domain class or confuse it with the persistent FGDB Stream. It is the local
database of record used to derive, review, and retain a Stream Network and
establish Reach segmentation. Its Stream-scale DEM and construction
intermediates are outside FGDB persistence scope.

The reviewed synthetic network is a governed, time-specific observation with
persistent FGDB identity. Model it separately from the durable Stream and Reach
entities: a Study-Area-owned Stream Network Configuration defines whether the observation
represents a connected multi-Stream network or one independently derived
Stream, while each Stream Network Observation represents the terrain time from which
its segment geometry and topology were derived. Candidate semantic alignment
is HY `HY_ChannelNetwork`, qualified by local derivation, temporal, and
provenance constraints. Full process reconstruction still depends on local
retention outside FGDB. See ADR-0014.

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
→ many typed Derived Dataset slots per Survey Event
→ one current accepted Dataset Edition per populated slot

Reprocessing an existing Survey Event replaces incorrect current content and
updates its current accepted edition; it does not create another Survey Event
or turn raw processing runs into a persistent domain hierarchy. Optional
execution or load-attempt history is operational audit data. Known-bad feature
rows are removed, while their invalidated edition metadata may remain as audit
and provenance evidence.

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
