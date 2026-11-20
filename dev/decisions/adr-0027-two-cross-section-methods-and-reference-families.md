# ADR-0027: Two cross-section methods and reference families

- Status: accepted owner/team scientific direction; implementation incomplete
- Date: 2026-11-19
- Supersedes: the Flowline-only reference-realization requirement of ADR-0013
  and ADR-0014 for RAS-style cross sections. Their Flowline rules continue to
  govern simple legacy sections; common frame/calibration invariants remain.
- Complements: ADR-0022, ADR-0023, ADR-0024 and ADR-0025

## Context

FluvialGeomorph studies morphological change through time in response to
infrastructure and landscape change. A terrain-derived Flowline can be sensitive
to flight-day water conditions and low-flow path variation. A centerline derived
from bankfull channel form is expected to reduce that coordinate noise and
comparison-event calibration anomalies. The expected benefit requires validation;
real bankfull migration and length change must remain observable.

Flowline remains necessary for REM creation. Replacing its referencing role for
new cross sections neither eliminates Flowline nor requires replacing every
historical cross section. FGDB must preserve interpretable legacy products while
supporting the selected new method.

## Decision

1. Support two cross-section method families:
   - **RAS-style:** bankfull channel centerline linear referencing for all new
     work and rework.
   - **Simple (straight-ish):** Flowline linear referencing, retained as the
     legacy method for backward compatibility and its open-source replacement.
2. Preserve distinct Flowline and bankfull centerline geometry, identity,
   edition and provenance. Flowline continues to support REM creation.
3. Retain explicit frame-relative base-event selection and calibration for both
   reference families. A frame records its exact base realizations, mouth,
   topology, upstream-increasing kilometer coordinate, methods and QA. A newer
   Survey Event does not silently change that frame or recalibrate observations.
4. FGDB must distinguish method family, scientific method/version, reference
   family, exact geometry edition, frame/base/calibration, source lineage and
   evidence status. These are related but separate concepts. A type flag alone
   does not define scientific meaning or establish comparability.
5. Preserve valid historical products and original measures under their
   applicable contracts and retention policy. Unknown provenance remains
   explicitly unresolved. Do not infer method from line shape or station values.
6. RAS-style rework creates an explicitly identified result with lineage to the
   source work. Neither method may overwrite another concurrent method's dataset
   slot or silently reuse a distinct transect's identity.
7. Common-axis cross-method analyses require an explicitly selected frame and
   accepted correspondence/additional positions. Equal station values do not
   prove equivalent sampling. Native-frame storage requires no universal
   historical conversion.
8. Retain standard `cross_section` naming and legacy import/export profiles.
   Analyze the shared physical table/type binding in the owning contract before
   implementation; exact code spellings and relations are not fixed by this ADR.
9. Keep accepted v11 geometry and v10 pruning as the starting baseline. Centerline
   stationing is an authorized functional change; optional shape optimization
   remains parked. Existing v11 Flowline-stationed drafts retain their actual
   provenance and are not automatically conforming RAS-style or simple outputs.

## Consequences

The model must extend its current Flowline-specific base/calibration relations
and separate section derivation lineage from longitudinal position. Backend,
FG Studio persistence, consumers, validators and compatibility exports must
identify the selected method and reference without changing established legacy
field meanings. RAS-style names do not confer hydraulic acceptance or HEC-RAS
export readiness. ArcPy production tools remain in place until their replacement
has demonstrated its defined compatibility scope.

## Binding and implementation route

- [Cross-section contract and storage analysis](../schemas/cross-section-feature-contract.md)
- [Longitudinal reference contract](../schemas/longitudinal-reference-model.md)
- [Implementation plan](../../../fgstudio/dev/goals/cross-section-implementation-plan.md)

The owner/team has accepted the two-method direction and requested implementation
planning. This ADR records that decision; it does not assert implemented schema,
successful calibration qualification, production deployment or batch reprocessing.
