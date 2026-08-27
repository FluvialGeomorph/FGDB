# FGDB feature catalog specification

## Status

Draft design specification with an accepted workflow-foundation scope. The
catalog will be extended through the Level 1, Level 2, and Level 3 workflows.
An entry describes a governed logical object or product; it does not by itself
require a separate Esri feature class, table, or mosaic dataset.

## Purpose and boundary

The feature catalog is the controlled inventory from which FGDB logical and
physical schemas, ingestion mappings, validation rules, services, and
documentation will be derived. Despite its historical name, it covers domain
entities, vector features, raster analysis products, and the metadata needed
to govern them.

The catalog contains only governed FGDB objects. Analyst choices and local
data preparation that produce an accepted load package remain outside FGDB.
They can be documented in the Tech Manual without becoming database entities
or retained database content.

Catalog order follows the analysis workflow and dependency graph. Flowline is
an important later consistency case, but it is not the first catalog object.

## Evidence states

| State | Meaning |
|---|---|
| Accepted | Established by an accepted FGDB decision or explicit design agreement. |
| Documented | Describes the current workflow or a historical artifact; it is not automatically the target design. |
| Proposed | Recommended target behavior awaiting review. |
| Unresolved | Evidence or a design decision is still required. |

## Required catalog record

Every catalog entry will eventually define the following properties. Unknown
values remain explicit rather than being inferred from legacy names or storage
locations.

| Property | Required meaning |
|---|---|
| Catalog ID | Stable identifier independent of a physical dataset name. |
| Preferred name and definition | Unambiguous domain meaning. |
| Legacy aliases | File-geodatabase, toolbox, manual, or application names. |
| Object kind | Domain entity, vector feature, derived raster, or governed metadata. |
| Workflow stage and level | Production order and applicable L1/L2/L3 stages. |
| Hierarchy owner | Collection, study area, stream, reach, or survey event. |
| Temporal scope | Current, event-specific, base-event-specific, or otherwise explicit. |
| Producer and method | Manual role, ArcPy tool, `{fluvgeo}` function, or other process plus versioned method. |
| Inputs and dependencies | Governed objects and local inputs required to create or interpret the object. |
| Spatial contract | Geometry/raster type, CRS, datum, units, resolution, extent, and NoData behavior as applicable. |
| Attribute contract | Fields, types, nullability, domains, keys, units, and definitions. |
| Identity and relationships | Immutable identity, display labels, cardinality, and parent keys. |
| QA and invariants | Structural, spatial, scientific, and workflow checks required for acceptance. |
| Persistence disposition | Authoritative, recomputable, temporary, excluded, or unresolved. |
| Publication behavior | Visibility, service representation, collection QA gate, and editability. |
| Replacement behavior | Participation in desktop reach-survey-event replacement or Shiny in-place editing. |
| Evidence | Documentation, code, samples, and decisions supporting the contract. |
| Contract maturity | Inventoried, draft, reviewed, accepted, implemented, or verified. |

## Accepted foundation rules

- A Study Area is one governed multipart-capable polygon feature and domain
  entity, not a table plus multiple extent geometries. It is an editable
  depiction of general project scope, not an official boundary.
- Its two-level name comprises a controlled three-letter uppercase USACE
  district code and a concise descriptive study-area name.
- Every Study Area has one required extent-type value from the controlled
  domain `SMALL_REACH`, `LONG_REACH`, or `WATERSHED`.
- LiDAR discovery, point-cloud acquisition and cleaning, contributing-watershed
  terrain, source DEMs, hillshades, and other local preparation artifacts are
  outside FGDB persistence scope.
- Cutlines are retained as governed assumption records, including the material
  hydro-modification method and parameters applied with them.
- The governed terrain raster is the hydro-modified DEM produced for one
  reach-survey-event. It is stored as an item in the Enterprise hydro DEM
  mosaic dataset and follows the collection's publication and mutation rules.
- Desktop processing uses an appropriate local projected horizontal CRS and
  vertical reference. Governed spatial content is transformed to Web Mercator
  (EPSG:3857) for consolidated Enterprise storage.
- Reprojection to EPSG:3857 changes the horizontal grid/coordinates; it does
  not define the raster elevation datum or unit. Native analysis CRS and
  vertical datum/unit are therefore required metadata, and transformations are
  approved per source CRS.
- Survey Event year is required; month and day are optional, with day dependent
  on month. Its concise label is derived as `YYYY` or `YYYY-MM` without
  inventing unknown components. FGDB stores no base-event designation.

