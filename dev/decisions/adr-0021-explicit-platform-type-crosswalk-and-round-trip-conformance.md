# ADR-0021: Explicit platform type crosswalk and round-trip conformance

- Status: accepted
- Date: 2026-09-02
- Complements: ADR-0018, ADR-0019, and ADR-0020

## Context

FluvialGeomorph data repeatedly crosses R, `sf`, GDAL/OGR, Esri file
geodatabases, OGC GeoPackage, ArcGIS Feature Services, PostgreSQL/PostGIS, and
Esri SDE. Project experience has shown that a dataset may remain readable while
field values, nulls, dates, identifiers, numeric precision, field widths,
geometry dimensionality, coordinate precision, or constraints change in ways
that can alter scientific results.

File geodatabase does not provide the project with an open normative storage
specification and vendor-supported open-source implementation that can serve as
the interoperability oracle. GDAL OpenFileGDB provides essential open-source
access, including vector write support, but its behavior is versioned and some
physical choices depend on creation options. GeoPackage is an open OGC standard,
but its SQLite encodings are not identical to R, file geodatabase, Feature
Service, PostgreSQL, or SDE types. A successful conversion is therefore not
evidence of semantic or scientific fidelity.

FGDB also uses an Esri **mosaic dataset** for enterprise raster management. A
mosaic dataset is a proprietary geodatabase dataset type that catalogs and
manages a collection of raster items, properties, functions, footprints, and
serving behavior. It is not the traditional noun *mosaic* for a combined raster
image, nor the verb *mosaic* for combining raster datasets.

## Decision

1. FGDB shall maintain a versioned, machine-readable platform type crosswalk as
   part of each physical schema contract.
2. Every governed field shall have one canonical logical type and explicit
   bindings for each supported platform. A platform's inferred type is evidence
   to compare with the contract, not the definition of the field.
3. Crosswalks shall cover R representation, GDAL/OGR type and subtype, Esri file
   geodatabase, GeoPackage, ArcGIS Feature Service/Esri JSON, PostgreSQL/PostGIS,
   and enterprise SDE wherever that relation crosses those boundaries.
4. Geometry crosswalks shall separately record geometry family, simple versus
   multipart rules, XY/Z/M dimensionality, empty and null behavior, CRS
   representation, axis order, coordinate resolution, tolerance, and required
   transformations.
5. Raster crosswalks shall separately record pixel type, NoData and NaN
   semantics, band count and order, dimensions, resolution, alignment, extent,
   horizontal and vertical reference metadata, units, compression, and the
   mapping from an accepted raster artifact to an enterprise mosaic dataset
   item.
6. Constraint crosswalks shall record primary and foreign keys, uniqueness,
   nullability, defaults, domains, range or coded constraints, indexes,
   relationship behavior, and whether each platform enforces, emulates, or only
   documents the rule.
7. Storage adapters shall use explicit driver, layer, field, and creation
   options wherever implicit inference could change a contracted type or
   property. Silent coercion, truncation, precision loss, identifier mutation,
   dimensionality loss, or constraint loss is a validation failure.
8. A known lossy mapping is prohibited for governed scientific data unless an
   accepted field-specific transform documents why the loss is scientifically
   immaterial, defines its tolerance or recovery rule, and records approval.
9. Conformance shall be established through value-bearing round-trip tests, not
   schema inspection alone. Boundary cases shall include nulls, extrema,
   precision-sensitive values, Unicode, maximum accepted text length, dates and
   times, stable identifiers, multipart geometry, Z/M coordinates where
   applicable, empty geometry where allowed, and CRS transformations.
10. The test framework shall exercise each supported direct boundary and the
    operational multi-platform path. At minimum this includes R/`sf` to local
    storage and back, file geodatabase to GeoPackage and back where supported,
    and accepted local relations through Feature Services to SDE and back in the
    licensed integration environment.
11. Conformance comparisons shall test scientific invariants and declared
    tolerances in addition to exact values. Byte identity and platform-generated
    fields such as object IDs are not required unless the field contract says
    otherwise.
12. Every conformance result shall record logical schema version, crosswalk
    version, source and destination platforms, library and driver versions,
    creation options, test-data provenance, transformation path, and result.
13. Platform-generated identifiers, field-name case changes, and storage-engine
    metadata shall never be mistaken for governed scientific identity.
14. The exact term **mosaic dataset** shall be used for the Esri enterprise
    raster-management data type. Documentation shall use *raster mosaic* or
    *mosaicking* only when it actually means a combined image or the operation
    of combining rasters.
15. GDAL, GeoPackage, and local PostgreSQL/PostGIS conformance form part of the
    normal open-source development loop. SDE, Feature Service, and mosaic
    dataset conformance remain part of the licensed enterprise integration
    lane.

## Consequences

- Every schema feature slice must resolve its type mappings before its storage
  adapter or enterprise loader is complete.
- File geodatabase and GeoPackage remain supported bindings only to the extent
  demonstrated by the crosswalk and conformance tests; neither receives an
  assumption of lossless equivalence.
- The earlier difficulty adopting GeoPackage becomes explicit compatibility
  evidence and test work rather than an indefinite rejection of the open
  format.
- Driver and platform upgrades require rerunning affected boundary tests and
  reviewing crosswalk drift before release.
- Type conversion failures are treated as scientific data-integrity failures,
  even when all software calls return success.
- Licensed ArcGIS tests remain necessary because open-source round trips cannot
  prove SDE, Feature Service, or mosaic dataset behavior.

## Binding specification

`dev/schemas/platform-type-crosswalk.md` defines the required crosswalk
relations, validation classes, and conformance evidence.

