# Scientific traceability: vertical reference, source provenance and units

## Status and intent

**Accepted development obligations, 2026-09-12:** the project owner identifies
these three historic weaknesses as required upcoming work, not optional ideas.
They strengthen FluvialGeomorph science independently of FGDB. They are not new
blanket prerequisites for continued toolbox development or initial deployment;
operations that require unresolved scientific facts must still expose that limit.
This roadmap records requirements, not implemented capability or an approved
physical schema. Candidate mechanisms below remain **proposed**.

The aim is to automate reliable bookkeeping and expose only consequential
analyst decisions, not require more manual metadata paperwork. Both newly designed
studies and forensic reconstruction must preserve evidence, exceptions and unknowns.

## Required work and completion evidence

### 1. Vertical reference

[ADR-0026](../decisions/adr-0026-vertical-reference-recovery-and-preservation.md)
records the owner's identified root cause: historic tools and FG practice did not
provide dependable, interoperable vertical-reference preservation. Legacy
reconstruction is a required workflow, while new products must carry explicit,
testable declarations. This is not a claim that vertical standards did not exist
or that every archive ambiguity has the same cause. Missing, reader-unexposed,
conflicting and analyst-reconstructed metadata must remain distinguishable.

Preserve native horizontal and vertical reference definitions independently of
display/storage CRS. Record elevation units, height type, datum/realization and,
where applicable, geoid model and coordinate epoch. Distinguish assigning an
evidenced definition, converting units, transforming a datum and resampling a grid.
Never infer elevation units or datum from horizontal CRS or a filename.

**Typical archived workflow (owner clarification):** skilled analysts could choose
analysis horizontal/vertical references independently of incoming point-cloud
references, often preparing all project DEMs in one selected analysis framework
and deriving FG products from that common base. Preserve this transformation-on-
preparation strategy and its rationale. Recovery must distinguish source,
analysis and delivery/storage CRS and reconstruct their connecting operations;
unequal CRS definitions across those roles are not automatically an error.
The missing durable record does not imply that analysts lacked transformation
expertise. Future tooling should record the project choice once, link dependent
artifacts and capture source-specific operations and exceptions.

**Owner's historical clarification, 2026-09-12:** FG began without an adopted
mechanism for recording vertical CRS on its DEMs, and the project has not yet
adopted the later Esri capability. Preserve this account of FG practice; the precise
Esri introduction date/version was not established by this review. Today's support
does not repair the missing historical declarations.

**Proposed approach:** standards-based CRS definitions with authority identifiers
where available and loss-resistant WKT2/PROJJSON representations, plus explicit
artifact-linked metadata where clients/formats do not preserve the full meaning.
Keep embedded and linked declarations consistent; report conflicts rather than
silently choosing one. Preserve transformation operation, grids/resources,
versions and applicable accuracy/area limits.

**Completion evidence:** value-bearing fixtures cross R/sf/terra/GDAL/PROJ, QGIS
and licensed ArcGIS boundaries, exercising known references, unknowns, conflicting
metadata and unavailable transformation resources. Test units, elevations, masks
and definitions, not merely successful file opening or matching CRS strings.
Do not reopen the rejected universal raster-GeoPackage equivalence assumption.

### 2. Source data provenance

Keep acquisition/Survey Event, stewarded source product/version and FG derived
dataset edition distinct. Allow multiple source products per derivative and reuse
across derivatives/events without inventing new acquisitions. Acquisition period,
publication date, retrieval date and processing date have different meanings.

**Proposed minimum record:** provider; collection/work-unit/product identifiers;
version or DOI when supplied; asset and metadata links; retained metadata snapshot;
acquisition period; retrieval date; source CRS/vertical reference/units; and an
asset checksum when accessible. Link the exact inputs used to the derivative's
AOI/mask, processing steps/parameters, scientific/software versions and output
identity. Preserve analyst attribution and unresolved or competing legacy claims.
An overlapping catalog footprint is a candidate match, not proof of lineage.

The [WESM archive discovery findings](../architecture/wesm-archive-source-discovery.md)
verify older collection records and a live USGS query interface. Support later
evidence-backed enrichment when catalogs gain information, without depending on
an unverified promise of complete historical backfill.

**Completion evidence:** trace one thin derived terrain product back to its actual
source edition and recipe, including a multi-source case and unavailable/changed
remote-source case. A URL or persistent identifier alone does not pin exact bytes;
a checksum detects change but cannot restore data. Define recoverability/retention
rules before relying on remote reacquisition. Keep small metadata and recipes
locally; retain otherwise irrecoverable inputs in an appropriate local/archive
home when required. This does not expand FGDB into a source-LiDAR repository,
authorize archive deletion, or require public catalog coverage for legacy surveys.

### 3. Analysis variable units

Define units and dimensional meaning for input, intermediate and output variables,
including length, area, volume, elevation, slope and dimensionless quantities.
Separate native, computational, canonical storage and display units. Preserve the
historic feet convention and documented exceptions; no blanket SI migration is
decided here. Unknown units must not silently become a conversion assumption.

**Proposed approach:** use R's `units`/UDUNITS ecosystem for compatible conversion
and dimensional checking, coupled to versioned metric definitions and explicit
serialization contracts. Numeric database columns need retained unit definitions;
R class attributes alone are not a cross-platform persistence contract.

