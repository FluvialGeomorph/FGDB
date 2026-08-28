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

1. Develop the FluvialGeomorph semantic module first as a versioned crosswalk,
   controlled-vocabulary contract, and identity specification distinct from
   both the logical feature catalog and physical FGDB schema. A complete OWL
   ontology is not a prerequisite for FGDB implementation.
2. Use OGC HY_Features as the primary external conceptual alignment for
   hydrographic features. Local concepts remain local when HY_Features has no
   sufficiently precise equivalent.
3. Keep the relational design compatible with a future standards profile using
   OWL 2, SKOS, GeoSPARQL 1.1, PROV-O, SOSA/SSN, DCAT 3, and SHACL. Do not
   implement those projections until they are needed and accepted through the
   USACE ontology framework.
4. Maintain a versioned mapping contract from ontology terms and constraints
   to PostgreSQL/SDE tables, feature classes, relationship classes, domains,
   and mosaic items. Future RML/R2RML projection must follow the conventions of
   `usace-ukg-ontologies`; the operational geodatabase will not store RDF.
5. Base any future instance IRIs on immutable FGDB identifiers, never mutable
   names or Esri `OBJECTID` values. Namespace registration, publication, and
   versioning are governed by `usace-ukg-ontologies` and its
   `https://usace-data.com/` framework.
6. Treat mappings as reviewed claims with recorded evidence and scope.
   `owl:equivalentClass`, `owl:equivalentProperty`, and `owl:sameAs` require
   demonstrated identity; similarity alone uses a weaker relation or remains
   an explanatory note.
7. Use Geoconnex as the standard external reference-feature interface and
   source of persistent hydrologic links, not as the normative definition of
   the FG domain. Apply ADR-0008's qualified-link rules.
8. Treat hydrOntology and the USGS Surface Water Ontology/design pattern as
   informative prior art. Their distinctions—especially channel landform
   versus water body—remain useful, but their age and apparent maintenance
   state do not justify making either the normative base.

## Consequences

- The same scientific concept can be implemented consistently in the feature
  catalog, geodatabase, APIs, RDF projection, and documentation.
- FGDB can participate in knowledge graphs without coupling production writes
  to a graph database.
- Stable schema design and ingestion remain ahead of full ontology
  implementation on the critical path.
- Crosswalks and transformations become governed release artifacts that need
  tests, review, version pinning, and deprecation policy.
- Some familiar words will require sharper local definitions. In particular,
  `Stream`, `Reach`, and `Survey Event` cannot be assigned external identity by
  label matching alone.
- Initial work is slower than copying legacy fields directly, but semantic
  ambiguity is exposed before it becomes a long-lived physical contract.

## Acceptance questions

- Which `usace-ukg-ontologies` maintainers will sponsor and review a future
  FluvialGeomorph candidate and namespace reservation?
- What are the identity rules for Survey Events, their one-to-one current
  derivation provenance, and their retained derived datasets/features when
  legacy source metadata is incomplete?
- Does FG `Stream` denote a named hydrographic feature, a channel landform, a
  water body, or a managed aggregate with those aspects?
- What continuity rule makes a Reach the same Reach across survey events?
- Which physical-to-RDF mapping mechanism is supportable alongside SDE if and
  when semantic projection becomes an implementation requirement?
