# ADR-0009: Project-defined Stream and Reach extent and referencing

- Status: accepted
- Date: 2026-08-28

## Context

FGDB often represents small or unnamed streams that have no standardized
national linear referencing system. Its Streams and Reaches are delineated for
specific investigations from high-resolution terrain and analyst judgment.
Their extents do not correspond to the extents or segmentation of features in
national hydrography systems.

National systems remain valuable for candidate names, identifiers, discovery,
and contextual linkage. Treating their geometry, segmentation, or measures as
FGDB authority would nevertheless misrepresent the investigation and make
unnamed streams difficult or impossible to store consistently.

## Decision

1. FGDB Stream and Reach extent is project-defined. When an optional Stream or
   Reach geometry is stored, that geometry is the only direct representation
   of its FGDB extent. If no geometry is stored, FGDB makes no independent
   polygon-extent assertion for that entity.
2. National hydrography geometry, watershed boundaries, segment endpoints,
   measures, and linear referencing systems do not define or constrain FGDB
   Stream or Reach extent, identity, segmentation, or parentage.
3. Geoconnex and national feature identifiers are qualified contextual links.
   Spatial overlap, a shared name, or a candidate reference does not assert
   geometric equivalence or feature identity.
4. FGDB requires no independent national linear referencing system. Local
   stationing may reference an FGDB-stored Flowline representation. Its
   contract must identify the Flowline, origin, direction, units, method, and
   applicable Survey Event or representation version.
5. Local station values do not establish Stream or Reach identity and are not
   assumed comparable across different Flowlines or Survey Events without an
   explicit alignment method.
6. The governed hydro-modified DEM and derived features for each Survey Event
   are the authoritative FluvialGeomorph analysis products after applicable
   collection QA. This does not make FGDB the authority for discarded source
   point clouds or national hydrography.

## Consequences

- Small and unnamed streams can participate fully without a national segment
  or route identifier.
- External interoperability uses stable FGDB IDs, explicit geometry, qualified
  links, and documented mappings rather than forced shared segmentation.
- Applications must not substitute a national feature geometry when an FGDB
  Stream or Reach geometry is absent.
- Flowline stationing requires a local, version-aware referencing contract;
  measures must be recomputed or explicitly transformed when the reference
  Flowline changes.
- Multi-time-period analysis can preserve the project's own scientifically
  governed terrain and geometry without implying that all observations share a
  national reference route.

## Evidence

- Human-provided production and research history from Michael Dougherty.
- ADR-0006: optional hierarchy geometry and national hydrography names.
- `dev/schemas/feature-catalog.md`
- `dev/schemas/ontology-crosswalk.md`

