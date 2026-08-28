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
FG ontology + controlled vocabularies + external crosswalk
              |
              v
Logical feature catalog and integrity rules
              |
              v
Esri/PostgreSQL physical schema and governed services
              |
              v
Versioned RDF projection / USACE knowledge graph
```

The arrows are governed mappings, not assertions that adjacent layers are the
same artifact. Each layer can evolve on its own release cycle while mappings
make the effects of change explicit.

## Artifact responsibilities

| Artifact | Responsibility | Must not become |
|---|---|---|
| FG ontology | Machine-readable domain meaning and relationships | A copy of table structure |
| Controlled vocabularies | Governed values, definitions, aliases, and status | Unexplained coded-value lists |
| External crosswalk | Evidence-backed alignment claims and versions | Label-based equivalence guesses |
| Feature catalog | Human-reviewable logical object and attribute contract | An ontology serialization |
| SHACL shapes | Constraints on RDF instance graphs | The only integrity mechanism |
| Physical schema | Operational storage, keys, relationships, topology, and services | The sole source of term definitions |
| Mapping contract | Reproducible projection between physical records and semantic resources | Application-specific hidden logic |

Database constraints remain authoritative for production writes. SHACL tests
the semantic projection, while catalog and ingestion tests verify that the
database implements the same rules.

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

## Planned module boundary

The repository-level `ontology/` module begins as a design scaffold. If
ADR-0007 is accepted, its likely release artifacts are:

```text
ontology/
  README.md
  src/                 # OWL/RDF source modules
  vocab/               # SKOS concept schemes
  shapes/              # SHACL validation shapes
  mappings/            # external and physical-schema mappings
  examples/            # representative instance graphs
  tests/               # reasoning, validation, and mapping tests
```

Directories and normative RDF sources should be added only when they contain
reviewable content. A namespace must not be improvised from a source-control
URL if USACE will own the persistent identifiers.

## Governance and release rules

1. Pin the version and canonical evidence URL for every external standard.
2. Record whether each alignment is normative, informative, or experimental.
3. Review domain definitions from scientific, production, technical, and data
   interoperability perspectives.
4. Deprecate published terms and mappings rather than deleting or silently
   redefining them.
5. Version ontology, physical schema, and mapping contract independently and
   publish a compatibility matrix.
6. Test representative legacy, desktop, and Shiny instances before release.
7. Separate ontology term governance from reference-data stewardship; an
   external name suggestion does not redefine an FGDB entity.

## Phased design exercise

1. Answer competency questions using real L1/L2/L3 records and intended graph
   queries.
2. Define a small kernel: Collection, Study Area, Stream, Reach, Survey Event,
   hydro DEM, synthetic network, Flowline, and Cross Section.
3. Review external alignments and issue stable local definitions.
4. Select namespace governance and build a minimal OWL/SKOS/SHACL prototype.
5. Map one read-only SDE view to RDF and verify identifiers, geometry,
   provenance, and round-trip traceability.
6. Expand the ontology only as the feature catalog advances through workflow
   order.

