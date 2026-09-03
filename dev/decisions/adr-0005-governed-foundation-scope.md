# ADR-0005: Governed foundation scope and representation

- Status: accepted
- Date: 2026-08-27

## Context

The documented Level 1 workflow begins by locating a Study Area, finding and
preparing elevation data, building a source DEM, and hydrologically modifying
that DEM. Those steps involve many local and external artifacts. Treating all
of them as FGDB objects would make the database prescribe analyst acquisition
and data-wrangling choices that vary with study area, source, and available
clearinghouse tools.

The target database instead needs a clear boundary around the governed objects
that are consolidated, validated, published, and managed through collection
mutation rules. It also needs consistent spatial and temporal representations
for continental-scale display and repeated survey events.

## Decision

- A Study Area is represented by one multipart-capable polygon feature. Its
  identity, globally unique tiered name, Collection parent, and geometry reside
  in that governed object rather than in separate identity and planning-extent
  objects. The polygon is an editable expression of current project scope, not
  an official jurisdictional or scientific boundary.
- The tiered Study Area name has two components: a controlled three-letter
  uppercase USACE district code and a concise descriptive study-area name.
- Study Area has a required controlled extent type: `SMALL_REACH`,
  `LONG_REACH`, or `WATERSHED`.
- Terrain acquisition and preparation are outside the FGDB boundary. FGDB does
  not retain LiDAR searches or point clouds, source terrain, contributing-
  watershed DEMs or drainage-basin products, unmodified high-resolution DEMs,
  or hillshades.
- Cutlines are retained as governed assumption records because they identify
  where the source DEM was inadequate and hydro-modification interpolation was
  applied. The method/version and material parameters used with them are also
  required provenance.
- The enterprise `hydro_dem` mosaic dataset receives the hydro-modified DEM
  produced for each Reach–Survey Event. Each mosaic dataset item belongs to
  exactly one Survey Event and follows its Collection's publication and
  mutation rules.
- Desktop scientific analysis occurs in a relevant local projected horizontal
  CRS and vertical reference. Governed spatial content is transformed to Web
  Mercator (EPSG:3857) for consolidated Enterprise storage and publication.
- The native analysis horizontal CRS/unit and vertical datum/unit are retained
  as required provenance. Approved horizontal and vertical transformations are
  specified per source CRS. EPSG:3857 horizontal reprojection does not by
  itself specify or transform elevation values.
- Hydro DEM item properties conform to the enterprise `hydro_dem` mosaic
  dataset rather than being selected independently for each load.
- Survey Event always stores a known year. Month and day are stored when known;
  day cannot be present without month. A concise `YYYY` or `YYYY-MM` label is
  derived from the known precision. Labels are not identities or globally
  unique, and unknown components are not replaced with invented dates.
- FGDB does not store base-event status. Reports use the latest survey event as
  their default comparison base without changing database meaning.

## Consequences

- FGDB governs durable analysis outputs without standardizing how an analyst
  locates, cleans, or converts source terrain.
- Study Area selection can use one published polygon feature and a controlled
  geographic-extent rubric.
- Study Area geometry may be edited in place as project scope changes, so
  modification actor/time and geometry validation are required.
- Storage and services use one horizontal map reference, while scientific
  calculations remain in appropriate local coordinate systems.
- Loading must validate and record both the native analysis spatial reference
  and the Enterprise representation and must select an approved transformation
  for the source CRS.
- A detailed raster transformation contract is required to prevent unintended
  changes in resolution, alignment, NoData, interpolation, or vertical values.
- Source terrain cannot be recovered from FGDB and exact preprocessing cannot
  be reproduced from database contents alone; that is an intentional scope
  boundary.
- Retained cutlines and hydro-modification parameters explain where and how the
  accepted input surface was altered, without retaining that source surface.
- Historical year-only events remain valid at year precision. Month and day
  can be added only when supported by evidence.
