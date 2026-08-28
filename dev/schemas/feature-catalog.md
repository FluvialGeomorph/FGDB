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

The catalog defines governed FGDB objects and records explicit exclusion
decisions needed to prevent legacy workflow artifacts from being loaded by
mistake. Analyst choices and local data preparation that produce an accepted
load package remain outside FGDB. They can be documented in the Tech Manual
without becoming database entities or retained database content.

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
| Semantic term | Stable local ontology term and identity criteria once published. |
| External alignment | Versioned external concept, mapping relation, scope, rationale, and review status; no mapping is a valid explicit result. |
| Object kind | Domain entity, vector feature, derived raster, or governed metadata. |
| Workflow stage and level | Production order and applicable L1/L2/L3 stages. |
| Hierarchy owner | Collection, study area, stream, reach, or survey event. |
| Temporal scope | Current, event-specific, base-event-specific, or otherwise explicit. |
| Producer and method | Manual role, ArcPy tool, `{fluvgeo}` function, or other process plus versioned method. |
| Inputs and dependencies | Governed objects and local inputs required to create or interpret the object. |
| Spatial contract | Geometry/raster type, CRS, datum, units, resolution, extent, and NoData behavior as applicable. |
| Attribute contract | Fields, types, nullability, domains, keys, units, and definitions. |
| Identity and relationships | Immutable identity, display labels, cardinality, and parent keys. |
| Identity-change rule | Properties that may change while identity persists, and changes that require a new entity. |
| QA and invariants | Structural, spatial, scientific, and workflow checks required for acceptance. |
| Persistence disposition | Authoritative, recomputable, temporary, excluded, or unresolved. |
| Publication behavior | Visibility, service representation, collection QA gate, and editability. |
| Replacement behavior | Participation in desktop reach-survey-event replacement or Shiny in-place editing. |
| Physical mapping | Implementing table, feature class, mosaic item, key, relationship, domain, and semantic-projection rule. |
| Evidence | Documentation, code, samples, and decisions supporting the contract. |
| Contract maturity | Inventoried, draft, reviewed, accepted, implemented, or verified. |

## Accepted foundation rules

- A Study Area is one governed multipart-capable polygon feature and domain
  entity, not a table plus multiple extent geometries. It is an editable
  depiction of the rough Area of Interest (AOI), not an official boundary or
  evidence that a remediation project exists.
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
- Survey acquisition and feature derivation are conceptually distinct, but
  processing is not another level in the persistent domain hierarchy. Each
  Survey Event owns one current derived result set and current derivation
  provenance.
- Stream and Reach entity records are mandatory, but their polygons are
  optional. Survey Event polygon geometry is also optional and may be derived
  from the hydro DEM footprint; it represents analysis extent, not necessarily
  the source point-cloud acquisition footprint.
- Stream and Reach names use analyst-confirmed candidates from a configured
  current national hydrography service when available. External names and IDs
  are provenance, not FGDB identity or segmentation rules.
- Stream and Reach extents are project-defined by their own optional FGDB
  geometries. No national geometry, segmentation, measure, or linear
  referencing system defines them. Local stationing, when used, references a
  specific stored FGDB Flowline representation.

## Controlled feature-type vocabulary contract

Geomorphic types such as riffle, pool, bar, bankfull polygon, bankline, valley
bottom, and later L2/L3 types use stable concept IDs rather than free-text or
display labels as stored classifications. Each concept record requires:

- immutable concept ID and vocabulary ID;
- preferred label and unambiguous definition;
- authoritative source/citation and vocabulary version;
- lifecycle status such as `PROPOSED`, `ACCEPTED`, or `DEPRECATED`;
- effective and deprecation metadata when applicable; and
- zero or more aliases/synonyms that never serve as foreign keys.

Physical coded-value domains may mirror accepted concepts for Esri editing,
but the normalized concept table remains the semantic source. This contract is
designed for later SKOS mapping without requiring SKOS or OWL in the current
database implementation.

## Workflow-foundation entries

### FCAT-001: Study Area

