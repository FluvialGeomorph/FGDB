# Feature derivation consistency

## Problem

FGDB must support robust analysis of fluvial change over long periods and at
continental scale. Differences caused by derivation software must not be
silently interpreted as physical change.

## Current flowline evidence

| Behavior | Esri Python `_05a_Flowline.py` | R `fluvgeo::flowline()` |
|---|---|---|
| Input | Edited stream-network feature class | One `sf` line and a DEM |
| Reach handling | Dissolves segments by `ReachName` | Requires one feature and assigns one reach name |
| Shape processing | PAEK smoothing with supplied tolerance | No line smoothing |
| Direction | No DEM-based orientation in this function | Reverses line when needed so it is oriented upstream |
| Output count | Potentially one feature per reach name | Exactly one feature |
| Runtime | ArcPy/ArcGIS | Open-source R spatial stack |

The R tests verify single-feature structure, the expected schema through
`check_flowline()`, and upstream orientation. The discovered Python test refers
to an older module/function signature and a network file path, so it is not
current parity evidence for `_05a_Flowline.py`.

The ArcPy dissolve-by-`ReachName` behavior is a relic of an early, uncompleted
multi-Reach processing design. Production settled on one Reach per derivation
workspace because REM and downstream analysis assumptions are Reach-scale.
Under ADR-0012, multi-Reach vectorization is not a canonical parity
requirement: `{fluvgeo}` derives one Reach at a time, and FGDB composes those
results through hierarchy queries.

## Required canonical contract

Before replacing the Python flowline path, the owning repositories must define:

- accepted single-Reach input geometry and multipart behavior;
- verification that the input and output bind to exactly one Reach and Survey
  Event identity;
- binding of terrain-derived input geometry to its governed Synthetic Network
  Observation and source segment identities;
- output geometry type, fields, nullability, and topology;
- required CRS and horizontal/vertical unit handling;
- smoothing purpose, algorithm, parameter units, and acceptable geometric
  deviation;
- line orientation and behavior for flat, missing, or ambiguous endpoint
  elevations;
- error and warning behavior;
- deterministic method/version identifier; and
- performance requirements for large desktop study areas.

## Buildout and migration pattern

1. Build the FGDB catalog in workflow and dependency order, beginning with
   study-area definition and terrain inputs rather than flowline.
2. Inventory paired ArcPy and `{fluvgeo}` capabilities by feature family as
   each derived stage is reached.
3. Define the current desktop workflow order, manual interventions, and known
   failure modes alongside the streamlined Shiny workflow.
4. Select one bounded paired-implementation contract pilot when the catalog
   reaches such a stage; flowline remains a useful candidate, not the first
   catalog object.
5. Define the canonical schema and scientific invariants in `fluvgeo`.
6. Assemble representative, provenance-documented fixtures, including legacy
   edge cases.
7. Implement missing open-source stages without coupling them to Shiny state.
8. Continue until a coherent end-to-end `{fluvgeo}` workflow exists; do not
   repeatedly interrupt desktop production with partial cutovers.
9. Compare old and new outputs using topology, attributes, direction,
   length/shape tolerances, downstream metric sensitivity, and performance.
10. Obtain scientific approval for equivalence or an intentional method change.
11. Overhaul the desktop workflow as a coordinated migration that calls the
    complete canonical pipeline while preserving expert editing convenience.
12. Run producer tests first, then desktop and Shiny integration tests.
13. Release, document provenance/version boundaries, and deprecate duplicate
    ArcPy derivation only after rollback remains possible.

## FGDB requirements

FGDB ingestion and schemas must retain enough provenance to determine, for each
feature family:

- source application and version;
- derivation engine and method identifier;
- `{fluvgeo}` version when applicable;
- material parameters such as smoothing tolerance and station interval;
- source/load manifest; and
- validation contract version.

For longitudinal comparison, provenance also identifies the governed
reference frame, whether the Flowline is the selected base realization for its
Reach assignment, and the reviewed calibration used for a comparison
Flowline. Base status is not stored as a global Survey Event attribute.

This provenance supports scientific interpretation; it does not justify
retaining known-bad feature records in the active desktop collection.
