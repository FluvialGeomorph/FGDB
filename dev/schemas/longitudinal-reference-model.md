# Project longitudinal reference model

- Status: draft logical contract
- Updated: 2026-11-19
- Governing decisions: ADR-0013, ADR-0014 and ADR-0027

## Accepted direction: two cross-section methods

Owner/team decision, 2026-11-19: RAS-style cross sections use bankfull centerline
linear referencing for all new work/rework. Simple (straight-ish) cross sections
retain Flowline referencing as the legacy backward-compatible method. Flowline
remains required for REM creation. FGDB must distinguish both methods and their
reference contexts; see the
[cross-section contract](cross-section-feature-contract.md#accepted-two-method-direction).
The direction is recorded in
[ADR-0027](../decisions/adr-0027-two-cross-section-methods-and-reference-families.md),
which supersedes the Flowline-only requirement for RAS-style; common invariants
and simple legacy Flowline semantics are retained. Follow the
[implementation plan](../../../fgstudio/dev/goals/cross-section-implementation-plan.md)
for the contract and producer changes.
This resolves the adoption direction, not the physical implementation. It does
not authorize wholesale historical reprocessing. Existing saved drafts and legacy
measures retain their actual reference semantics.
The [FG Studio decision gate](../../../fgstudio/dev/goals/project-plan.md#near-term-decision-gate-the-xs-268-issue)
records the decision and remaining implementation scope. The detailed contract
below still describes the Flowline realization under ADR-0013/0014; it requires
an additive centerline extension, not reinterpretation of old Flowline measures.

### Owner clarification and proposed coexistence extension

Owner clarification (2026-11-19): Flowline remains required for REM creation.
The additional reference selected for RAS-style sections is a centerline derived from the **bankfull
channel polygon**, with its own base-event selection and comparison-event
calibration. The scientific purpose is to reduce low-flow-path length noise
when studying morphological response to infrastructure and landscape change.
Reduced variance and fewer calibration anomalies are expected benefits to test,
not established measurements. Flowline and bankfull centerline coexist.

The [FG Studio assessment](../../../fgstudio/dev/goals/xs-268-reference-analysis.md#primary-finding-coexistence-in-fgdb)
describes native historical Flowline frames alongside future centerline frames.
Existing configuration-to-many-frame and Dataset Edition contracts provide a
foundation, but the explicit Flowline-only base/calibration relationships below
do not yet support centerline stationing. Proposed additive design work is:

- retain distinct event-owned Flowline and bankfull-centerline geometry identities,
  with exact Dataset Edition and source-polygon lineage for centerline;
- generalize base selections/calibrations through an edition-qualified, typed
  reference alignment with enforced source-geometry foreign keys; preserve legacy
  Flowline bindings and propose one declared reference family per frame;
- distinguish Cross Section derivation lineage from frame-specific positions so
  a historical section can keep its original position and gain an accepted
  additional position without changing its transect identity/geometry;
- require an explicitly selected common frame and reviewed mappings for queries
  that need shared longitudinal positions; permit separate native-frame queries
  without cross-project spatial conversion; and
- preserve original legacy measures and compatibility profiles. Generalizing the
  scientific contract does not authorize silent reinterpretation of old values.

Storage coexistence does not require rebuilding historical cross sections,
centerlines or terrain. A common-frame comparison may need selected calibration
or additional positioning; historical bankfull geometry is necessary only when
the scientific operation actually requires it. Matching station values alone do
not establish equivalent transect sampling. Missing historical reference evidence
retains its existing unverified/unavailable disposition.

The two-method direction is accepted; the relations above remain a proposal for
review, not an implemented physical schema. ADR-0027 records the scoped
supersession of ADR-0013/0014; implementation must reconcile the kernel's Flowline-specific
Cross Section link, frame/base/calibration relations, feature/edition identities,
scientific method and schema contracts, legacy output profiles and query/export
validation. The existing Flowline-based contract below remains in force pending
that implementation; its Flowline-only wording is not a finding that coexistence is
scientifically or architecturally impossible.

## Purpose

This model governs the common `distance_to_mouth_km` coordinate used to
assemble independently derived Reach observations at Stream or connected
Study Area/watershed scale. It retains the reviewed, versioned synthetic
network under ADR-0014 while excluding the Stream Geodatabase and temporary
construction products.

The common coordinate is **not independent of Flowline geometry**. A frame is
the governed identity and provenance wrapper for stationing realized by the
explicitly selected base-event Flowline(s). Comparison-event stationing is
obtained by calibration to those base Flowlines, consistent with the existing
project method.

## Conceptual structure

```text
Study Area
  -> Stream Network Configuration
       -> Stream Network Observation(s)
       -> Longitudinal Reference Frame(s)
       -> explicit Mouth/Origin
       -> Reach Reference Assignment(s)
            -> Base Survey Event Flowline selection
            -> comparison Flowline Calibration(s)
                 -> positioned Flowline points/features
       -> reusable analysis Path(s)
            -> ordered references to Reach Assignment(s)
```

## Proposed relations

| Relation | Owner | Cardinality | Purpose |
|---|---|---|---|
| `longitudinal_reference_frame` | one Stream Network Configuration | configuration 1:0..N frames | Identifies one base-realization-specific project coordinate and calibration method. |
| `reference_mouth` | one frame | frame 1:1 mouth | Stores the zero-position point and its analyst-defined meaning/provenance. |
| `reach_reference_assignment` | one frame and one Reach | frame 1:1..N assignments | Stores each Reach once per frame with topology and governed downstream/upstream measure interval. |
| `reference_path` | one frame | frame 1:1..N paths | Names a main-stem or tributary-to-mouth analysis path through the calibrated network. |
| `reference_path_reach` | one path and one Reach assignment | path 1:1..N ordered members; assignment 1:1..N paths | Reuses calibrated Reach assignments in one or more ordered analysis paths. |
| `reference_base_flowline` | one Reach assignment and one Flowline | assignment 1:1 base for every participating Reach; Flowline 1:0..N frames | Selects the Survey Event representation that defines common stationing for that Reach in this frame. |
| `flowline_calibration` | one Reach assignment, one base selection, and one comparison Flowline | comparison Flowline 1:0..1 calibration per frame | Maps a non-base Survey Event representation onto the selected base stationing. |

A frame inherits its Study Area, configuration mode, and included Streams from
one `stream_network_configuration` defined in
`stream-network-geodatabase-schema.md`. `STREAM` has exactly
one Stream; `STUDY_AREA_NETWORK` represents the connected Streams calibrated
to the selected common mouth.

## Longitudinal reference frame contract

| Field/concept | Required rule |
|---|---|
| `reference_frame_id` | Immutable identifier for the governed frame/version. |
| `stream_network_configuration_id` | Required owner; supplies Study Area, configuration mode, and included Streams. |
| `base_stream_network_observation_id` | Optional only when no governed Stream Network Observation can support the frame; otherwise identifies the selected topology realization and must belong to the same configuration. |
| `preferred_label` | Human-readable project label; never identity. |
| `canonical_measure` | `distance_to_mouth_km`. |
| `measure_unit` | Canonical value `KILOMETER`; source units and conversions remain provenance. |
| `measure_direction` | Required value `INCREASES_UPSTREAM`. |
| `origin_measure` | Required numeric zero. |
| `method_id` / `method_version` | Required controlled derivation/calibration contract. |
| `lifecycle_status` | Draft, validated, active, retired, or superseded under a governed domain. |
| provenance | Responsible actor/process, creation/validation time, source evidence, software where applicable, parameters/tolerances, and notes. |

## Base-event calibration contract

Base-event status is not stored on Survey Event. It is a relationship inside
one reference frame:

- every participating Reach assignment selects exactly one base Flowline and
  therefore one explicit base Survey Event;
- a frame may select one base stream network observation for topology and
  path context;
- all selected base Flowlines must belong to the frame's stream network configuration and be
  compatible with its selected base stream network observation when one is declared;
- the base Flowline's calibrated measure begins at its governed Reach interval
  and participates in the common mouth-based coordinate; and
- every other included Survey Event Flowline is calibrated to the applicable
  base Flowline using documented control points/method and QA.

The same Survey Event can be base in one frame and non-base in another. A
report may default to the latest event, but it must resolve that choice to an
explicit frame; changing the base selection creates a different frame identity
so alternative analyses remain reproducible.

## Analyst-initiated latest-event preset

The predominant applied workflow is **compare all previous Survey Events to
the latest validated event**. Analyst-facing producer clients should offer
this as the normal analyst-selected frame-creation preset:

1. an analyst starts **Create Longitudinal Reference Frame**;
2. the tool proposes the latest validated/published Survey Event available for
   each participating Reach under the approved partial-date and tie rules;
3. the analyst confirms or changes the base Flowlines and chooses which
   comparison events to process;
4. the tool calculates and stages the requested calibrations;
5. the analyst reviews the results and explicitly accepts/publishes them; and
6. only an explicit analyst action may designate the accepted frame as the
   current operational default.

The preset name (for example, `LATEST_VALIDATED_EVENT`) is useful provenance,
but it never substitutes for storing the resolved Survey Event and Flowline
IDs. Loading or publishing a newer Survey Event has no calibration side
effects: it does not create a frame, recalibrate any Flowline, or change the
current/default frame. A new latest-event frame exists only if an analyst later
initiates, reviews, and accepts that operation. The prior frame remains
reproducible and may still answer a different scientific comparison question.

This preserves the foundational toolbox contract: tools expose standardized,
composable operations, while an analyst chooses their order, parameters,
inputs, and scientific purpose. FGDB validation may reject invalid results and
a client may suggest eligible inputs, but the database does not initiate
scientific derivation.

## Mouth/origin model

The mouth is a required governed point representation in Enterprise CRS with
native/source CRS provenance when applicable.

| Configuration mode | Meaning |
|---|---|
| `STREAM` | Analyst-selected downstream-most point of the project-defined Stream extent/path. |
| `STUDY_AREA_NETWORK` | Analyst-selected outlet of the connected watershed/network represented by the Study Area analysis. |

The mouth is not asserted to equal a national hydrography endpoint or an
official watershed outlet. Geoconnex/national identifiers may be associated as
context but do not define it.

## Stream path and Reach assignment contract

Each included Reach has one assignment per reference frame, even when several
tributary-to-mouth analysis paths share it downstream. Each assignment records
at minimum:

- `reach_id`, `reference_frame_id`, and its included Stream membership;
- downstream and upstream adjacency or an explicit terminal/confluence role;
- `downstream_measure_km` and `upstream_measure_km`;
- calibration/source method and evidence;
- validation status and tolerance; and
- branch, gap, overlap, or ambiguity disposition when applicable.

`upstream_measure_km` must exceed `downstream_measure_km`. Adjacent assignments
on a continuous path must agree at their shared boundary within the governed
tolerance. At a tributary confluence, paths may share the same confluence
measure; this does not make their upstream positions identical or merge their
Stream identities.

`reference_path` and `reference_path_reach` provide ordered main-stem or
tributary profile paths without copying Reach calibration. A downstream Reach
shared by several tributary paths retains one frame assignment and is simply
referenced by each applicable path.

## Flowline calibration contract

Each Survey Event Flowline retains local geometry and its direct Survey Event
ownership. A base selection defines the Reach stationing for the frame; a
calibration associates a comparison representation with that base:

- comparison `flowline_id`, `reference_base_flowline_id`,
  `reach_reference_assignment_id`, and `reference_frame_id`;
- calibration method/version and responsible actor/process;
- endpoint and any interior control-point correspondences;
- local-measure and frame-measure units;
- transformation/alignment parameters;
- residual/error or quality evidence when available;
- validation result and applicable tolerance; and
- source evidence, including legacy `km_to_mouth` when used.

The materialized `distance_to_mouth_km` on Flowline points, Cross Sections, or
other features is derived data. It must retain or be traceable to the frame and
calibration IDs. A measure without those references is not a fully governed
longitudinal position.

The existing output field name `km_to_mouth` remains mandatory in open-source
replacement outputs where the legacy-derived-feature compatibility profile
requires it. A normalized enterprise base table may expose it through a
compatibility view or migrated feature class rather than duplicating it
internally. Its numerical meaning does not change: for a
comparison event it expresses position with respect to the selected base-event
Flowline stationing. The new model adds the frame/base/calibration identifiers
needed to say which selection produced that value.

## Identity and version rules

Preserve a reference-frame identity when correcting labels, documentation, or
an erroneous calibration while retaining the same intended configuration, base
realization, mouth, and network-path semantics. Create a new frame/version when
changing:

- the base stream network observation or any base Flowline selection;
- the mouth/origin;
- `STREAM` versus `STUDY_AREA_NETWORK` configuration mode;
- the subject or included Stream network;
- a selected path through an ambiguous/branching network;
- measure direction or canonical unit semantics; or
- the scientific interpretation of the coordinate.

Reach resegmentation requires new Reach assignments and may require a new frame
version when it changes path topology or calibrated intervals materially.

## Validation invariants

1. Exactly one mouth exists and has measure zero.
2. Every included Stream and Reach belongs to the frame's Study Area.
3. Every Reach assignment belongs to the appropriate included Stream
   membership.
4. Measures are nonnegative and increase upstream.
5. Reach intervals are nonzero and continuous within tolerance where the
   selected path is declared continuous.
6. Confluences and branches have explicit topology; equal measures across
   tributaries are permitted but never treated as unique keys.
7. Every governed materialized measure references one frame and the applicable
   Reach assignment plus base selection/Flowline calibration.
8. A calibration cannot bind a Flowline to a Reach other than its Survey
   Event's Reach.
9. Every participating Reach selects exactly one base Flowline, and base status
   is never inferred from date or a global Survey Event flag.
10. Active longitudinal-profile queries use one declared frame version.
11. Legacy values that fail or lack sufficient evidence are flagged
    `UNVERIFIED` or recomputed; validation never invents missing evidence.

## Legacy migration states

| State | Meaning |
|---|---|
| `VALIDATED_LEGACY` | Existing `km_to_mouth` values were bound to a reconstructed frame and passed topology/continuity checks. |
| `RECOMPUTED` | A governed frame was reconstructed and positions recalculated from accepted evidence. |
| `UNVERIFIED` | Values exist but frame origin, topology, or calibration cannot be established sufficiently. |
| `NOT_AVAILABLE` | No usable longitudinal position was retained. |

Unverified values may remain as source evidence but must not be exposed as
scientifically comparable canonical stationing.

## Grounded FG Studio implementation evidence

The current/base-event FG Studio workflow now demonstrates an automatic local
`STUDY_AREA_NETWORK` precursor without weakening this governed contract. It
uses the analyst-defined Stream corridors to assign each Stream's downstream
endpoint to one parent Stream, requires exactly one outlet Stream, projects
each tributary endpoint onto the selected parent Flowline, and propagates the
resulting confluence measures from the outlet through an acyclic graph. The
local `stream_connections` evidence records parent, confluence measure,
projection gap, raster-derived tolerance, and outlet status. Every resulting
`flowline_points.km_to_mouth`/`POINT_M` value therefore uses one shared mouth
origin while retaining Stream and Reach identity.

This resolves the earlier question of whether automated open tooling can
reproduce the legacy manual offset convention. It does not resolve governed
frame identity, acceptance, base-Flowline binding, comparison-event
calibration, or the final enterprise physical topology representation; those
remain FGDB responsibilities.

## Remaining design questions

1. Whether mouth geometry is stored directly with the frame or in a general
   governed reference-location feature class.
2. Exact topology representation: downstream Reach foreign key, edge table,
   path table, or a combination supporting branches.
3. Tolerances and QA behavior for gaps, overlaps, endpoint displacement, and
   changing Flowline lengths.
4. Whether validated frame measures are materialized on feature classes or
   exposed through versioned views.
5. How manual-survey stationing is calibrated when no terrain-derived Flowline
   representation exists.
