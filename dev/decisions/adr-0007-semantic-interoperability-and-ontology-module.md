# ADR-0007: Semantic interoperability and an FG ontology module

- Status: proposed
- Date: 2026-08-28

## Context

FGDB needs stable scientific meaning beyond the names and constraints that can
be expressed in an Esri enterprise geodatabase. Its content must remain
interpretable across desktop, browser, service, and future USACE knowledge
graph implementations. The physical schema must therefore implement, but not
silently define, the domain semantics.

Relevant standards do not provide a complete FluvialGeomorph vocabulary.
OGC HY_Features supplies a strong conceptual model for hydrologic features and
their multiple spatial representations, but intentionally avoids terms such as
`reach` whose meanings vary by community. General W3C and OGC standards supply
the remaining semantic infrastructure. Older domain ontologies are useful
design evidence but are not sufficiently current to adopt as FGDB's normative
foundation.

## Proposed decision

1. Develop a versioned FluvialGeomorph ontology module as a semantic contract
   distinct from both the logical feature catalog and physical FGDB schema.
2. Use OGC HY_Features as the primary external conceptual alignment for
   hydrographic features. Local concepts remain local when HY_Features has no
   sufficiently precise equivalent.
3. Use the following standards profile:
   - RDF and OWL 2 for identifiers, classes, properties, and formal axioms;
   - SKOS for controlled concepts, definitions, alternate labels, and
     qualified mapping assertions;
   - GeoSPARQL 1.1 for features, geometries, and spatial relations;
   - PROV-O for derivation, loading, replacement, agents, and software
     provenance;
   - SOSA/SSN 2023 as a candidate model for observations and collections of
     observations, subject to a Survey Event modeling exercise;
   - DCAT 3 for discoverable datasets, distributions, and data services; and
   - SHACL 1.0 for validating RDF graph constraints.
4. Maintain a versioned mapping contract from ontology terms and constraints
   to PostgreSQL/SDE tables, feature classes, relationship classes, domains,
   and mosaic items. Evaluate R2RML for relational views that can be projected
   as RDF, without requiring the operational geodatabase itself to store RDF.
5. Base instance IRIs on immutable FGDB identifiers, never mutable names or
   Esri `OBJECTID` values. Do not select or publish the persistent namespace
   until USACE knowledge-graph ownership and identifier governance are known.
6. Treat mappings as reviewed claims with recorded evidence and scope.
   `owl:equivalentClass`, `owl:equivalentProperty`, and `owl:sameAs` require
   demonstrated identity; similarity alone uses a weaker relation or remains
   an explanatory note.
7. Evaluate Geoconnex as a linked-data integration profile and source of
   persistent reference-feature links, not as the normative definition of the
   FG domain.
8. Treat hydrOntology and the USGS Surface Water Ontology/design pattern as
   informative prior art. Their distinctions—especially channel landform
   versus water body—remain useful, but their age and apparent maintenance
   state do not justify making either the normative base.

## Consequences

- The same scientific concept can be implemented consistently in the feature
  catalog, geodatabase, APIs, RDF projection, and documentation.
- FGDB can participate in knowledge graphs without coupling production writes
  to a graph database.
- Crosswalks and transformations become governed release artifacts that need
  tests, review, version pinning, and deprecation policy.
- Some familiar words will require sharper local definitions. In particular,
  `Stream`, `Reach`, and `Survey Event` cannot be assigned external identity by
  label matching alone.
- Initial work is slower than copying legacy fields directly, but semantic
  ambiguity is exposed before it becomes a long-lived physical contract.

## Acceptance questions

- Which USACE organization controls the persistent namespace and publication
  endpoint?
- Is a Survey Event principally an observation collection, a provenance
  activity, a dataset grouping, or a local concept related to all three?
- Does FG `Stream` denote a named hydrographic feature, a channel landform, a
  water body, or a managed aggregate with those aspects?
- What continuity rule makes a Reach the same Reach across survey events?
- Which physical-to-RDF mapping mechanism is supportable alongside SDE?

