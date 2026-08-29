# Semantic interoperability architecture

- Status: proposed
- Updated: 2026-08-28

## Purpose

FGDB needs a semantic layer that preserves scientific meaning independently of
any particular storage or client technology. This layer does not replace the
enterprise geodatabase. It defines the concepts that the geodatabase
implements and provides a controlled path into USACE knowledge graphs.

```text
External standards and reference identifiers
              |
              v
FG semantic crosswalk + controlled vocabularies
              |
              v
Logical feature catalog and integrity rules
              |
              v
Esri/PostgreSQL physical schema and governed services
              |
              v
Future RDF projection / USACE Unified Knowledge Graph
```

The arrows are governed mappings, not assertions that adjacent layers are the
same artifact. Each layer can evolve on its own release cycle while mappings
make the effects of change explicit.

## Artifact responsibilities

| Artifact | Responsibility | Must not become |
|---|---|---|
| FG semantic module | Kernel definitions, identity rules, and reviewed mappings | A full ontology required before schema implementation |
| Controlled vocabularies | Governed values, definitions, aliases, and status | Unexplained coded-value lists |
| External crosswalk | Evidence-backed alignment claims and versions | Label-based equivalence guesses |
| Feature catalog | Human-reviewable logical object and attribute contract | An ontology serialization |
| Future SHACL shapes | Constraints on a future RDF instance graph | A current FGDB implementation dependency |
| Physical schema | Operational storage, keys, relationships, topology, and services | The sole source of term definitions |
| Mapping contract | Reproducible projection between physical records and semantic resources | Application-specific hidden logic |

Database constraints remain authoritative for production writes. Catalog and
ingestion tests verify current rules. Future SHACL tests will validate a
semantic projection after that projection is authorized.

## Identity and geometry

- Every governed object receives an immutable FGDB identifier. An instance IRI
  is deterministically constructed from that identifier after namespace
  governance is established.
- Human-readable names are labels and discovery keys, not identity.
- External identifiers such as national hydrography or Geoconnex identifiers
  are qualified links with source, retrieval date, match method, and review
  status.
- A domain feature and its geometry are different resources conceptually.
  GeoSPARQL provides this separation; the physical implementation may retain
  geometry in the feature class `Shape` column.
- An optional geometry does not make its domain entity optional. Stream and
  Reach remain identifiable even when no defensible polygon exists.

## Current module boundary

The `dev/ontology/` route is a durable semantic-design scaffold. Its
current maintained artifacts are the crosswalk, controlled-vocabulary
requirements, identity rules, and links to governing decisions. A complete
ontology source tree is deferred.

If future USACE knowledge-graph integration requires normative artifacts, they
may include:

```text
dev/ontology/
  README.md
  src/                 # OWL/RDF source modules
  vocab/               # SKOS concept schemes
  shapes/              # SHACL validation shapes
  mappings/            # external and physical-schema mappings
  examples/            # representative instance graphs
  tests/               # reasoning, validation, and mapping tests
```

These artifacts must be promoted through `usace-ukg-ontologies`, whose current
framework uses `https://usace-data.com/` ontology, taxonomy, data, and named
graph namespaces. FGDB will not improvise a public namespace or modify the
TopBraid-compatible hierarchy independently.

## Current-phase schema safeguards

- Give Stream, Reach, Survey Event, current derivation provenance, Flowline,
  Cross Section, retained derived datasets, and derived features explicit
  identifiers and documented identity-change rules.
- Separate persistent entities from their geometries and dataset
  representations.
- Distinguish acquisition meaning from current derivation provenance and
  derived results without requiring discarded source/intermediate datasets or
  processing attempts to become persistent domain entities.
- Use normalized concept/reference tables with stable concept IDs, preferred
  labels, definitions, citations, vocabulary versions, lifecycle status, and
  aliases.
- Store Geoconnex links as qualified external references with match evidence;
  do not make them the FGDB primary key.

## Governance and release rules

1. Pin the version and canonical evidence URL for every external standard.
2. Record whether each alignment is normative, informative, or experimental.
3. Review domain definitions from scientific, production, technical, and data
   interoperability perspectives.
4. Deprecate published terms and mappings rather than deleting or silently
   redefining them.
5. Version the physical schema and semantic mapping independently and publish
   a compatibility matrix when a USACE ontology candidate exists.
6. Test representative legacy, desktop, and Shiny instances before release.
7. Separate ontology term governance from reference-data stewardship; an
   external name suggestion does not redefine an FGDB entity.

## Phased design exercise

1. Answer competency questions using real L1/L2/L3 records and intended graph
   queries.
2. Define a small persistent kernel: Collection, Study Area, Network Scope,
   time-specific Synthetic Network Observation, Stream, Reach, Survey Event,
   hydro DEM, Flowline, longitudinal reference frame/base realization, and
   Cross Section. Exclude the local Stream Geodatabase and its construction
   intermediates under ADR-0010 as partially superseded by ADR-0014.
3. Review external alignments and issue stable local definitions.
4. Finalize the ontology-ready relational schema and ingestion validation.
5. When USACE knowledge-graph integration is scheduled, nominate a candidate
   through `usace-ukg-ontologies`, reserve the approved namespace, and then
   build a minimal OWL/SKOS/SHACL projection.
6. Map one read-only SDE view using the USACE RML conventions and verify
   identifiers, geometry, provenance, and round-trip traceability.
