# Ontology design records

This directory is the design scaffold for FGDB semantic interoperability. It
does not publish a normative ontology, mint persistent terms, or place full
ontology development on the FGDB implementation critical path.

The proposed architecture, standards profile, and governance questions are in
[`dev/architecture/semantic-interoperability.md`](../architecture/semantic-interoperability.md),
with the initial mappings in
[`dev/schemas/ontology-crosswalk.md`](../schemas/ontology-crosswalk.md) and
the proposed decision in
[`dev/decisions/adr-0007-semantic-interoperability-and-ontology-module.md`](../decisions/adr-0007-semantic-interoperability-and-ontology-module.md).

Current work remains in the feature catalog and ontology crosswalk: kernel
definitions, persistent identity rules, current derivation provenance,
controlled-concept requirements, HY_Features mappings, and Geoconnex
external-reference rules.

Any future normative RDF source must be sponsored, validated, versioned, and
registered through the workspace repository `usace-ukg-ontologies`. That
repository—not FGDB—governs the `https://usace-data.com/` ontology framework,
named graphs, candidate pipeline, and manifest. See ADR-0008.
