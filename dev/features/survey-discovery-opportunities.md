# Survey discovery and change-over-time opportunities

## Accepted requirement (2026-09-12)

One primary purpose of FG is scientifically defensible interpretation of fluvial
change across multiple observations. The owner identifies finding lidar surveys
as a historically expensive, specialist-dependent bottleneck. Reduce that cost so
more customers can obtain multi-period analysis and more observations can support
fluvial science. This is a critical roadmap capability, not merely provenance repair.

Enable analysts to review each accessible FGDB Study Area for additional terrain
acquisitions, including older collections newly discovered or published as well as
new surveys. Present actionable opportunities to extend its observation history.
The capability is required. A first offline, single-study fluvgeo summary/report
is implemented under [its bounded input contract](../../../fluvgeo/dev/schemas/survey-opportunity-inputs.md).
The broader live/batch/FGDB design below remains proposed and unimplemented.
The [multi-catalog direction](../architecture/multi-catalog-terrain-provenance.md)
is grounded in a USIEI/3DEP comparison, not an assumption of one complete catalog.

## Analyst outcome

Follow the accepted [deterministic user-tooling boundary](../../../FG-architecture/dev/decisions/adr-0006-deterministic-user-tooling.md).
Discovery and classification must use implemented spatial/temporal rules and
traditional catalog services, not agentic AI analysis. Unresolved dates, identity
or lineage require structured source evidence or an attributed analyst decision.
Developer-assisted source research is not a deployed discovery capability. Future
AI experiments require separate approval; none is included in this feature.

A concise opportunity report should answer:

- What acquired periods are already represented, and which sources are confirmed?
- What additional acquisitions overlap the Study Area, selected Streams or Reaches?
- Would each candidate extend the time series, fill a historical gap, or only
  revise an existing product? Which relationships are still uncertain?
- What is available now, what needs scientific/source review, and what should the
  analyst do next? Where can supporting metadata and data be obtained?

Use an acquisition timeline and footprint map with an expandable evidence record.
Keep existing observations distinct from catalog candidates and planned/unpublished
collections. Show partial reach coverage and source processing limitations without
reintroducing raster rectangle-occupancy or intentional-NoData quality scores.
Customer-facing summaries explain the potential value without promising that an
additional collection will reveal measurable change.

## Discovery and review requirements

1. Search spatially across acquisition time, not only publication dates or years
   later than the most recent event. Missing dates require review, not exclusion
   disguised as no opportunity. Use project/collection/work-unit relationships to
   avoid counting several tiles or work units from one acquisition as new surveys.
2. Distinguish newly acquired observations, newly cataloged historical observations,
   revised/reprocessed products of an existing acquisition, already represented
   sources, and unresolved candidates. These are proposed report concepts, not
   approved physical enums. Cross-provider duplicates need evidence-backed links.
3. Begin with WESM/3DEP discovery and retain a provider-neutral boundary. USGS is
   not verified as a complete clearinghouse for USACE GRiD, state, local or other
   collections. Accept analyst-supplied catalog evidence and future authorized
   adapters; no new credentialed integration is authorized here.
4. Preserve catalog snapshot/retrieval date, source identifiers, acquisition interval,
   footprint, metadata links, source reference/units, product type, status and
   known processing/quality information. Store the basis for each candidate and
   analyst disposition separately from accepted scientific lineage.
5. Support on-demand review of one Study Area and eventual repeat/batch review
   across authorized FGDB studies. Compare with prior discovery evidence to avoid
   repeatedly presenting dismissed or unchanged candidates. Record failed/partial
   searches and stale snapshots; no results is not proof that no survey exists.
6. Keep local/offline snapshot review possible. FGDB supplies authorized study and
   existing-event context; shared fluvgeo logic performs candidate assessment and
   reporting. QGIS/Shiny are clients, not separate discovery/science engines.
7. Discovery never automatically creates Survey Events, overwrites source assertions,
   downloads large terrain payloads, reprocesses data, loads FGDB or contacts customers.
   Recurrence, notifications and deployment require a separately configured workflow;
   none is scheduled by this roadmap decision.

## Scientific acceptance boundary

Availability is not comparability. Before using a candidate for change analysis,
review native vertical/horizontal references and transformations, spatial support,
resolution, acquisition conditions, uncertainty and terrain-conditioning methods.
Reprocessing differences must not be interpreted as geomorphic change. A catalog
match alone does not prove that existing FG outputs used that acquisition.
Follow the [scientific traceability roadmap](../goals/scientific-traceability-roadmap.md)
and existing edition/method contracts; do not add a new scientific hierarchy.

## First implementation slice and completion evidence

First build a read-only, single-Study-Area opportunity report from a saved catalog
snapshot and explicit existing-event/source inventory. Use a bounded online adapter
only after qualifying its pagination, date/ID encoding, geometry and failure behavior.
Do not require enterprise connectivity to test shared logic.

Qualify controlled cases for: a genuinely later survey; a newly found older survey;
a reissued product with no new acquisition; duplicate work units/providers; partial
coverage; missing dates; invalid footprints; dismissed/unchanged candidates; and
service failure. Synthetic cases must be labeled. Retained Cole Creek evidence
grounds the design but does not by itself establish every case or a new opportunity.
Then qualify authorized FGDB context access and batch/incremental review separately.

## Grounding evidence

The [Papio investigation](../architecture/wesm-archive-source-discovery.md) found
that a matching regional name/year and a broad project report do not establish
work-unit overlap. The live spatial search returned a 2016/2017 acquisition candidate,
not a proven new time period beyond the retained 2016 event. These findings motivate
explicit spatial and temporal classification rather than a list of download links.
