# Legacy project staging contract — review draft 0.1

Status: **proposed**, 2026-09-10. This draft makes the accepted
[migration architecture](../../../FG-architecture/dev/decisions/adr-0005-analyst-staged-archive-migration.md)
reviewable. It is not an accepted physical binding, executable validator or
instruction to rearrange existing data. No converter is implemented by this work.

## Analyst outcome

An analyst should be able to say: **this is the Study Area, these are its Streams
and Reaches, these are the observations through time, and these are the selected
source artifacts.** Conversion should preserve that account rather than infer it.
The Study Area report should show what is known and the next unresolved decision,
with technical inventories available as supporting detail.

The archive stays untouched. Analysts copy selected clean artifacts into FileGDB
staging and reconstruct missing parent-level records there. Qualified conversion
creates the GPKG desktop home. Only that qualified representation proceeds to
FGDB desktop/archive intake; enterprise acceptance is a separate step.

## Proposed folder profile

```text
FileGDB/Collections/<collection>/<study>/
  StudyArea.gdb
  Streams/<stream>/
    Stream.gdb
    Reaches/<reach>/SurveyEvents/<event>/
      <retained-source-name>.gdb

GPKG/Collections/<collection>/<study>/
  study_area.gpkg
  Streams/<stream>/
    stream.gpkg
    Reaches/<reach>/SurveyEvents/<event>/
      event.gpkg
      rasters/       (GeoTIFF terrain)
      metadata/      (linked inventory, provenance and validation)
      reports/
```

These proposed names apply to reconstructed containers; copied event FileGDBs
retain their source names. Folder tokens are readable locators, **not identity**.
An event token must distinguish separate acquisitions even in the same year or
on the same date; final naming grammar remains open. A reprocessing run is not
a new Survey Event. Existing Copperas folders are evidence, not noncompliant
deliveries under a standard that has already been adopted.

Shared terrain and network observations need explicitly declared owners and
dependencies at the appropriate project level. Do not duplicate or clip them
merely to fit this event layout. Their exact folder binding remains open.
New native projects need no FileGDB intermediate. No reverse synchronization or
automatic deletion of staging is part of this profile.

## Proposed minimum hierarchy records

The [kernel model](kernel-relational-model.md) supplies the logical identities,
parentage and geometry cardinality. The following table proposes authoritative
local homes, not a second enterprise model. All listed identity/parent/name
fields are required; exceptions are explicitly marked.

| Home | Record | Minimum content and rule |
| --- | --- | --- |
| StudyArea.gdb | `study_area` | One row: `study_area_id`, `collection_id`, `study_area_name`. |
| StudyArea.gdb | `study_area_geometry` | Exactly one polygon record keyed by `study_area_id`; multipart allowed. |
| StudyArea.gdb | `stream_catalog` | Staging-only locator: one row per `stream_id`, with Study-root-relative `stream_gdb_path`. |
| Stream.gdb | `stream` | One row: `stream_id`, `study_area_id`, `stream_name`. |
| Stream.gdb | `stream_geometry` | Optional polygon, at most one per `stream_id`. |
| Stream.gdb | `reach` | One row per Reach: `reach_id`, `stream_id`, `reach_name`. |
| Stream.gdb | `reach_geometry` | Optional polygon, at most one per `reach_id`. |
| Stream.gdb | `survey_event` | One row per event: `survey_event_id`, `reach_id`, required `survey_year`, optional `survey_month`, `survey_day`. |
| Stream.gdb | `event_source` | Staging-only association: `survey_event_id`, `source_id`; initially one selected Reach–Survey–Event FileGDB per event. |

Rules for the first profile:

- IDs are persistent logical UUIDs, not names, OBJECTIDs, measures or paths.
  FileGDB GUID and canonical UUID-text target bindings must be qualified under
  the [type crosswalk](platform-type-crosswalk.md). Candidate local IDs do not
  claim enterprise acceptance. Reuse known governed IDs or reconcile explicitly;
  never silently replace identities or invent a governed Collection.
