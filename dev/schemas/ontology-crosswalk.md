# Initial ontology and physical-model crosswalk

- Status: exploratory
- Updated: 2026-08-28
- Scope: semantic kernel and early workflow objects

## Crosswalk discipline

This crosswalk records a claim, not just a similar label. Each maintained row
will include the local term IRI, label, external specification and version,
external term identifier, mapping relation, mapping scope, rationale, evidence
URL, reviewer, review date, and status.

Mapping relations have deliberately different strengths:

- **Conforms to**: the local implementation follows an external conceptual
  contract without asserting OWL identity.
- **Subclass of**: every local instance satisfies the external class meaning.
- **Exact/close/broad/narrow match**: SKOS mapping assertions for concepts.
- **Related to**: a useful association that is not subsumption or identity.
- **No direct match**: the local concept remains an FG extension.
- **Candidate**: further competency questions and instance tests are required.

HY_Features is a conceptual UML standard and permits conforming ontology or
schema implementations. Until a sanctioned machine-readable HY namespace is
selected, this document cites its UML class names and the OGC specification;
it does not invent HY class IRIs.

## Initial concept assessment

| FG concept | Candidate external alignment | Assessment and boundary |
|---|---|---|
| Collection | PROV `Collection`; DCAT `DatasetSeries` | Candidate relationships, not equivalence. FG Collection is first a governance and authority boundary. |
| Study Area | GeoSPARQL `Feature` | Local `Area of Interest`; no direct HY class. Its required multipart polygon is one changeable spatial representation. |
| Stream | HY `HY_HydroFeature`; potentially related to `HY_Channel` and `HY_River` | Model initially as a named local hydrographic feature. Do not equate the name-bearing aggregate with either the channel landform or water body until its semantics are resolved. |
| Reach | HY `HY_HydroFeature` at most | Local analysis segmentation selected for investigation objectives. HY deliberately avoids the ambiguous term `reach`; no exact external mapping is justified. |
| Survey Event | SOSA `ObservationCollection` | Candidate alignment for the terrain observation/acquisition period represented by one current FG analysis result set. The operational FGDB object may have minimal legacy acquisition metadata. |
| Current Derivation Provenance | PROV `Activity` | Future semantic projection may describe the processing activity that generated the current results. Operationally this is a one-to-one current provenance record, not another persistent domain hierarchy or retained history of bad outputs. |
| Source Dataset Reference | DCAT `Dataset`; PROV `Entity` | Optional metadata-only reference when a source can be identified. Missing or discarded point clouds and intermediates are recorded as unknown/not retained rather than represented by invented dataset instances. |
| Derived Dataset | DCAT `Dataset`; PROV `Entity` | Current retained product associated with one Survey Event and its current derivation provenance; distinguish dataset identity from its individual features and GIS representation. |
| Cutline | GeoSPARQL `Feature`; PROV `Entity` | Local terrain-correction assumption record. No direct HY match; link its geometry, method, parameters, input, output, and derivation activity. |
| Hydro-modified DEM | DCAT `Dataset`; PROV `Entity` | Derived raster dataset. Its mosaic footprint is a geometry of its coverage/domain, not the raster itself. Coverage vocabulary evaluation remains open. |
| Synthetic stream network | HY `HY_ChannelNetwork` | Strong candidate: a terrain-derived network of potential channels through which water may or may not flow. Do not classify it as a hydrographic network by default. |
| Flowline | HY `HY_Flowpath` | Strong candidate if the FG line represents the path water follows through the reach. Orientation and derivation rules remain local constraints. |
| Flowline station/point | HY `HY_IndirectPosition` and/or `HY_HydroLocation` | Candidate for a position referenced along a particular FGDB Flowline. The mapping does not adopt an external linear reference system; distinguish the local measure and reference Flowline from a materialized point geometry. |
| Cross Section | HY `HY_CrossSection` | Strong conceptual alignment; FG sampling, orientation, stationing, and attribution are narrower local constraints. |
| Cross-section point | HY `HY_HydroLocation` | Candidate spatial realization associated with a cross section and sampled elevation observation. |
| Relative Elevation Model | DCAT `Dataset`; PROV `Entity` | Specialized local derived raster with no identified direct HY class. Define its reference surface and derivation explicitly. |
| Bankfull, bankline, valley, riffle, and later L2/L3 features | GeoSPARQL `Feature` plus local classes | Defer precise alignment until each feature-catalog entry has an accepted scientific definition and identity rule. |

