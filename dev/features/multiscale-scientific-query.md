# Multiscale scientific query capability

- Status: draft feature specification
- Updated: 2026-08-29

## Scientific outcome

FGDB must make independently produced measurements and derived representations
of fluvial conditions directly discoverable and comparable across Study Area,
Stream, Reach, and Survey Event scopes. This is the database capability that
replaces the abandoned idea of processing many Reaches in one toolbox run.

The long-term objective is empirical analysis of geomorphic process across
multiple observation times and decades. The model must accommodate historic
manual field surveys as well as modern terrain and point-cloud methods without
pretending that different methods are automatically equivalent.

## Query invariant

Every Reach-derived feature retains one direct Survey Event owner and the
complete hierarchy path:

```text
Collection -> Study Area -> Stream -> Reach -> Survey Event -> Feature/Dataset
```

A broader-scope query selects descendants; it does not reassign ownership or
create duplicate authoritative rows.

Synthetic-network segments follow a parallel governed path because one
terrain-time network may span several Reaches:

```text
Collection -> Study Area -> Network Scope -> Network Observation -> Segment
                                      |-> Stream/Reach classifications
                                      `-> associated Reach Survey Events
```

A query must return the Network Observation identity and may not collapse
segments from different terrain times into one apparently timeless network.

| Requested scope | Required selection behavior |
|---|---|
| Study Area | Select governed descendants across one or more Streams, Reaches, and explicitly selected Survey Events. |
| Stream | Select governed descendants across all or selected Reaches and explicitly selected Survey Events. |
| Reach | Select one or more Survey Events and their governed feature families. |
| Survey Event | Select the current accepted result set and provenance for one direct observation/derivation unit. |

## Required query dimensions

Queries and service views must be able to constrain or return:

- immutable Collection, Study Area, Stream, Reach, Survey Event, dataset, and
  feature identities;
- observation date components and precision;
- feature/dataset type and semantic role;
- observation/source method, derivation method, software and contract version;
- native and Enterprise CRS, horizontal/vertical datum, and units;
- validation, authority, publication, and metadata-completeness status; and
- source/load manifest or provenance reference.

Human-readable names and date labels support selection and display but are not
join keys.

## Stream longitudinal-profile use case

A request for one Stream longitudinal profile may combine profile observations
from several Reach-owned Flowlines. A reproducible composition must declare:

1. the Stream and included Reaches;
2. the downstream-to-upstream Reach order or network path;
3. one selected Survey Event for each Reach;
4. the Flowline representation used by each selected Survey Event;
5. project longitudinal reference frame/version, its explicitly selected base
   Flowline for each Reach assignment, and comparison-Flowline calibrations;
6. handling of gaps, overlaps, branches, or unavailable Reaches;
7. elevation datum/unit compatibility and any transformations; and
8. observation/derivation compatibility and warnings.

The profile is a query result or reproducible analysis product. It is not a
replacement for the authoritative Reach-owned Flowlines.

The governed project longitudinal reference frame supplies the common x-axis.
It uses either the downstream-most point of one Stream or the mouth/outlet of a
connected Study Area/watershed network as zero, with
`distance_to_mouth_km` increasing upstream. The frame is realized by one
explicit base Flowline per participating Reach assignment; comparison-event
Flowlines are calibrated to those base realizations. Base status is therefore
relative to the frame, not a global Survey Event flag, and alternative valid
base choices may coexist as distinct frames.

Existing desktop `km_to_mouth` values are migration evidence. They become
canonical only when bound to a reconstructed reference frame and validated;
otherwise they remain unverified. See ADR-0013, ADR-0014, and
`dev/schemas/longitudinal-reference-model.md`.

## Temporal selection

A Stream or Study Area query must not silently select records by matching year
labels alone. It needs an explicit policy, for example:

- a reviewed set of Survey Event IDs representing one analysis snapshot;
- the latest compatible event per Reach before a stated date; or
- events linked to the same documented source acquisition when evidence exists.

The response must expose the selected Survey Event and date precision for every
Reach. A future grouping object may be justified if repeated use cases require
durable cross-Reach snapshot membership, but it is not added to the kernel
without evidence and review.

## Cross-method durability

Historic field-survey and modern remote-sensing records can answer related
scientific questions only when the database preserves the meaning and fitness
of each measurement. Feature contracts therefore need controlled method/type
identifiers, definitions, units, datum, sampling/derivation procedure,
resolution or spacing, uncertainty/quality information when known, and
provenance. Missing legacy values remain unknown rather than fabricated.

## Acceptance scenarios

1. Selecting a Stream returns current Flowlines for its chosen Reach Survey
   Events without relying on `ReachName` parsing.
2. Selecting a Study Area returns derived features from all descendant Streams
   while retaining direct Reach/Survey Event ownership.
3. A longitudinal-profile query rejects or warns about missing/invalid
   reference-frame calibration, incompatible vertical datums/units, or
   ambiguous temporal selection.
4. Two Survey Events derived with different method versions remain visibly
   distinguishable in a change analysis.
5. A historic manual cross section and a modern terrain-derived cross section
   can coexist without asserting equivalence unless an approved comparison
   contract supports it.
6. Selecting a Network Scope returns distinct synthetic Network Observations
   by terrain time, including Stream/Reach classifications and explicit
   cross-time segment correspondence where it has been reviewed.

## Open contracts

- Physical representation and validation tolerances for Network Observation
  topology, cross-time segment correspondence, base Flowline selection, and
  comparison-Flowline calibration.
- Cross-Reach temporal snapshot selection or grouping.
- Measurement-method vocabulary and compatibility rules.
- Query/view naming, parameters, indexes, pagination, and service exposure.
- Rules for materializing derived query products versus recomputing them.
