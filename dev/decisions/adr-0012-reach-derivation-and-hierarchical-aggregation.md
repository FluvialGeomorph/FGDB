# ADR-0012: Reach-scoped derivation and hierarchical aggregation

- Status: accepted
- Date: 2026-08-29

## Context

Early ArcPy tools retained an experimental ability to process several Reaches
by dissolving or vectorizing on `ReachName`. Production experience showed that
the scientific and practical assumptions of the Relative Elevation Model
workflow are most reliably applied to one Reach at a time. Multi-Reach tool
execution was never developed into a production workflow and remained in code
because removing it safely would have disrupted the operational toolchain.

The streamlined `{fluvgeo}` replacements intentionally accept one Reach-scale
input. FGDB, rather than a derivation tool, must provide the missing scale-up
capability: separately derived Reach/Survey Event results must be queryable and
composable at Stream and Study Area scales. A Stream longitudinal profile, for
example, may use Flowlines and profile points from several independently
processed Reaches.

The scientific purpose extends beyond displaying current LiDAR products. FGDB
must preserve comparable, provenance-rich representations of fluvial
conditions across multiple spatial scales, observation methods, and decades.

## Decision

1. The normative desktop derivation and replacement unit is one Reach and one
   Survey Event. Multi-Reach vectorization in legacy ArcPy tools is non-normative
   compatibility residue and is not a parity requirement for `{fluvgeo}`.
2. Every retained derived feature or dataset has one direct Survey Event owner
   and therefore one Reach, Stream, Study Area, and Collection through explicit
   foreign keys. Content is not duplicated merely to create Stream- or Study
   Area-level ownership.
3. FGDB queries, views, and services provide spatial scale-up by traversing the
   hierarchy. They must support selection at Study Area, Stream, Reach, and
   Survey Event scopes while preserving each result's direct owner and
   provenance.
4. One populated Reach/Survey Event has at most one current Flowline. The
   combined Flowline or longitudinal profile for a Stream is a query-derived
   composition of Reach-owned results, not a second authoritative copy.
5. Stream-scale composition requires an explicit project-defined ordering and
   station-alignment contract. It must identify direction/origin, units,
   Reach ordering or topology, offsets/alignment method, reference Flowlines,
   and applicable Survey Events. Hierarchy membership alone does not establish
   longitudinal order.
6. Temporal aggregation must use an explicit Survey Event selection rule.
   Equal year/date labels do not by themselves prove that different Reaches
   are synchronous or derived from the same source acquisition.
7. FGDB is observation-method neutral at the kernel level. Historic manual
   field surveys and modern remote-sensing derivations may coexist when their
   measurement definitions, units/datums, spatial/temporal scope, method,
   software where applicable, quality, and provenance are explicit.
8. Scientific comparisons must retain enough contract and provenance metadata
   to distinguish geomorphic change from differences in measurement,
   derivation method, resolution, datum, or software version.

## Consequences

- Removing legacy multi-Reach behavior from a future coordinated toolbox
  refactor does not remove a required capability.
- Hierarchy keys and query indexes are core scientific infrastructure, not
  administrative metadata.
- Stream and Study Area services can expose composed result sets without
  weakening Survey Event ownership or duplicating authoritative geometry.
- A governed Stream-scale stationing/alignment design is now required before a
  multi-Reach longitudinal-profile service can be considered reproducible.
- Existing `km_to_mouth` values are useful legacy evidence, but their manual
  input and divergent implementation do not yet constitute that governed
  contract.
- Cross-method and cross-time comparisons require explicit fitness and
  compatibility rules; co-location in FGDB does not imply comparability.

## Evidence

- Human-provided development and scientific context from Michael Dougherty,
  2026-08-29.
- `FluvialGeomorph-toolbox/tools/_05a_Flowline.py`.
- `FluvialGeomorph-toolbox/tools/_06_FlowlinePoints.py`.
- `fluvgeo/R/flowline.R` and `fluvgeo/R/flowline_points.R`.
- `FG-Tech-Manual/data_dictionary.csv`.
- ADR-0003: collection governance and mutation.
- ADR-0004: canonical feature derivation.
- ADR-0009: project-defined Stream/Reach extent and referencing.

