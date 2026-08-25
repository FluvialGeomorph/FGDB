# Checkpoint: Initial FGDB design

- Updated: 2026-08-25
- Status: active

## Objective

Turn the database-migration problem statement into an agreed FGDB design and
an implementable, staged work plan.

## Current state

FGDB is an otherwise empty Git repository with the `{reproducibleai}` base
agentic-context profile. The initial initiative brief captures the goals and
constraints supported by the technical-manual source. No implementation
architecture or database technology has been selected.

## Completed

- Inspected the FGDB repository, branch, worktree, and remote.
- Read the database-migration problem statement.
- Reviewed current FluvialGeomorph capability ownership and dependency records.
- Scaffolded and validated agentic-context standard 0.1 with the `base` profile.
- Recorded the initial scope, desired outcomes, constraints, and unknowns in
  `dev/goals/initiative-brief.md`.

## Remaining

1. Define FGDB's system boundary and authoritative data responsibilities.
2. Define users, use cases, and priority queries.
3. Formalize entities, identifiers, temporal semantics, spatial semantics,
   provenance, and integrity constraints.
4. Decide artifact-storage boundaries and ingestion behavior.
5. Evaluate database, deployment, interface, and repository-implementation
   options against the agreed requirements.
6. Define the legacy inventory and migration crosswalk.
7. Record accepted decisions, schemas, architecture, workflows, and a staged
   delivery plan in their durable routes.
8. Add FGDB to the organization repository catalog and capability map through
   a separately reviewed cross-repository change when its role is accepted.

## Evidence and verification

- Source brief: `../FG-Tech-Manual/DB-migration.qmd` from the workspace root.
- Organization evidence: `FG-architecture/dev/architecture/` and
  `FG-architecture/repositories.yml`.
- `validate_agentic_context("FGDB")` returned `valid = TRUE` with no findings.
- `git status` confirmed that only the new scaffold and design artifacts are
  untracked in this new repository.

## Next safe action

Agree on the FGDB system boundary, beginning with what is authoritative in the
central database and what remains an externally stored source or derived
artifact.

## Blockers or decisions

The first design decision is the storage and authority boundary. In
particular, determine whether FGDB stores only relational metadata and curated
queryable vector/tabular features while referencing large source/derived
artifacts, or whether it is also responsible for raster and file-geodatabase
artifact storage.

