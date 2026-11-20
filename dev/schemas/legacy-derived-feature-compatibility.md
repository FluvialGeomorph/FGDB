# Legacy-derived feature compatibility

- Status: accepted cross-repository production constraint
- Updated: 2026-10-06
- Feature families: `flowline`, `flowline_points`; inspected `xs` layout-stage contract below

## Purpose and lifecycle

`FluvialGeomorph-toolbox` contains the legacy ArcPy geospatial workflow.
`fluvgeo` is progressively replacing those tools with reusable open-source
functions, and FG Studio is the implementation-first client used to prove a
viable end-to-end workflow. After those replacements are established, FGDB
design and implementation will resume using the resulting contracts as roll-up
inputs.

The relationship is deliberately iterative. FGDB supplies accepted domain,
identity, compatibility, and governance constraints. Grounded FG Studio work
supplies implementation evidence needed to finish portable GeoPackage schemas,
interoperability rules, persistence boundaries, and analyst workflow contracts.
Verified findings flow back into FGDB for review and incorporation. Draft FGDB
physical bindings are not presumed complete, and working app-local choices are
not canonical until reconciled through FGDB governance.

Replacement therefore means a new backend and potentially better logic,
validation, automation, defaults, and robustness. It does not mean inventing a
new incompatible derived-feature schema. Historical projects must be able to use
the replacement tooling without wholesale schema conversion.

## Governing distinction

This document governs the production compatibility profile emitted by
`fluvgeo`, persisted by FG Studio, and exposed by replacement desktop tooling.
It is distinct from FGDB's normalized canonical base tables.

A canonical enterprise table may use immutable IDs and related calibration
records rather than duplicating legacy attributes. That normalization does not
authorize removal or reinterpretation of legacy fields in open-source production
outputs. Any enterprise compatibility view or export presented as a replacement
for a legacy feature class must reproduce this profile.

## General invariants

1. Preserve the established feature-class/layer name.
2. Preserve every established field name exactly, including capitalization.
3. Preserve the field's logical type, unit, null behavior, and meaning.
4. Preserve geometry family and documented direction/measure semantics.
5. Additive fields are permitted; substitution or silent semantic changes are
   not.
6. Platform-managed `OBJECTID`, geometry, and length fields are not scientific
   identity. Their physical names may be supplied by the target driver.
7. A method may be scientifically different from ArcPy while retaining its
   output schema. Schema compatibility does not assert numerical equivalence.
8. Conflicting legacy versions or evidence require a documented profile and
   migration decision; they are not resolved by silently choosing a convenient
   implementation.

## `flowline` compatibility profile

The portable layer name is `flowline`; FG Studio may also store reviewed raw or
diagnostic layers, but the replacement deliverable retains this named layer.
Geometry is a nonempty polyline beginning downstream and ending upstream.

| Field | Type | Unit | Requirement and meaning |
|---|---|---|---|
| `ReachName` | text | none | Required legacy Reach label. Preserve exact name; it is not durable identity. |
| `from_measure` | double | kilometer | Required for station-ready output; downstream route measure for the Reach. |
| `to_measure` | double | kilometer | Required for station-ready output; upstream route measure for the Reach and greater than `from_measure`. |

`OBJECTID`, `Shape`, and `Shape_Length` are driver-managed when applicable.
`InLine_FID` and `SmoLnFlag` occur in ArcGIS smoothing outputs; retain them when
reading or round-tripping source evidence, but do not invent authoritative
identity or method results when the open algorithm has no equivalent. Open
outputs may add immutable Reach identity, order, length, method, source-lineage,
and provenance fields without replacing the legacy fields.

For a continuous selected Stream path, adjacent Reach intervals use kilometers,
increase upstream, and meet at their shared boundary. Until a governed
longitudinal reference frame is created, these values are explicitly local
candidate stationing from the selected Stream outlet rather than canonical FGDB
stationing.

## `flowline_points` compatibility profile

The portable layer name is `flowline_points`; geometry is point. The baseline
legacy output retains:

| Field | Type | Unit | Requirement and meaning |
|---|---|---|---|
| `ReachName` | text | none | Required legacy Reach label. |
| `POINT_X` | double | feature-class horizontal unit | Required X coordinate. |
| `POINT_Y` | double | feature-class horizontal unit | Required Y coordinate. |
| `POINT_M` | double | kilometer for the ArcPy-replacement profile | Required route position. The ArcPy route is constructed from kilometer-valued `from_measure`/`to_measure`; the replacement profile preserves that measure. |
| `POINT_M_uncalibrated` | double | kilometer | Required route position before optional comparison-event calibration; equals `POINT_M` for the uncalibrated base result. |
| `calibration_diff` | double | kilometer | Required signed calibration adjustment, calculated as `POINT_M - POINT_M_uncalibrated`; zero for the uncalibrated base result. |
| `Z` | double | source DEM elevation unit | Required sampled terrain elevation. |
| `km_to_mouth` | double | kilometer | Required additive compatibility field in new open outputs; numerically identical to `POINT_M` in the selected Stream- or Study-Area-network frame and retained under its established downstream-consumer name. Only the frame outlet begins at zero; a tributary begins at its downstream confluence measure. |

