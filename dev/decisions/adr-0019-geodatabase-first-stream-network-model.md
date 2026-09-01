# ADR-0019: Geodatabase-first Stream Network model

- Status: accepted
- Date: 2026-09-01
- Complements: ADR-0015 through ADR-0018

## Context

FluvialGeomorph is an object-relational GIS system. Analysts work with feature
classes and tables in Study Area, Stream, and Reach–Survey Event
geodatabases. `fluvgeo` operates on data frames and `sf`, which correspond
directly to those geodatabase relations. FGDB loads the approved local
relations into their enterprise SDE counterparts.

Every retained value must be an attribute of a modeled scientific feature,
entity, relationship, review decision, validation result, or load record. The
design does not use a separate generic delivery object as the organizing unit.

## Decision

1. The Study Area/Stream Geodatabase is the local database of record for a
   configured Stream Network and its time-specific realizations.
2. `stream_network` is the governed polyline feature class. Each row represents
   one directed Stream Network segment with stable identity and explicit
   relationships to its configuration, time-specific observation, Stream, and
   optional Reach.
3. Metadata shared by several segments is normalized into related geodatabase
   tables representing named project objects, including Stream Network
   Configuration and Stream Network Observation. It is not stored as an unattached
   variable or generic document.
4. `fluvgeo` functions consume and return data frames or `sf` and write those
   same relations to the local geodatabase. ArcGIS Pro and future QGIS tools
   are client wrappers; Shiny uses the same relations in application-managed
   storage.
5. Every proposed repair, classification, or validation result presented to an
   analyst is a row in a table or feature class. Spatial proposals use a
   feature class so the analyst can inspect both geometry and attributes before
   accepting or rejecting the proposal.
6. Accepted operations and lineage remain related to the affected Stream
   Network Observation and segments. Review decisions are explicit data, not hidden
   client state.
7. The local file-geodatabase schema matches the normalized FGDB schema as
   closely as practical. Differences are limited to storage-engine fields,
   enterprise load/audit/authorization relations, and deliberate local editing
   aids.
8. FGDB loads directly from the analyst-approved geodatabase. It revalidates,
   maps governed identities, stages, and transactionally creates or corrects
   enterprise rows.
9. File geodatabases are the immediate ArcGIS Pro binding. GeoPackage or
   another open relational spatial database may implement the same logical
   relations for Shiny, direct R, and QGIS without changing object meaning.

## Consequences

- Analysts review the same feature classes and tables that are eligible for
  enterprise loading.
- Local and enterprise schemas can be compared relation by relation and field
  by field.
- FGDB remains a lightweight enterprise loader and manager rather than an
  object-conversion layer.
- New scientific attributes must be assigned to an explicit modeled object or
  relationship before they enter the schema.
- Validation and repair tooling must expose reviewable relational outputs and
  persist analyst decisions.

## Binding

`dev/schemas/stream-network-geodatabase-schema.md` defines the proposed
relations and fields. `dev/features/prepare-stream-network.md` assigns function
ownership and specifies how `fluvgeo` creates, reviews, validates, and writes
them.