| Property | Current specification |
|---|---|
| Definition | The named geographic Area of Interest being evaluated, represented by one polygon within which Streams, Reaches, Survey Events, and governed analysis products are organized. The evaluation may precede or never result in a remediation project. |
| Object kind | Polygon domain entity; it is not a derived geomorphic feature. |
| Workflow stage | 01 - establish study-area identity and location. |
| Hierarchy owner | Exactly one Collection. |
| Temporal scope | Durable across multiple Streams, Reaches, and Survey Events. |
| Identity | Immutable ID plus a globally unique human-readable two-level name. `district_code` is a controlled three-letter uppercase USACE district code; `study_area_name` is a concise descriptive name. Separator and normalization rules remain unresolved. |
| Geometry | Exactly one valid, nonempty, multipart-capable polygon feature in Enterprise Web Mercator (EPSG:3857). One feature may contain one or more polygon parts. |
| Boundary meaning | Rough AOI currently under consideration, chosen by the analyst; not an official jurisdictional, regulatory, watershed, or scientific boundary. |
| Mutation | Editable in place throughout the investigation lifecycle to reflect AOI changes; record last modifying actor/process and time. Deeper geometry history is unresolved. |
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

### FCAT-002: Survey Event identity and current derivation

| Property | Current specification |
|---|---|
| Definition | The terrain condition/acquisition period represented by the current governed analysis content for one Reach, with date precision no coarser than year. One Reach may own many Survey Events. |
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
| Geometry | Zero or one optional polygon representing the DEM/analysis AOI. It may be supplied by the analyst or derived from the Hydro-modified DEM footprint; it is not asserted to be an acquisition-tile footprint. Historical loads do not fabricate a source polygon. |
| Geometry provenance | When materialized, required controlled value `ANALYST_SUPPLIED` or `HYDRO_DEM_FOOTPRINT`, plus derivation method/version when applicable. |
| Identity-change rule | Correcting descriptive metadata or increasing date precision for the same documented acquisition preserves identity. Evidence that records represent a different acquisition occurrence requires a new ID. Exact merge/split adjudication remains unresolved. |
| Minimum legacy population | Immutable ID, Reach parent, required year, known date precision, and evidence basis such as legacy event label, file geodatabase, report, folder, or analyst knowledge. Provider, collection ID, clearinghouse URI, month/day, and source footprint are nullable. |
| Source status | Record metadata completeness (`MINIMAL`, `PARTIAL`, or `DOCUMENTED`) and source retention (`NOT_RETAINED`, `EXTERNAL`, `TEMPORARY`, or `RETAINED`) without inventing missing metadata. Point clouds and intermediate terrain products remain outside FGDB persistence scope. |
| Current derivation provenance | Exactly one current provenance record when derived content exists: processing time, tool/method and version, `{fluvgeo}` and caller versions where applicable, material parameters/configuration, responsible agent/process, known inputs, retained outputs, validation, and load outcome. |
| Reprocessing | A correction preserves the Survey Event ID, atomically replaces its incorrect current derived content, and updates current derivation provenance. It does not create a second persistent derivation entity. Optional execution/load history is operational audit data only. |
| QA | One Reach parent; valid immutable ID; known valid year; valid component dependencies/ranges; precision and label agree with components; exactly one current derivation-provenance record whenever current derived content exists. |
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
| Stream Geodatabase (legacy `Site Geodatabase`) | Optional local preprocessing workspace; not an FGDB entity, load package, or retained object. |
| Stream-scale DEM | Local terrain preparation input; not retained in the Enterprise hydro DEM mosaic. |
| Pre-segmentation synthetic stream network and drainage intermediates | Local construction artifacts; not retained. |
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

| Property | Current specification |
|---|---|
| Definition | A durable project-identified watercourse or connected watercourse unit within one Study Area; it may be unnamed in national systems, and the current manuals often call this unit a `site`. |
| Object kind | Mandatory domain entity with an optional spatial representation. |
| Hierarchy owner | Exactly one Study Area. |
| Temporal scope | Durable across Reaches and Survey Events. |
| Identity | Immutable ID. Human name is proposed unique within its Study Area; legacy combined `ReachName` strings are aliases, not keys. |
| Geometry | Zero or one optional polygon in EPSG:3857. Do not require a WBD HUC, catchment/drainage area, floodplain proxy, or analyst-drawn polygon. |
| Geometry purpose | Optional cartographic AOI only; it is not required by the analysis and does not enforce parentage. |
| Extent authority | The stored FGDB geometry, when present, is the only direct assertion of Stream extent. National feature and watershed geometries are contextual references and are never substituted when it is absent. |
| Name discovery | Query Geoconnex through `hydrogeofetch` for intersecting/nearby reference-feature candidates. Prefer current USGS 3DHP-backed references when available, retaining `gnisidlabel`/`gnisid`, `mainstemid`, and `id3dhp` context returned or subsequently resolved. Analyst confirms the selected name or records an override/`NO_NATIONAL_NAME` disposition and governed FGDB project name. |
| Naming provenance | Source product/service, external identifier(s), supplied label, service/version or retrieval date, selection status, and override reason when applicable. |
| National-data limitation | A national flowline or watershed unit does not define the FGDB Stream AOI. WBD HUCs are watershed context, not default Stream polygons or names. |
| QA | One Study Area parent; non-null immutable ID; valid confirmed name; naming provenance; valid optional polygon when present; no hierarchy derived from name parsing or containment. |
| Evidence | Level 1 "Criteria for Creating Sites"; Site-to-Stream terminology decision; target prototype; ADR-0006; current USGS 3DHP service. |
| Maturity | Accepted entity/geometry/naming-source contract; exact name grammar and service integration remain draft. |

