# ADR-0014: Versioned synthetic networks and base-event calibration

- Status: accepted
- Date: 2026-08-29
- Supersedes: ADR-0010 decisions 3 and 7 for synthetic-network persistence;
  ADR-0013 decision 1 where it made the reference frame independent of every
  Survey Event Flowline

## Context

Further review established that the terrain-derived `stream_network` is not
merely temporary construction geometry. It is the reviewed spatial evidence
used to define project network topology, assign Streams and Reaches, establish
paths to the project mouth, and calibrate longitudinal stationing. Discarding
it would leave those consequential decisions dependent on undocumented manual
expertise and would prevent direct study of network change through time.

A single Study Area can represent either a connected watershed/network or a
discontinuous collection of independently analyzed Streams. In addition, each
terrain observation produces an ontologically distinct synthetic-network
realization because drainage topology and its terrain-derived representation
can change over time.

Longitudinal comparisons introduce a related requirement. A selected Survey
Event Flowline (or one selected base Flowline per participating Reach) defines
the common stationing to which other Survey Event Flowlines are calibrated.
The base selection is arbitrary and analysis-dependent; it is not an intrinsic
or permanent property of a Survey Event.

## Decision

1. FGDB retains the reviewed synthetic stream network as governed,
   time-specific derived geometry. The Stream Geodatabase and intermediate
   flow-direction/accumulation products remain excluded.
2. One Study-Area-owned `network_scope` normalizes ownership. It has scope mode
   `STUDY_AREA_NETWORK` for one connected multi-Stream network or `STREAM` for
   one independently processed Stream. A discontinuous Study Area therefore
   owns several Stream-scoped network scopes rather than one falsely connected
   network.
3. A physical enterprise `stream_network` feature class may contain all
   segment rows, but every row belongs to exactly one immutable
   `synthetic_network_observation`. Rows are never distinguished only by
   appended names or source strings.
4. Each `synthetic_network_observation` belongs to exactly one network scope
   and represents one terrain-observation time and one derivation/review
   result. A later valid observation creates a new identity; correcting an
   erroneous derivation for the same intended observation replaces that
   observation's current segment set and provenance.
5. Network segments belong directly to their observation. After analyst
   review, they carry explicit Stream identity and optional Reach identity as
   classifications/relationships; these do not replace observation ownership.
6. A network observation may relate to many Reach-owned Survey Events, and a
   Reach Survey Event may identify the network observation used to establish
   its topology/stationing. This association bridges scales without moving
   Survey Event out of the accepted Reach hierarchy.
7. Network observations are preserved across time as valid scientific
   observations. Cross-time segment correspondence is explicit and is never
   inferred from equal geometry, order, or names.
8. A longitudinal reference frame is owned by one network scope and selects a
   base calibration realization. It has one project-defined mouth and one base
   Flowline for each participating Reach/path position needed by the analysis.
9. Base-event status is frame-relative. Do not store a global `is_base` flag on
   Survey Event. The same Survey Event may be a base in one reference frame and
   a comparison event in another.
10. Each non-base Survey Event Flowline is calibrated to the applicable base
    Flowline and common mouth-based stationing. A new base selection creates a
    new reference-frame/calibration identity so alternative scientific
    comparisons can coexist reproducibly.
11. A frame may select a base synthetic-network observation when network
    topology is part of the calibration context. The selected base Flowlines
    and their Survey Events must be explicit even when they share the same
    year/date label.
12. The reference frame does not make stationing independent of Flowline
    geometry. Its common measures are realized by the selected base-event
    Flowline(s), and comparison-event Flowlines are calibrated to them.
13. `LATEST_VALIDATED_EVENT` is the normal analyst-selected base-selection
    preset for current-condition assessment. The resolved base Survey Event
    and Flowline IDs are stored explicitly.
14. Loading or publishing a newer Survey Event has no calibration side
    effects. Only an analyst-initiated tool run may create a new frame,
    calibrate a selected set of earlier Flowlines, and—after review—designate
    the accepted frame as the current operational default.

## Consequences

- FGDB gains enforceable provenance for the topology and segmentation that
  underpin its hierarchy and stationing.
- Connected and discontinuous Study Areas use the same normalized schema
  without nullable polymorphic ownership.
- One physical feature class can serve Enterprise GIS efficiently while
  logical dataset identity, time, scope, and provenance remain normalized.
- Valid historical network observations are retained rather than overwritten
  by later terrain observations; only corrections of the same intended
  observation use idempotent replacement.
- Network change can be studied directly, subject to explicit cross-version
  correspondence and derivation-method compatibility.
- “Latest Survey Event is the base” is no longer a database invariant. A
  client/report offers it as the normal operational default, but it must
  create or use an explicit reference frame containing the resolved IDs.
- New observations never trigger automatic scientific recomputation. Clients
  may suggest the latest eligible event, but the analyst controls execution,
  included comparison events, review, acceptance, and default designation.
- The loading workflow must validate scope membership, observation time,
  topology, Stream/Reach assignments, source provenance, and calibration
  relationships before publication.

## Evidence

- Human-provided methodological clarification from Michael Dougherty,
  2026-08-29.
- `FluvialGeomorph-toolbox/tools/_04_StreamNetwork.py` and related network
  tools.
- `FluvialGeomorph-toolbox/tools/_05a_Flowline.py`.
- `FluvialGeomorph-toolbox/tools/_06_FlowlinePoints.py`.
- ADR-0003: collection governance and mutation.
- ADR-0009: project-defined Stream/Reach extent and referencing.
- ADR-0010: Stream Geodatabase preprocessing boundary.
- ADR-0013: governed project longitudinal reference frame.
