# FluvialGeomorph project history

- Recorded: 2026-08-27
- Updated: 2026-08-28
- Evidence status: human-provided historical context from Michael Dougherty

## Origin

The FluvialGeomorph tooling began around 2017. Chris Haring was seeking ways to
accelerate fluvial geomorphic analysis, and Michael Dougherty proposed deriving
features from LiDAR using GIS. The team valued the approach and ideas embodied
in the River Bathymetry Toolkit, but that toolkit was no longer being actively
maintained. The team therefore began building and maintaining a flexible,
open-source FluvialGeomorph workflow informed by those ideas.

## Evolution

The project grew through sustained production use. Early ArcGIS/Python tools
automated geospatial steps that were feasible at the time, while trained
analysts performed remaining interpretation and editing manually. R functions
in `{fluvgeo}` supplied fluvial geomorphic calculations and later expanded into
open-source geospatial derivation to support browser-based Shiny applications.

Production experience produced many ideas for streamlining the workflow,
removing avoidable manual steps, changing processing order, and detecting
errors earlier. The need to keep the desktop workflow continuously operational
made a coordinated redesign difficult, so the desktop and browser processing
paths diverged over time. ADR-0004 records the accepted target of completing a
canonical, client-independent `{fluvgeo}` backend before a coordinated desktop
workflow migration.

## Database motivation

Reach-survey-event file geodatabases have been produced independently for many
study areas and repeat customers. A shared database has long been desired for
comprehensive display and analysis, particularly scientific analysis of change
through time. Progress was constrained not by the absence of individual ideas,
but by the volume and interaction of requirements, legacy schemas, scientific
contracts, software behavior, manual workflows, migration cases, and deployment
constraints that one lead developer also had to keep operational.

FGDB addresses that integration problem by externalizing the design into
versioned evidence, explicit decisions, schemas, crosswalks, and workflows. AI
assistance supports inventory, comparison, traceability, contradiction
detection, and drafting; scientific, technical, operational, program, and
documentation judgments remain human responsibilities.

## Terrain and research-data infrastructure gap

The project developed in a period when no national system provided a
high-resolution, multi-time-period terrain collection suitable for the needed
fluvial geomorphic analysis. The team therefore created procedures to process
terrain, derive analysis features, and organize repeated observations through
time. FGDB is intended to make the accepted hydro-modified terrain and derived
geometry centrally discoverable and analyzable rather than leaving each
reach-survey-event isolated in a delivered file geodatabase.

This addresses a broader historical limitation in fluvial geomorphology.
Stream surveys were commonly collected manually, retained in paper field
notebooks or researcher-specific files, represented without consistent digital
standards, and unavailable through a shared clearinghouse. The resulting data
fragmentation constrained reuse, comparison, and long-term change analysis.
FGDB seeks to preserve governed digital representations, consistent identity,
multi-time-period terrain products, and distributable derived geometry while
remaining honest about legacy source metadata and artifacts that were never
retained.
