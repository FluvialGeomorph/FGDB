# Versioned synthetic-network model

- Status: draft logical contract
- Updated: 2026-08-29
- Governing decision: ADR-0014

## Design answer

Use one physical Enterprise `stream_network` feature class, partitioned by
normalized logical dataset identity. Do not represent the design as either one
anonymous Study Area network or separate physical feature classes per Stream.

The ownership chain is:

```text
Study Area
  -> Network Scope
       -> included Stream membership(s)
       -> Synthetic Network Observation
            -> Stream Network Segment features
            -> related Reach Survey Event(s)
```

This handles both project patterns:

| Project pattern | Representation |
|---|---|
| Connected watershed or Study Area network | One `STUDY_AREA_NETWORK` scope with all included Streams and one network observation per terrain-observation time. |
| Discontinuous selected Streams | One `STREAM` scope per independently processed Stream, each with its own observations and source provenance. All scopes still share the Study Area owner. |

## Proposed relations

| Relation | Identity and ownership | Cardinality | Purpose |
|---|---|---|---|
| `network_scope` | immutable `network_scope_id`; one Study Area owner | Study Area 1:0..N scopes | Defines one connected derivation/reference scope without pretending disconnected Streams form one network. |
| `network_scope_stream` | (`network_scope_id`, `stream_id`) | scope 1:1..N Streams | Declares participating Streams. `STREAM` requires exactly one. |
| `synthetic_network_observation` | immutable `network_observation_id`; one scope owner | scope 1:0..N observations | Identifies one time-specific terrain-derived and analyst-reviewed network dataset. |
| `stream_network_segment` | immutable `network_segment_id`; one observation owner | observation 1:1..N segments | Stores governed polyline geometry and segment-level classifications. |
| `network_observation_reach_event` | (`network_observation_id`, `survey_event_id`, `relationship_role`) | observation N:M Reach Survey Events | Records which Reach analyses used, refined, or were evaluated against the network observation. |
| `network_segment_correspondence` | immutable correspondence ID; two observation/segment references | optional N:M across observations | Records reviewed persistence, split, merge, appearance, disappearance, or uncertain correspondence through time. |

## Network scope contract

| Field/concept | Rule |
|---|---|
| `study_area_id` | Required ultimate owner. |
| `scope_mode` | `STUDY_AREA_NETWORK` or `STREAM`. |
| `scope_label` | Human-readable and unique within Study Area; not identity. |
| Stream membership | `STREAM` has exactly one member. `STUDY_AREA_NETWORK` contains the connected Streams intended for common topology/stationing. |
| connectedness | Required validation for `STUDY_AREA_NETWORK`; disconnected components require explicit exception or separate scopes. |
| lifecycle | Draft, active, retired, or superseded with actor/time and reason. |

Changing scope mode or materially changing the intended included network creates
a new scope identity. Correcting a membership mistake before or during review
may preserve identity under controlled audit rules.

## Synthetic-network observation contract

An observation represents one derived network realization, not the persistent
real-world Stream and not merely a processing run.

Required concepts include:

- immutable observation ID and network-scope ID;
- required observation year, optional month/day, and derived date precision;
- source-terrain/acquisition references when known;
- derivation engine, method/version, threshold and material parameters;
- native CRS/resolution and Enterprise transformation provenance;
- analyst review/segmentation status and responsible actor/time;
- validation and publication state;
- current source/load manifest; and
- correction/replacement fingerprint and outcome.

A new terrain time creates a new observation even if geometry is identical. A
correction to the derivation or attributes for the same intended terrain time
preserves observation identity and atomically replaces its segment set. Two
distinct observations may share the same date and require separate immutable
IDs.

## Segment feature contract

All rows may reside in one physical SDE feature class. Each row requires:

- `network_segment_id` and non-null `network_observation_id`;
- polyline geometry in Enterprise CRS plus native derivation CRS provenance;
- explicit `stream_id` after Stream classification;
- nullable `reach_id` until or unless the reviewed segment is assigned to one
  Reach;
