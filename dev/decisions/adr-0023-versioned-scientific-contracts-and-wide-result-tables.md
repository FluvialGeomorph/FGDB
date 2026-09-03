# ADR-0023: Versioned scientific contracts and wide result tables

- Status: accepted
- Date: 2026-09-02
- Complements: ADR-0003, ADR-0004, ADR-0015, ADR-0021, and ADR-0022

## Context

FluvialGeomorph results span approximately a decade of `{fluvgeo}` and
`FluvialGeomorph-toolbox` releases. A newly available Survey Event will often
be analyzed with newer software than earlier events in the same Reach. Software
changes can correct defects, add metrics, change scientific methods, alter an
output schema, or merely change implementation without changing scientific
meaning.

FGDB must preserve what method produced each accepted result, determine whether
results are scientifically comparable, and support analyst-approved batch
reanalysis. These requirements do not require dimensions to be converted from
their established wide, typed tables into an entity-attribute-value or long
measurement table. Avoiding a historical rerun is also not a sufficient reason
to change the canonical dimensions representation.

## Decision

1. FGDB separates four independently versioned contracts:
   - software releases and their material components;
   - scientific method contracts;
   - logical output-schema contracts; and
   - platform/storage compatibility profiles governed by ADR-0021 and
     ADR-0022.
2. Feature-specific dimension relations remain canonical, typed, wide tables.
   One row represents the dimension record for one governed feature under one
   accepted dataset edition; named columns represent defined metrics.
3. `dimension_metric_definition` is the in-database catalog of stable metric
   meaning. It records canonical name, definition, datatype, unit, applicable
   dataset/feature type, ontology reference, and lifecycle state.
4. Version-dependent calculation meaning is not overwritten in the metric
   definition. A versioned scientific method contract and its metric bindings
   state how each metric is calculated. Producing software releases separately
   declare and demonstrate which contract they implement.
   A method contract is production metadata for a Dataset Type; it is not a
   real-world hierarchy entity, feature class, or grouping that must contain
   metrics. Geometry-only methods may have no metric bindings.
5. `derived_dataset` identifies the durable semantic slot for one Survey Event,
   dataset type, and role. `derived_dataset_edition` identifies an accepted
   realization of that slot under explicit scientific, schema, software, and
   platform contracts.
6. Exactly one accepted edition per derived-dataset slot is current for normal
   query and publication. A correction or approved reanalysis stages and
   validates a complete candidate before changing that current designation.
7. Raw processing attempts are operational records, not dataset editions. A
   candidate becomes an edition only after analyst review and acceptance.
8. Known-bad feature geometry and scientific attributes are not retained as
   valid queryable history. Their edition metadata may remain with an
   `INVALIDATED` validity status and audit reason after the associated scientific
   rows are removed from production storage.
9. A scientifically valid superseded edition may be retained when a documented
   research, publication, reproducibility, or migration need justifies its
   content retention. It is excluded from current/default service views.
   Edition metadata remains even when its content-retention policy is metadata
   only.
10. New software never mutates accepted data automatically. An analyst invokes
    an update-planning operation, reviews affected dependencies and proposed
    actions, and explicitly initiates correction, backfill, or reanalysis.
11. Batch reruns followed by idempotent replacement are an accepted and often
    preferred update strategy. FGDB does not require historical events to be
    upgraded merely because a newer software release exists.
12. Scientific comparability is declared at the applicable feature or metric
    scope. Co-location in FGDB, matching column names, or successful platform
    conversion does not establish comparability.
13. Legacy results may be accepted with explicitly unresolved method or
    software provenance after their source artifact and schema are validated.
    Unknown values remain null and comparison compatibility remains `UNKNOWN`;
    FGDB does not fabricate historical versions or infer them from load dates.
14. A long observation representation may later be exposed as a derived
    interoperability or knowledge-graph view. Adopting it as canonical physical
    storage requires a separate decision.

## Consequences

- Existing `{fluvgeo}` data-frame and geodatabase conventions remain directly
  recognizable to analysts and ArcGIS clients.
- Typed fields, database constraints, field-based symbology, and ordinary
  feature-layer queries remain straightforward.
- Adding or changing a metric requires deliberate catalog, scientific-contract,
  schema, migration, and test updates rather than an unconstrained new row type.
- FGDB can distinguish a durable dataset slot from the accepted result that
  currently realizes it without treating every execution as scientific data.
- Historical results can remain interpretable even when their scientific rows
  are replaced or unavailable.
- Update tooling must understand scientific dependencies, but analysts retain
  authority over whether and when historical analyses are rerun.

## Binding specification

`dev/schemas/scientific-result-contract.md` defines the relations, fields,
statuses, and update protocol implementing this decision.