## Workflow-foundation entries

### FCAT-001: Study Area

| Property | Current specification |
|---|---|
| Definition | The named geographic subject of a FluvialGeomorph project, represented by one polygon within which streams, reaches, survey events, and governed analysis products are organized. |
| Object kind | Polygon domain entity; it is not a derived geomorphic feature. |
| Workflow stage | 01 - establish study-area identity and location. |
| Hierarchy owner | Exactly one Collection. |
| Temporal scope | Durable across multiple Streams, Reaches, and Survey Events. |
| Identity | Immutable ID plus a globally unique human-readable two-level name. `district_code` is a controlled three-letter uppercase USACE district code; `study_area_name` is a concise descriptive name. Separator and normalization rules remain unresolved. |
| Geometry | Exactly one valid, nonempty, multipart-capable polygon feature in Enterprise Web Mercator (EPSG:3857). One feature may contain one or more polygon parts. |
| Boundary meaning | General area currently under consideration, chosen by the analyst; not an official jurisdictional, regulatory, watershed, or scientific boundary. |
| Mutation | Editable in place at any project-lifecycle stage to reflect scope changes; record last modifying actor/process and time. Deeper geometry history is unresolved. |
| Extent type | Required controlled value: `SMALL_REACH`, `LONG_REACH`, or `WATERSHED`. This describes project geographic extent and does not alter hierarchy. |
| Producer | Desktop analyst or authorized Shiny workflow, subject to collection rules. |
| Persistence | Authoritative governed feature. |
| Publication | Available for map display and hierarchical selection subject to collection visibility and authorization. |
| QA | Unique immutable ID; controlled district code; globally unique composed name; valid polygon including every part; one Collection parent; valid extent-type code; EPSG:3857 target geometry. |
| Evidence | `FG-Tech-Manual/Level-1.qmd`; target prototype `FG_StudyArea`; accepted conceptual hierarchy; ADR-0005. |
| Maturity | Accepted conceptual contract; logical fields remain draft. |

The polygon serves both as the Study Area's spatial identity and its governed
extent. Coarse longitudinal hydrography and acquisition search areas used to
draw it are workflow inputs, not additional FGDB objects.

### FCAT-002: Survey Event temporal identity

| Property | Current specification |
|---|---|
| Definition | The observation context for all governed analysis content belonging to one Reach, with date precision no coarser than year. |
| Object kind | Domain entity and governed temporal metadata. |
| Workflow stage | Established before loading reach-survey-event content. |
| Hierarchy owner | Exactly one Reach. |
| Temporal scope | Required year, optional month, and optional day. |
| Identity | Immutable ID. The date and display label do not replace it. |
| Date fields | `survey_year` is required; `survey_month` and `survey_day` are nullable integers. Day requires month; supplied components must form a valid calendar date. Do not synthesize January or first-of-month values. |
| Date precision | Derived controlled value `YEAR`, `MONTH`, or `DAY`. |
| Display label | `YYYY` when month is unknown; otherwise `YYYY-MM`. Day is retained as data but omitted from the concise label. The label is not assumed globally unique. |
| Ordering | Use known date components. Tie-breaking and ordering when precision differs remain unresolved. |
| Base event | Not represented in FGDB. Reports use the latest Survey Event as their default base. |
| QA | One Reach parent; valid immutable ID; known valid year; valid component dependencies/ranges; precision and label agree with components. |
| Evidence | Historical year-based event names; documented monthly reflights; accepted conceptual hierarchy; ADR-0005. |
| Maturity | Accepted conceptual contract; logical fields remain draft. |

### FCAT-003: Cutlines

