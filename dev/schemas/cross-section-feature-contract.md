# Cross-section naming and layout metadata

## Status and scope

The owner directed on 2026-11-16 that FGDB establish a standard cross-section
feature-class name and store descriptive variables in table metadata, rather
than embedding them in feature-class names. That naming principle is accepted.
The physical spelling below follows the existing kernel entity `cross_section`.
The owner accepted the layout as a robust MVP on 2026-11-18 and method v11 as a
sufficiently performant "80% solution," good for now, on 2026-11-19. Residual
shape optimization is parked; it is not the selected next increment. This narrow
contract does not establish hydraulic acceptance, settle
governed cross-section identity or complete the broader feature contract.

## Accepted two-method direction

Owner/team decision, 2026-11-19:

Recorded by [ADR-0027](../decisions/adr-0027-two-cross-section-methods-and-reference-families.md).
The [implementation plan](../../../fgstudio/dev/goals/cross-section-implementation-plan.md)
sequences contracts, centerline referencing, the open simple-layout replacement
and multi-event/delivery qualification.

| Cross-section method family | Longitudinal reference | Intended use |
|---|---|---|
| RAS-style | Bankfull channel centerline | All new work and rework. |
| Simple (straight-ish) | Flowline | Legacy method retained for backward compatibility. |

Flowline remains an input to REM creation for the RAS-style workflow. Retain both
Flowline and bankfull centerline identities and lineage. RAS-style is a method
family label, not a claim of HEC-RAS certification, export readiness or hydraulic
acceptance. Method v11 geometry remains accepted and closed; its existing
Flowline-stationed drafts do not yet implement centerline referencing and must
not be silently relabeled as either completed RAS-style products or simple legacy
sections. Preserve their actual method/version/reference provenance.

The two-method direction is accepted. Exact physical fields, controlled-code
spellings and reference relations remain design work; no migration or batch
historical reprocessing is implied. Historical simple sections can load in their
original reference frames. Rework creates a separately identified RAS-style
result under the new contract while preserving source evidence and lineage.
Valid older scientific results follow the approved retention policy; they are
not invalidated merely because the preferred method changes.

### Minimum distinguishing metadata (proposed binding)

Every governed section must resolve the following through its own attributes
or its dataset edition and reference-position relationships. Service views and
exports must expose the applicable method and reference context.

| Metadata | Required interpretation |
|---|---|
| Method family | RAS-style or simple; proposed controlled codes `RAS_STYLE` and `SIMPLE_LEGACY`. Unknown historical evidence remains explicitly unresolved. |
| Scientific method/version | Exact algorithm/contract, distinct from broad family and software release. Existing `scientific_method_contract_id` provides the edition-level binding. |
| Longitudinal reference | Centerline or Flowline, exact reference geometry identity **and edition**, frame/version, Reach assignment, base selection and applicable calibration. A text type flag alone is insufficient. |
| Ownership/identity | Survey Event, Reach, dataset/edition and section identity; `Seq` and station are not persistent identities. |
| Measures and calibration | Units, direction, mouth/origin, calibrated and uncalibrated positions, calibration method/controls/QA; distinguish longitudinal measures from distance along a section. |
| Derivation provenance | Source DEM/REM, Flowline and, for RAS-style, source bankfull polygon/centerline editions, parameters and review evidence. |
| Legacy/rework lineage | Original layer/profile and source section/result associations where available, with evidence status for unknowns. |

Enforce the accepted pairings for products claiming conformance: RAS-style uses
centerline stationing; simple uses Flowline stationing. Preserve nonconforming or
transitional source artifacts under their actual evidence status rather than
fabricating conformance. Geometry shape alone cannot identify a method family.

Both families can use the standard `cross_section` feature class, with compatible
shared fields and method-specific metadata. For concurrent products in one Survey
Event, the proposed dataset binding uses separate semantic roles under the same
feature family, each with its own current accepted edition. A second method must
not overwrite the first role's current-edition pointer or reuse a distinct
transect's identity. Final role codes and cross-method section correspondence
require the broader identity contract. Nullable/not-applicable parameters must
have documented semantics rather than invented legacy values.

