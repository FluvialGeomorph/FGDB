# ADR-0010: Stream Geodatabase preprocessing boundary

- Status: accepted as amended by ADR-0014 and ADR-0019
- Date: 2026-08-28

## Context

The historical desktop workflow has sometimes used a cross-reach file
geodatabase called the `Site Geodatabase`. The preferred name for this role is
`Stream Geodatabase`. An analyst may use it to hold a Stream-scale DEM, derive
and edit a synthetic stream network, divide a long Stream into Reaches, and
optionally clip the Stream-scale DEM into manageable Reach-scale terrains.

This work establishes analysis units and prepares inputs for the governed
reach-survey-event workflow. Historical practice has not required retention of
every Stream Geodatabase, source point cloud, terrain intermediate, or
synthetic-network construction artifact. The reviewed `stream_network` and its
related configuration, observation, lineage, review, and validation records are
now governed outputs under ADR-0014 and ADR-0019.

## Decision

1. `Stream Geodatabase` is the preferred name for this optional local
   preprocessing workspace. `Site Geodatabase` is a legacy alias and does not
   define an FGDB domain entity.
2. A Stream Geodatabase is the local database of record for Stream Network
   feature classes and related tables, but it is not itself an FGDB hierarchy
   entity. The FGDB `Stream` remains a durable hierarchy object and must not be
   conflated with the physical geodatabase.
3. FGDB does not retain the Stream-scale DEM, the pre-segmentation synthetic
   stream network, flow-direction/accumulation products, or other construction
   intermediates from this workspace.
4. The analyst's reviewed Stream and Reach segmentation is represented by the
   durable hierarchy records and approved `stream_network` feature rows. FGDB
   loads only feature classes, tables, and rasters defined by the governed
   schema. Copying source geometry into a geodatabase does not, by itself, make
   that geometry governed.
5. The retained Reach/Survey Event hydro-modified DEM and governed downstream
   features are the authoritative FGDB analysis products after applicable QA.
6. A project that requires complete process reproducibility must retain its
   local inputs and preprocessing workspace outside FGDB. FGDB requires
   traceability and provenance for retained results, but does not promise
   reconstruction from every discarded input and intermediate.
7. The reviewed `stream_network` feature class and related governed tables load
   under the Stream Network Geodatabase schema. Stream-scale terrain and
   construction intermediates remain excluded unless separately governed.

## Consequences

- Stream Network Configuration and Observation identities resolve ownership
  before and across final Stream/Reach segmentation.
- The enterprise `stream_network` feature class is required; a Stream-scale
  terrain mosaic item is not.
- Migration tooling distinguishes reviewed Stream Network geometry from
  pre-segmentation and construction artifacts. A legacy convenience copy may be
  used as evidence only after classification and validation.
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