The channel/water-body distinction is foundational. A dry channel landform can
persist while the water occupying it changes. FG terms should not collapse
these continuants merely because legacy feature-class names did so.

HY river-referencing concepts are interoperability patterns, not a requirement
to adopt a national route. FGDB Stream and Reach extent remains project-defined
by stored FGDB geometry. Any local indirect position must identify its exact
Flowline reference, origin, direction, units, method, and temporal or
representation scope.

## Bridge to the physical GIS model

| Semantic construct | Proposed physical realization |
|---|---|
| Class instance | Row or feature identified by immutable UUID/GUID |
| Instance IRI | Deterministic projection of the immutable ID under the governed namespace |
| Object relationship | Typed foreign key plus geodatabase relationship class where client behavior requires it |
| GeoSPARQL feature geometry | SDE feature-class `Shape`, exposed by a documented serialization and CRS |
| Optional geometry | Nullable relationship to a geometry-bearing realization, not a nullable entity identity |
| SKOS concept scheme | Governed reference table and/or coded-value domain with stable concept identifiers |
| PROV entity/activity/agent | One-to-one current derivation provenance linked to its Survey Event and results; optional operational load log remains outside the domain hierarchy |
| Raster dataset | Mosaic item plus governed metadata, footprint, and provenance |
| External identifier | Qualified identifier/link table with authority, version, evidence, and match status |

The eventual mapping manifest must name exact classes, columns, transforms,
null behavior, cardinalities, and identifier templates. A future RML/R2RML
projection must follow `usace-ukg-ontologies` conventions; SDE-specific
geometry extraction may need a documented preprocessing view or an additional
mapping component.

## USACE ontology-framework alignment

The workspace repository `usace-ukg-ontologies` is the authoritative semantic
publication framework. The inspected version is 1.7.0 and establishes:

- `https://usace-data.com/ontology/` namespaces for domain ontologies;
- `https://usace-data.com/taxonomy/` and `/codelist/` for governed concepts;
- `https://usace-data.com/data/usace-kg/{domain}#{identifier}` as the current
  instance-URI pattern;
- `https://usace-data.com/graph/{domain}/{name}` named graphs;
- OWL/SKOS metadata, semantic versioning, manifest registration, and a gated
  candidate-review pipeline; and
- RML mappings and GeoSPARQL among its existing implementation patterns.

These patterns are evidence, not authorization to mint an FG namespace.
FluvialGeomorph terms remain local design identifiers until a domain expert
sponsors a candidate and the USACE maintainers approve its namespace and
placement. Full OWL, SHACL, and RML artifacts are deferred under
`dev/ontology/ontology-guidance.md`.

## Geoconnex external-reference contract

Geoconnex is the standard discovery interface for external hydrologic
reference features. New R integration uses `hydrogeofetch`:

- `discover_geoconnex_reference()` discovers available collections and their
  attributes;
- `get_geoconnex_reference()` retrieves candidates by AOI, feature type, or
  identifier; and
- collection IDs and returned schemas are treated as externally versioned
  interfaces rather than hard-coded ontology classes.

Each reviewed link should retain `external_reference_id`, canonical URI,
Geoconnex collection/type, returned label, retrieval timestamp, match method,
match status, analyst/reviewer, and optional service/client version. The
relation may be `candidate`, `related`, `broader`, `narrower`, or `exact` only
after review. Spatial intersection or label similarity never establishes
identity by itself.

## Competency questions for the first workshop

1. Can the graph distinguish a named stream, its channel landform, water that
   occupies it, and the synthetic network used to delineate it?
2. What makes a Reach the same entity across survey events when its derived
   geometry changes or its analyst-defined segmentation is revised?
3. Can a query retrieve all current Flowlines, Cross Sections, terrain
   assumptions, known source references, methods, parameters, and software
   versions for one reach-survey-event?
