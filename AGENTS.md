# Agent instructions

## Identity and scope

`FGDB` is the current repository. Treat its code, tests, configuration, and maintained documentation as the authoritative evidence for repository-local behavior.

## Always-applicable rules

- Inspect repository and Git evidence before making consequential changes.
- Keep this file concise; route detailed knowledge into maintained artifacts under `dev/`.
- Preserve unrelated user changes and keep work within the requested repository scope.
- Distinguish verified evidence, reasonable inference, and unknowns.
- Keep the normalized enterprise model distinct from the mandatory production
  compatibility contract for open-source replacements of legacy ArcPy tools.
  FGDB normalization must not be interpreted as permission for `fluvgeo` or
  `fgstudio` to remove, rename, repurpose, recapitalize, or change the units of
  established legacy feature-class fields.
- Treat FG Studio as grounded implementation evidence for still-developing
  GeoPackage, interoperability, persistence, and workflow portions of the FGDB
  specification. Accepted FGDB invariants constrain the app, but verified app
  findings must be reconciled back into FGDB rather than discarded or silently
  promoted. Distinguish accepted contracts, proposals, and implementation
  evidence explicitly.

## Conditional context routes

- Goals, scope, or success criteria: `dev/goals/`
- Architecture, dependencies, or ownership boundaries: `dev/architecture/`
- Consequential and durable choices: `dev/decisions/`
- Governance or artifact lifecycle: `dev/governance/`
- Repeatable development procedures: `dev/workflows/`
- Human, reasoning-environment, and repository-agent routing:
  `dev/workflows/human-agent-collaboration.md`
- Exact structural contracts: `dev/schemas/`
- Legacy-derived feature replacement and cross-repository output compatibility:
  `dev/schemas/legacy-derived-feature-compatibility.md`
- Ontology design and semantic-interoperability guidance: `dev/ontology/`
- Cohesive user-visible capabilities: `dev/features/`
- Resumable unfinished work: `dev/checkpoints/current/`
- Repository-type-specific rules: inspect the repository's native configuration and workflows.
- R package development or tests: `DESCRIPTION`, `R/`, `tests/testthat/`, and
  `dev/workflows/r-package-development.md`.

Full session transcripts are not normal context sources. Use maintained durable artifacts and concise checkpoints.

## Completion governance

Before declaring meaningful work complete, determine whether it changed goals, architecture, a durable decision, a schema or interface, a repeatable workflow, feature behavior, or resumable state. Update the applicable durable artifact. Create a checkpoint only when useful unfinished state remains.

## Verification and information governance

Run checks proportionate to the change, inspect Git status and diff, and confirm the change boundary. Never record secrets, credentials, PII, restricted data, or unnecessarily large logs in agentic-context artifacts.
