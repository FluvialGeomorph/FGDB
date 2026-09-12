# ADR-0026: Recover legacy vertical references and preserve future declarations

- Status: accepted
- Date: 2026-09-12

## Context

The project owner identifies the historic lack of dependable, widely
interoperable vertical-reference handling across the tools used by FG as a
primary cause of today's archive ambiguity. FG did not adopt a durable vertical
CRS record on its DEMs. Forensic recovery is therefore a required migration
capability, not evidence that an earlier analyst failed a requirement that FG
had not established. The same experience must inform new-project design.

This is an accepted account of FG's practical experience, not a verified claim
that no vertical standards or vendor capabilities existed before a recent year.
The [OGC GeoTIFF standard](https://docs.ogc.org/is/19-008r4/19-008r4.html), including
Annex H, documents earlier vertical keys and their subsequent clarification.
Standards, implementation, cross-client fidelity and project adoption are
different things. A precise industry-wide adoption timeline remains unknown.

Current evidence illustrates the distinction: the 2022 Douglas County samples
contain a NAVD88/international-foot declaration that a default GDAL read did not
expose. A supported reader option recovers it. See the
[sample findings](../../../fluvgeo/dev/features/cole-creek-source-access-review.md).
Other legacy declarations may genuinely be missing or conflict with source
documentation; present-day software cannot manufacture that evidence.

**Owner's workflow clarification:** experienced FG analysts, supported by
specialist reach-back, could deliberately choose analysis horizontal and vertical
references different from the input point clouds. A common practice was to prepare
the project DEMs in one chosen analysis reference framework and derive subsequent
FG products from those DEMs, reducing repeated transformations and interoperability
workarounds during analysis. Missing durable records must not be interpreted as
lack of competence or proof that the transformations were mishandled. This is
the owner's account of typical practice, not verification of every archived recipe.

## Decision

**Legacy recovery is a first-class workflow; explicit, testable preservation is
the new-project requirement.** Shared tooling shall support the following sequence:

1. Inspect selected staged copies without changing the original archive. Retain
   artifact identity, reader/version/options, embedded declarations and external
   metadata as separately attributable evidence. Check whether the reader merely
   failed to expose a declaration before reporting it as missing.
2. Recover unresolved facts from surviving processing records, source-product
   metadata and evidenced source matches. Owner/analyst recollections are useful
   but must remain attributed recollections, not independently verified facts.
   Catalog overlap, a horizontal CRS or a filename cannot establish vertical
   lineage. Preserve disagreements instead of silently ranking sources.
   Distinguish source acquisition/product CRS, the chosen analysis DEM CRS, and
   any later delivery/storage CRS. A difference between these roles is not itself
   a conflict: recover the evidenced transformation path and rationale. Never
   copy the source CRS onto a derived DEM merely because its analysis CRS record
   is incomplete. Separate contradictory claims about the same artifact from
   legitimate differences between input and output artifacts.
3. Present what is known and the next consequential analyst decision. Record an
   analyst's reconstructed interpretation, evidence and remaining uncertainty
   separately from the original declarations. Permit later evidence-backed
   enrichment without overwriting the earlier record.
4. Keep unresolved projects discoverable, stageable and reviewable. Prevent only
   the operations whose scientific validity depends on an unresolved fact; do not
   turn complete metadata recovery into a blanket gate on all migration progress.

For new terrain products, retain explicit height type, vertical reference and
exact elevation unit, with datum realization, geoid model and coordinate epoch
where applicable. Keep source and derivative references distinct and record any
unit conversion, datum transformation or resampling as different operations.
Preserve the useful common-analysis-reference strategy as a supported project
choice, not a requirement that all source collections arrive in that CRS or that
one CRS is suitable for every project. Record the selected reference framework
and preparation recipe once and link dependent DEMs/products to it; retain
per-source transformations and documented exceptions without repetitive paperwork.
Do not infer a geoid model from a datum name or mistake unit conversion for a
datum transformation. Record supported standards-based definitions alongside
artifact-linked provenance when a container/client cannot preserve all meaning.

Qualify preservation with read-back and value-bearing round trips across the
actual supported R, QGIS and licensed ArcGIS paths. Successful opening, a CRS
label or matching metadata alone does not demonstrate correct elevations or
cross-survey comparability. No universal interoperability is assumed.

## Consequences and ownership

- FGDB owns the persistence/scientific contract; fluvgeo owns reusable inspection,
  recovery support and reporting; QGIS and Shiny expose the shared results without
  duplicating science. The analyst remains responsible for consequential
  interpretations that evidence cannot automate.
- [ADR-0025](adr-0025-folder-deliverables-and-geotiff-terrain.md) remains in force:
  GeoPackage vectors/tables and external GeoTIFF terrain in linked folders.
- No automatic relabeling, elevation conversion, datum transformation, archive
  repair, source acceptance or new Survey Event follows from this decision.
- The [scientific traceability roadmap](../goals/scientific-traceability-roadmap.md)
  remains required upcoming work. This ADR does not approve a complete physical
  schema or make the whole overhaul a prerequisite for current development.
- The first bounded implementation is read-only recovery of reader-exposed versus
  embedded GeoTIFF vertical declarations. Conflict adjudication, report integration
  and cross-platform preservation qualification follow separately.
