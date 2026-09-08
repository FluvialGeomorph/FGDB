# Terrain Development workflow and FGDB evolution

Status: direction accepted by the user; first reporting slice in fluvgeo;
persistent project-context and downstream loading interfaces remain to be built.
Updated: 2026-09-08.

FGDB development should be exercised from the start of a new Study Area, not
only through loading historical outputs. The pre-Level-1 Terrain Development
report is the first consumer: it combines supplied Study Area, selected Stream,
Reach and Survey Event context with a local network Observation and terrain
evidence. It can start before network extraction or Level 1 feature production.

The authoritative report design/implementation lives in fluvgeo:
`dev/features/terrain-development-report.md`. Its first HTML report and reusable
summary run through open R/GDAL tooling and the network GeoPackage binding.
Reports never infer hierarchy by containment, substitute DEM rectangles for
Study Area AOIs, infer Survey Events from network dates, or grant acceptance.

The user-selected first example is Cole Creek, Reach R1, within the Papillion
Creek Study Area, with Survey Events 2006, 2010 and 2016 retained in fluvgeodata.
Open-source inspection verifies flowlines and two raster subdatasets in each
file, plus a one-feature stream_network in the 2006 file. These are Reach-scale
fixtures, not evidence of a retained full Study Area/Stream extraction context.
The demonstration uses expressly provisional UUIDs, no asserted Study Area AOI,
and no acceptance or enterprise reconciliation.

## Independent reporting purpose and design feedback

The user-established [fluvgeo reporting intent](../../../fluvgeo/dev/goals/reporting-intent.md)
addresses a scientific reporting gap independently of FGDB: the reviewed existing
reports describe Reach analysis, not the development and organization of its
parent Study Area and Streams. Terrain Development should provide a thorough,
visual, durable account for analysts and customers, both while configuring a
study and after its definition. A valid study still needs that descriptive record.

Use maps, relationship views and multi-period evidence comparisons to reason
through FGDB's design and reveal missing or ambiguous contracts. The report is
the primary human-facing review artifact, not a substitute for persistence
validation. Shiny should offer the Study Area view and saved report while asking
for detailed input only where a human decision is needed. This accepted intent
does not imply those presentation or shared-assessment capabilities are already
implemented, nor authorize new enterprise fields or retention rules.

## Design consequences to test next

The accepted [parallel QGIS migration decision](../../../fg-qgis-toolbox/dev/decisions/ADR-0001-parallel-open-source-migration.md)
provides a separate desktop implementation and user-testing path. The production
ArcGIS Pro toolbox remains in use; fg-qgis-toolbox may restructure interaction
while sharing fluvgeo methods with Shiny. Reports and qualified GeoPackage
examples from that path should exercise FGDB contracts incrementally. QGIS review
success does not certify enterprise loading, and this decision changes neither
FGDB's service boundary nor production deployments.

The user has added forensic archive reconstruction as a third reporting job and
selected GeoPackage as the target local standard; see
[ADR-0024](../decisions/adr-0024-geopackage-local-standard-and-archive-reconstruction.md).
The first fluvgeo visual relationship/event-grid view and interpretation ledger
are implemented. They expose supplied context without accepting it or creating
persisted hierarchy relations. A bounded Cole Creek conversion probe is not a
general archive converter.

### Proposed directory organization (not yet a storage contract)

[ADR-0025](../decisions/adr-0025-folder-deliverables-and-geotiff-terrain.md) makes
the Reach–Survey–Event **folder** the delivery unit: GeoPackage vectors/tables,
external GeoTIFF terrain and linked metadata. Esri raster-tile support must not
be mistaken for qualified analytical terrain coverage support. The
[folder requirements](../schemas/local-project-folder-requirements.md) define the
metadata/validation obligations; exact file names below remain illustrative.

The user reaffirmed this direction after the
[completed ArcGIS experiment](../experiments/geopackage-raster/FINAL-FINDINGS.md).
Proceed to the versioned folder manifest and shared artifact-resolution checks;
do not hold this workflow for broad single-GeoPackage equivalence testing.

Standardized organization is an accepted requirement; this concrete layout is a
proposal to exercise next, not an implemented or approved loader contract:

```text
project-workspace/
  intake/<case-id>/                 # unassigned archive candidates; no forced UUID guesses
    source-copy.gpkg                # selected vector/table copies
    rasters/<terrain-artifact-id>.tif
    manifest.json                  # proposed artifact/metadata inventory
  studies/<study-area-id>/
    context.gpkg                   # proposed hierarchy, evidence and decision relations
    networks/<configuration-id>/<observation-id>/network.gpkg
    streams/<stream-id>/reaches/<reach-id>/surveys/<survey-event-id>/
      analysis.gpkg
      rasters/<terrain-artifact-id>.tif
      manifest.json                # proposed links to artifacts and parentage
    reports/<report-edition>/study-area.html
```

Original archives remain outside this managed candidate area, referenced by
source identity/checksum. Intake case keys are not scientific identities. Names
and years are human labels, not directory-based foreign keys. Related table rows
must identify the actual artifacts and parentage; moving a folder must not alter
scientific meaning. After reconciliation, publish new identified candidates
rather than destructively moving or rewriting source archives. HTML/Markdown and
report exports are documents; durable scientific/context tables belong in the
qualified GeoPackage relations, which still need a project-context binding.
The proposed manifest is a portable inventory, not a competing identity store;
its exact relationship to those tables must be defined and validated. Shared
Study/Stream source terrain may use a declared project asset location instead
of duplicate event copies. No implicit clipping follows from this folder layout.

### Remaining implementation boundaries

- Keep local report context separate from the currently network-only GeoPackage
  schema. Do not silently add Study Area/Stream/Reach/Survey Event tables to that
  binding or treat report input columns as an implemented enterprise migration.
- Obtain the defined Study Area AOI and a documented full terrain/network pair,
  with more than one Reach and a junction. Use the analyst's choices to establish
  segmentation rationale and actual network-to-Survey-Event relationships.
- Use subsequent report sections to expose required persistent identity,
  terrain-edition, provenance and availability fields. Distinguish source inputs
  retained locally from FGDB's accepted Reach hydro-DEM/network outputs; expanding
  reporting does not silently expand enterprise raster retention.
- Reuse fluvgeo scientific checks and report components in Shiny. FGDB owns
  persistence/services and identity reconciliation, not another topology engine.
- A current network PASS/acceptance is not sufficient evidence for Level 1
  readiness. Define that handoff against actual required analysis inputs later.

No source-data acquisition, new fixture data, FGDB loader, enterprise schema
migration or Shiny deployment is included in this first reporting slice.
