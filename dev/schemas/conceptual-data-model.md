# FGDB conceptual data model

## Status

This document records accepted conceptual invariants. It is not yet a logical
or physical Esri geodatabase schema.

## Domain hierarchy

```text
Collection
└── Study Area
    └── Stream
        └── Reach
            └── Survey Event
                └── FG Feature and raster content
```

The hierarchy is mandatory for both collections. Client convenience must not
create records that bypass a level:

- each study area belongs to exactly one collection;
- each stream belongs to exactly one study area;
- each reach belongs to exactly one stream;
- each Survey Event belongs to exactly one Reach; and
- every governed feature record and raster item belongs to exactly one Survey
  Event.

One Reach may have many Survey Events. Each Survey Event identifies one terrain
condition/acquisition period and owns one current set of derived content.
Acquisition and derivation remain conceptually distinct, but processing is not
another persistent level in the domain hierarchy.

Each parent may own one or more children of the next type. Shiny applications
may create required child records automatically when the user should not have
to manage the hierarchy directly, but they must preserve the same foreign-key
chain. Association entities needed for external references remain to be
defined without weakening this ownership hierarchy.

## Collection

`collection` is both the top-level partition and a governance boundary.

| Collection class | Source | Audience | Meaning | Initial visibility | Mutation model |
|---|---|---|---|---|---|
| Desktop | ArcGIS Pro and `FluvialGeomorph-toolbox` | Experienced GIS analysts and authorized customers | Expert-produced, authoritative analysis | After rigorous QA | Idempotent reach-survey-event replacement |
| Shiny | Browser-based FluvialGeomorph applications | General USACE users | Self-service, informative analysis | Immediately after valid save, subject to authorization | Edit in place |

The schema must expose collection membership unambiguously for every governed
entity, feature record, and raster item. Whether this is implemented by direct
foreign keys, inherited ownership, separate datasets, or a combination is a
physical-design decision.

## Identity and names

- Each durable domain entity has an immutable machine identifier.
- Study-area names are human-readable and globally unique across collections.
- A study-area name has two governed components: a controlled three-letter
  uppercase USACE district code and a concise descriptive study-area name. The
  canonical separator and remaining character/normalization rules are not yet
  specified.
- Each study area is one governed, multipart-capable polygon feature in Web
  Mercator (EPSG:3857). It denotes the analyst's current rough Area of Interest
  (AOI), including evaluation work that may precede any remediation project.
  It is not an official boundary and may be edited in place as the investigation
  scope changes, with modification actor/time recorded.
- Each study area has one controlled extent type: `SMALL_REACH`, `LONG_REACH`,
  or `WATERSHED`.
- Display names are not substitutes for immutable identifiers in foreign keys,
  ingestion keys, or service contracts.
- Rename, alias, reservation, and reuse rules remain unresolved.

## Spatial representation cardinality

Hierarchy entities are mandatory; geometry availability is not what enforces
their relationships.

| Entity | Geometry cardinality | Meaning |
|---|---:|---|
| Study Area | exactly 1 polygon feature | Required rough AOI for discovery, communication, and spatial organization. |
| Stream | 0 or 1 polygon feature | Optional cartographic AOI; no required HUC, drainage-area, floodplain, or hand-drawn proxy. |
| Reach | 0 or 1 polygon feature | Optional cartographic/analysis AOI; identity remains valid without geometry. |
| Survey Event | 0 or 1 polygon feature | Optional DEM/analysis AOI, supplied by an analyst or derived from the hydro DEM footprint. It is not asserted to be the source point-cloud acquisition footprint. |

Optional geometry absence is not a hierarchy-integrity failure. If a Survey
Event polygon is materialized, its origin must distinguish
`ANALYST_SUPPLIED` from `HYDRO_DEM_FOOTPRINT`. Exact derivation and refresh
rules remain to be specified.

## Stream and Reach names

- Stream and Reach records retain FGDB immutable IDs regardless of external
  national identifiers.
- Future workflows query a configured current national hydrography service for
  candidate names and identifiers and require analyst confirmation.
- Store the selected source product, external feature identifier, source name,
  service/version or retrieval date, and analyst disposition as naming
  provenance.
- Current implementation planning should begin with USGS 3DHP Flowline names
  and identifiers. NHD, WBD, and NHDPlus HR are legacy products as of the
  2026-08-28 design review.
- WBD names/HUCs may inform watershed-type Study Areas but do not define Stream
  or Reach polygons and are not automatically substituted for stream names.
- National hydrography is advisory for naming. The analyst still segments the
  terrain-derived network into FGDB Streams and Reaches based on investigation
  objectives.

## Survey Event time and current derivation

