# ADR-0020: Service-mediated enterprise access and licensed administration

- Status: accepted
- Date: 2026-09-02
- Clarifies: ADR-0001, ADR-0015, and ADR-0018
- Supersedes in part: ADR-0002

## Context

FGDB will operate in USACE-managed ArcGIS Enterprise infrastructure, while
scientific development, local analysis, and most automated testing must remain
possible on computers that do not have an ArcGIS Pro license or access to the
USACE network. Requiring ArcGIS Pro for ordinary reads, controlled loads, or
Shiny persistence would make the open-source R implementation dependent on a
proprietary desktop client and prevent a practical off-network development
loop.

The target deployment is an Esri enterprise geodatabase hosted in PostgreSQL
RDS in the USACE private cloud, currently AWS GovCloud IL4. The database is an
SDE data source registered with the USACE ArcGIS Enterprise deployment. ArcGIS
Portal Feature Services are the supported application boundary for the FGDB
vector and tabular data model.

Current open-source tooling can create, read, update, and test ordinary vector
feature classes in file geodatabases through GDAL OpenFileGDB. The R-ArcGIS
ecosystem can authenticate to an ArcGIS Enterprise portal and read and edit
Feature Service layers. It does not replace all licensed administration needed
to create and configure an SDE geodatabase, mosaic datasets, registered data
sources, and referenced services.

## Decision

1. The authoritative FGDB deployment uses PostgreSQL RDS as its database
   platform, Esri SDE-managed enterprise geodatabase objects, and a registered
   data-store connection in the USACE ArcGIS Enterprise environment.
2. ArcGIS Portal Feature Services are the supported application interface for
   FGDB vector feature classes and tables. Raster publication from enterprise
   mosaic datasets uses the applicable ArcGIS raster-capable service contract
   defined by the later raster design.
3. Read-only viewer applications obtain FGDB data through query-capable Portal
   services. They do not connect directly to PostgreSQL or SDE.
4. FGDB load tools and open-source web GIS applications, including Shiny,
   perform authorized reads and controlled writes through edit-capable Portal
   Feature Services. Service capabilities, application authorization, and FGDB
   validation must prevent these privileged write paths from becoming general
   end-user editing access.
5. R clients use the supported `{arcgis}` package ecosystem. This currently
   means `{arcgislayers}` for Feature Service data operations and
   `{arcgisutils}` for authentication, Portal interaction, Esri JSON, geometry
   conversion, and request infrastructure. FGDB wraps those dependencies behind
   its own versioned service and loading contracts.
6. Routine scientific processing, local geodatabase creation, FGDB client
   development, schema validation, and service-client tests do not require
   ArcGIS Pro. They use R, `sf`/GDAL, direct outputs governed through
   `fluvgeodata`, temporary file geodatabases or open relational stores, and
   mocked service responses where a live Portal is unavailable.
7. FGDB admin-facing tooling owns repeatable provisioning and configuration of
   a new enterprise FGDB instance. Operations not exposed by supported web GIS
   interfaces may use ArcPy and must run in an appropriately licensed ArcGIS
   Pro or ArcGIS Enterprise administrative environment.
8. The licensed administrative plane includes, as required, SDE schema
   creation or registration, geodatabase-specific configuration, mosaic
   dataset creation, registered data-store configuration, and referenced
   service publication. Exact license level and execution host are deployment
   requirements, not assumptions embedded in the R client.
9. ArcPy remains an infrastructure adapter. It does not implement independent
   scientific derivation, redefine the object-relational schema, or become the
   ordinary FGDB read/write client.
10. No FGDB tool or application directly modifies SDE system tables. All
    database, geodatabase, Portal, and service operations use supported
    PostgreSQL, ArcGIS, or service interfaces appropriate to the operation.
11. Release conformance uses a small licensed integration-test lane to verify
    provisioning, SDE behavior, mosaic datasets, service publication, and
    ArcGIS compatibility. Deterministic R and GDAL tests remain the primary
    development loop and use the same governed data and schema contracts.

## Access planes

```text
Local and off-network development
  fluvgeodata outputs -> fluvgeo -> sf/data frames
    -> local feature classes and tables -> FGDB validation

Application data plane
  FGDB / Shiny / viewers
    -> arcgis + arcgislayers + arcgisutils
    -> authenticated Portal Feature Services
    -> registered SDE feature classes and tables in PostgreSQL RDS

Licensed administrative plane
  FGDB admin tooling -> ArcPy where required
    -> SDE and geodatabase configuration
    -> mosaic datasets and registered data store
    -> referenced ArcGIS Enterprise services
```

## Consequences

- ArcGIS Pro is not a prerequisite for the normal `{fluvgeo}` or `{FGDB}` R
  development loop, for local scientific analysis, or for application access
  to an already provisioned FGDB deployment.
- A USACE-hosted, authenticated integration environment is still required to
  verify licensed ArcGIS administration and actual deployed-service behavior.
- User-facing and admin-facing FGDB functions have different dependencies,
  permissions, execution environments, and test strategies and must not be
  conflated.
- Viewer services or credentials remain read-only. Controlled writers use
  separately authorized edit capabilities with collection governance,
  validation, identity reconciliation, replacement rules, verification, and
  audit enforced by FGDB workflows.
- ADR-0002's blanket statement that client-facing Feature Layer services are
  read-only is narrowed to viewer access. Its ArcGIS Pro desktop load path is
  replaced by service-mediated R loading as the target user-facing mechanism;
  licensed ArcGIS tooling remains necessary in the administrative plane.
- Local GDAL conformance cannot prove SDE registration, Esri-managed schema
  behavior, mosaic dataset behavior, Portal authorization, or service
  publication. Those claims require evidence from the licensed integration
  lane.
- Environment URLs, connection files, tokens, credentials, cloud identifiers,
  and other sensitive deployment configuration remain outside version control.