- segment role/topology attributes and controlled review status;
- downstream/upstream node or edge topology references as selected by the
  physical design; and
- derivation/review provenance inherited from the observation, with
  segment-specific overrides only when materially necessary.

`stream_id` and `reach_id` must belong to the observation scope's Study Area
and Stream membership. A segment cannot use a Reach whose Stream differs from
its explicit Stream relationship.

Source/process attributes that apply to the entire observation belong on
`synthetic_network_observation`, not repeated as denormalized free text on
every segment. Service views may expose them for client convenience.

## Relationship to Reach Survey Events

The existing hierarchy remains:

```text
Stream -> Reach -> Survey Event
```

The association to `synthetic_network_observation` records cross-scale
provenance without making the network observation a child of one arbitrary
Reach. Candidate controlled roles are:

- `TOPOLOGY_SOURCE` — used to establish the Reach/Stream segmentation;
- `STATIONING_SOURCE` — used for project longitudinal reference calibration;
- `DERIVATION_CONTEXT` — relevant source context but not the direct geometry
  copied into the Reach result; and
- `COMPARISON_TARGET` — included in a network-change analysis.

Exact role vocabulary and whether one role is mandatory per populated Reach
Survey Event remain to be reviewed.

## Cross-time network change

Every observation retains its own segment identities. A later observation does
not update the geometry of an earlier valid observation. Correspondence is a
separate reviewed assertion with a controlled relation such as:

- `PERSISTS_AS`;
- `SPLIT_INTO` / `MERGED_FROM`;
- `APPEARED` / `DISAPPEARED`;
- `REALIGNED`; or
- `UNCERTAIN_MATCH`.

Geometry overlap or proximity may generate candidates but never establishes
identity automatically. Comparisons must expose derivation method, terrain
resolution, threshold, and review differences so apparent network change is
not assumed geomorphic.

## Physical feature-class recommendation

Use one SDE polyline feature class for governed segment geometry, indexed at
minimum by:

- `network_observation_id`;
- `stream_id`;
- `reach_id` when present;
- observation date fields through a joined/materialized service view;
- publication/validation status; and
- spatial index.

Logical dataset and provenance tables remain normalized. Enterprise service
views can denormalize Study Area, scope, Stream, Reach, date, method, and
status fields for filtering without copying authoritative geometry.

## Validation invariants

1. Every segment belongs to exactly one network observation and scope.
2. Every classified Stream/Reach belongs to the scope's Study Area and declared
   Stream memberships.
3. `STREAM` scopes contain exactly one Stream; connected-network scopes pass
   the approved connectivity test or carry an explicit reviewed exception.
4. Observation date components and precision are valid and never fabricated.
5. Geometry, topology, derivation parameters, method/version, and analyst
   review state are complete before authoritative publication.
6. A correction replaces one observation's complete active segment set without
   altering other valid observation times.
7. Cross-time correspondence is explicit and version-qualified.
8. Network observation and Reach Survey Event associations never substitute
   names or geometry containment for immutable IDs.

## Open design questions

1. Exact node/edge topology implementation and whether nodes are persisted as
   a governed companion feature class.
2. Connectivity rules for braided, distributary, artificial, intermittent, or
   intentionally partial networks.
3. Whether observation time should reuse a shared acquisition reference when
   available or remain copied controlled metadata with a qualified link.
4. Required relationship role between a network observation and each Reach
   Survey Event.
5. Cross-version correspondence workflow and scientific QA.

## Immediate implementation boundary

The normalized model is not a requirement that analysts populate every table
manually or that all relations ship in the first release. The first ArcGIS Pro
loader needs only `network_scope`, `network_scope_stream`,
`synthetic_network_observation`, and the `stream_network` segment feature
class. Reach-event association, cross-time correspondence, persisted nodes,
and longitudinal-calibration relations can be added in controlled increments.
See `dev/workflows/import-synthetic-network.md` for the concrete legacy import
workflow.

Network association is optional for legacy Reach Survey Events when no source
network survives. Absence must carry an explicit completeness status; a
Flowline or lineage string is not promoted into fabricated network geometry.