| Property | Current specification |
|---|---|
| Definition | Analyst-drawn polylines identifying where the source DEM inadequately represented a channel flow path and where hydro-modification interpolation was applied. |
| Legacy aliases | `cutlines`. |
| Object kind | Governed assumption/provenance vector feature. |
| Workflow stage | Level 1 hydro-modification, before Hydro-modified DEM. |
| Hierarchy owner | Exactly one Survey Event. |
| Geometry | Polyline transformed from the native analysis CRS to Enterprise Web Mercator (EPSG:3857). Z/M policy remains unresolved. |
| Producer | Analyst interpretation of flow blockages, usually infrastructure such as road embankments, culverts, bridges, or underground conveyance. |
| Meaning | Each line begins upstream of a blockage, crosses the inadequate terrain, and ends downstream in good data. It records an analytical assumption, not observed stream geometry. |
| Method provenance | Required: hydro-modification method/engine/version and material parameters. For the current `_02_HydroDEM.py` method this includes `widen_cells`; the algorithm assigns the minimum source-DEM elevation along each cutline to intersecting/expanded cells. |
| Attributes | The legacy data dictionary defines no business fields and the prototype contains only geometry plus a nullable string survey-event key. The target requires a non-null typed Survey Event key; feature-level notes/reason codes remain unresolved. |
| Zero-cutline case | A reach-survey-event may legitimately require no cutlines. How the load explicitly distinguishes "reviewed, none required" from "not evaluated" remains unresolved. |
| Persistence | Retained authoritative assumption record. |
| Replacement | Included in complete desktop reach-survey-event replacement; Shiny follows in-place collection rules. |
| QA | Complete hierarchy ownership; valid nonempty line for each record; approved source-CRS transformation; method and parameters present; spatial relationship to the Hydro-modified DEM footprint. |
| Evidence | `FG-Tech-Manual/Features.qmd`; `FG-Tech-Manual/Level-1.qmd`; `_02_HydroDEM.py`; target prototype `FG_Cutlines`; ADR-0005. |
| Maturity | Accepted persistence and meaning; detailed attribute contract remains draft. |

### FCAT-004: Hydro-modified DEM

| Property | Current specification |
|---|---|
| Definition | The hydrologically corrected terrain raster used as the governed elevation surface for one reach-survey-event analysis. |
| Legacy aliases | `dem_hydro`, `hydroDEM`, `hydro_DEM`, and project-specific variants. The preferred catalog name is Hydro-modified DEM. |
| Object kind | Governed derived raster. |
| Workflow stage | Level 1 terrain preparation, after local source-DEM creation and cutline processing. |
| Hierarchy owner | Exactly one Survey Event and therefore exactly one Reach, Stream, Study Area, and Collection through the mandatory hierarchy. |
| Producer | Current desktop workflow burns analyst-created cutlines into a local DEM. Canonical producer/method ownership will be specified when this derivation stage is reviewed. |
| Local inputs | Source point clouds, source DEM, contributing-watershed products, and acquisition tooling are outside FGDB persistence scope. FCAT-003 Cutlines are retained. |
| Native analysis reference | Required provenance: source projected horizontal CRS, horizontal unit, vertical datum, vertical unit, cell size, extent, and NoData definition used for scientific analysis. |
| Enterprise spatial contract | Raster item transformed to Web Mercator (EPSG:3857) using the approved horizontal and vertical transformations for its source CRS. Item properties must match the Enterprise `hydro_dem` mosaic dataset. |
| Pixel contract | Documented legacy pixel type is 32-bit floating-point elevation. Target pixel type remains to be confirmed against production rasters. |
| Persistence | Authoritative mosaic item in the Enterprise hydro DEM mosaic dataset. Source terrains and watershed products are not retained. |
| Replacement | Included in atomic desktop replacement of its complete reach-survey-event. Shiny behavior follows in-place collection rules when Shiny produces this object. |
| QA | Complete hierarchy key; readable nonempty raster; declared native and Enterprise spatial references; declared vertical datum/unit; approved per-source-CRS transformations; expected reach coverage; item parameters conform to the `hydro_dem` mosaic; derivation and load provenance. |
| Publication | Governed by collection visibility and future raster-service contracts. |
| Evidence | `FG-Tech-Manual/Features.qmd`; `FG-Tech-Manual/Level-1.qmd`; `data_dictionary.csv`; target XML reference to `AMD_DEM_hydro_CAT`; ADR-0005. |
| Maturity | Accepted persistence and ownership contract; detailed raster contract remains draft. |

## Workflow context explicitly outside FGDB

The following remain important Tech Manual workflow steps but are not FGDB
catalog objects or retained data:

| Workflow material | FGDB disposition |
|---|---|
| Study-area acquisition/search extent separate from the final polygon | Not retained as a separate object. |
| Initial coarse longitudinal hydrography | Not retained. |
| Contributing-watershed DEM and drainage-basin products | Not retained. |
| LiDAR clearinghouse searches, downloads, point clouds, and cleaning | Outside FGDB scope. |
| Unmodified high-resolution source DEM | Not retained. |
| Optional hillshade | Not retained; recomputable presentation material. |

Exclusion from FGDB does not remove these steps from the production workflow
or its documentation. The load contract begins at governed objects and must
not attempt to prescribe how an analyst acquired or prepared the source
terrain.

## Governed foundation sequence

