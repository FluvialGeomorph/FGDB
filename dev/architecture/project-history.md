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

Analysts have sometimes used a cross-reach `Site Geodatabase`, now more clearly
called the `Stream Geodatabase`, as an optional local preprocessing workspace.
It holds a Stream-scale DEM and a terrain-derived network while the analyst
edits the network, divides long Streams into Reaches, and optionally clips
terrain into manageable Reach inputs. The governed outputs are then developed
in reach-survey-event geodatabases. This local workspace was a means to produce
those results, not a consistently retained archival product.

Some early ArcPy tools also retained an experimental ability to dissolve or
vectorize by `ReachName` so one run might process several Reaches. As REM and
production workflows matured, the team standardized operationally on one Reach
at a time. The unfinished multi-Reach path remained in production code because
unwinding it offered little benefit relative to refactoring risk; it was
intentionally omitted from later `{fluvgeo}` replacements. FGDB now supplies
the intended scale-up by querying independently derived Reach results through
the Study Area/Stream/Reach/Survey Event hierarchy.

The Stream Geodatabase also supported the project's longitudinal reference
workflow. Analysts chose the downstream-most project point of a Stream as its
mouth, or chose the watershed/network outlet when a Study Area represented
connected Streams. They manually segmented and linearly referenced the network
so each Reach received `km_to_mouth` stationing against that common origin.
This enabled multi-Reach and multi-tributary longitudinal profiles, but
integrity depended on expert manual checks because the tooling did not enforce
origin, topology, continuity, or calibration rules.

The reviewed synthetic Stream Network is durable, time-specific evidence used
to establish topology, segmentation, and stationing. The Study Area/Stream
Geodatabase is its local database of record, and FGDB governs the corresponding
feature classes and tables while excluding the Stream-scale DEM and
construction intermediates. Base-event Flowlines are explicit realizations of
a selected longitudinal reference frame rather than a report-only convention.

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

Its primary scientific goal is to make direct observations and derived
representations of fluvial conditions comparable across space and time so
geomorphic processes can be studied empirically over decades. That requires
method-neutral identities with method-specific provenance: historic manual
field surveys and modern remote-sensing products can coexist, but their
measurement definitions, units/datums, quality, temporal scope, and derivation
methods must remain distinguishable.

Accordingly, FGDB does not claim complete reconstruction of the local
preprocessing chain. Analysts may retain point clouds, Stream Geodatabases, and
intermediates locally when that level of reproducibility is required; FGDB
centralizes governed stream network observations and accepted Reach/Survey
Event results with their provenance.
