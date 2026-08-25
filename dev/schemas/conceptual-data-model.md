# FGDB conceptual data model

## Status

This document records accepted conceptual invariants. It is not yet a logical
or physical Esri geodatabase schema.

## Domain hierarchy

```text
Collection
└── Study Area
    └── Stream
        └── Reach
            └── Survey Event
                └── FG Feature and raster content
```

The hierarchy is mandatory for both collections. Client convenience must not
create records that bypass a level:

- each study area belongs to exactly one collection;
- each stream belongs to exactly one study area;
- each reach belongs to exactly one stream;
- each survey event belongs to exactly one reach; and
- every governed feature record and raster item belongs to exactly one survey
  event.

Each parent may own one or more children of the next type. Shiny applications
may create required child records automatically when the user should not have
to manage the hierarchy directly, but they must preserve the same foreign-key
chain. Association entities needed for external references remain to be
defined without weakening this ownership hierarchy.

## Collection

`collection` is both the top-level partition and a governance boundary.

| Collection class | Source | Audience | Meaning | Initial visibility | Mutation model |
|---|---|---|---|---|---|
| Desktop | ArcGIS Pro and `FluvialGeomorph-toolbox` | Experienced GIS analysts and authorized customers | Expert-produced, authoritative analysis | After rigorous QA | Idempotent reach-survey-event replacement |
| Shiny | Browser-based FluvialGeomorph applications | General USACE users | Self-service, informative analysis | Immediately after valid save, subject to authorization | Edit in place |

The schema must expose collection membership unambiguously for every governed
entity, feature record, and raster item. Whether this is implemented by direct
foreign keys, inherited ownership, separate datasets, or a combination is a
physical-design decision.

## Identity and names

- Each durable domain entity has an immutable machine identifier.
- Study-area names are human-readable and globally unique across collections.
- Study-area names follow a tiered naming convention that is not yet specified.
- Display names are not substitutes for immutable identifiers in foreign keys,
  ingestion keys, or service contracts.
- Rename, alias, reservation, and reuse rules remain unresolved.

## Desktop replacement unit

The logical replacement key is one desktop collection reach-survey-event. The
exact key fields will be finalized with the identifier model.

For a corrected load:

1. inventory the complete source;
2. calculate an input manifest or equivalent fingerprint;
3. validate a complete candidate dataset;
4. stage all affected feature and raster content;
5. replace all active target content owned by the replacement key;
6. verify completeness and integrity across target datasets; and
7. record the load outcome and manifest.

An exact repeat must not create duplicates. A changed source must not be
treated as an exact repeat. Known-bad prior geometry and attributes are removed
from active/queryable production content rather than retained as data
revisions.

## Shiny edit unit

A saved Shiny analysis has a durable identity and is updated in place. Updates
must retain at least the last modifying actor/process and modification time.
Optimistic concurrency, change audit depth, deletion versus retirement, and
multi-user sharing behavior remain unresolved.

## Shared provenance

Both collections require:

- collection identity and source class;
- originating application and version;
- `{fluvgeo}` version and, where needed, calculation-contract version;
- derivation method/engine and method version for each feature family;
- responsible actor or process;
- creation/load and last-modification timestamps as applicable;
- terrain or survey-event source identity;
- spatial reference;
- validation outcome; and
- source/load manifest appropriate to the workflow.

Shared `{fluvgeo}` provenance identifies common scientific implementation. It
does not imply that records from the two collections have equal authority,
review, spatial scope, or fitness for a particular use.

## Required future contracts

- Collection codes and immutable ID formats.
- Tiered study-area naming grammar and uniqueness enforcement.
- Desktop QA states and publication gates.
- Feature-class and mosaic-dataset ownership keys.
- Shiny save/restore payload, edit concurrency, and authorization.
- Cross-collection query and service behavior.
