# ADR-0018: R-first implementation and evidence-based testing

- Status: accepted
- Date: 2026-08-31
- Complements: ADR-0004, ADR-0015, and ADR-0017

## Context

The FluvialGeomorph system already has an R-centered scientific architecture.
`fluvgeo` owns reusable calculations and increasingly owns geospatial feature
derivation; Shiny applications call R directly; and ArcGIS Pro and future QGIS
tools are intended to be client adapters over the same open-source functions.
FGDB therefore needs to participate in that architecture rather than introduce
an independent implementation language for its core contracts.

The project also has a deliberate test-data practice. `fluvgeodata` retains
provenance-documented outputs from `fluvgeo` and the historical
FluvialGeomorph toolbox. Those real outputs include both retained synthetic
networks and legacy Reach geodatabases in which only derived Flowlines survive.
They are the shared evidence base for migration and conformance tests.

## Decision

1. FGDB is an R package. Its package-native implementation, validation, data
   access, and automated tests use R unless a platform boundary demonstrably
   requires another language.
2. FGDB uses `testthat` and normal R-package testing conventions.
3. Shared geospatial test inputs are direct, provenance-documented tool outputs
   stored in `fluvgeodata`. If an additional representative output is needed,
   it is added to that package through its governed data-ingestion process.
4. Tests do not commit manufactured geospatial datasets as substitutes for
   tool output. To test failure handling, a test may copy a real output to a
   temporary location or make a minimal in-memory R transformation, with that
   transformation visible beside the assertion.
5. When a reproducible derived test artifact is genuinely necessary, an R
   script near the owning data or test creates it from documented source data.
6. `fluvgeo` remains the long-term owner of reusable scientific derivation,
   reconstruction, topology, calibration, and scientific-validation
   functions. FGDB calls those validators and owns only additional
   enterprise-state validation, identity reconciliation, enterprise mapping,
   loading, and management.
7. ArcGIS Pro, Shiny, direct R, and future QGIS workflows consume the same R
   data-frame/`sf` and geodatabase relations. ArcPy may remain a thin ArcGIS client bridge,
   but it does not define an independent scientific schema or test oracle.
8. File-geodatabase and GeoPackage support should be exercised from R through
   `sf`/GDAL where the installed drivers provide the required behavior. Any
   unavoidable ArcGIS-specific binding receives a round-trip compatibility
   test against the same R contract.

## Consequences

- Package behavior has one primary implementation and test vocabulary.
- FGDB tests reflect actual historical and current producer behavior, including
  incomplete legacy preservation.
- `fluvgeodata` becomes an explicit development dependency of FGDB as well as
  `fluvgeo`.
- Structural error cases remain easy to test without curating fake datasets:
  each test begins with real evidence and introduces only the invalid condition
  under examination in temporary R state.
- Cross-repository implementation still requires reviewed changes in the
  repository that owns each function or dataset.

## Initial evidence

The initial FGDB tests use retained-network outputs
`AntelopeCreek_2013.gdb`, `testing_data.gdb`, and `y2006_R1.gdb`, plus
Flowline-only outputs `AntelopeCreek_2017.gdb`, `y2010_R1.gdb`, and
`y2016_R1.gdb`, all supplied by `fluvgeodata`.
