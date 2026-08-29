# Import a legacy synthetic stream network

- Status: proposed immediate implementation workflow
- Updated: 2026-08-29
- Governing decision: ADR-0014

## Purpose

Implement the versioned synthetic-network design without requiring analysts to
understand or edit the normalized enterprise tables directly. For surviving
legacy artifacts, a new FGDB migration tool, provisionally named **Register
Legacy Synthetic Network**, accepts one or more reviewed `stream_network`
feature classes and creates or replaces one governed Network Observation.

This is an ingestion/registration tool. It does not replace the existing
network-derivation tool and it does not yet calibrate longitudinal reference
frames.

The legacy migration tool and database-write orchestration live in `FGDB`.
Under ADR-0015, the target workflow is split: an analyst-facing
producer tool in `FluvialGeomorph-toolbox`, backed by `fluvgeo`, documents the
network and writes a local exchange package; a lightweight FGDB tool validates
and loads that package. Existing production derivation remains local during
the transition.

## Minimum physical slice

The first implementation needs four new physical objects in addition to the
existing Study Area, Stream, Reach, and Survey Event hierarchy:

| Physical object | Rows created by one import | Analyst-facing meaning |
|---|---:|---|
| `network_scope` | zero or one | Reuse an existing scope or create the connected Study Area network / independently processed Stream scope. |
| `network_scope_stream` | zero to many | Records which governed Stream IDs participate in that scope. |
| `synthetic_network_observation` | one | Header for this terrain-time network dataset, its source, method, review, and load identity. |
| `stream_network` feature class | one per imported source feature after transformation | Governed segment geometry, each carrying the observation ID, generated segment ID, Stream ID, and optional Reach ID. |

The analyst interacts with one tool dialog; the tool performs these normalized
writes. The following logical objects can be deferred without losing the
initial network geometry:

- `network_observation_reach_event`, populated when Reach Survey Events are
  registered or reconciled;
- `network_segment_correspondence`, added when cross-time change mapping is
  implemented;
- a governed node feature/table if node/edge topology requires it; and
- longitudinal reference-frame, path, base-Flowline, and comparison-calibration
  tables, populated by a later calibration tool.

## Actual legacy input

The current `_04_StreamNetwork.py` workflow uses raster-to-polyline conversion
and adds only a nullable text `ReachName` field. ArcGIS-generated fields such as
`OBJECTID`, `Shape`, `Id`/`gridcode`, and `Shape_Length` may also be present.

The supplied Papillion R1 2016 XML workspace does **not** contain a
`stream_network` feature-class definition. The term appears only in lineage
metadata for the derived Flowline, referring back to a Stream-Geodatabase
source path. This confirms that reach-survey-event geodatabases cannot be
assumed to contain an importable network.

The importer therefore treats:

- `Shape` as source geometry;
- `ReachName` as a mapping hint requiring analyst confirmation;
- source `OBJECTID`, `Id`, `gridcode`, paths, and names as nonpersistent source
  evidence, never enterprise identity; and
- absent threshold, terrain date, derivation version, and CRS-transformation
  metadata as analyst-supplied or explicitly unknown legacy metadata under the
  applicable publication rules.

## Proposed tool parameters

### Context and operation

| Parameter | Behavior |
|---|---|
| Enterprise connection | Authorized FGDB database connection selected by the analyst. |
| Study Area | Existing immutable Study Area selected by name but resolved to ID. |
| Operation | `CREATE_NEW_OBSERVATION` or `REPLACE_CORRECTED_OBSERVATION`. Replacement requires selecting the exact existing observation ID. |
| Input network feature class(es) | One reviewed whole-network feature class, or a batch of nonoverlapping fragments known to form the same observation. |

### Scope

| Parameter | Behavior |
|---|---|
| Network Scope | Select an existing scope or create one. |
| Scope mode | `STUDY_AREA_NETWORK` or `STREAM`; only needed when creating a scope. |
| Participating Streams | One Stream for `STREAM`; one or more connected Streams for `STUDY_AREA_NETWORK`. |

### Observation and provenance

| Parameter | Behavior |
|---|---|
| Observation year/month/day | Required year and optional month/day for the terrain realization represented by the network. |
| Source terrain / Survey Event references | Optional known references; absence remains explicit for legacy material. |
| Derivation method/version | Select current tool/method or `LEGACY_UNKNOWN`. |
| Stream-initiation threshold and units | Required when known; otherwise explicit legacy-unknown status. |
| Analyst/reviewer and review state | Required before authoritative Desktop publication. |
| Notes/source workspace label | Nonidentity migration evidence; source paths should not be required durable identifiers. |

### Classification mapping

The tool presents a mapping grid of distinct source `ReachName` values and/or
input layers to governed IDs:

| Source hint | Required Stream | Optional Reach | Disposition |
|---|---|---|---|
| source layer + `ReachName` value | one Stream ID in the selected scope | one Reach ID belonging to that Stream, or null while unsegmented | import, ignore, or resolve before publication |

For a single-Stream/single-Reach legacy feature class, the analyst can assign
one Stream and Reach to all rows without relying on `ReachName`. For a connected
network, the grid makes the historical manual classification explicit and
validates it against the FGDB hierarchy.

