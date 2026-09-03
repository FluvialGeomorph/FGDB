# ADR-0022: Versioned compatibility profiles and controlled contract change

- Status: accepted
- Date: 2026-09-02
- Complements: ADR-0018, ADR-0020, and ADR-0021

## Context

FGDB's supported platforms, libraries, services, and storage formats evolve on
independent schedules. R, `sf`, GDAL/OGR, OpenFileGDB, GeoPackage, PostgreSQL,
PostGIS, ArcGIS Pro, ArcGIS Enterprise, SDE, Portal Feature Services, and their
configuration options can change type inference, supported capabilities, and
round-trip behavior without changing the FluvialGeomorph scientific meaning.

Historically, these changes have been discovered while troubleshooting
production workflows. That consumes scarce development time, delays scientific
capabilities, and risks accepting scientifically altered data because a file or
service remains technically readable.

A static crosswalk cannot manage this risk. Compatibility must be an explicit,
versioned system with a controlled lifecycle for discovering, testing,
accepting, deprecating, migrating, and retiring platform profiles.

## Decision

1. Logical schema versions, platform profiles, binding versions, adapter
   versions, conformance-suite versions, and data-instance provenance are
   distinct identities. None is inferred solely from another.
2. A platform profile identifies the material runtime combination needed to
   interpret a result, including platform and format versions, libraries and
   drivers, service or database version where applicable, creation/open
   options, and relevant capabilities.
3. Capability probes supplement version checks. Compatibility is determined by
   observed behavior under an accepted test contract, not by a version string
   alone.
4. Every directional boundary transform is versioned independently. Support
   from platform A to B does not imply equivalent support from B to A.
5. FGDB maintains a machine-readable compatibility matrix relating logical
   schema version, source profile, destination profile, transform version,
   execution lane, and support status.
6. A previously unseen or materially changed profile begins as `unverified`.
   It cannot write production data until the applicable conformance suite
   passes and the profile is explicitly accepted.
7. An accepted profile whose behavior drifts becomes `blocked` for affected
   writes until the difference is classified and resolved. Read-only recovery
   may remain available under an explicit qualified profile.
8. Accepted contract records are immutable. Corrections and changes create new
   versions and explicit supersession links rather than rewriting the evidence
   under which older data was accepted.
9. Schema and binding changes use explicit migrations. Each migration declares
   source and destination versions, preconditions, transformations, expected
   loss class, validation, reversibility or recovery behavior, and approval.
10. Data provenance records the exact accepted schema, bindings, transforms,
    adapters, and platform profiles used to create and load it. New platform
    support does not retroactively change the interpretation of existing data.
11. Adapters perform runtime profile discovery and compare it with accepted
    compatibility records before material reads, writes, or migrations. A
    mismatch produces an actionable diagnostic and safe failure mode.
12. Package and platform upgrades follow a compatibility-change workflow:
    observe, diff, classify, test, update the adapter or crosswalk, review,
    accept, migrate when required, and only then release.
13. Conformance suites shall be modular by logical type, feature family,
    boundary, and platform capability so an upgrade can rerun all affected
    tests without requiring unrelated enterprise operations.
14. FGDB may support multiple accepted read profiles concurrently. Each
    deployment has one declared write profile per contract and environment so
    new output remains predictable.
15. Deprecation and retirement require a support window, inventory of affected
    data and workflows, migration or read-recovery plan, and explicit approval.
16. Compatibility telemetry and reports shall identify versions and outcomes
    without recording credentials, restricted endpoints, customer data, or
    other sensitive environment details.

## Consequences

- Platform upgrades become planned compatibility events instead of incidental
  dependency updates.
- The project can add a new GeoPackage, GDAL, ArcGIS, or database profile
  without weakening or rewriting older accepted contracts.
- Runtime capability checks fail earlier and with better diagnostics than
  downstream scientific calculations.
- The compatibility registry and conformance harness become maintained product
  infrastructure with their own versions, tests, migrations, and release
  notes.
- Supporting multiple historical read profiles adds complexity, but preserves
  the ability to interpret and migrate older scientific data correctly.
- A new platform version is not automatically rejected, but it is prevented
  from writing governed data until evidence supports it.

## Binding specifications

- `dev/schemas/platform-type-crosswalk.md` defines the registry relations and
  support states.
- `dev/workflows/platform-compatibility-change.md` defines the upgrade and
  change-control workflow.

