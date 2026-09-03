# Platform compatibility change workflow

## Purpose

Evaluate and adopt changes to R, spatial libraries, storage drivers, database
platforms, ArcGIS software, Feature Services, or creation options without
silently changing scientific data. This workflow implements ADR-0021 and
ADR-0022.

## Triggers

Run this workflow when any of the following changes:

- R, `sf`, GDAL/OGR, PROJ, GEOS, or a raster library;
- OpenFileGDB, GeoPackage, PostgreSQL, PostGIS, SDE, or database configuration;
- ArcGIS Pro, ArcGIS Enterprise, Portal, Feature Service API, or the R-ArcGIS
  package ecosystem;
- a driver open, creation, precision, CRS, transaction, or compatibility option;
- a logical schema, platform binding, boundary transform, or adapter;
- observed behavior under a previously accepted profile.

## Procedure

### 1. Capture the candidate profile

Run capability probes and create a candidate `platform_profile` and
`capability_observation`. Record only non-sensitive version, driver, option,
and capability facts. Do not overwrite an accepted profile.

### 2. Diff against supported profiles

Compare the candidate with the current write profile and applicable read
profiles. Identify changed types, subtypes, field widths, null behavior,
geometry capabilities, CRS handling, constraints, raster behavior, service
capabilities, and material defaults.

### 3. Select affected conformance modules

Use the compatibility registry to select tests by:

- logical type and field binding;
- geometry or raster binding;
- source and destination boundary;
- feature family and scientific validator;
- local, open-integration, mocked-service, or licensed-ArcGIS execution lane.

Do not substitute a broad package pass for missing boundary evidence.

### 4. Execute direct-evidence tests

Use provenance-documented producer outputs governed through `fluvgeodata`.
Copy them to temporary storage when mutation is required. Add explicit
in-memory boundary values beside the relevant assertions when the direct
output does not exercise a type limit or failure condition.

### 5. Classify differences

Classify each difference as:

- no contracted change;
- lossless representation change;
- tolerance-bounded change;
- qualified loss requiring scientific approval;
- adapter or platform defect;
- unsupported capability;
- expected platform-generated difference; or
- unresolved.

Any unresolved or unapproved difference blocks the affected write path.

### 6. Resolve the contract

As applicable:

- update an explicit creation/open option;
- update or add a platform binding;
- implement a new directional transform or adapter version;
- define a field-specific scientific tolerance;
- create a schema or data migration;
- retain the previous write profile;
- restrict the candidate to read-only recovery; or
- mark the candidate unsupported.

Never loosen a scientific invariant merely to make a conversion pass.

### 7. Review and accept

Review the crosswalk diff, conformance results, scientific consequences,
migration behavior, and operational effects. Acceptance creates new immutable
registry versions and supersession links. It does not rewrite prior results.

### 8. Release and observe

Declare the environment's single write profile, publish compatibility and
migration notes, rerun deployment smoke tests, and monitor for drift. Preserve
the prior recovery path until the accepted support window closes.

## Required outputs

- candidate and accepted platform-profile records;
- capability observations;
- crosswalk and compatibility-matrix diff;
- conformance results with direct evidence and execution class;
- adapter or transform changes;
- migration specification and results when applicable;
- scientific and operational approval references;
- release-note entry and supported-profile declaration.

## Failure behavior

- An unknown profile is `unverified` and cannot become the production write
  profile automatically.
- A failed or drifted accepted profile is `blocked` for affected writes.
- A failed conversion does not modify the accepted source.
- A partial output is not published or reported as conformant.
- Read-only recovery is permitted only through an explicit profile that
  documents its limitations.

