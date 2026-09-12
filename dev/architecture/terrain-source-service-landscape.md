# Terrain discovery and access services

## Recommendation (2026-09-12)

Extend the [multi-catalog direction](multi-catalog-terrain-provenance.md), not the
number of assumed independent acquisitions. Distinguish a discovery inventory,
source steward, delivery endpoint and processing service. The same observation
can appear through all four, and the same organization can supply several roles.
Access, cost and reuse rights are separate questions. These are investigated
candidate services, not newly deployed integrations or purchased subscriptions.

| Service family | Verified role/access | Recommended FG treatment |
|---|---|---|
| USGS WESM/3DEP, The National Map, LidarExplorer | WESM/index discovery; TNM product discovery/download; LidarExplorer searches, visualizes and processes 3DEP products. Direct HTTP and TNMAccess are available. Some bulk AWS routes are requester-pays. | One USGS service family with distinct catalog and asset references; do not count alternate viewers as independent holdings. Explore non-standard contributed products as well as the published-lidar index. |
| USIEI | Multiagency inventory and discovery pointers, not the host of every source. | Continue broad discovery and historical leads; resolve actual access with the steward. |
| NOAA Digital Coast DAV and NOAA coastal lidar AWS | DAV supports selection and custom processing. Public AWS assets/catalogs support direct access without an AWS account. Representations include different formats and CRS conventions; not every project has every representation. | Next national service family to qualify. Treat DAV and AWS as related access/processing paths, not separate acquisitions. Preserve product transformations and reference systems. |
| State, county, regional and university repositories | DOGIS supplies actual 2022 Douglas County products and metadata that a national inventory links to. Nebraska maintains a statewide elevation coordination effort. | First-class source stewards, especially for archive reconstruction. Begin with project-relevant portals rather than a universal crawler. |
| OpenTopography | Mixed model: some hosted high-resolution and global data are free; nonacademic access to USGS/NOAA high-resolution services uses OT+. Academic eligibility differs. API terms and limits are distinct. | Explore unique research/community collections and optional processing convenience. Do not require a subscription for FG's core public-data discovery or mistake replicated USGS/NOAA access for new observations. |
| USACE/NGA GRiD | Public landing page documents CAC/GEOAxIS account access. HEC-RAS documents an authorized terrain-query workflow. | Agency-authorized source, not established as a commercial subscription service. Qualify on-network with authorized users; actual FG-accessible holdings, permissions and API entitlement remain unknown. No login or restricted-data access performed here. |

## Priority and provenance implications

1. Continue WESM/USIEI; use TNM and steward links to resolve actual products.
2. Qualify NOAA Digital Coast's public catalogs/assets as the next national family;
   retain targeted state/local sources now, as demonstrated by Cole Creek.
3. Assess OpenTopography's distinct hosted collections separately from optional paid
   processing/access convenience. Verify terms for any FG application integration.
4. Qualify GRiD through an authorized agency session. Do not export restricted
   catalog assertions or assets into public reports/repositories by default.

Proposed source-access records should distinguish anonymous/account/authorized
access, service cost, license/reuse conditions, metadata versus asset access,
retrieval date, original versus transformed edition, and failed versus unsearched
endpoints. Download availability is not permission to redistribute. A mirror can
improve reliability without adding an observation. No source is required to have
a WESM ID; no portal name alone establishes acquisition identity.

The [Cole Creek access review](../../../fluvgeo/dev/features/cole-creek-source-access-review.md)
verified useful public paths but also found date, CRS and rights ambiguities.
This makes the separation practical, not merely theoretical. A national estimate
of unique holdings across these services has not been performed.

## Primary sources checked

- [USGS GIS download and delivery routes](https://www.usgs.gov/the-national-map-data-delivery/gis-data-download)
- [USGS direct links and TNMAccess](https://www.usgs.gov/faqs/can-national-map-data-be-downloaded-direct-links)
- [USIEI](https://coast.noaa.gov/digitalcoast/tools/inventory.html)
- [NOAA coastal lidar/DAV](https://www.coast.noaa.gov/digitalcoast/data/coastallidar.html)
- [NOAA coastal lidar AWS registry, formats, access and STAC links](https://registry.opendata.aws/noaa-coastal-lidar/)
- [DOGIS open data](https://data.dogis.org/)
- [Nebraska elevation program](https://nitc.nebraska.gov/advisory-groups/gis-council/workgroups/nebraska-statewide-elevation-program-workgroup)
- [OpenTopography access tiers](https://opentopography.org/about/subscriptions)
- [OpenTopography developer terms and API routes](https://opentopography.org/developers)
- [GRiD public access description](https://grid.nga.mil/grid/)
- [HEC-RAS authorized GRiD terrain access](https://www.hec.usace.army.mil/confluence/rasdocs/rmum/6.6/terrain-layer)

Pricing and access descriptions are observations on the review date, not enduring
entitlements. No account creation, purchase or cloud compute job was performed.
