# FGDB kernel relational model

- Status: draft for design review
- Updated: 2026-08-29
- Scope: persistent identity, ownership, cardinality, and representation

## Purpose

This model translates accepted FGDB conceptual decisions into a minimal
relational kernel. It is intentionally independent of final Esri feature-class
names, PostgreSQL types, relationship-class settings, and service views.

The model distinguishes:

- durable domain entities from their spatial representations;
- a Survey Event from its current derivation provenance;
- current derived-dataset identity from replaceable dataset content; and
- governed records from local preprocessing artifacts.

## Kernel relationship graph

```text
Collection 1 ---- N Study Area 1 ---- N Stream 1 ---- N Reach
                         |                  |             |
                         | 1                | 0..1        | 0..1
                         v                  v             v
                 Study Area Geometry  Stream Geometry  Reach Geometry

Reach 1 ---- N Survey Event
                    |
                    +---- 0..1 Survey Event Geometry
                    +---- 0..1 Current Derivation Provenance
                    +---- 0..N Retained Derived Dataset

Survey Event 1 ---- 0..1 Flowline
Flowline    1 ---- 0..N Cross Section

Study Area 1 ---- 0..N Network Scope ---- 0..N Network Observation
Network Observation 1 ---- 1..N Stream Network Segment
Network Segment N ---- N Cross-time Segment Correspondence
Network Scope 1 ---- 0..N Longitudinal Reference Frame
Reference Frame 1 ---- 1..N Reach Assignment ---- 1 Base Flowline
Reach Assignment 1 ---- 0..N Comparison Flowline Calibration
Reference Frame 1 ---- 1..N Analysis Path ---- N:M Reach Assignment
```

The lower bounds of derived content are zero so a hierarchy and Survey Event
may be registered before analysis content is accepted. A populated Survey
Event must satisfy the conditional invariants below.

## Proposed logical relations

| Relation | Persistent identity | Required owner | Key cardinality | Purpose |
|---|---|---|---|---|
| `collection` | `collection_id` | none | two initial governed rows/classes | Top-level source, authority, visibility, and mutation boundary. |
| `study_area` | `study_area_id` | one Collection | Collection 1:N Study Area | Durable named AOI identity and nonspatial metadata. |
| `study_area_geometry` | `study_area_id` as PK/FK | one Study Area | Study Area 1:1 geometry | Required multipart-capable AOI representation. |
| `stream` | `stream_id` | one Study Area | Study Area 1:N Stream | Project-identified watercourse identity. |
| `stream_geometry` | `stream_id` as PK/FK | one Stream | Stream 1:0..1 geometry | Optional project-defined cartographic AOI. |
| `reach` | `reach_id` | one Stream | Stream 1:N Reach | Durable investigation-specific segmentation identity. |
| `reach_geometry` | `reach_id` as PK/FK | one Reach | Reach 1:0..1 geometry | Optional project-defined cartographic/analysis AOI. |
| `survey_event` | `survey_event_id` | one Reach | Reach 1:N Survey Event | Terrain condition/acquisition-period identity with known year. |
| `survey_event_geometry` | `survey_event_id` as PK/FK | one Survey Event | Survey Event 1:0..1 geometry | Optional analyst-supplied or hydro-DEM-derived analysis AOI. |
| `current_derivation` | `current_derivation_id`; unique `survey_event_id` | one Survey Event | populated Survey Event 1:1 current provenance | Mutable current-provenance slot; not a processing-run history. |
| `derived_dataset` | `derived_dataset_id` | one Survey Event and its current derivation | Survey Event 1:0..N datasets | Identity and metadata for each retained current dataset or mosaic item. |
| `flowline` | `flowline_id` | one Survey Event and one derived-dataset record | Survey Event 1:0..1 Flowline; exactly one when the Flowline product exists | Current event-specific reference path and local stationing basis. |
| `cross_section` | `cross_section_id` | one Survey Event, one Flowline, and one derived-dataset record | Flowline 1:0..N Cross Sections | Current event-specific transect identity and geometry. |
| `network_scope` | `network_scope_id` | one Study Area | Study Area 1:0..N scopes | Normalizes connected Study Area networks and independently processed Stream scopes. |
| `network_scope_stream` | (`network_scope_id`, `stream_id`) | one scope and one Stream | scope 1:1..N memberships | Declares participating Streams without polymorphic ownership. |
| `synthetic_network_observation` | `network_observation_id` | one network scope | scope 1:0..N observations | One time-specific terrain-derived and reviewed network dataset. |
| `stream_network_segment` | `network_segment_id` | one network observation | observation 1:1..N segments | Governed network polyline geometry with Stream and optional Reach classification. |
| `network_observation_reach_event` | (`network_observation_id`, `survey_event_id`, `relationship_role`) | one observation and one Reach Survey Event | N:M association | Preserves topology/stationing/derivation provenance across scale. |
| `network_segment_correspondence` | `network_correspondence_id` | two version-qualified network segments/observations | optional N:M across observations | Stores reviewed persistence, split, merge, appearance, disappearance, realignment, or uncertainty through time. |
| `longitudinal_reference_frame` | `reference_frame_id` | one network scope | scope 1:0..N frames | Versioned project coordinate with one mouth and explicit base realization. |
| `reach_reference_assignment` | `reach_reference_assignment_id`; unique (`reference_frame_id`, `reach_id`) | one frame and one Reach | frame 1:1..N assignments | Stores each Reach calibration interval/topology once per frame. |
| `reference_path` | `reference_path_id` | one frame | frame 1:1..N paths | Named main-stem or tributary-to-mouth analysis path. |
| `reference_path_reach` | (`reference_path_id`, `reach_reference_assignment_id`) | one path and one Reach assignment | ordered N:M association | Allows paths to reuse shared downstream Reach assignments without duplication. |
| `reference_base_flowline` | `reference_base_flowline_id`; unique `reach_reference_assignment_id` | one Reach assignment and one Flowline | assignment 1:1 base selection | Selects the Survey Event representation defining that Reach's common stationing in this frame. |
| `flowline_calibration` | `flowline_calibration_id` | one Reach assignment, base selection, and comparison Flowline | comparison Flowline 1:0..1 per frame | Aligns a non-base Survey Event representation to the selected base stationing. |