- Every child has exactly one declared parent. All references resolve, and IDs
  are unique within their entity type across the staged project. Paths remain
  inside the declared Study root. Folder placement and geometric containment
  must agree with the declaration but cannot establish parentage themselves.
- Stream names live in `stream`, not a second editable copy in `stream_catalog`.
  Entity and geometry tables may be physically combined later if identity and
  cardinality are preserved without duplicate editable attributes.
- Year is an acquisition year, not a processing or file-modification year.
  Month requires year; day requires month and a valid calendar date. Do not fill
  missing month/day with January 1. Different events may share dates. Unknown
  year is allowed during inventory but blocks configured, conversion-ready status.
  Periods not representable by this year/month/day model need a reviewed temporal
  extension; do not invent a representative date.
- One source GDB cannot silently represent multiple Reaches or acquisitions in
  this first profile. Such cases need reviewed reconstruction before selection.
- Proposed definition evidence accompanies hierarchy and date decisions:
  `definition_basis` (`SOURCE`, `ANALYST_CONFIRMED`, `INFERRED`, `UNKNOWN`),
  `source_ref` or explanatory reference, and reviewer/time when confirmed.
  An inference is reviewable, not an automatically accepted required definition.
- Analysts supply meaning and approve choices. Later tooling should generate
  IDs, inventory objects, compute checksums and scaffold records; those are not
  intended as tedious manual data-entry requirements.

### Boundaries and networks

A Study Area and its sole Stream may have coincident polygons while remaining
distinct entities. Record that interpretation explicitly. HUC12-based boundaries
and names are an optional analyst convention, not a universal rule. Stream and
Reach polygons are optional; do not manufacture them to complete a diagram.

Legacy Stream-workspace `flowline` rows are not automatically accepted event
Flowlines. Networks reuse the existing
[network contract](stream-network-geodatabase-schema.md): Study Area-owned
configuration, explicit Stream membership and separately identified observations.
Do not require fabrication of an observation date or build a competing topology
schema in the hierarchy catalog. Preserve source Z/M coordinates; the network
contract's geometry constraints do not authorize stripping dimensions from
unrelated legacy event features.

## Proposed source inventory and conversion plan

StudyArea.gdb holds two normalized staging tables:

| Table | Minimum content |
| --- | --- |
| `migration_source` | `source_id`, Study-root-relative `staged_path`, `source_kind` (`COPIED` or `RECONSTRUCTED`), `archive_ref` when applicable, `snapshot_ref`, `prepared_by`, `prepared_at`. One row per source container or independent asset. |
| `migration_item` | `source_id`, `item_name`, `role`, `disposition`, `mapping_ref`, `target_path`, `target_object`, `reason`. One row per layer, table or raster object; `(source_id, item_name)` uniquely identifies it within the snapshot. |

Allowed dispositions are `CONVERT`, `SOURCE_ONLY`, `EXCLUDE`. `CONVERT` requires
a qualified mapping reference and explicit target; the others require a reason.
Every source object must be accounted for before conversion readiness is claimed.
Unclassified content must not disappear silently. Desktop preservation and
enterprise loading are separate selections: a useful local artifact need not
belong in FGDB.

Snapshots identify a closed, coherent FileGDB or independent asset using relative
component paths, sizes and SHA-256 checksums. Transient lock files are not source
content. Verify copied bytes against the archive when available; an off-network
inspection cannot establish archive-to-copy equality. Reconstructed catalogs
carry authorship and references, not a false claim of being original archive
bytes. Keep restricted archive locators in controlled project records, not public
repository documentation. Do not add metadata fields to copied legacy features
merely to express their hierarchy: the staging catalog supplies those links.

Conversion mappings must cover values, nulls, field types, domains/relationships,
geometry dimensions, CRS and units, plus raster grids, values and masks under the
[platform crosswalk](platform-type-crosswalk.md) and
[folder requirements](local-project-folder-requirements.md). Successful opening
is insufficient. No implicit reprojection, resampling, snapping, smoothing,
reorientation or scientific repair is part of format conversion.

