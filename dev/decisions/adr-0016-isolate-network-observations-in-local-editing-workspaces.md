# ADR-0016: Isolate Network Observations in local editing workspaces

- Status: accepted
- Date: 2026-08-29
- Complements: ADR-0014 and ADR-0015

## Context

Each terrain time produces an ontologically distinct synthetic Network
Observation. The enterprise model must retain many such observations for
change-over-time analysis, which can suggest storing their segments together
in one physical `stream_network` feature class and filtering by
`network_observation_id`.

That is unsafe as the initial local ArcGIS editing design. The current User
Manual directs an analyst to delete unwanted tributaries and lines, split and
edit vertices, create connecting lines, snap disconnected linework, smooth and
recheck geometry, and make Stream/Reach-identifying attributes consistent.
These are deliberately interactive and sometimes destructive operations over
the working feature class. A missed definition query or selection could alter
another terrain time, and coincident networks from several times would be hard
to interpret visually.

The manual also prescribes a separate Site Geodatabase and a separate Reach
Geodatabase for each LiDAR survey. The proposed binding therefore preserves an
existing time-isolation convention while renaming and formalizing its network
role.

The current manual clearly documents cleanup and repair of a single derived
main-channel network. It describes project-goal-based Reach definition and
matching `ReachName` values, but it does not fully document the historical
multi-Stream/multi-Reach segmentation and copy procedure. That gap should not
be mistaken for evidence that several terrain times are safe to edit together.

## Decision

1. One editable local ArcGIS Network geodatabase contains exactly one active
   `fg_network_observation` row and one `stream_network` feature class for that
   observation.
2. Every `stream_network` segment in that geodatabase carries the same
   `network_observation_id`. Producer validation rejects mixed observation IDs.
3. A new terrain time is edited in a separate time-specific Network
   geodatabase. Correcting the same intended observation retains its UUID and
   replaces its reviewed segment set under the correction rules.
4. Several time-specific geodatabases may implement one logical Network Scope.
   They carry the same `network_scope_id`; an exchange-package manifest
   assembles and validates their cross-workspace references.
5. The enterprise FGDB may consolidate segments from many Network Observations
   and Network Scopes in one physical feature class. Mandatory stable foreign
   keys, database constraints, governed write paths, and service filters provide
   the isolation that local manual editing lacks.
6. Local tools may display several observations together for comparison, but
   a comparison map or read-only composite layer is not the editable source of
   record. Editing tools require one explicit observation workspace.
7. This decision specifies physical isolation, not the scientific order of
   operations. Analysts still decide when and how to derive, edit, classify,
   review, package, and submit each observation.

## Consequences

- Existing manual cleanup tools can continue to treat `stream_network` as the
  complete working network for one terrain time.
- Accidental cross-time deletion, snapping, splitting, and attribute editing
  are prevented by workspace structure rather than relying only on a layer
  definition query.
- Local storage uses more small metadata snapshots and geodatabases, and
  package assembly must reconcile stable IDs across them.
- Cross-time reference frames and comparisons must reference observation IDs
  across workspaces instead of relying on physical co-location.
- Enterprise queries still gain one normalized, temporally explicit network
  collection without forcing that physical pattern onto analyst editing.
- The User Manual needs a future workflow update that explicitly distinguishes
  network cleanup, Stream/Reach classification, time-specific observation
  identity, and packaging.

## Approval and follow-up

Accepted on 2026-08-29. The design intentionally retains the familiar analyst
editing workflow while making its previously implicit boundaries explicit.
Producer-tool implementation should precede prescriptive User Manual changes
so that the documented procedure describes tested behavior rather than a
speculative interface.

The future analyst-facing workflow should make these stages visible:

1. derive one terrain-time synthetic network;
2. remove out-of-scope branches and repair anomalous geometry;
3. establish direction and validate network coherence;
4. classify retained segments by stable Stream and optional Reach identity;
5. review and accept the Network Observation; and
6. explicitly package it for optional FGDB submission.