The separate geometry relations express ontology-ready entity/representation
separation and enforce optionality without nullable identity rows. A physical
Esri design may combine an entity and its geometry in one feature class only
if it preserves the same identity, cardinality, and nonspatial relationship
contracts.

## Accepted integrity invariants

1. Every non-root entity has exactly one explicit parent foreign key. Geometry
   containment and name parsing never establish parentage.
2. Collection membership is inherited through the mandatory hierarchy and
   must be unambiguous for every retained dataset and feature.
3. A Study Area has exactly one current governed polygon. Stream, Reach, and
   Survey Event each have at most one current governed polygon.
4. A Survey Event has a required year, optional month/day, and at most one
   current derivation-provenance record.
5. When a Survey Event has any current derived content, it has exactly one
   current derivation-provenance record and every retained dataset references
   it.
6. A desktop correction replaces all current content within one
   reach-survey-event replacement unit without changing the Survey Event ID.
7. The local Stream Geodatabase, its temporary drainage/route intermediates,
   and legacy `boundary` feature class have no kernel relation. The reviewed
   synthetic-network observation and segments are governed kernel content.
8. ArcGIS `OBJECTID`, geometry, names, filesystem paths, and display labels are
   never persistent identifiers.
9. Derivation occurs for one Reach and one Survey Event. Study Area- and
   Stream-scale results are descendant queries that preserve direct ownership;
   they are not duplicated kernel entities.
10. A populated Survey Event has at most one current Flowline. The legacy
    ArcPy ability to emit one Flowline per `ReachName` is not a target
    multi-Reach processing contract.
11. A governed project longitudinal position names one reference frame/version
    and the applicable Reach assignment/Flowline calibration. The common
    measure increases upstream from one explicit mouth and is never identity.
12. Every network segment belongs to one time-specific network observation.
    New observation times coexist; corrections replace only the same intended
    observation's current segment set.
13. Base-event status exists only through a reference-frame base Flowline
    selection. It is never a global Survey Event attribute.

## Recommended identity-change rules for review

These rules are the next decisions required before logical fields and database
constraints can be finalized.

| Entity | Preserve identity when | Create a new identity when |
|---|---|---|
| Collection | label, description, or policy metadata changes without changing its source/authority class | the source/authority and mutation regime becomes a different governed collection |
| Study Area | name or AOI geometry is corrected/expanded for the same investigation context | records represent a different independently governed AOI; merge/split creates successor identities |
| Stream | name, national reference, or optional geometry changes for the same project-identified watercourse | Study Area parent changes, or a merge/split changes the project-identified watercourse unit |
| Reach | name or optional geometry is refined without changing the intended analytical segment | Stream parent changes, or resegmentation materially changes, splits, or merges the analytical segment |
| Survey Event | metadata/date precision is corrected for the same acquisition occurrence, or derived content is reprocessed | evidence identifies a different acquisition occurrence, including a distinct same-date survey |
| Current derivation | provenance values are replaced when the same Survey Event is reprocessed | Survey Event changes; processing attempts are audit records rather than new current-derivation identities |
| Derived dataset | current content is corrected/replaced for the same Survey Event, feature family, and semantic role | Survey Event, feature family, or semantic role changes |
| Flowline | geometry/attributes are corrected for the same Survey Event and reference-path role | Survey Event or semantic role changes; a materially different concurrent reference path is introduced |
| Cross Section | geometry/attributes are corrected for the same Survey Event and intended transect | Survey Event, cross-section type/role, or intended transect changes |
| Network scope | label/documentation or reviewed membership error is corrected for the same intended derivation scope | scope mode or intended connected/included Stream set changes materially |
| Synthetic network observation | derivation/attributes are corrected for the same intended terrain-observation occurrence | terrain-observation occurrence or network scope changes |
| Network segment | geometry/attributes are corrected within replacement of the same observation and reviewed segment correspondence is preserved | observation changes or review establishes a different time-specific segment |
| Longitudinal reference frame | labels, documentation, or erroneous calibration are corrected for the same scope, base realization, mouth, and path semantics | base network/Flowline selection, mouth, scope, selected path semantics, direction/unit semantics, or scientific interpretation changes |