```text
Collection
  -> Study Area polygon (with extent type)
      -> Stream
          -> Reach
              -> Survey Event (known year; optional month/day)
                  -> Cutlines
                  -> Hydro-modified DEM mosaic item
                  -> subsequent governed FG features and REM
```

## Remaining foundation questions

1. Choose the canonical separator and character/whitespace normalization for
   the composed Study Area name, plus rename and alias rules.
2. Decide whether mutable Study Area geometry needs history beyond last
   modifying actor/time.
3. Define ordering and client disambiguation for Survey Events with equal dates
   or different date precision.
4. Define the approved per-source-CRS horizontal/vertical transformation
   registry and the complete `hydro_dem` mosaic contract.
5. Define how a no-cutline case records that terrain was evaluated and no
   intervention was required.

## Next-stage draft entries

### FCAT-005: Stream

| Property | Draft specification |
|---|---|
| Definition | A durable named watercourse or connected watercourse unit within one Study Area; the current manuals often call this unit a `site`. |
| Object kind | Domain entity. Whether it owns an independently stored geometry remains unresolved. |
| Hierarchy owner | Exactly one Study Area. |
| Temporal scope | Durable across Reaches and Survey Events. |
| Identity | Immutable ID. Proposed human name unique within its Study Area; legacy combined `ReachName` strings are not keys. |
| Geometry evidence | The target prototype represents `FG_Stream` as a polygon plus a parallel table. The current workflow primarily establishes a Stream through edited network lines and named tributaries. Neither artifact yet establishes the target geometry contract. |
| QA | One Study Area parent; non-null immutable ID; valid name; no hierarchy derived from string parsing. |
| Evidence | Level 1 "Criteria for Creating Sites"; Site-to-Stream terminology decision; target prototype `FG_Stream` and `FG_Stream_Table`. |
| Maturity | Draft; geometry and naming contract require review. |

### FCAT-006: Reach

| Property | Draft specification |
|---|---|
| Definition | A durable analytical segment of one Stream, divided where drainage area, slope, sinuosity, infrastructure, or study objectives justify a separate unit. |
| Object kind | Domain entity with a likely polygon representation. |
| Hierarchy owner | Exactly one Stream. |
| Temporal scope | Durable across Survey Events. |
| Identity | Immutable ID. Proposed concise reach name unique within its Stream, such as `R1`; legacy combined site/reach names are aliases, not relationship keys. |
| Geometry evidence | Legacy `boundary` is a manually drawn polygon associated with a reach-survey-event geodatabase. The target prototype represents `FG_Reach` as a polygon plus a parallel table. Whether the durable Reach polygon is the normalized legacy boundary or a different general scope polygon remains unresolved. |
| QA | One Stream parent; non-null immutable ID; valid name; geometry contract once accepted; no hierarchy derived from `ReachName`. |
| Evidence | Level 1 "Define Reaches"; Tech Manual `boundary`; User Manual "Create a Boundary"; target prototype `FG_Reach` and `FG_Reach_Table`. |
| Maturity | Draft. |

### FCAT-007: Synthetic stream network

| Property | Draft specification |
|---|---|
| Definition | A terrain-derived polyline network created from flow accumulation and then manually edited to retain and segment the watercourses analyzed in the Study Area. |
| Legacy aliases | `stream_network`; intermediate raster/vector names include `derived_streams`. |
| Object kind | Derived and analyst-edited polyline. Persistence disposition unresolved. |
| Workflow stage | Level 1, after Hydro-modified DEM and before Flowline. |
| Inputs | Hydro-modified DEM through unretained drainage intermediates; initiation `threshold`; derivation engine/version; analyst edits. |
| Identity evidence | Legacy `ReachName` combines site/stream and reach semantics. Target relationships must instead use immutable Stream/Reach/Survey Event keys. |
| Ownership issue | The current network is initially derived across a Study Area or Stream and can span several Reaches, while governed analysis features currently require Survey Event ownership under one Reach. The target must either retain reach-survey-event segments or classify the full network as a local construction artifact. |
| Persistence evidence | The target prototype has no `FG_StreamNetwork`; the supplied wild-caught reach XML does not contain `stream_network`. Absence is evidence, not a decision. |
| QA if retained | Valid lines; no unintended gaps/duplicates; documented threshold and method; analyst-edit completion; explicit immutable ownership; approved CRS transformation. |
| Maturity | Inventoried; target disposition requires review. |

## Next catalog slice

Resolve the Stream geometry, Reach/boundary normalization, and synthetic
stream-network persistence questions. Then accept the corresponding contracts
before proceeding to Flowline.
