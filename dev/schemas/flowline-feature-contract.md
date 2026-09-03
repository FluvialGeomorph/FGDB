# Flowline feature contract

- Status: draft for design review
- Updated: 2026-09-02
- Dataset type: `FLOWLINE`
- Workflow position: after reviewed Stream Network/Reach segmentation and before Flowline Points

## Meaning and ownership

A Flowline is the Survey Event-specific polyline representing the likely flow
path through one governed Reach. It is derived from terrain evidence and
reviewed geometry, but it is not asserted to be the wetted flow path, channel
centerline, or surveyed thalweg. Non-bathymetric LiDAR frequently cannot observe
the submerged thalweg.

The durable hierarchy remains:

```text
Study Area → Stream → Reach → Survey Event
                                  |
                                  +→ FLOWLINE Derived Dataset slot
                                         |
                                         +→ current accepted Dataset Edition
                                                |
                                                +→ one Flowline feature
```

The scientific method is metadata on the Dataset Edition. It describes how the
Flowline geometry was produced and validated; it is not a geographic object,
feature class, or hierarchy parent.

## Identity and cardinality

1. A populated `FLOWLINE` dataset edition contains exactly one Flowline.
2. A Survey Event has at most one current `FLOWLINE` dataset slot for the
   canonical reference-path role.
3. `flowline_id` is the immutable identity of that Survey Event/role-specific
   Flowline. It is not an Esri `OBJECTID`, name, geometry fingerprint, or route
   measure.
4. An accepted correction or method reanalysis preserves `flowline_id`, creates
   a new Dataset Edition, and replaces current geometry. A different Survey
   Event or genuinely concurrent semantic Flowline role requires a different
   Flowline identity.
5. Alternative base-event calibrations do not create alternative Flowlines.
   They create distinct longitudinal reference frames and calibration records
   referring to the applicable Flowline.

## Canonical feature-class fields

The minimal scientific feature class is intentionally narrow.

| Field | Required | Logical type | Meaning |
|---|---:|---|---|
| `flowline_id` | yes | UUID | Immutable Flowline identity; maps to an Esri GlobalID in the enterprise binding. |
| `dataset_edition_id` | yes | UUID | Accepted `FLOWLINE` Dataset Edition governing this realization. |
| `survey_event_id` | yes | UUID | Direct owning Survey Event, repeated for efficient relationship and service validation; must agree with the Dataset Edition path. |
| `Shape` | yes | polyline geometry | Nonempty Flowline geometry under the rules below. |

Stream name, Reach name, Survey Event label/year, Collection, dataset type, and
publication state are obtained through governed relationships or service views.
They are not duplicated editable scientific attributes on the base feature
class.

### Related source relations

When a retained Stream Network supplied geometry, `flowline_source_segment`
contains one row per contributing governed segment:

| Field | Required | Meaning |
|---|---:|---|
| `flowline_id` | yes | Resulting Flowline. |
| `stream_network_segment_id` | yes | Reviewed input segment. |
| `source_order` | yes | Downstream-to-upstream input order within this Flowline. |
| `source_relationship_code` | yes | Initially `GEOMETRY_SOURCE`. |

Candidate uniqueness is (`flowline_id`, `stream_network_segment_id`). Source
order is also unique within one Flowline. A legacy Flowline with no surviving
Stream Network has no fabricated segment rows; its Dataset Edition records the
qualified missing lineage.

When a hydro-modified DEM was used to infer or verify orientation,
`flowline_terrain_source` relates `flowline_id` to the applicable hydro-DEM
Dataset Edition with role `ORIENTATION_EVIDENCE`. It does not imply that the DEM
alone uniquely determines the accepted Flowline geometry.

## Geometry contract

- Logical geometry is one continuous, single-part line. A storage driver may
  expose it as `MULTILINESTRING`, but the accepted geometry must contain exactly
  one connected line part after lossless normalization.
- Geometry is nonempty, valid, simple, and longer than the accepted coordinate
  tolerance.
- The start vertex is downstream and the end vertex is upstream.
- The entire line is covered by the applicable hydro-modified DEM within an
  explicit boundary tolerance.
- The line represents the likely flow path and remains within the analyst-
  accepted channel corridor. The method contract defines how that corridor or
  equivalent review evidence is evaluated.
- Local scientific production occurs in the accepted projected analysis CRS.
  Enterprise geometry is transformed to EPSG:3857 using the governed transform.
- Canonical Flowline geometry is XY. Z samples belong to governed Flowline
  Points/profile observations. M values belong to an explicit local route or
  project longitudinal reference frame and calibration. Embedding Z or M in the
  canonical Flowline would incorrectly make one sampled terrain or reference
  frame appear intrinsic to the Flowline.

Endpoint elevation is useful orientation evidence, but it is not a universal
orientation rule: flat water surfaces, noisy terrain, adverse slopes, missing
cells, and engineered systems can make it ambiguous. Automated orientation must
return a review-required status when its evidence is inconclusive.

Exact cross-event endpoint snapping is not yet a canonical invariant. Events
must represent the intended Reach extent and have reviewed endpoint
correspondence sufficient for calibration; arbitrary geometry edits solely to
force equality would erase real or method-dependent differences.

## Legacy and prototype field disposition

