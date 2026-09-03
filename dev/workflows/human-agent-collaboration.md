# Human-agent collaboration

## Purpose

Use the right participant for the missing work while preserving rapid FGDB
development and accountable scientific decisions. This workflow supplements,
but does not repeat, normal Codex repository inspection, implementation, and
verification behavior.

## Route the task

- Use a conversational reasoning environment when the objective needs
  clarification, alternatives need deep synthesis, or an expert is articulating
  tacit scientific or GIS knowledge.
- Use the repository agent when the answer depends on actual FGDB or
  cross-FluvialGeomorph code, history, contracts, dependencies, implementation,
  or tests.
- Consult the applicable human perspective in `../governance/human-review.md`
  as soon as intent, visual judgment, analyst practice, or domain expertise is
  the missing input.
- Escalate before committing a materially different scientific, semantic,
  architectural, release, or deployment choice.
- Otherwise proceed with the authorized work.

Do not investigate broadly merely because a subject is scientific. For
reversible defaults and visual workflow choices, propose a sensible starting
point and obtain focused analyst feedback. Stop investigating when more
repository evidence is unlikely to change the next action.

## Compact handoffs

From a reasoning environment or human to the repository agent, provide:

- objective and desired outcome;
- decisions and assumptions already established;
- repositories in scope;
- unresolved repository questions;
- permitted changes; and
- completion criteria.

From the repository agent to a human or reasoning environment, return:

- the conclusion or decision needed;
- only the repository facts that materially affect it;
- remaining uncertainty;
- the recommended next action; and
- one precise question when consultation is required.

Do not transfer full transcripts. Use a formal decision packet only when a
complex consequential choice cannot be reviewed clearly in a shorter handoff.

## Durable result

After a consequential human decision, update the narrowest applicable FGDB
goal, ADR, architecture, schema, workflow, feature, documentation, test, or
code artifact. Apply the evidence classes in
`../governance/design-evidence.md` when the distinction affects the decision;
they are not mandatory formatting for routine work.