The existing selected-file intake and Study Context writer are useful building
blocks, **not** implementations of this complete catalog or conversion profile.
Exact field widths, physical domains, snapshot serialization, shared-asset
binding and recoverable publication/retry behavior still need qualification.

## Proposed review gates: what “clean” means

| Outcome | Evidence needed | What it does not establish |
| --- | --- | --- |
| Selected clean source | Analyst identifies the intended deliverable, resolves competing versions, confirms a coherent readable copy, and inventories relevant content and known issues. | Complete hierarchy, scientific revalidation or lossless conversion. |
| Ready to convert | Required hierarchy, Study Area polygon and acquisition years are confirmed; parents and sources resolve; structural ambiguities are resolved; every selected object has a qualified mapping or explicit non-conversion disposition. | Converted data or FGDB approval. |
| Conversion verified | Reopened output preserves declared identities, relationships, values, geometry/CRS and raster meaning; dependencies resolve after relocation and source snapshots still match. | Scientific comparability or enterprise acceptance. |
| Ready for FGDB review | Qualified GPKG content meets the identity, provenance and dataset contracts for the explicitly selected load scope. | A successful committed enterprise load. |

“Clean” is not “rerun every historical analysis.” Preserve known limitations.
**Proposed:** unknown vertical reference or method may remain explicitly unknown
through a demonstrably faithful conversion that does not require interpreting it.
An operation or load requiring that information stays blocked. Contradictory
metadata or a transform requiring an assumed datum is not equivalent to preserving
an unknown. Missing required survey year blocks hierarchy readiness regardless
of whether geometry can be copied.

These are separate outcomes, not one green compliance score. The report should
name the next analyst decision and its affected records, while keeping low-level
mapping evidence collapsible. Partial output must never be presented as a
complete conversion; transactional publication and retry details remain open.

## Copperas Creek: evidence and next analyst action

**Verified locally, 2026-09-10:** the FileGDB branch contains one Stream GDB and
fifteen Reach GDBs, `CC_R1.gdb` through `CC_R15.gdb`, beneath `Reaches/R01`–`R15`.
There is no separate Study Area GDB or Survey Event folder level. The GPKG branch
contains no project delivery. The Stream GDB has one `stream_network` feature,
sixteen `flowline` records labelled R1–R15 (R2 appears twice), and one
`StudyArea_Stream` polygon. The inspected Stream layers report NAD83 / UTM zone
15N. The R1 GDB lists twenty-one vector layers, including Z- and M-enabled
geometry. This was a read-only sample inspection, not a complete geometry,
attribute, raster or scientific-fidelity audit of all fifteen GDBs.

**User-confirmed:** Copperas Creek contains one Stream, so `StudyArea_Stream`
defines coincident Study Area and Stream boundaries. Preserve both roles with
distinct hierarchy identities. Its filename or buffer attributes alone would
not have established that meaning.

**Unknown, confirmed as requiring analyst input:** acquisition year/period for
the Reach GDBs. The user reports that the artifacts do not establish it. Do not
infer it from filenames, modification times or processing dates. The analyst
must supply supported event dates and distinguish acquisitions before the project
can be marked ready to convert.

**Unresolved source interpretation:** the two R2-labelled flowline records share
the displayed scalar measures and length. Exact geometry equivalence was not
tested; they are not established duplicate features. Their intended relationship
to the durable Reach must be reviewed, not automatically deleted or merged.

**Inferred workflow implication:** folder placement alone cannot supply the
missing event identity or explain repeated Reach labels. The proposed catalog
makes those decisions explicit without rewriting the archive.

## Next bounded step

Review the proposed catalog homes, explicit Survey Event folder level and
readiness rules. After agreement, build a **read-only staging inspector** for one
project that inventories what is known and reports missing analyst inputs using
the Study Area report. It must tolerate incomplete staging without creating dates,
moving files or claiming conversion readiness. Converter implementation, complete
target bindings, staging retention and renewed QGIS deployment remain later work.
