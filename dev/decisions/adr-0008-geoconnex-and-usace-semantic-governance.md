# ADR-0008: Geoconnex access and USACE semantic governance

- Status: accepted
- Date: 2026-08-28

## Context

FGDB needs one supported way to discover and reference external hydrologic
features. It must also fit the emerging USACE Unified Knowledge Graph rather
than create an independent publication and governance framework. The current
`fluvgeo` package depends on the retiring `nhdplusTools` package for NLDI
processing calls. Its replacement, `hydrogeofetch`, preserves those APIs and
also provides direct Geoconnex reference-feature discovery and retrieval.

The design constraints in `dev/ontology/ontology-guidance.md` require enough semantics to
protect the FGDB schema and future interoperability, while keeping a complete
fluvial geomorphology ontology and RDF projection outside the implementation
critical path.

## Decision

1. Geoconnex is the standard external reference-feature interface for FGDB and
   FluvialGeomorph workflows. Product-specific USGS services may still perform
   specialized processing, but returned identity links are normalized through
   the FGDB external-reference contract where Geoconnex coverage exists.
2. `fluvgeo` will replace its direct `nhdplusTools` dependency with
   `hydrogeofetch`. New Geoconnex access will use
   `discover_geoconnex_reference()` and `get_geoconnex_reference()` rather
   than application-specific HTTP calls.
3. A Geoconnex URI is a qualified external identifier, not FGDB identity.
   Store the URI, collection/type, label if supplied, retrieval time, client
   and service version where available, match method, analyst disposition, and
   relationship strength. Do not infer `owl:sameAs` from a spatial or name
   match.
4. `usace-ukg-ontologies` is authoritative for USACE ontology namespaces,
   ontology promotion, versioning, named graphs, and semantic validation.
   FGDB may develop definitions and crosswalk candidates locally, but any
   normative OWL/SKOS module must pass that repository's candidate pipeline
   and be registered in its manifest.
5. FGDB will not mint an independent public ontology namespace. A future
   FluvialGeomorph namespace and instance-URI pattern require coordination
   with the maintainers of `usace-ukg-ontologies` and must follow the
   `https://usace-data.com/` conventions they approve.
6. The current deliverable is an ontology-ready relational schema: immutable
   IDs, explicit relationships, controlled concept tables, accepted
   dataset-edition provenance with one current edition per populated dataset
   slot, and HY_Features kernel mappings. Full OWL, SHACL, RML/R2RML, and RDF generation remain
   future semantic-projection work unless a physical-schema decision
   demonstrably depends on them.

## Clarification of current service use

The existing `fluvgeo::pt_watershed_area()` calls
`get_raindrop_trace()` and `get_split_catchment()`. These are NLDI/processing
service operations exposed by `hydrogeofetch`; they are not direct Geoconnex
reference-feature queries. Migrating the package dependency is therefore
separate from adding a governed Geoconnex identifier-discovery workflow.

## Consequences

- External hydrographic links become portable, reviewable references rather
  than hidden names or service-specific keys.
- `fluvgeo` follows the supported USGS R package transition without changing
  the two currently used function signatures.
- FGDB can proceed to enterprise-schema implementation before a full ontology
  is published.
- Semantic artifacts eventually intended for the USACE knowledge graph must
  comply with its namespace, metadata, TopBraid directory, review, validation,
  semantic-versioning, and manifest rules.
- Geoconnex availability, collection changes, ambiguity, and outages require
  explicit client behavior; an external lookup cannot be a hidden prerequisite
  for preserving an already established FGDB identity.

## Evidence

- `dev/ontology/ontology-guidance.md`
- `../usace-ukg-ontologies/README.md`
- `../usace-ukg-ontologies/MANIFEST.md`
- `../usace-ukg-ontologies/CONTRIBUTING.md`
- `../fluvgeo/R/pt_watershed_area.R`
- `hydrogeofetch` migration and reference documentation