Cross-method longitudinal comparisons require an explicitly selected common
frame and reviewed correspondence/calibration; shared storage does not imply
numerical or sampling equivalence. See the
[longitudinal-reference extension](longitudinal-reference-model.md#owner-clarification-and-proposed-coexistence-extension).

### Storage alternatives and recommended binding

Status: analyzed recommendation for implementation; exact physical binding and
code spellings remain proposed. The accepted standard feature-class name remains
`cross_section`.

| Alternative | Assessment |
|---|---|
| Separate RAS/simple feature classes | Both are polylines with shared ownership, endpoint, identity and position needs. Separate classes duplicate validation, relationships and consumer unions; no demonstrated geometry/storage requirement justifies that duplication. |
| One class with only a free-text `type` | Easy to display, but cannot establish algorithm/version, exact reference realization or calibration. Typing errors and contradictory metadata would remain possible. Insufficient as the complete design. |
| One class, controlled method family, edition contracts and reference relations | Recommended. Shared querying and symbology with explicit scientific/version semantics; requires consistency constraints and method-specific parameter bindings. |

Expose `cross_section_type` with proposed codes `RAS_STYLE` and `SIMPLE_LEGACY`.
Make family authoritative through the method contract/dataset role and edition;
derive the field in a view or enforce any stored feature copy against that
authority. Use one family per role/edition. Do not allow an editable row label to
contradict its edition or reference family. Legacy evidence that cannot be
classified remains qualified unresolved evidence, not a guessed default.

Use separate roles for concurrent families within one Survey Event under the
existing (`survey_event_id`, `dataset_type_id`, `role_code`) dataset-slot model.
Each role retains its own current accepted edition. Exact role identifiers remain
to be registered; algorithm upgrades normally create editions, not new feature
classes or arbitrary new roles. New distinct transects receive distinct identities;
rework/cross-method correspondence is an explicit relationship, not a `Seq` join.

Keep common section attributes in the feature class and typed method-specific
parameters in edition/run relations or their portable exposure. Avoid adding
every future method parameter as a mandatory shared feature column. A normalized
binding must still reproduce the existing portable and legacy field contracts
where those profiles are claimed, including meaningful not-applicable values.

Keep reference family separate from method family. Validate their accepted
pairings and resolve the exact geometry edition, frame, Reach assignment and
base/calibration through enforceable relations. Review the kernel's present
Flowline-specific section link as derivation provenance rather than universal
stationing ownership. Source Flowline may remain a RAS derivation input while
the bankfull centerline supplies its position. Multiple frame positions can be
related to one section without duplicating its geometry.

The contract increment must specify and test foreign keys, allowed type/reference
pairings, edition consistency, role uniqueness, geometry and units, unknown source
handling, compatibility views and frame-qualified query/export behavior before
declaring either method integrated. A type-field migration alone is incomplete.

## Standard representation

Use `cross_section` for the regular cross-section feature class/GeoPackage
feature table, independent of spacing, width, water levels or method. Do not
parse scientific parameters from a name. Separate editions/lineage identify
different results. Channel/floodplain riffle product bindings remain separate
design work; this name does not collapse their roles.

Retain established nonconflicting legacy attributes, including `ReachName`,
mutable integer `Seq` and double endpoint coordinates in feature CRS units.
Later-stage fields remain governed by their own processing stage. Preserve
imported historical layer names as source evidence. `xs_<spacing>_<width>`
remains a legacy import/export profile, not the standard FGDB table name.
Never rename source archives in place or replace field semantics while migrating.

## Layout metadata in tables

The following columns define the portable local draft profile implemented by
FG Studio. They are grounded implementation evidence for the governed binding;
their exact normalized enterprise placement remains proposed. The accepted
principle is that descriptive variables belong in tables, not feature names.
For adaptive layout, the feature table carries explicit typed columns:

| Column | Type/unit | Meaning |
|---|---|---|
| `layout_spacing_m` | double, metres | Requested initial longitudinal spacing; not a claim that edited/deleted sections remain uniformly spaced. |
| `layout_direction_window_m` | double, metres, nullable | Retired loess support-distance metadata; preserved for old drafts and typed missing for the polygon-centerline method. Never repurpose as cartographic tolerance. |
| `layout_tangent_distance_m` | double, metres | Local chord distance along a polygon centerline for measuring direction. |
| `layout_centerline_spacing_m` | double, metres | Boundary densification spacing for Voronoi centerline extraction; existing polygon vertices remain. |
| `layout_smoothing_refinements` | integer | Number of Chaikin cartographic smoothing passes. |
| `layout_overbank_angle_limit_deg` | double, degrees | Maximum local floodplain-normal rotation searched by the provisional layout method. |
| `layout_allow_overbank_bends` | boolean | Whether automatic layout may add floodplain vertices for deconfliction; default true, no one-bend cap or centerline-only restriction. Manual corrections remain explicit. |
| `layout_width_mode` | text | `floodplain_extent` for adaptive endpoints; fixed-width legacy runs must declare their distinct mode and retain their original width and unit in metadata. |
| `channel_rem_elevation` | double | Selected channel threshold in declared REM elevation units. |
| `floodplain_rem_elevation` | double | Selected floodplain threshold, strictly above channel. |
| `rem_reference_elevation` | double | Numeric REM reference; 100 for the current detrend method. |
| `rem_elevation_units` | text | Elevation unit, distinct from horizontal coordinate units. |
| `layout_method` | text | Versioned method identifier; not a claim of scientific acceptance. |
| `edited` | boolean | Whether the generated candidate geometry was manually corrected. |

The owning edition/run metadata table retains the exact source Study/Event,
Flowline, Flowline Points and Hydro DEM edition/hash links, parameter set,
software versions, creation evidence and review state. Parameters may later be
normalized behind a run/edition foreign key; a portable table/view must expose
them without relying on descriptive feature-class names. Source DEM vertical
reference and REM reference are distinct metadata.

## Identity and lifecycle limits

The accepted MVP represents channel, left descending-bank
floodplain and right descending-bank floodplain as separate review regions,
each with its own polygon-derived centerline. The current portable draft binds
these to three multipart `hydraulic_regions` rows, with disconnected
`region_components`, raw/smoothed `centerline_raw`/`centerline`, skeleton and
diagnostic layers. Each centerline links to its component and region role.
These are implementation evidence for a future governed three-region model;
geometric centerlines are not accepted center-of-mass hydraulic flow paths.
The copied toolbox Centerline algorithm need not be retained and is not used.
The owner's visual review accepts the three-region model and its centerline and
smoothing defaults. Local method `polygon-centerline-v11` retains raw preparation
evidence and implements ordered boundary anchors, bounded joint target/route
planning and polygon-contained floodplain routing. Channel-width minimization is excluded:
perpendicular remains the preferred channel direction. It jointly deconflicts
contact/bank-order windows with or without mapped overbanks, before constructing
overbank directions and targets, using
full-width, station-preserving angular alternatives, hard bank rank and all-pair
nonintersection. The 2.5-degree grid, 30-degree search bound and separate
15-degree review threshold are provisional local geometry policies, not
accepted hydraulic limits. Windows include up to two eligible neighbors on
either side, with 64-section/50,000-node limits; failed/exhausted windows keep
their original flagged geometry. Unresolved channel contacts remain explicit. Bank/outer
anchor ranks follow centerline station order along connected boundary chains.
Midwest starting levels are 103/109 ft. Automatic additional
vertices are checked by default; deconfliction is the high-value workflow.
layout_channel_angle_limit_deg and layout_channel_rotation_review_deg are
double-degree local draft columns. Per-section channel_angle_limit_deg and
channel_rotation_review_deg retain the corresponding policy; actual rotation,
channel_rotated, channel_skewed and channel_limit_exceeded refresh on review.
channel_deconfliction_status records the generated angular outcome or explicit
manual_review after bank editing. These additive diagnostics retain the
established layout-stage names, types, coordinate units and meanings.
Per-side leg status, signed rotation in degrees, shortened-tangent and raw-route
flags are additive draft diagnostics. Zero floodplain width at a bank is distinct
from an unavailable route or incomplete leg. These diagnostics and the geometric
resolver remain implementation evidence, not a governed hydraulic rule.
The local direction match records when polygon-contained visibility replaces a
nearest projection across a channel indentation, without changing the source
centerline. The analyst can set the floodplain search bound from zero through 60 degrees;
rotations above 30 degrees remain review flags, not accepted hydraulic angles.
One or more additional floodplain vertices are permitted in tight bends,
without restricting their location to the centerline. The
local schema-9 / method-v11 draft retains LINESTRING geometry, with two or more vertices and
explicit integer left_bank_vertex/right_bank_vertex indices identifying the
adjacent channel banks. Owner-approved channel-only cross sections have two bank
vertices; one-sided overbanks are equally legitimate. Absent or failed legs
require no duplicated coordinates. no_floodplain denotes mapped absence,
distinct from failed construction and insufficient/uncertain terrain coverage.
section_parts describes constructed geometry independently of leg-status and
coverage diagnostics. Endpoint bank indices retain their bank role in editing
and persistence. This is grounded local implementation evidence; governed
hydraulic acceptance remains separate. Logical per-side bend flags and integer counts retain
bend presence and count; routed flags identify optional polygon routes. Manual addition/removal
retains bank/end coordinates and candidate identity. Historical backend profiles
retain their own geometry restrictions. Incompatible drafts never silently match
the current input fingerprint; explicit local cleanup may retire superseded
automatic drafts while preserving accepted/edited evidence. Region-specific hydraulic formulas
and their acceptance contracts remain separate scientific work.

The app also persists precomputed analytical/display REM GeoTIFF preparation
assets under a Study/Event/Reach input-recipe hash. Exact upstream and output
hashes, recipe metadata and complete-directory publication govern reuse across
sessions. This is local preparation evidence consistent with external GeoTIFF
terrain storage, not a completed governed REM product binding. Permanent map
section labels use existing mutable Seq, not a new governed identity.

Local schema 9 also retains boundary_chains LINESTRING and boundary_anchors
POINT evidence: directed shared edges and whole-channel bank arcs, generated
bank anchors/planned outer targets, feature-CRS chainage units and explicit
ordering/availability status. Per-section actual order diagnostics are refreshed
after edits; generated planning evidence remains distinct. These additive local
artifacts do not settle normalized enterprise placement. The owner's subdivision
centerline (informal quartile-guide) proposal is a parked adaptive direction/
waypoint option, not selected forward work or an implemented hydraulic subdivision.

The owner accepts the method-v10 channel polygon pruning approach and its
defaults as the cross-section channel-preparation baseline. Acceptance covers
the reviewed pruning behavior. The accepted v11 geometric baseline includes
known shape limitations; neither acceptance establishes governed channel
classification or hydraulic model acceptance. Channel-arm evaluation uses the
polygon channel centerline.
The local method derives a raw channel medial route and uses boundary-distance
discs to identify off-route lobes. Method v10 depth-screens shallow chips, tests
single connected attachments and prunes qualifying lobes in one overlay without
replacing other original banks. Defaults use 0.5 m padding, 1 m minimum depth
and full-attachment depth at least half the attachment endpoint chord width;
native CRS conversion is explicit. Local tangent advance is diagnostic only,
allowing hooked arms. Valid geometry, component count and the reference route
are protected. These geometric defaults do not establish universal hydraulic
or tributary classification rules. The saved Flowline selects
the longitudinal route; it is not the cleanup geometry or width reference.
channel_outer_raw, channel_reference_centerline and channel_branch_review retain
raw geometry, reference and lobe evidence beside the prepared channel_outer.
Branch review dimensions mouth_width/depth/advance are double values in explicit
feature-CRS measure_units; advance is local tangent extent, not chainage.
depth retains maximum distance from the attachment endpoint chord. Additive
double attachment_depth uses the full attachment curve in the same measure_units;
text cleanup_status distinguishes removal, wide attachment, reference protection
and a failed topology guard. The review layer contains depth-screened,
single-attachment candidates, not every raster-edge chip. Layout metadata
records prepare_channel; the normal app path enables cleanup. Schema 9 / method
v11 governs current layout matching. Older revisions are never overwritten;
explicit lifecycle cleanup may retire redundant unedited local drafts while
retaining accepted and useful comparison evidence.
Region diagnostics add logical route_fragment_fallback and double
route_span_fraction. Failed global-anchor extraction can retry within the
connected skeleton component with the greatest Flowline-measure span; fragments
are never joined. Existing successful routes remain unchanged. Ordered targets
beyond the straight angular bound may use one clamped-initial-angle waypoint
at half the endpoint distance, subject to fixed endpoints, containment and
nonintersection. This is an optional repair, not a mandatory bend per leg.
Removed channel areas remain in the total footprint and become LOB/ROB as
appropriate. These are portable local artifacts, not new governed branch entities.

Logical left/right_geodesic_direction and left/right_group_routed columns retain
generated evidence for contained direction association and group routing.
side_support direction_status distinguishes geodesic_centerline. Run metadata
declares lobe criteria, source reference, spacing/padding, crowding/clearance
policy and group budgets. Fixed banks/ordered targets, coverage and actual
nonintersection checks still govern geometry; group repair first maximizes
complete routes, then reduces interior crowding. None of these additions assigns
governed identity or confers hydraulic acceptance.

Local method v11 adds bounded whole-bend target/route planning after that initial
repair. It reuses schema-9 fields: final outer boundary measures and existing
group-selection flags describe the selected layout. Channel banks and saved
Flowline stationing remain fixed. Candidate distributions are evaluated together
with contained, nonintersecting routes; complete family coverage precedes adaptive
endpoint spacing and turn quality. No successful existing leg may be lost.
An unsuccessful search retains the incumbent. This does not change accepted
method-v10 pruning or settle the pending Flowline-versus-centerline reference
decision recorded in longitudinal-reference-model.md.

Additive logical channel_oriented and outer_chord_oriented expose bank direction
and endpoint-chord direction separately for bent sections. The existing oriented
field retains its combined meaning. The local UI reports chord turns separately
from reversed channel banks; these diagnostics do not replace intersection,
containment or boundary-rank checks.

`Seq` is mutable order. A local candidate may use an opaque persistent candidate
key scoped to its local saved set. It must not be relabelled a governed
`cross_section_id` or default to a platform object ID. FGDB kernel identity,
source-stable replacement keys, Survey Event/Dataset Edition binding and
acceptance remain unresolved. Correcting the same intended candidate retains
its local identity; regenerating a layout creates a new set. Reopening must
verify exact upstream lineage and output integrity. Invalid/conflicting
candidates may be saved explicitly as drafts, with their diagnostics retained;
draft persistence is not hydraulic or FGDB acceptance.

See `legacy-derived-feature-compatibility.md` for inspected ArcPy, manual and
retained-data evidence and the unresolved later-stage measure-unit conflict.