## Import execution

### 1. Inventory and preflight

The tool inventories source feature counts, geometry type, multipart/null/empty
geometry, CRS, distinct `ReachName` values, and source fields. It rejects
non-polyline geometry, missing CRS, invalid hierarchy mappings, or unexpected
overlap among batch fragments. It warns rather than inventing unavailable
legacy provenance.

### 2. Resolve or create the scope

- Connected watershed case: select or create one `STUDY_AREA_NETWORK` scope
  and confirm every participating Stream.
- Discontinuous case: run one import per independently derived Stream, each
  against its `STREAM` scope. Do not append disconnected inputs into a single
  observation merely because they share a Study Area.

Scope creation and Stream memberships normally occur once; later terrain-time
observations reuse the same scope.

### 3. Establish observation identity

For a new valid terrain time, generate one immutable
`network_observation_id`. For a correction, require the analyst to select the
existing observation explicitly. A year, filename, `ReachName`, or geometry
match is never sufficient to choose replacement identity.

The tool calculates a source manifest/fingerprint from the ordered input
inventory, geometry/attribute content, mappings, observation metadata, and
material parameters. An exact accepted repeat is a no-op; changed content
under `CREATE_NEW_OBSERVATION` requires a new ID or explicit correction choice.

### 4. Transform and stage segments

For each source feature, the tool:

1. copies geometry to a staging feature class;
2. applies the approved source-to-Enterprise transformation to EPSG:3857;
3. generates an immutable `network_segment_id`;
4. assigns the one `network_observation_id`;
5. resolves `stream_id` and optional `reach_id` from the reviewed mapping;
6. retains source feature/layer references only as migration evidence; and
7. validates geometry, scope membership, classification, and required
   provenance.

Multipart handling and whether topology edges must be split at every junction
remain physical-contract decisions. The first loader should preserve reviewed
source geometry unless an accepted deterministic edge-splitting rule exists.

### 5. Commit as one governed unit

After all checks pass, the tool writes or reuses scope records, writes the
observation header, and appends all staged segments. Publication state changes
only after committed counts, IDs, geometry, and relationships are verified.

For a correction, stage and validate the complete replacement first, then
replace every active segment belonging to that exact observation ID and update
its current provenance/manifest. Other observation times are untouched. The
database transaction or compensating rollback must prevent a partially
replaced network from becoming queryable.

## Handling existing storage patterns

### Preferred: whole Stream-Geodatabase network

Import the reviewed whole network once. This best preserves branches,
confluences, segmentation context, and the distinction between connected and
independent derivations.

### Only Reach-geodatabase convenience copies survive

Do not automatically create one Network Observation per Reach copy. If the
copies are known to be fragments of the same original terrain-time network,
submit them together as one batch and map each fragment to its Stream/Reach.
The tool must detect or require resolution of duplicated/overlapping segments.
If common origin cannot be established, load them only with an explicit
legacy-evidence status or defer publication; do not fabricate a connected
network.

### No network geometry survives

Load otherwise valid legacy Reach Survey Event results without a Network
Observation association and record `NETWORK_NOT_RETAINED` (or an equivalent
controlled completeness status). Flowline lineage may identify that a network
once existed, but a smoothed Reach Flowline is not substituted for the lost
network. A future network derived from a newly processed terrain is a new
observation, not a reconstruction of the missing historical one.

### Several disconnected Stream networks

Run one observation import for each Stream scope. They share the Study Area
through their scopes and remain independently derived, dated, and versioned.

## Separate longitudinal-calibration step

Registering or loading a network does not by itself define a base event. A
separate analyst-facing **Create Longitudinal Reference Frame** tool in the
producer workflow will:

1. select one Network Scope and, normally, one base Network Observation;
2. select the mouth and participating Reach paths;
3. select one base Survey Event Flowline for every participating Reach;
4. establish the common `distance_to_mouth_km` intervals; and
5. calibrate other Survey Event Flowlines to those base Flowlines.

When an analyst starts the separate calibration tool, its normal preset is to
propose the latest validated Survey Event Flowline for each participating
Reach. The analyst confirms or changes that base and selects which previous
events to calibrate. The tool stores the resolved IDs so the result remains
reproducible after a newer event is added. Stationing remains dependent on the
chosen base Flowline; the frame does not create a geometry-independent
stationing system.

The resulting frame, calibrations, and metadata are first written to the local
workspace and may later be submitted through an FGDB loader. Registering or
loading a newer Network Observation or Survey Event never
launches this calibration tool, recalibrates previous events, or changes the
operational default. Those actions require a separate analyst-initiated,
reviewed, and accepted operation.

This separation keeps the first importer feasible and faithful to existing
file-geodatabase content while preserving the evidence required for the more
rigorous stationing workflow.

## Immediate feasibility conclusion

No change to `_04_StreamNetwork.py` is required to prove the database design.
The first migration deliverable can be an FGDB legacy registration/import tool
operating on surviving output. It will not populate a Network Observation for
every historical Reach geodatabase because many did not retain that geometry.
The target producer workflow should later emit a richer local manifest and
stable source keys, enabling a lighter FGDB loader. Those improvements are not
a prerequisite for loading legacy Reach results with an explicit completeness
status.
