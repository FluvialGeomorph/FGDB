# Initial FGDB use cases

## Status

These are accepted design drivers. Detailed schemas, interfaces, permissions,
and acceptance tests remain under design.

## UC-01: Desktop analyst loads a reach survey event

### Actor

An experienced GIS analyst using ArcGIS Pro and the
`FluvialGeomorph-toolbox` desktop workflow.

### Context

Approximately ten years of analyses are held in local file geodatabases. New
LiDAR collections produce additional reach-survey-event geodatabases and
updated reports for repeat customers. The reports are delivered, but customers
do not currently have a convenient way to inspect the underlying derived
geometry.

### Intended workflow

1. The analyst selects a completed reach-survey-event geodatabase.
2. The FGDB loading workflow inventories and validates its required datasets,
   geometry, spatial reference, attributes, identifiers, and provenance.
3. The analyst supplies or confirms its study area, stream, reach, survey
   event, terrain source, and other required metadata.
4. The workflow presents a preflight result before changing FGDB.
5. The workflow loads feature content and registers DEM/REM raster content in
   the applicable mosaic datasets as one controlled operation or recoverable
   set of operations.
6. The workflow verifies committed target records and records a load manifest.
7. Repeating the same approved load does not duplicate records. A changed,
   corrected load atomically replaces all active feature and raster content for
   the affected reach-survey-event.
8. Authorized customers can discover and inspect the published geometry
   through read-only ArcGIS Enterprise services.

### Design requirements

- Support legacy and future file-geodatabase inputs.
- Support repeated survey events for the same reach without overwriting prior
  observations.
- Retain source-to-target lineage and enough evidence to reconcile a load.
- Detect exact repeats, changed inputs, partial loads, and identifier
  collisions.
- Remove known-bad prior feature records when a corrected reach-survey-event is
  accepted; do not expose them as historical observations.
- Separate preflight, commit, verification, and publication outcomes.
- Do not treat report delivery as proof that the database load succeeded.

## UC-02: USACE Shiny user saves and revisits a self-service analysis

### Actor

An authenticated USACE employee using a browser-based FluvialGeomorph Shiny
application. The user need not be an experienced GIS analyst.

### Context

The Shiny applications analyze smaller areas quickly and currently hold drawn
and derived geometry only within application-session state. Users need to save
their work and return in a later session by navigating the map or selecting a
named study area.

### Intended workflow

1. The user draws or selects a small analysis area and completes the supported
   Shiny analysis.
2. The app validates the minimum metadata and geometry required by the FGDB
   contract.
3. The user supplies a display name and any required descriptive metadata.
4. An authenticated, application-mediated FGDB write workflow saves the raw
   user inputs, reproducible provenance, and selected derived outputs.
5. The user receives an unambiguous save result and durable analysis identity.
6. In a later authenticated session, the user finds authorized saved analyses
   by map extent or a name-based selector and restores the supported state.
7. Valid content may be visible immediately under the applicable authorization
   rules.
8. The owner edits the saved analysis in place under its stable identity.
9. Read-only client services do not provide general-purpose feature editing.

### Design requirements

- Persist across Shiny processes, deployments, and browser sessions; do not
  rely on reactive or mutable global state.
- Record creating identity, originating application and version, calculation
  versions, terrain/source-data identity, creation time, and coordinate
  reference information.
- Distinguish raw user-drawn inputs from derived outputs.
- Define ownership, sharing, correction, deletion/retirement, retention, and
  name-collision behavior.
- Preserve stable identity while applying permitted edits in place.

## Shared retrieval behavior

- Users can discover authorized study areas spatially and by human-readable
  name.
- Study-area display names are human-readable and globally unique under a
  tiered naming convention; immutable identifiers remain the relationship and
  API keys.
- Retrieval can distinguish streams, reaches, survey events, revisions, and
  origin workflows.
- Services expose only content and operations authorized for the caller.

## Shared provenance minimum

The exact schema remains to be designed, but both workflows require:

- durable dataset and entity identifiers;
- origin workflow (`desktop` or `shiny`) and originating software version;
- creating actor or accountable process;
- creation and load timestamps;
- source terrain or survey-event identity;
- input/source manifest or equivalent lineage evidence;
- spatial reference;
- calculation or schema version;
- validation and lifecycle status; and
- visibility or access classification.

## Initially excluded

- Direct end-user editing through published Feature Layer services.
- Storage of delivered reports, maps, and general export files in FGDB.
- Treatment of self-service results as expert-reviewed authoritative analysis.