| Existing field/property | Canonical treatment |
|---|---|
| `ReachName` | Reconcile to immutable Reach/Survey Event ownership; expose the governed name only through a view if useful. Never use as identity. |
| `InLine_FID` | Processing residue; retain only in source/load evidence when needed, not the canonical feature class. |
| `SmoLnFlag` | Esri smoothing diagnostic; retain in method execution/validation evidence when material, not as Flowline identity. |
| `from_measure`, `to_measure` | Do not map directly. These values have represented both local and project stationing. Bind verified values to a longitudinal reference frame/calibration or recompute them. |
| `Shape_Length` | Platform-managed display value, not a canonical scientific metric or identity. Scientific lengths are calculated in an explicit CRS/unit under a metric contract. |
| `Stream_Name`, `Reach_Name`, `SurveyEvent_Year` | Prototype denormalization; provide from relationships/views. |
| `SurveyEventGlobalID` | Replace the prototype text field with the governed typed `survey_event_id` relationship. |
| `FType` | Replace with the governed Dataset Type relationship. |
| target Z/M capability | Reject as a canonical requirement. The target mockup conflicts with legacy and R evidence and would conflate the Flowline with sampled elevation and frame-relative stationing. |

Compatibility views may expose legacy aliases during migration, but their
lineage and non-authoritative status must be documented.

## Scientific method contract examples

These examples explain the role of `scientific_method_contract`. They document
observed workflows; neither asserts that the two methods are equivalent or that
the future open method is fully designed.

### `FLOWLINE_ARCPY_PAEK_LEGACY`

Observed production recipe:

1. take an analyst-edited `stream_network` feature class;
2. dissolve segments by legacy `ReachName`;
3. apply ArcGIS PAEK line smoothing using the supplied tolerance;
4. inspect that the smoothed line remains in the channel;
5. manually reverse it when necessary so digitization runs downstream to
   upstream; and
6. select/export exactly one Reach feature to each Reach–Survey Event
   geodatabase.

The method contract records smoothing algorithm, tolerance value and unit,
ArcGIS implementation, source-network lineage when available, and analyst
review. The obsolete ability to emit several Reach rows is source behavior, not
the canonical FGDB cardinality.

### `FLOWLINE_R_DEM_ORIENTATION_CURRENT`

Observed `fluvgeo::flowline()` recipe:

1. accept exactly one supplied `sf` line and Reach name;
2. require the Flowline and DEM to use the same CRS;
3. sample elevations at the original start and end;
4. reverse the line when the end elevation is lower than the start; and
5. return one upstream-oriented line without smoothing it.

This function standardizes and orients supplied geometry; it does not yet
replace the legacy Stream Network dissolve/smoothing workflow. Therefore its
method contract differs materially from `FLOWLINE_ARCPY_PAEK_LEGACY`, and their
initial scientific compatibility is `UNKNOWN`.

### Future open canonical method

The future `{fluvgeo}` method must explicitly decide how reviewed Stream Network
segments are selected/assembled, whether and how smoothing occurs, how
orientation ambiguity is handled, which manual edits remain allowed, and what
geometry deviations downstream metrics tolerate. ArcGIS Pro, Shiny, and a
future QGIS toolbox will call that same method; FGDB will only validate and load
its accepted output.

## Worked relational example

For Papillion Creek, Reach R1, Survey Event 2016:

1. `dataset_type` has the reusable `FLOWLINE` row.
2. the 2016 Survey Event owns one `derived_dataset` row with role
   `CANONICAL_REFERENCE_PATH`;
3. its accepted `derived_dataset_edition` points to the applicable legacy
   Flowline method contract, legacy Flowline schema contract, source manifest,
   and known software/platform evidence;
4. the `flowline` feature class contains one row whose `dataset_edition_id`
   points to that edition and whose `survey_event_id` points to 2016;
5. any surviving contributing Stream Network segments receive normalized
   `flowline_source_segment` rows; absent segments remain missing lineage rather
   than reconstructed facts; and
6. verified `from_measure`/`to_measure` evidence is handled by a separate
   longitudinal reference-frame calibration, not stored as intrinsic Flowline
   attributes.

A 2028 Survey Event receives a different Survey Event, Derived Dataset, Dataset
Edition, and Flowline identity. If 2016 is deliberately rerun with the 2028
open method, the 2016 Flowline identity and dataset slot remain stable while a
new accepted edition replaces its current geometry.

## Validation contract

Acceptance requires tabular validation evidence for:

1. one row and one logical line part;
2. non-null identities and consistent Survey Event/Dataset Edition ownership;
3. valid, nonempty, simple geometry;
4. projected local CRS during scientific processing and accepted enterprise
   transform during loading;
5. downstream-to-upstream orientation with evidence and ambiguity status;
6. hydro-DEM coverage and channel-corridor review;
7. source Stream Network segment lineage when claimed;
8. recorded method, schema, software, parameter, and analyst-review evidence;
9. no unqualified legacy route measures promoted as canonical stationing; and
10. complete replacement of the current Flowline realization during correction.

## Direct evidence and unresolved decisions

- The Papillion XML source is XY polyline with `ReachName`, `InLine_FID`,
  `SmoLnFlag`, `from_measure`, and `to_measure`. The target prototype is XYZM and
  redundantly stores hierarchy labels; neither is accepted unchanged.
- Direct `fluvgeodata` Flowlines are one-row, valid geometries exposed by GDAL
  as `MULTILINESTRING`. The inspected 2010 and 2016 Papillion geometries are
  exactly equal, which proves those retained artifacts match but does not prove
  why or establish a general cross-event rule.
- Current User Manual, Tech Manual, parameter table, and Python comments do not
  agree on smoothing ranges. The actual tolerance and unit must be captured per
  edition; an accepted future domain requires scientific review rather than
  selecting one documented range arbitrarily.
- Quantitative smoothing-deviation, channel-corridor, endpoint, and orientation
  ambiguity tolerances remain to be specified and tested from direct producer
  evidence.
