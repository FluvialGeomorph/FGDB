# Multi-catalog terrain discovery and provenance

## Working direction and authority

2026-09-12: following the owner's request, use a provider-neutral report input
contract and retain multiple catalog references. This is the prudent direction
even without a national estimate of holdings unique to each catalog. It extends
the existing external-reference principle; exact FGDB physical tables and new
live adapters remain proposed, not deployed.

Keep four concepts separate:

1. **Acquisition:** the observation campaign and its spatial/temporal scope.
2. **Source product/edition:** a point-cloud or terrain realization from one or
   more acquisitions, including its transformations and processing.
3. **Catalog record:** a steward's description/discovery entry for a collection,
   work unit or product. Several catalogs may describe the same object at different
   granularity. Catalog owner need not be acquisition provider or data host.
4. **FG derivative:** a local/accepted analysis product linked to the actual inputs
   used, with independent FG identity and retained scientific provenance.

**Proposed persistence:** stable local source identities, provider-qualified
catalog record IDs, versioned retrieved assertions, asset/edition references and
reviewed links with evidence/attribution. Allow many references, disagreement,
missing external IDs and later enrichment. Do not force every source to obtain a
WESM ID, merge identities by names/years, or copy uncertain source CRS onto FG DEMs.
Records for work-unit subsets must not silently identify an entire campaign.
This is compatible with existing Survey Event/derived-edition and Geoconnex
boundaries; it does not introduce a new hierarchy or EAV result model.

## Verified USIEI contribution in this probe

Official [USIEI documentation](https://coast.noaa.gov/digitalcoast/tools/inventory.html)
describes a multi-agency elevation inventory with external data links, downloads
and a map service. Its [March 2023 FAQ](https://coast.noaa.gov/data/docs/digitalcoast/inventory/faq.pdf),
pages 2 and 4, says it does not host the source data, may omit small collections,
and uses generalized non-authoritative footprints. These are discovery boundaries,
not guarantees of exact data support. Source metadata remains necessary.

On 2026-09-12, the same Cole Creek DEM-envelope search against USIEI topographic
lidar [layer 2](https://maps.coast.noaa.gov/arcgis/rest/services/USInteragencyElevationInventory/USIEIv2/MapServer/2)
returned six records, versus one in the earlier 3DEP published-lidar layer-24 query:

| USIEI ID | Catalog title/year | Interpretation before source review |
|---|---|---|
| 23976 | 2004 MAPA, Douglas/Sarpy/Washington counties | Historical lead; no data link supplied. Could bear on the retained 2004/2006 ambiguity. |
| 24256 | 2010 Eastern Nebraska | Broader legacy lead; not automatically the northern WESM work unit. |
| 39542 | 2013 NGA Omaha | Intervening-period lead; catalog June label and linked April path need reconciliation. |
| 23873 | 2016 Eastern Nebraska | Candidate cross-listing of WESM 59026, not an independently counted survey. |
| 47476 | 2022 Eastern Nebraska Douglas County | Later-period lead; catalog links to Douglas/Omaha GIS. |
| 54494 | 2026 Southeast Nebraska | Planned/funded, not an available acquisition. |

The full NWO_Papillion bounding-envelope probe returned 17 USIEI and nine 3DEP
index records, each response count-checked. The report then tests actual geometry
against the Cole Creek R1 flowline; envelope results alone do not prove overlap.
**Inferred:** USIEI materially improves discovery for this example. **Unknown:**
the national number of additional independent acquisitions, whether these leads
are absent from other USGS products/indexes, and exact asset availability/lineage.
The 2013 record itself points to USGS non-standard contributed holdings: absence
from the queried 3DEP layer does not mean absence from USGS.

## Implementation boundary

The subsequent [service landscape review](terrain-source-service-landscape.md)
distinguishes additional catalogs from alternate delivery/processing routes and
records free, subscription and agency-authorized access boundaries. The linked
Cole Creek source-access review resolves the 2013 project-flight interval while
preserving the original USIEI assertion and additional unresolved metadata issues.

The first fluvgeo [offline input contract](../../../fluvgeo/dev/schemas/survey-opportunity-inputs.md)
and report preserve catalog records and evidence rather than flattening catalogs
into claimed acquisitions. The demo uses saved public GeoJSON responses under
`fluvgeo/dev/outputs/terrain-development/survey-opportunities-v1/` and explicit
fixture-only date normalization. USIEI free-text dates and links require adapter
qualification; no generic parser or complete live integration is claimed.

Continue with [survey opportunity requirements](../features/survey-discovery-opportunities.md).
Shared fluvgeo assessment/reporting, FGDB persistence/access, and thin clients
retain their existing ownership. WESM and USIEI are initial discovery sources,
not an exclusive list; other public, restricted or local evidence can be added
through authorized, independently qualified adapters.