### FCAT-006: Reach

| Property | Current specification |
|---|---|
| Definition | A durable analytical segment of one Stream, divided where drainage area, slope, sinuosity, infrastructure, or study objectives justify a separate unit. |
| Object kind | Mandatory domain entity with an optional spatial representation. |
| Hierarchy owner | Exactly one Stream. |
| Temporal scope | Durable across Survey Events unless a revised segmentation requires a new Reach identity. |
| Identity | Immutable ID. Human name is proposed unique within its Stream; legacy combined site/reach names are aliases, not relationship keys. |
| Segmentation | Analyst divides the edited synthetic network into Reaches based on investigation objectives and geomorphic/operational criteria. National hydrography segments do not override that decision. |
| Geometry | Zero or one optional polygon in EPSG:3857. Do not require an analyst to draw an arbitrary channel/floodplain AOI merely to spatialize the hierarchy. |
| Extent authority | The stored FGDB geometry, when present, is the only direct assertion of Reach extent. It is independent of national segment endpoints, route measures, and geometry. |
| Linear referencing | No external or national route is required. Derived stationing references a specific FGDB Flowline and must declare origin, direction, units, method, and representation/Survey Event scope. |
| Name discovery | Use the confirmed national Stream name and relevant current hydrography identifiers as naming context. A national feature ID may be associated with a Reach but does not replace its FGDB ID or imply identical boundaries. Exact Reach display-name grammar remains unresolved. |
| Legacy boundary | The legacy `boundary` polygon may represent a survey-specific DEM/analysis AOI rather than the durable Reach. Migration mapping therefore targets optional Survey Event geometry unless evidence establishes another meaning. |
| QA | One Stream parent; non-null immutable ID; valid analyst-confirmed name; naming provenance; valid optional polygon when present; no hierarchy derived from `ReachName` or geometry containment. |
| Evidence | Level 1 "Define Reaches"; Tech Manual `boundary`; User Manual "Create a Boundary"; target prototype; ADR-0006. |
| Maturity | Accepted entity/optional-geometry/segmentation contract; exact naming and legacy-boundary crosswalk remain draft. |

### FCAT-007: Synthetic stream network

| Property | Current specification |
|---|---|
| Definition | A terrain-derived polyline network created from flow accumulation and then manually edited to retain and segment the watercourses analyzed in the Study Area. |
| Legacy aliases | `stream_network`; intermediate raster/vector names include `derived_streams`. The containing local workspace was historically called a `Site Geodatabase`; `Stream Geodatabase` is now preferred. |
| Object kind | Excluded local preprocessing artifact, not a governed FGDB feature. |
| Workflow stage | Stream-scale terrain preprocessing before governed reach-survey-event analysis and Flowline derivation. |
| Inputs | Local Stream-scale DEM through unretained drainage intermediates; initiation `threshold`; derivation engine/version; analyst edits. |
| Segmentation role | Analyst uses investigation objectives to divide the edited network into Streams and Reaches. National hydrography names and identifiers inform labels but do not dictate segment boundaries. |
| Governed handoff | The reviewed segmentation is represented by durable Stream and Reach identities. Geometry copied or transformed into a reach-survey-event workspace is loaded only when it satisfies a separate governed downstream feature contract, such as Flowline. |
| Persistence | Excluded. Do not create an `FG_StreamNetwork` target or load a convenience copy from a legacy reach geodatabase. The Stream-scale DEM and flow-direction/accumulation intermediates are also excluded. |
| Reproducibility | Analysts may retain the Stream Geodatabase and its inputs locally when full process reconstruction is required. FGDB records provenance for retained results but is not a complete preprocessing archive. |
| Evidence | Target prototype has no `FG_StreamNetwork`; supplied wild-caught XML has no `stream_network`; historical manual workflow; human clarification; ADR-0010. |
| Maturity | Accepted excluded disposition. |

## Next catalog slice

Resolve the exact Stream and Reach display-name grammar and the legacy
`boundary` crosswalk. Then proceed to Flowline.
