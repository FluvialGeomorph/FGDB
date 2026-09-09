# Development context

This directory contains durable, repository-owned context for human and agentic development. `AGENTS.md` routes tasks here; the artifacts below hold the detail.

- `goals/`: scope, outcomes, and success criteria
- `architecture/`: system structure and ownership boundaries
- `decisions/`: accepted architectural decision records
- `governance/`: artifact authority and lifecycle rules
- `workflows/`: repeatable procedures
- `schemas/`: exact structural contracts
- `features/`: cohesive capability specifications
- `checkpoints/`: concise resumable state
- `scripts/`: supporting development automation

Chat transcripts and generated output are not canonical project context.

## Current migration reading path

- [Purpose and current development focus](goals/initiative-brief.md)
- [Why Study Area reporting guides design as well as loading](../../fluvgeo/dev/goals/reporting-intent.md)
- [Accepted folder/GeoTIFF delivery decision](decisions/adr-0025-folder-deliverables-and-geotiff-terrain.md)
- [Folder requirements and the boundary of the implemented intake slice](schemas/local-project-folder-requirements.md)
- [Storage experiment: conclusions before raw test counts](experiments/geopackage-raster/FINAL-FINDINGS.md)

The separate [QGIS/R execution experiment](../../fg-qgis-toolbox/dev/features/qgis-provider-qualification.md)
tests desktop access to the backend; it neither qualifies FGDB loading nor
reopens the accepted terrain storage choice.
