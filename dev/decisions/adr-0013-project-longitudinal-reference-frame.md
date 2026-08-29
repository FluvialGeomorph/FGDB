# ADR-0013: Governed project longitudinal reference frame

- Status: accepted
- Date: 2026-08-29

## Context

The optional Stream Geodatabase was historically used to derive and edit the
synthetic network, divide it into Streams and Reaches, and linearly reference
each Reach to a common downstream mouth. For a single-Stream analysis, the
mouth was the downstream-most project point on that Stream. For a Study Area
treated as a connected watershed network, the watershed outlet was the common
mouth and all participating Streams and Reaches used distance along the
selected network path to that origin.

This produced `km_to_mouth`, a common longitudinal coordinate that allowed
independently processed Reaches and tributaries to be assembled for analysis.
The historical workflow depended on analyst expertise and contained no durable
mechanism to enforce scope, origin, topology, direction, calibration, units, or
continuity. The Stream Geodatabase itself remains an excluded preprocessing
workspace under ADR-0010, but the accepted reference-frame definition and
calibration are scientifically meaningful governed outputs.

## Decision

1. FGDB will govern a project-defined longitudinal reference frame independent
   of national linear referencing systems and independent of any one Survey
   Event Flowline geometry.
2. A reference frame has exactly one Study Area owner and one scope mode:
   `STREAM` for one Stream or `STUDY_AREA_NETWORK` for a connected set of
   Streams within the Study Area.
3. The frame has one explicit mouth/origin. Canonical
   `distance_to_mouth_km` is zero at that origin, nonnegative, and increases
   upstream along each selected network path.
4. A Stream-scoped frame uses the project's downstream-most Stream point as
   its mouth. A Study-Area-network frame uses the analyst-selected watershed or
   connected-network outlet and references every included Reach to that common
   mouth.
5. The durable contract retains frame identity/version, scope, mouth geometry
   and meaning, included Streams, Reach topology/path, direction, units,
   derivation/calibration method, responsible actor/process, validation state,
   and provenance.
6. Each participating Reach receives a governed reference assignment with its
   downstream and upstream measures and network-path context. Each Survey
   Event Flowline is calibrated to that assignment so event-specific geometry
   can be compared in the common frame.
7. `distance_to_mouth_km` is a position, not an identifier. Equal values may
   occur on different tributaries or representations and must be qualified by
   reference-frame, Stream/Reach, Flowline, and feature identity as applicable.
8. The reference frame is not defined by the discarded synthetic-network
   feature class. FGDB retains the reviewed calibration contract and values,
   not the local preprocessing geometry or intermediate route products.
9. Legacy `km_to_mouth` values are imported only with explicit frame binding
   and validation. Unverifiable values remain unverified or are recomputed;
   missing frame metadata is not fabricated.
10. Changing the mouth, scope mode, included network, or path semantics creates
    a new reference-frame identity/version. Correcting erroneous calibration
    within the same intended frame follows controlled replacement and QA.

## Consequences

- Independently processed Reach results can share a reproducible Stream- or
  watershed-scale x-axis without sharing one derivation workspace.
- Multiple tributaries can appear in sophisticated longitudinal analyses while
  remaining distinguishable by Stream/path; `km_to_mouth` alone is not unique.
- Survey Event Flowlines may change through time without redefining the common
  project reference frame.
- The logical schema requires reference-frame, included-Stream/path,
  Reach-assignment, and Flowline-calibration contracts.
- Load validation must test topology, monotonicity, endpoint continuity,
  scope membership, units, mouth definition, and calibration quality rather
  than trusting analyst-entered offsets.
- A branch, distributary, loop, gap, or ambiguous route requires an explicit
  selected path/disposition; hierarchy membership cannot resolve it silently.

## Evidence

- Human-provided production workflow clarification from Michael Dougherty,
  2026-08-29.
- `FluvialGeomorph-toolbox/tools/_06_FlowlinePoints.py`.
- `FG-Tech-Manual/data_dictionary.csv`.
- ADR-0009: project-defined Stream/Reach extent and referencing.
- ADR-0010: Stream Geodatabase preprocessing boundary.
- ADR-0012: Reach-scoped derivation and hierarchical aggregation.

