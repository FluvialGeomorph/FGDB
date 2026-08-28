# ADR-0006: Optional hierarchy geometry and national hydrography names

- Status: accepted
- Date: 2026-08-28

## Context

Collection, Study Area, Stream, Reach, and Survey Event form a mandatory
referential hierarchy, but that does not mean every entity has a useful or
defensible polygon.

A Study Area polygon has a clear purpose: it identifies the rough Area of
Interest (AOI) being evaluated, including investigations that occur before any
remediation project exists. Stream and Reach polygon extents are often
ambiguous. A watershed or catchment includes land far beyond the channel and
floodplain normally analyzed, while a hand-drawn floodplain buffer would
consume analyst effort without supporting the calculations. A Survey Event
extent is operationally meaningful because it bounds the DEM and computational
work, but historical workflows often retained only the DEM.

Historically, analysts derived a synthetic stream network from terrain and
manually divided it into Streams (formerly `sites`) and Reaches according to
study objectives. Names were also assigned manually. Current national
hydrography services can provide more consistent candidate names and durable
external references, but national hydrographic segments and watershed units do
not define FGDB's investigation-specific Reach segmentation.

## Decision

- Entity records are mandatory at every hierarchy level; spatial
  representation cardinality varies by level.
- Study Area requires exactly one multipart-capable polygon representing the
  current rough AOI. The term does not imply that a remediation project exists.
- Stream has zero or one optional polygon. FGDB does not require a WBD HUC,
  catchment, drainage-area, floodplain, or analyst-drawn proxy merely to make
  the hierarchy spatial at this level.
- Reach has zero or one optional polygon for the same reason. Reach identity
  and parentage do not depend on polygon availability.
- Survey Event has zero or one optional polygon representing the analysis/DEM
  AOI. It may be supplied by the analyst or derived from the governed
  hydro-modified DEM footprint. Historical loads need not fabricate source
  vector geometry when the DEM is the only retained evidence.
- Absence of optional Stream, Reach, or Survey Event geometry does not weaken
  referential integrity and is not a validation failure.
- The terrain-derived synthetic network is manually reviewed and segmented by
  the analyst into investigation-relevant Stream and Reach units. National
  dataset segmentation does not override that scientific and investigative
  judgment.
- Future naming workflows query a configured current national hydrography
  service and present candidate names and identifiers for analyst confirmation.
  The service is an advisory naming source, not an authority for FGDB identity,
  hierarchy, analysis geometry, or Reach boundaries.
- The selected external dataset/product, feature identifier, supplied name,
  service/version or retrieval date, and analyst disposition are retained as
  naming provenance. FGDB immutable IDs remain the relationship keys.
- Watershed names and HUC identifiers may provide context for watershed-type
  Study Areas, but WBD polygons are not the default Stream or Reach geometry
  and WBD names are not automatically substituted for stream names.

## Current national-service evidence

As reviewed on 2026-08-28, USGS states that maintenance shifted from NHD, WBD,
and NHDPlus HR to the 3D Hydrography Program (3DHP) in 2024. The current 3DHP
Feature Service publishes Flowline features with fields including `id3dhp`,
`mainstemid`, `gnisid`, and `gnisidlabel`. It is therefore the preferred
starting point for a current implementation, while the integration must remain
configurable because national products and endpoints evolve.

- USGS access page: <https://www.usgs.gov/3d-hydrography-program/access-3dhp-data-products>
- Current 3DHP Feature Service: <https://3dhp.nationalmap.gov/arcgis/rest/services/usgs_3dhp_all/FeatureServer>
- Current Flowline layer: <https://3dhp.nationalmap.gov/arcgis/rest/services/usgs_3dhp_all/FeatureServer/50>

## Consequences

- FGDB tables and relationship keys, not polygon containment, enforce the
  hierarchy.
- Analysts are not required to invent arbitrary Stream or Reach AOIs.
- Applications can map an entity using its optional polygon, child geometry,
  Survey Event DEM footprint, or derived service view as appropriate.
- The logical schema must separate mandatory entity rows from optional spatial
  representations, even if Esri implementation uses paired tables and feature
  classes.
- Survey Event footprint derivation must be deterministic and record whether
  geometry was analyst-supplied or DEM-derived.
- National-name lookup requires service configuration, candidate-selection UX,
  provenance fields, fallback behavior, and tests that do not assume permanent
  service availability.
- Unnamed or ambiguous national features still require an analyst-confirmed
  FGDB display name; the reason for manual selection or override is retained.
- Synthetic-network persistence and its ownership granularity remain a
  separate feature-catalog decision.
