# XML Workspace schema assessment

- Reviewed: 2026-08-27
- Status: working design evidence

## Sources and roles

### FGDB target prototype

[`FluvGeo_DB_ExportXMLWorkspac.xml`](../../FluvGeo_DB_ExportXMLWorkspac.xml)
is a schema-only XML Workspace export from a file-geodatabase mockup. It is a
historical design prototype for the database to which legacy and future
derived content may be migrated. It is not an accepted logical or physical
enterprise schema.

### Papillion production example

[`y2016_R1_ExportXMLWorkspaceD.xml`](../../y2016_R1_ExportXMLWorkspaceD.xml)
is a schema-only XML Workspace export from a wild-caught
`FluvialGeomorph-toolbox` reach-survey-event geodatabase for Papillion Creek,
reach R1, survey event 2016. Human-provided context establishes that it contains
outputs produced after the Level 1, Level 2, and Level 3 workflows. It is a
production example, not a canonical source schema for every legacy project or
toolbox version.

## Verified structural inventory

| Property | Target prototype | Papillion source example |
|---|---:|---:|
| Dataset definitions | 27 | 29 |
| Feature classes | 21, including 3 views | 28 |
| Tables | 5 | 0 |
| Feature datasets | 0 | 1 |
| Relationship classes | 1 attachment relationship | 0 |
| Business domains | 0 | 0 |
| Raster or mosaic definitions | 0 | 0 |
| Spatial reference | EPSG:3857 | EPSG:26914 |
| Embedded records | 0 | 0 |

The exports support structural assessment only. They do not establish record
counts, value distributions, actual nulls, hierarchy assignments, or feature
validity.

## Target prototype observations

### Useful concepts

- Introduces collection, study area, stream, reach, and survey-event objects.
- Gives most derived feature classes a survey-event reference field.
- Separates some identity tables from polygon representations.
- Anticipates client-facing views, survey-event footprints, and raster
  footprints.

### Referential-integrity gaps

- Hierarchy references are nullable strings, commonly length 255, rather than
  typed GUID foreign keys.
- No business relationship classes or explicit hierarchy constraints are
  present.
- Study-area name is nullable and not uniquely indexed.
- Survey-event reference fields are not consistently named or indexed.
- Collection/source labels and hierarchy names are redundantly copied into
  some derived feature classes even though they can be inherited by joins.

The prototype therefore describes hierarchy intent without enforcing the
mandatory hierarchy in `conceptual-data-model.md`.

### Spatial and service gaps

- All target geometries use Web Mercator (EPSG:3857), while the production
  example uses NAD83 / UTM zone 14N (EPSG:26914). The authoritative storage,
  transformation, horizontal/vertical datum, unit, Z, and M policies are not
  designed.
- The three exported views have no ObjectID.
- `FG_Flowline_Points_VW` is a polygon view using the same
  `AMD_DEM_hydro_CAT` geometry as `FG_DEM_Footprint_VW`, which appears
  inconsistent with its name and intended feature family.
- The referenced `AMD_DEM_hydro_CAT` object is absent from the export.
- No DEM or REM mosaic-dataset definition is present.

### Derived-schema gaps

- `FG_Flowline_Points` omits the source point attributes `ReachName`,
  `POINT_X`, `POINT_Y`, `POINT_M`, and `Z`.
- Level 1 and Level 2 dimension targets have identical wide schemas even though
  their production sources differ.
- Several added `_gte_*` fields have unresolved scientific meaning and are
  typed as doubles.
- Process fields such as OID/FID variants appear in source or target schemas
  without durable semantic identity.
- Geometry Z/M capabilities differ materially between source and target
  feature families.

## Initial dataset disposition

### Direct or near-direct candidates

| Source | Candidate target | Required design work |
|---|---|---|
| `bankfull_area` | `FG_BankfullArea` | Survey-event key and Z policy |
| `banklines` | `FG_Banklines` | Measure preservation and Z/M policy |
| `features` | `FG_Features` | Survey-event key and naming cleanup |
| `flowline` | `FG_Flowline` | Canonical flowline contract and provenance |
| `loop_points` | `FG_Loop_Points` | M policy and survey-event key |
| `valleyline` | `FG_Valleyline` | Smoothing provenance and Z/M policy |
| `xs_50` | `FG_Cross_Sections` | Loop/bend disposition and canonical naming |
| `xs_50_points` | `FG_CrossSection_Points` | Channel/floodplain classification disposition |
| `xs_50_dims_L1` | `FG_CrossSection_Dim_L1` | Exact L1 contract |
| `xs_50_dims_L2` | `FG_CrossSection_Dim_L2` | Exact L2 contract |

### Ambiguous consolidations

- Channel and floodplain riffle cross sections both appear to map to
  `FG_Riffle_CrossSection`, but the target lacks a clear discriminator.
- General, channel-riffle, and floodplain-riffle point datasets may converge on
  `FG_CrossSection_Points`, but provenance and feature subtype are unresolved.
- `flowline_points` has a named target whose current fields do not preserve the
  production source contract.

### No clear target in the prototype

- `stream_network` is now intentionally excluded as a Stream Geodatabase
  preprocessing artifact under ADR-0010; its lack of an `FG_StreamNetwork`
  target is consistent with the accepted scope.
- `bankline_points`
- `flood_prone`
- `gradient_100`
- Level 3 cross-section dimension lines and points
- Level 2 and Level 3 riffle dimension lines and points
- channel and floodplain polygon buffers

Each must be classified as migrate, transform, consolidate, recompute, retain
outside FGDB, or discard as a temporary/intermediate artifact. L1, L2, and L3
coverage must remain explicit; absence from the prototype is not evidence that
a mature workflow output is unnecessary.

## Migration implications

- The source does not encode its complete collection-study-stream-reach-event
  chain. Legacy loading requires an operator-reviewed manifest that binds the
  geodatabase to pre-registered immutable hierarchy IDs.
- Every authoritative feature and mosaic item needs one consistent, non-null,
  indexed survey-event ownership key.
- Corrected desktop loads require complete staging, validation, logical atomic
  replacement, verification, and a load manifest.
- Legacy and future records need application, derivation method, `{fluvgeo}`,
  schema, and material-parameter provenance so processing differences are not
  interpreted as geomorphic change.
- A loader must not map a pre-segmentation `stream_network`, Stream-scale DEM,
  or associated drainage intermediate into FGDB. If a legacy reach
  geodatabase contains a convenience copy, it remains excluded unless used as
  evidence to transform and validate a separately governed downstream feature.

## Next specification work

1. Create a complete L1/L2/L3 dataset-disposition matrix.
2. Define the canonical hierarchy tables, GUID types, constraints, and naming
   rules independently from the file-geodatabase prototype.
3. Define geometry, CRS, datum, unit, Z, and M policy by feature family.
4. Specify canonical feature contracts jointly with the `{fluvgeo}` workflow
   inventory and modernization plan.
5. Obtain separate XML exports or authoritative evidence for DEM and REM mosaic
   datasets and their source-file lifecycle.
6. Design service-ready views only after base identities and relationships are
   stable.
