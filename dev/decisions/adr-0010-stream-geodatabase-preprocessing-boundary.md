# ADR-0010: Stream Geodatabase preprocessing boundary

- Status: accepted
- Date: 2026-08-28

## Context

The historical desktop workflow has sometimes used a cross-reach file
geodatabase called the `Site Geodatabase`. The preferred name for this role is
`Stream Geodatabase`. An analyst may use it to hold a Stream-scale DEM, derive
and edit a synthetic stream network, divide a long Stream into Reaches, and
optionally clip the Stream-scale DEM into manageable Reach-scale terrains.

This work establishes analysis units and prepares inputs for the governed
reach-survey-event workflow. It is not itself a durable analysis result. Any
geometry needed downstream is copied or transformed into the applicable
reach-survey-event workspace. Historical practice has not required retention
of every Stream Geodatabase, source point cloud, terrain intermediate, or
synthetic-network construction artifact.

## Decision

1. `Stream Geodatabase` is the preferred name for this optional local
   preprocessing workspace. `Site Geodatabase` is a legacy alias and does not
   define an FGDB domain entity.
2. A Stream Geodatabase is not an FGDB hierarchy level, migration unit, load
   package, or governed database object. The FGDB `Stream` entity remains a
   durable hierarchy object and must not be conflated with this workspace.
3. FGDB does not retain the Stream-scale DEM, the pre-segmentation synthetic
   stream network, flow-direction/accumulation products, or other construction
   intermediates from this workspace.
4. The analyst's reviewed Stream and Reach segmentation is represented by the
   durable FGDB hierarchy records. Only downstream features and rasters that
   enter an accepted reach-survey-event package and have a governed catalog
   contract are loaded. Copying source geometry into that workspace does not,
   by itself, make the preprocessing artifact governed.
5. The retained Reach/Survey Event hydro-modified DEM and governed downstream
   features are the authoritative FGDB analysis products after applicable QA.
6. A project that requires complete process reproducibility must retain its
   local inputs and preprocessing workspace outside FGDB. FGDB requires
   traceability and provenance for retained results, but does not promise
   reconstruction from every discarded input and intermediate.
7. A future need to retain a Stream-scale terrain or synthetic network requires
   a reviewed catalog contract and a new decision; it must not be introduced
   implicitly by a loader.

## Consequences

- The unresolved ownership problem for a network created before final
  Stream/Reach segmentation is removed from the FGDB physical model.
- No target `FG_StreamNetwork` or Stream-scale terrain mosaic item is required
  for the current scope.
- Migration tooling must classify these preprocessing artifacts as excluded,
  even if a legacy reach geodatabase contains a convenience copy. It may use
  them as transformation evidence for a separately governed downstream object.
- FGDB preserves the scientifically reviewed segmentation and accepted results
  without becoming a complete archive of the analyst's local processing state.
- Tech and User Manual terminology should be updated separately and carefully,
  because historical uses of `Site Geodatabase` include other cross-reach
  operations beyond synthetic-network derivation.

## Evidence

- Human-provided workflow clarification from Michael Dougherty, 2026-08-28.
- `FG-Tech-Manual/DB-migration.qmd`, especially proposed nested Stream and Reach
  folders and the reach-survey-event feature inventory.
- `FG-User-Manual/Concepts.qmd` and `FG-User-Manual/Level-1.qmd`.
- ADR-0005: governed foundation scope.
- ADR-0006: optional hierarchy geometry and hydrography names.

