# ADR-0016: Isolate Stream Network Observations in local geodatabases

- Status: accepted
- Date: 2026-08-29
- Clarified by: ADR-0019

## Context

Analysts manually review and edit one time-specific `stream_network` feature
class at a time. Mixing observations in the same editable feature class would
make it easy to alter or classify the wrong terrain-time geometry.

## Decision

1. One editable Study Area/Stream Geodatabase contains exactly one active
   `stream_network_observation` row and one `stream_network` feature class for
   that observation.
2. Every segment row carries the same `stream_network_observation_id`.
   `fluvgeo` validation rejects a mixed-observation feature class.
3. A new terrain time is edited in a separate geodatabase. A correction to the
   same intended observation retains its UUID and replaces its complete
   accepted segment set.
4. Geodatabases representing other terrain times reuse the same
   `stream_network_configuration_id` when they implement the same Study
   Area/Stream configuration.
5. Read-only comparison layers may display several observations together, but
   they are not editable sources of record.
6. FGDB may consolidate segments from many configurations and observations in
   one enterprise feature class because stable keys, database constraints,
   controlled writes, and service filters preserve isolation.

## Consequences

- ArcGIS editing follows the established one-network-at-a-time workflow.
- Local validation can enforce observation identity before enterprise loading.
- Cross-time comparisons use explicit configuration/observation IDs rather
  than physical co-location.
- The analyst workflow is: create the observation table row, edit and classify
  `stream_network`, review proposal feature classes/tables, validate, accept,
  and optionally invoke the FGDB geodatabase loader.
