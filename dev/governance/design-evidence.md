# Design evidence governance

## Purpose

FGDB consolidates design work and historical artifacts that originated across
multiple people, repositories, production workflows, and time periods. This
repository preserves that evidence and turns it into one coherent,
reviewable design for deployment.

## Evidence classes

- **Problem and requirement sources** describe intended outcomes or constraints
  but may not specify implementation.
- **Design prototypes** demonstrate prior ideas but may be incomplete,
  inconsistent, or unsuitable as production contracts.
- **Production examples** demonstrate structures that actually occurred in a
  workflow, including legacy defects and temporary artifacts.
- **Implementation evidence** demonstrates current code or deployed behavior.
- **Accepted design records** are maintained ADRs, schemas, architecture,
  features, and workflows that govern the intended FGDB design.

An artifact can belong to more than one evidence class. Classification must be
explicit; repository presence alone does not establish authority.

## Synthesis rules

1. Preserve original historical artifacts in Git when they are safe and useful
   evidence.
2. Do not silently edit an original artifact to resemble the emerging design.
3. Record its source, intended role, observed coverage, limitations, and review
   date in a maintained assessment or catalog.
4. Distinguish verified observations, human-provided context, inferences,
   accepted decisions, and unresolved questions.
5. Crosswalk source artifacts to accepted concepts rather than copying legacy
   names and process fields directly into the canonical schema.
6. Treat contradictions as design questions to resolve, not as reasons to
   select whichever artifact is newest or most complete-looking.
7. Keep credentials, sensitive infrastructure details, restricted data,
   personal information, and unnecessary embedded paths out of synthesized
   artifacts.
8. When the unified design changes a cross-repository contract, update the
   owning repository through the approved cross-repository workflow.

## Authority order

For intended FGDB behavior, accepted ADRs and explicit schema/interface
contracts govern over historical prototypes and production examples. Current
code and deployed systems remain evidence of actual behavior and must be
checked for drift from the intended design.

