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

## Flowline contract status

The first concrete contract is now specified in
`dev/schemas/flowline-feature-contract.md`. It resolves:

- one Flowline per current `FLOWLINE` Dataset Edition and Survey Event role;
- a continuous, logically single-part, upstream-oriented XY line;
- immutable Flowline identity separated from accepted edition/realization;
- normalized source-segment and hydro-DEM orientation evidence;
- exclusion or relational reinterpretation of legacy process, length, and
  route-measure fields; and
- distinct legacy ArcPy and current R method contracts with no presumed
  equivalence.

Scientific review still must define smoothing/channel-corridor tolerances,
orientation ambiguity behavior, the future open derivation recipe, and
performance requirements before the Python path can be replaced.

## Buildout and migration pattern

1. Build the FGDB catalog in workflow and dependency order, beginning with
   study-area definition and terrain inputs rather than flowline.
2. Inventory paired ArcPy and `{fluvgeo}` capabilities by feature family as
   each derived stage is reached.
3. Define the current desktop workflow order, manual interventions, and known
   failure modes alongside the streamlined Shiny workflow.
4. Use the Flowline contract as the first bounded paired-implementation pilot.
5. Define the canonical schema and scientific invariants in `fluvgeo`.
6. Assemble representative, provenance-documented direct producer outputs,
   including legacy edge cases, through `fluvgeodata`.
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