The ArcPy producer also emitted `POINT_M_uncalibrated` and `calibration_diff`
for both calibrated and uncalibrated runs. The replacement profile therefore
requires both fields. For an uncalibrated base result,
`POINT_M_uncalibrated = POINT_M` and `calibration_diff = 0`; for a calibrated
comparison result, preserve the pre-calibration measure and calculate the signed
kilometer difference `POINT_M - POINT_M_uncalibrated`.

`OBJECTID` and `Shape` are driver-managed. Additional immutable Stream/Reach
identities, ordering, downstream-Stream/confluence evidence, explicit unit,
origin, frame/calibration, sampling, and provenance fields are additive.

FG Studio implementation evidence confirms the legacy tool's analyst-entered
`km_to_mouth` parameter can be derived for a connected Study Area without
changing its meaning. Prior Stream corridors determine parentage, the sole
uncontained downstream endpoint identifies the Study outlet, and a tributary's
downstream endpoint is projected onto its parent Flowline to obtain the
confluence measure. The local candidate records those connections and fails on
ambiguous parentage, multiple outlets, cycles, or excessive connection gaps.
This is grounded implementation evidence for a future governed
`STUDY_AREA_NETWORK` frame; it is not itself accepted FGDB publication.

## Cross-section layout evidence and standard naming

The inspected layout producer is `_11_XSLayout.py`; `_13a_XSResequence.py`
subsequently orders `Seq` by ascending `POINT_M`. The Technical Manual's `xs`
dictionary combines multiple processing stages. It is not evidence that layout
alone supplies watershed area, river position, station measures, loops or bends.

The legacy layout layer is named `xs_<spacing>_<width>` (rounded numeric
parameters). Width is the analyst-specified distance from the Flowline to an
outer endpoint; spacing uses the Flowline coordinate unit. Layout emits
`ReachName` (text), `Seq` (short integer), and `x_start`, `y_start`, `x_end`,
`y_end` (doubles in feature-class coordinate units), plus driver-managed fields.
Retained Copperas Creek R15 `xs_100_100` confirms integer `Seq`, double endpoint
coordinates, polyline geometry and the later-stage fields. Its `POINT_M` equals
kilometer `km_to_mouth`; its cross-section `to_measure` values are section
lengths, demonstrating a conflict with the dictionary's generic kilometer Reach
description. Later-stage measure profiles require further review before export.

Owner direction on 2026-11-16 supersedes parameterized legacy naming for the
new FGDB standard: use `cross_section` and store layout parameters as explicit
table metadata under `cross-section-feature-contract.md`. Variable widths do
not require inventing a filename width. Legacy names remain import/export
compatibility profiles, with original names retained in source evidence.
This is an explicit naming migration, not permission to change established
field names, types, units or meanings. Legacy-profile export still requires
the matching `check_*` contract, short-integer range enforcement where applicable,
downstream station-point verification and GeoPackage round trips. Neither a
local `candidate_id` nor `Seq` establishes governed cross-section identity.

Evidence: `_11_XSLayout.py`, `_13a_XSResequence.py`, `data_dictionary.csv` rows
for `xs`, `parameters.csv` for `xs_layout`/`xs_resequence`, retained
`CC_R15.gdb/xs_100_100`, `fluvgeo::cross_section()`,
`check_cross_section()`, `cross_section_points()`, and `xs_upstream()`.

## Existing R-client distinction

Historical `fluvgeo::flowline_points()` and consumers such as `ohwm2` use local
`POINT_M` values in projected linear units, commonly metres. That is an existing
R API contract but is not the ArcPy-replacement output profile. Preserve that
default for current callers. The FG Studio replacement chain must request an
explicit ArcPy-compatible profile with kilometer `POINT_M`, kilometer
`km_to_mouth`, and the legacy field set. Validators and tests must cover both
profiles so the distinction cannot become implicit.

## Required verification

For each replacement producer:

- validate exact required names and types;
- validate geometry and CRS prerequisites;
- validate finite coordinates, measures, and elevations;
- validate downstream-to-upstream measures and Reach continuity;
- validate `POINT_X`/`POINT_Y` against geometry within a documented tolerance;
- validate the declared relationship between `POINT_M` and `km_to_mouth`;
- test renamed, removed, mistyped, and unit-changed failure cases;
- compare representative legacy and new outputs structurally; and
- assess downstream consumers before release.

The `fluvgeo::check_*` family is the normal defensive-programming location for
these checks. Constructor tests are also required: a validator alone cannot prove
that the producer emits the contract.

## Evidence

- `FluvialGeomorph-toolbox/tools/_05a_Flowline.py`
- `FluvialGeomorph-toolbox/tools/_06_FlowlinePoints.py`
- `FG-Tech-Manual/data_dictionary.csv` and `parameters.csv`
- retained `fluvgeo::sin_flowline_sf` and `sin_flowline_points_sf` data
- `fluvgeo::flowline()`, `flowline_points()`, `check_flowline()`, and
  `check_flowline_points()`
- `flowline-feature-contract.md`, `longitudinal-reference-model.md`, ADR-0013,
  and the XML workspace assessment