4. Can it compare survey events without mistaking changed derivation software
   for physical geomorphic change?
5. Can it explain which source and transformation produced every hydro DEM and
   REM mosaic item?
6. Can it traverse from an FG Stream to reviewed national hydrography and
   Geoconnex reference identifiers without asserting false identity?
7. Can the graph distinguish the Survey Event's acquisition meaning from the
   current derivation activity without requiring a one-to-many processing-run
   hierarchy or fabricating missing legacy source metadata?
8. Can both desktop replacement and Shiny in-place editing be represented
   without exposing known-bad superseded feature content as current truth?

## Conformance ladder

1. **Lexical**: definitions, labels, aliases, and source citations exist.
2. **Conceptual**: reviewed external alignment and local identity criteria
   exist.
3. **Graph (future)**: USACE-approved OWL/SKOS resources and SHACL constraints
   validate examples when semantic projection is scheduled.
4. **Physical**: every semantic requirement maps to enforceable or tested GIS
   storage behavior.
5. **Instance**: representative legacy, desktop, and Shiny records project to
   the expected graph with traceable provenance.

## Standards and prior-art register

All links were checked on 2026-08-28. Adoption of a standard does not imply
that every class in it applies to FGDB.

| Resource | Version/status used | Proposed role |
|---|---|---|
| Workspace `usace-ukg-ontologies` | Repository version 1.7.0 inspected 2026-08-28 | Authoritative USACE namespace, ontology promotion, versioning, named-graph, validation, and mapping framework |
| [OGC WaterML 2 Part 3: HY_Features](https://docs.ogc.org/is/14-111r6/14-111r6.html) | 1.0, OGC 14-111r6 | Primary surface-hydrology conceptual alignment and conformance target |
| [OGC GeoSPARQL](https://www.ogc.org/standards/geosparql/) | 1.1 | Feature, geometry, serialization, CRS, and spatial-query semantics |
| [OWL 2 Overview](https://www.w3.org/TR/owl2-overview/) | W3C Recommendation, second edition | Ontology language |
| [SKOS Reference](https://www.w3.org/TR/skos-reference/) | W3C Recommendation | Controlled concepts, labels, definitions, and mapping relations |
| [PROV-O](https://www.w3.org/TR/prov-o/) | W3C Recommendation | Derivation, load, replacement, software, and agent provenance |
| [SOSA/SSN 2023](https://www.w3.org/TR/vocab-ssn-2023/) | W3C Recommendation | Candidate observation and observation-collection semantics |
| [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) | W3C Recommendation | Dataset, series, distribution, and service discovery |
| [SHACL](https://www.w3.org/TR/shacl/) | W3C Recommendation (SHACL 1.0) | RDF instance validation; do not depend initially on draft SHACL 1.2 |
| [R2RML](https://www.w3.org/TR/r2rml/) | W3C Recommendation | Candidate relational-to-RDF mapping serialization |
| [Geoconnex reference features](https://docs.geoconnex.us/access/reference/) and [ontology repository](https://github.com/internetofwater/ontologies.geoconnex.us) | Standard external interface; collection/schema evidence pinned per integration release | Persistent reference-feature discovery and linked-data integration |
| [`hydrogeofetch`](https://CRAN.R-project.org/package=hydrogeofetch) | 2.0.1 reviewed 2026-08-28 | Supported R client for Geoconnex discovery/retrieval and retained NLDI processing calls |
| [USGS Surface Water ontology design pattern](https://www.usgs.gov/publications/ontology-design-pattern-surface-water-features) | 2014 publication; related USGS project marked completed | Informative prior art for container landforms versus contained water bodies |
| [hydrOntology](https://oeg.fi.upm.es/index.php/es/ontologies/107-hydrontology/index.html) | UPM/OEG work originating in 2009 | Informative hydrographic terminology and mapping prior art, not a USGS ontology or normative base |

HY_Features 1.0 is older than the general standards profile but remains the
identified OGC conceptual standard for surface-hydrology features. Its own
conformance model explicitly permits OWL/RDF implementation schemas and
schema mappings. External-version monitoring is therefore required; “current”
must be re-evaluated at each FG ontology release rather than assumed forever.