The recommended rule for derived datasets treats identity as the stable
"current dataset of this type and role for this Survey Event" slot. Dataset
content fingerprints and derivation metadata change during correction; the
dataset ID does not. Operational load history may record the replaced bytes or
rows without exposing known-bad versions as current data.

## Recommended uniqueness constraints for review

| Relation | Candidate uniqueness rule | Reason |
|---|---|---|
| `study_area` | normalized globally composed Study Area name | Accepted global human-readable uniqueness; exact grammar remains open. |
| `stream` | normalized display name within `study_area_id` | Prevent duplicate dropdown entries while allowing the same stream name in different Study Areas. |
| `reach` | normalized display name within `stream_id` | Keeps analyst-facing hierarchy concise without using the name as identity. |
| `survey_event` | no date-only uniqueness | Two acquisitions may occur on the same known date; immutable ID disambiguates them. |
| `current_derivation` | unique `survey_event_id` | Enforces at most one current provenance record. |
| `derived_dataset` | unique (`survey_event_id`, `dataset_type_id`, `role_code`) | Enforces one current dataset per governed semantic slot while allowing distinct roles/subtypes. |
| `flowline` | unique `survey_event_id` | Accepted one current reference Flowline per reach-survey-event under ADR-0012. |
| `cross_section` | source-stable key unique within (`survey_event_id`, `cross_section_type_id`) | Needed for idempotent replacement; exact source key is unresolved and must not default silently to `OBJECTID`. |
| `synthetic_network_observation` | no date-only uniqueness; candidate source manifest uniqueness within scope | Distinct observations can share a date; immutable ID and reviewed evidence disambiguate them. |
| `stream_network_segment` | immutable segment ID unique globally; source-stable key unique within observation when available | Supports complete replacement and explicit cross-time correspondence without using `OBJECTID`. |

## Legacy implementation evidence affecting the recommendations

- `fluvgeo::flowline()` requires exactly one input feature and returns one
  Flowline. The ArcPy flowline tool dissolves by `ReachName` and produces one
  record per unique Reach name. Human workflow evidence establishes the latter
  as residue from an abandoned multi-Reach design. The governed production and
  load unit represents one Reach and Survey Event, so one current Flowline per
  Survey Event is accepted rather than merely proposed.
- The Tech Manual data dictionary calls Cross Section `Seq` a unique
  identifier, but `_11_XSLayout.py` initially calculates it from the ArcGIS
  object ID. Other tooling can resequence Cross Sections. `Seq` is therefore a
  useful legacy matching candidate, not yet an accepted immutable key.
- Regular, channel-riffle, and floodplain-riffle Cross Sections are distinct
  source families. Any uniqueness rule must include a governed type/role and
  must not merge equal `Seq` values across those families.
- The ArcPy Flowline-points tool accepts a manual `km_to_mouth` offset and uses
  it as the Flowline route start, while the current R implementation starts
  local measures at zero. These values are evidence of a needed cross-Reach
  stationing contract, not yet a reliable Stream-scale key.

## Hierarchical query and composition requirements

Indexes and service views must support traversal from Study Area or Stream to
Reach-owned content without duplicating authoritative feature rows. Every
result retains its Survey Event and derivation provenance.

Stream-scale longitudinal composition uses the project longitudinal reference
frame for mouth/origin, selected base network/Flowlines, paths, Reach topology
and intervals, units, and comparison Flowline calibration. It additionally
requires explicit Survey Event selection and datum/method compatibility
checks. See ADR-0012 through ADR-0014,
`dev/schemas/synthetic-network-model.md`,
`dev/schemas/longitudinal-reference-model.md`, and
`dev/features/multiscale-scientific-query.md`.

## Lifecycle fields common to kernel entities

Every kernel entity should support immutable ID, creation actor/process and
time, last-modification actor/process and time, and a controlled lifecycle
status. Retirement is preferable to identifier reuse for hierarchy entities.
Whether geometry changes and Shiny edits require deeper history remains a
separate audit-policy decision.

Derived records additionally require their current derivation reference,
method/software version, source/load manifest reference, validation outcome,
and collection publication state as applicable.

## Questions for the next design review

1. Confirm whether Stream identity is project-scoped such that changing its
   Study Area parent always creates a new Stream.
2. Confirm that a material Reach split, merge, or resegmentation retires the
   old identity and creates successor Reach IDs rather than editing in place.
3. Confirm the stable-current-slot identity rule for `current_derivation` and
   `derived_dataset` during desktop correction.
4. Decide how Cross Sections receive a source-stable key and whether
   correspondence across Survey Events needs a separate alignment relation.
5. Review the proposed physical topology representation and validation rules
   in `dev/schemas/longitudinal-reference-model.md`.
