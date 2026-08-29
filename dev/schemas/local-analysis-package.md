# Local analysis package and platform bindings

- Status: draft logical contract
- Updated: 2026-08-29
- Governing decision: ADR-0015

## Design answer

The historical Stream Geodatabase is a good ArcGIS desktop location for
network-scope scientific metadata. It is already the workspace where analysts
derive and edit the synthetic network, classify Streams and Reaches, establish
topology, choose a mouth, and develop common stationing.

The `.gdb` format is not the canonical cross-platform contract. It is one
physical binding of a platform-neutral **local analysis package** defined by
`fluvgeo` scientific data contracts and the FGDB exchange profile.

## Local ownership by analytical scale

| Local workspace | Scientific content authored there |
|---|---|
| Network workspace (historical Stream Geodatabase) | Network Scope metadata; time-specific Network Observations; segment geometry and topology; Stream/Reach classifications; mouth; reusable paths; longitudinal frame definitions; package manifest. |
| Reach–Survey Event workspace | Hydro DEM, Cutlines, Flowline and points, Cross Sections and later derived features; event-specific calibration results and provenance; package manifest entries. |

Stable UUIDs relate records across workspaces. Filesystem paths, geodatabase
`OBJECTID`s, and feature-class names are locators or aliases, not relationship
keys. The package/export operation inventories the referenced local workspaces
and produces a self-consistent submission manifest.

For one independently processed Stream, the historical term **Stream
Geodatabase** remains accurate. For a connected Study Area network containing
several Streams, the same physical role is more precisely a **Study Area
Network Geodatabase**. Both implement the logical Network Workspace owned by
one Network Scope. Discontinuous Streams use separate Stream Geodatabases and
separate scopes.

## Minimum ArcGIS binding

The first forward-looking Stream/Network Geodatabase binding can remain much
simpler than the enterprise schema:

| Local object | Purpose |
|---|---|
| `stream_network` feature class | Reviewed segment geometry with stable segment, observation, Stream, and optional Reach IDs. |
| `fg_network_observation` table | One row per terrain-time network, including stable ID, date precision, method/version, threshold, provenance, and review state. |
| `fg_network_scope` table | Scope ID, mode, label, Study Area source identity, mouth/reference context, and lifecycle metadata. |
| `fg_network_scope_stream` table | Stable participating Stream identities. |
| `fg_reference_frame` table | Analyst-created frame identity, base-selection metadata, method, and review state. |
| `fg_reference_assignment` table | Reach/path membership and stable references to base Flowlines and event-specific calibration outputs. |
| `fg_package_manifest` table or sidecar | Contract version, included workspaces/datasets, fingerprints, source identities, completeness, and validation outcome. |

Exact table consolidation remains open. For example, a one-scope-per-geodatabase
binding may store scope fields in the manifest rather than requiring a
one-row `fg_network_scope` table. The local format should optimize analyst
workflow and portability; the FGDB loader performs enterprise normalization.

## Platform bindings

| Client | Local-first binding |
|---|---|
| ArcGIS Pro | Stream/Study Area Network file geodatabase plus Reach–Survey Event geodatabases and a package manifest, written by `FluvialGeomorph-toolbox` wrappers around `fluvgeo`. |
| Shiny | User/application-scoped `sf`/tabular objects and durable application workspace or export package produced from the same `fluvgeo` contracts; no FGDB load is required to complete analysis. |
| QGIS | Future QGIS wrappers around `fluvgeo`, with an open local container such as GeoPackage plus the same logical manifest. |
| Direct R | `sf`/data-frame domain objects returned and validated by `fluvgeo`, with package read/write helpers independent of any GUI. |

The bindings may differ physically but must preserve the same stable identity,
scientific meaning, required provenance, controlled values, and validation
behavior. Cross-platform parity concerns scientific contracts, not identical
storage-engine fields or byte representation.

## Function ownership

`fluvgeo` should eventually provide:

- platform-neutral constructors and validators for Network Scope, Network
  Observation, topology, reference frame, and calibration objects;
- open-source replacements for scientific/geospatial ArcPy derivation stages;
- package manifest construction, validation, and platform-neutral
  serialization helpers where appropriate; and
- explicit method/version identifiers and scientific QA results.

Client adapters remain responsible for UI, interactive editing, platform
layer selection, and format-specific I/O:

- `FluvialGeomorph-toolbox` translates ArcGIS Pro parameters and file
  geodatabase features to/from `fluvgeo` contracts;
- Shiny applications translate reactive/user state to/from those contracts;
- a QGIS toolbox translates QGIS layers and user interaction to/from them; and
- FGDB translates a validated exchange package into normalized Enterprise
  rows, mosaics, and services without rerunning the analysis.

## Boundary tests

The architecture passes only if:

1. an analyst can complete and retain the full analysis without FGDB access;
2. the same scientific function and contract can be invoked from ArcGIS Pro,
   Shiny, direct R, and a future QGIS adapter;
3. the local result contains enough metadata to understand and validate it
   before enterprise submission;
4. the FGDB loader can ingest a valid package without deriving topology,
   selecting a base event, or recalibrating a Flowline; and
5. adding FGDB support does not remove or degrade a local analytical
   capability.

## Open questions

1. Exact local table/field schema and whether the manifest is stored inside
   the geodatabase/container, beside it, or both.
2. Offline UUID creation, enterprise identity reconciliation, and conflicts.
3. How a package assembles cross-workspace references without depending on
   mutable paths.
4. Which metadata are mandatory for new packages versus permitted unknown for
   legacy migration.
5. Version negotiation between `fluvgeo`, client adapters, package profiles,
   and FGDB loaders.