- Each Survey Event has a required year, optional month, and optional day. A
  day requires a month, and all supplied components must form a valid date.
- Unknown components are null and are never represented by invented dates.
- Its concise display label is `YYYY` when month is unknown and `YYYY-MM` when
  month is known, derived from the stored components.
- The display label is not an identity and is not assumed globally unique.
- Chronological operations use the known date components, not the label or load
  timestamp. Ordering events with equal or incomplete dates remains unresolved.
- Base-event status is not stored in FGDB. Reports select the latest event as
  the default comparison base.
- Each Survey Event has exactly one current derivation-provenance record when
  governed derived content exists. It records the best available source
  metadata, processing timestamp, method/tool and version, material parameters,
  responsible agent/process, retained outputs, validation, and load outcome.
- Reprocessing because of an error does not create a new Survey Event or a
  second authoritative derivation entity. It atomically replaces the incorrect
  derived content and updates the Survey Event's current derivation provenance.
- Optional operational load/attempt logs may record that replacement occurred,
  but they are audit records rather than authoritative geomorphic content or a
  one-to-many domain relationship.
- Legacy Survey Events may have only a known year and evidence such as a file
  geodatabase, folder, report, or analyst knowledge. Missing clearinghouse
  metadata, point-cloud footprints, and discarded source/intermediate files
  remain explicitly unknown or not retained; FGDB does not fabricate them.

## Governed terrain boundary

FGDB retains the active hydro-modified DEM for each reach-survey-event as an
Enterprise mosaic item. Terrain acquisition and local preparation artifacts,
including point clouds, contributing-watershed products, source DEMs,
and hillshades, are outside FGDB persistence scope. Cutline polylines are the
exception: FGDB retains them as governed records of where source terrain was
judged inadequate and hydro-modification interpolation was applied.

Desktop analysis uses an appropriate local projected horizontal CRS and
vertical reference. Governed geometry and rasters are transformed to Web
Mercator (EPSG:3857) for consolidated Enterprise storage. Native analysis CRS,
horizontal unit, vertical datum, and vertical unit remain required provenance;
horizontal reprojection does not define or normalize elevation values.
Horizontal and vertical transformations are approved per source CRS. Raster
item properties must conform to the Enterprise `hydro_dem` mosaic dataset.

## Desktop replacement unit

The logical replacement key is one desktop collection reach-survey-event. The
exact key fields will be finalized with the identifier model. Each key has at
most one current accepted derived result set and one current derivation record.

For a corrected load:

1. inventory the complete source;
2. calculate an input manifest or equivalent fingerprint;
3. validate a complete candidate dataset;
4. stage all affected feature and raster content;
5. replace all active target content owned by the replacement key;
6. verify completeness and integrity across target datasets; and
7. update the current derivation provenance and record the load outcome and
   manifest.

An exact repeat must not create duplicates. A changed source must not be
treated as an exact repeat. Known-bad prior geometry and attributes are removed
from active/queryable production content rather than retained as data
revisions.

## Shiny edit unit

A saved Shiny analysis has a durable identity and is updated in place. Updates
must retain at least the last modifying actor/process and modification time.
Optimistic concurrency, change audit depth, deletion versus retirement, and
multi-user sharing behavior remain unresolved.

## Shared provenance

Both collections require:

- collection identity and source class;
- originating application and version;
- `{fluvgeo}` version and, where needed, calculation-contract version;
- derivation method/engine and method version for each feature family;
- responsible actor or process;
- creation/load and last-modification timestamps as applicable;
- Survey Event identity and known date components/precision;
- source metadata and retention/completeness status when known;
- current derivation-provenance identity, processing time, software/method
  version, material parameters, inputs when known, and retained outputs;
- native analysis horizontal CRS/unit and vertical datum/unit;
- Enterprise spatial reference;
- validation outcome; and
- source/load manifest appropriate to the workflow.

Shared `{fluvgeo}` provenance identifies common scientific implementation. It
does not imply that records from the two collections have equal authority,
review, spatial scope, or fitness for a particular use.

## Required future contracts

- Collection codes and immutable ID formats.
- Tiered study-area naming grammar and uniqueness enforcement.
- Desktop QA states and publication gates.
- Feature-class and mosaic-dataset ownership keys.
- Hydro DEM raster transformation, cell alignment, resampling, NoData, pixel,
  and vertical-value rules.
- Approved per-source-CRS horizontal and vertical transformation registry.
- Shiny save/restore payload, edit concurrency, and authorization.
- Cross-collection query and service behavior.
- Survey Event identity rules, minimal legacy metadata, derivation-provenance
  fields, and enforcement of one current accepted result set.
