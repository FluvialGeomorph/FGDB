# Human roles and review participation

- Recorded: 2026-08-27
- Status: working governance context
- Source: roles described by Michael Dougherty

## Team context

| Person | Stated role | Relevant design perspective |
|---|---|---|
| Michael Dougherty | Geographer and lead developer | Technical integration, GIS/software architecture, implementation history, and cross-repository contracts |
| Chris Haring | Fluvial geomorphologist and FluvialGeomorph program manager | Scientific meaning, methodology, program priorities, and fitness for fluvial analysis |
| Tom Darby | Geographer who performs study-area analyses | Production workflow, analyst decisions, QA, legacy variation, and operational usability |
| Bobby Oliver | Geographer managing updates to the Tech and User Manuals | Terminology, procedures, documentation consistency, and communication to users |

These roles are durable context but are not, by themselves, a formal RACI or
delegation of organizational approval authority. Formal approval requirements
must be recorded explicitly when needed.

## Working review map

The following participation is recommended from the stated roles:

| Design area | Essential perspectives |
|---|---|
| Scientific feature meaning and method changes | Chris for scientific/program review; Michael for implementation contract; Tom for production applicability |
| Canonical processing architecture | Michael for technical integration; Chris for scientific acceptance; Tom for analyst workflow impact |
| Existing feature catalog and legacy disposition | Tom for production evidence; Michael for producer behavior; Chris for scientific value; Bobby for documented terminology |
| FGDB hierarchy, identifiers, ingestion, and replacement | Michael for technical design; Tom for operational validation; Chris for scientific-use implications |
| Tech/User Manual alignment | Bobby for documentation stewardship, with the applicable scientific, technical, and operational reviewers |
| Deployment and security | Applicable USACE infrastructure/security authorities, who remain to be identified, plus Michael for application integration |

## AI-assisted design boundary

AI assistance may:

- inventory and classify artifacts;
- trace fields, tools, functions, workflows, and repository ownership;
- compare historical schemas and implementations;
- expose contradictions, gaps, and unverified assumptions;
- draft crosswalks, contracts, ADRs, tests, and review questions; and
- maintain concise checkpoints and design traceability.

AI assistance does not establish scientific validity, approve engineering or
security decisions, resolve ambiguous human intent without review, or replace
the team members who own program, scientific, operational, technical, and
documentation judgment.

## Review-record expectation

Consequential artifacts should identify:

- evidence reviewed;
- unresolved assumptions;
- affected repositories and consumers;
- required scientific, operational, technical, documentation, or infrastructure
  review; and
- the human acceptance that changes an artifact from proposed to accepted.

