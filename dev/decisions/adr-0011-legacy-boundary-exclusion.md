# ADR-0011: Exclude the legacy boundary feature class

- Status: accepted
- Date: 2026-08-29

## Context

The Papillion wild-caught reach-survey-event geodatabase contains a manually
added polygon feature class named `boundary`. It was not produced, written, or
required by a FluvialGeomorph tool. Its analyst-assigned purpose may have been
to depict a Stream or Reach extent, but the file geodatabase does not provide a
reliable contract establishing which hierarchy entity it represented.

FGDB now has explicit spatial-representation contracts: Study Area geometry is
required, Stream and Reach geometries are optional, and Survey Event geometry
is an optional DEM/analysis AOI supplied by an analyst or derived from the
governed hydro-modified DEM footprint. Inferring one of these governed
representations from an ambiguous convenience layer would create false
authority.

## Decision

1. The legacy `boundary` feature class is excluded from FGDB migration and
   persistence.
2. A loader must not automatically map it to Study Area, Stream, Reach, or
   Survey Event geometry.
3. Its presence or absence is not a load-completeness or QA condition because
   no FluvialGeomorph tool required it.
4. Governed hierarchy geometries are populated independently under their
   accepted contracts and provenance requirements.
5. An analyst may consult a legacy `boundary` as informal evidence when
   deliberately creating or reviewing a governed polygon, but the new polygon
   is a separately asserted FGDB representation; it is not a migrated
   `boundary` record.

## Consequences

- The legacy crosswalk no longer needs to infer an unrecorded semantic role.
- Optional Stream, Reach, and Survey Event geometry remains genuinely optional
  for historical loads.
- Migration validation can ignore `boundary` without losing a tool-produced
  analysis result.
- Any later decision to preserve a particular legacy polygon requires explicit
  analyst review and provenance under the target entity's geometry contract.

## Evidence

- Human-provided workflow clarification from Michael Dougherty, 2026-08-29.
- Papillion R1 2016 XML Workspace schema evidence.
- ADR-0006: optional hierarchy geometry and hydrography names.
- `dev/schemas/feature-catalog.md`.

