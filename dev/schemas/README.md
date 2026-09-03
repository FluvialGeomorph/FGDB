# Schemas

Store exact, reviewable structural contracts here. Prefer explicit required fields, allowed values, invariants, and validation rules over narrative implication.

## Active contracts

- `stream-network-geodatabase-schema.md` defines the accepted Stream Network
  feature classes, related tables, and local-to-enterprise mapping.
- `stream-network-source-evidence.md` catalogs direct legacy geodatabase
  evidence and the first `fluvgeo` implementation coverage.
- `platform-type-crosswalk.md` specifies the machine-readable field, geometry,
  constraint, raster, transform, and conformance relations required to verify
  cross-platform scientific fidelity.
- `scientific-result-contract.md` specifies wide dimension-table semantics,
  metric definitions, scientific and schema contracts, producing-software
  provenance, accepted dataset editions, and analyst-controlled updates.
- `scientific-reference-data.md` defines the reusable Dataset Type, unit,
  value-domain, and null-semantics relations needed by concrete contracts.
- `flowline-feature-contract.md` is the first concrete Dataset Type, schema,
  method, source-lineage, geometry, and migration binding under ADR-0023.
