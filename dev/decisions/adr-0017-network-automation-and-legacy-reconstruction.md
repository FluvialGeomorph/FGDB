# ADR-0017: Separate network automation, legacy reconstruction, and FGDB loading

- Status: accepted
- Date: 2026-08-29
- Complements: ADR-0014, ADR-0015, and ADR-0016

## Context

FGDB integrity benefits from a reviewed Stream Network Observation that makes the
project-defined Stream/Reach topology and segmentation explicit. The current
desktop workflow can produce that evidence, but it requires time-consuming
manual deletion, repair, snapping, orientation, and classification. That
burden is poorly suited to general users of Shiny applications and is already
a target for improvement in `fluvgeo`.

The legacy backlog is mixed. Some Stream Geodatabases retain the edited
`stream_network`; some retain only Reach-owned Flowlines; and some may retain
neither. The ArcPy Flowline tool dissolved the edited network by `ReachName`
and then smoothed it. A surviving Flowline therefore preserves strong evidence
of the accepted Reach path, but not the original segment boundaries, exact
pre-smoothing geometry, discarded branches, or complete derivation metadata.

Requiring completion of fully automated network extraction before any FGDB
loader work would couple two large initiatives and delay useful migration.
Conversely, silently treating Flowlines as the original network would
fabricate provenance. Referential integrity requires valid identifiers and
relationships; it does not require pretending that unavailable evidence
exists.

## Decision

1. Use one versioned Stream Network Geodatabase schema for all producers and
   the FGDB loader, with controlled evidence/provenance classes at least for:
   `SOURCE_NETWORK_RETAINED`, `RECONSTRUCTED_FROM_REACH_FLOWLINES`, and
   `NETWORK_NOT_RETAINED`.
2. New producer workflows should create and review a Stream Network Observation as
   part of the local-first analysis. New Shiny workflows should minimize
   geometry editing through automated candidate extraction, pruning, repair,
   orientation, topology validation, and classification assistance.
3. Automation must not infer project purpose silently. The user still confirms
   the intended configuration/outlet, retained paths, Stream/Reach classification, and
   any exceptions. The target interaction is exception review and confirmation
   rather than line-by-line construction.
4. A surviving legacy `stream_network` is imported as retained source evidence
   after explicit classification and review.
5. When the original network is missing but applicable Reach Flowlines survive,
   an explicit analyst-initiated reconstruction operation may create a new
   reviewed Stream Network Observation. It must be labeled
   `RECONSTRUCTED_FROM_REACH_FLOWLINES`, retain source-Flowline lineage, expose
   geometry changes, and never claim to reproduce the lost source network.
6. Reconstruction may copy/assemble Flowline paths, split them deterministically
   into topology edges, and propose endpoint snapping within a recorded
   tolerance. It must not smooth them again or silently create missing
   branches. Gaps, overlaps, ambiguous junctions, asynchronous survey times,
   and partial configuration coverage require explicit resolution or qualified status.
7. When neither network nor adequate Flowlines survive, otherwise valid legacy
   Reach Survey Events may still load with `NETWORK_NOT_RETAINED`. The optional
   network association remains absent; network-dependent publication/query
   capabilities must expose or enforce that limitation.
8. Automated extraction and Flowline reconstruction are scientific/geospatial
   producer functions owned by `fluvgeo`. ArcGIS Pro, Shiny, and future QGIS
   clients provide interaction and platform I/O. An FGDB legacy-migration tool
   may orchestrate an explicitly selected reconstruction step, but loading
   never reconstructs a network as a hidden side effect.
9. FGDB schema and loader development may proceed once the common schema,
   evidence classes, and validators are specified. Full extraction automation
   is not a prerequisite for the first loader, but new-work authoritative
   publication rules may require a reviewed source Stream Network Observation.

## Recommended sequence

1. Finalize the Stream Network Geodatabase schema, evidence classes,
   topology invariants, coverage states, and validation result model.
2. Inventory legacy projects into retained-network, reconstructable-Flowline,
   and missing-network cohorts without altering their data.
3. Implement `fluvgeo` network validators and a reviewed
   Flowline-reconstruction function, exposed through an analyst-facing
   migration workflow.
4. Implement the FGDB geodatabase validator and loader against the same schema,
   initially supporting retained and reviewed-reconstructed observations plus an
   explicit missing-network legacy exception.
5. Implement and refine automated terrain-to-network derivation in `fluvgeo`,
   first for Shiny and then through ArcGIS Pro and future QGIS wrappers.
6. Update the User Manual after the producer tools and review interactions are
   tested.

## Consequences

- FGDB can begin loading valuable legacy Reach results without inventing
  network geometry or waiting for complete extraction automation.
- Reconstructable projects gain governed topology adequate for hierarchy,
  stationing, and many cross-Reach queries, with visible evidence limitations.
- Exact historical stream-network geometry and discarded branches remain
  unrecoverable from smoothed/dissolved Flowlines.
- New Shiny and desktop work converge on the same open-source scientific
  functions and Stream Network relational schema.
- Publication and query services must distinguish relational integrity from
  scientific completeness and report network evidence/coverage explicitly.
- The project must define reconstruction tolerances, topology rules, source
  lineage, coverage states, and acceptance tests before implementation.

## Approval and follow-up

Accepted on 2026-08-29. The next design step is to freeze a minimum local
Stream Network Geodatabase schema before specifying either producer tools or
the FGDB loader. That schema must resolve physical field types and
domains, segment/topology grain, offline identity and reconciliation,
Flowline-reconstruction lineage, validation outcomes, and review tables. Tool
specifications then bind to that shared schema rather than defining independent
representations.