**Completion evidence:** inspect existing calculations, qualify representative
mixed-unit paths and powered units, reject incompatible dimensions, and verify
round trips through supported storage/services and report labels. Include distinct
international-foot/U.S.-survey-foot fixtures. Unit conversion must not masquerade
as vertical-datum transformation or establish cross-event comparability.

## Verified external capabilities and their limits

Official documentation reviewed 2026-09-12. The subsequent linked WESM probe reads
public catalog records and one service candidate; no FG catalog integration or
cross-platform scientific qualification was performed.

- [3DEP WESM](https://www.usgs.gov/3d-elevation-program/3dep-spatial-metadata)
  supplies work-unit/project identifiers, acquisition dates and links to source
  elevation products and project metadata. This is a promising provenance source.
- [USGS elevation-derived hydrography metadata requirements](https://www.usgs.gov/ngp-standards-and-specifications/elevation-derived-hydrography-acquisition-specifications-metadata)
  already describe selected WESM source footprints clipped to the hydrography
  production area, with non-3DEP sources documented separately. This is a useful
  model for FG source-footprint lineage, not a requirement to adopt that entire schema.
- [Geoconnex reference features](https://docs.geoconnex.us/access/reference/)
  identify hydrologic features; [NLDI](https://api.water.usgs.gov/docs/nldi/)
  supports network-linked discovery, currently described against NHDPlusV2.
  Neither automatically establishes which elevation acquisition produced an FG
  raster. Do not assume NLDI already provides universal 3DHP lineage.
- [PROJJSON](https://proj.org/en/stable/specifications/projjson.html) represents
  CRS/coordinate-operation semantics corresponding to WKT2:2019. This supports the
  proposed open contract but does not prove every client preserves it.
- [ArcGIS Project Raster](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/project-raster.html)
  documents vertical CRS/transformation support. The user's historical workflow
  weakness is accepted experience; a universal claim that Esri cannot represent
  vertical reference is not established. Actual format/client fidelity needs tests.
- [R units](https://r-quantities.github.io/units/articles/units.html) supports
  measurement units and compatible conversion. [NIST distinguishes two feet](https://www.nist.gov/pml/us-surveyfoot):
  a legacy foot assertion requires an exact definition before precise conversion.

## Ownership, continuity and sequencing

### Future extension: point clouds to DEMs

**Accepted future requirement, 2026-09-12:** prepare to extend the FG tooling
boundary upstream into reproducible lidar point-cloud-to-DEM production as the
ecosystem becomes suitable. Point clouds and DEMs are complementary: retain the
DEM as a computationally efficient, durable record of terrain assumptions used
by FG analysis. Continue to accept externally prepared DEMs; point-cloud processing
is not a new prerequisite for existing users or archive migration.

Future design must record the input collection/edition, selected point classes,
filtering and overlap treatment, interpolation, breaklines/conditioning, grid,
mask, vertical operations and method/software versions where applied. Preserve
source bare-earth and analysis-conditioned terrain as distinguishable products.
Review mature open-source tools before selecting dependencies; no processing
package, default algorithm or universal automation policy is selected now.
Qualify a bounded source-to-DEM case for scientific validity, repeatability,
resources and interoperability before exposing it through QGIS or Shiny. Human
terrain assumptions remain reviewable. This extends local scientific tooling,
not FGDB into a point-cloud storage or acquisition-management system.

### Required capability: survey discovery for change-over-time analysis

The owner adds [Study Area survey-opportunity review](../features/survey-discovery-opportunities.md)
as a critical future capability. Reuse source discovery to find additional old or
new acquisitions for existing FGDB studies, not only reconstruct provenance. Reduce
specialist search effort and make multi-period analysis more affordable. Distinguish
a new observation from newly published metadata or reprocessing of an old survey;
retain non-3DEP sources and explicit scientific comparability review. Start with a
read-only single-study report, then qualify repeat/batch review across authorized
studies. No scheduled monitor, external integration deployment or automatic processing
is created by this requirement.

### Existing owners and near-term sequence

FGDB owns persistence, intake and scientific-contract requirements; fluvgeo owns
shared scientific calculations, source linkage, validation and reporting. QGIS
and Shiny orchestrate that backend without duplicate science or validators;
fluvgeodata supplies representative fixtures when available. Existing ownership
is unchanged. Discovery follows [ADR-0008](../decisions/adr-0008-geoconnex-and-usace-semantic-governance.md),
including hydrogeofetch and separation of external references from FG identities.
Extend [ADR-0023](../decisions/adr-0023-versioned-scientific-contracts-and-wide-result-tables.md)
metric units, scientific contracts and derived editions; do not replace typed wide
tables or add a processing-run hierarchy. Native reference preservation supplements,
not silently changes, the current governed storage CRS policy.

Proceed incrementally: preserve assertions/unknowns in current intake; next define
and qualify one source-to-derivative vertical-reference/provenance contract; then
extend dimensional validation across calculation families. These are future
implementation slices, not an instruction to perform the entire overhaul now.
No external source match, vertical datum or exact foot variant has been established
for Cole Creek by this review. Its owner-confirmed feet convention is recorded in
the [terrain metadata feature](../../../fg-qgis-toolbox/dev/features/record-terrain-metadata.md#owner-clarification-2026-09-12).
The owner's subsequent correction specifies generic **feet**, not U.S. survey
feet. The [ArcGIS unit investigation](../architecture/legacy-esri-elevation-feet.md)
records the context-dependent Esri meanings and historic international-foot
conversion evidence without automatically relabeling any archive DEM.
