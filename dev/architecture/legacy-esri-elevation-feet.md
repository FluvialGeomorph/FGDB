# Legacy ArcGIS elevation units: what did "feet" mean?

## Corrected owner evidence (2026-09-12)

The owner clarifies that FG required elevation values in **feet**, selected during
ArcMap/ArcGIS Pro raster work, not specifically U.S. survey feet. Earlier wording
"US feet" is superseded; the subsequent claim of an FG US-survey-foot convention
was unsupported. Do not relabel retained DEMs or convert values on that basis.

The owner subsequently recalls deriving a DEM from meter-valued point-cloud data,
then using Raster Calculator with `0.3048` to convert its elevations to feet.
For that direction the expression is `DEM_feet = DEM_meters / 0.3048`; it produces
international feet. The operator is reconstructed from the stated conversion
direction, not quoted from a retained expression. Multiplication by 0.3048 is the
reverse conversion (feet to meters). Preserve the owner's "I believe" qualification:
this supports a workflow interpretation, not verified execution for every raster.

## Verified distinctions

Esri does not use one universal interpretation of every "feet" label:

| Context | Documented interpretation | Evidence boundary |
|---|---|---|
| Raster elevation conversion using 0.3048 m/ft or approximately 3.2808399 ft/m | International foot, exactly 0.3048 m | Esri explicitly identifies these pixel-conversion factors as international foot. |
| ArcMap/Pro raster surface z-factor guidance | Uses 0.3048 for vertical feet to horizontal meters | Evidence for that calculation, not proof of a particular input DEM's preparation. |
| ArcGIS Pro 3.4 generic geoprocessing Linear Unit Python keyword `Feet` | U.S. survey foot, exactly 1200/3937 m | A distance/tolerance parameter, not automatically a raster elevation declaration. `FeetInt` is international feet. Do not extrapolate every historical UI label/version from this table. |
| A selected horizontal or vertical coordinate system | Whatever its actual unit definition specifies | Horizontal unit alone does not identify elevation-cell units. Defining metadata is not proof of numerical conversion. |

Primary sources:

- [Esri raster pixel conversion](https://support.esri.com/en-us/knowledge-base/convert-pixel-values-of-a-raster-from-meters-to-feet-an-000012381)
- [ArcMap z-factor guidance](https://desktop.arcgis.com/en/arcmap/latest/tools/spatial-analyst-toolbox/applying-a-z-factor.htm)
- [ArcGIS Pro z-factor guidance](https://pro.arcgis.com/en/pro-app/3.5/tool-reference/3d-analyst/applying-a-z-factor.htm)
- [ArcGIS Pro 3.4 Linear Unit keywords](https://pro.arcgis.com/en/pro-app/3.4/tool-reference/appendices/geoprocessing-considerations-for-length-and-area-units.htm)
- [ArcMap Unit Conversion raster function](https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/unit-conversion-function.htm)
  lists a Feet choice but does not state its numerical factor on that page; the
  dropdown's implementation is not independently qualified by this review.

## Repository and history evidence

- [FG technical manual](../../../FG-Tech-Manual/CreateTerrain.qmd), lines 8-9,
  distinguishes horizontal feet from US survey feet but specifies only feet for
  vertical values. Its conversion sections require conversion without specifying
  a factor or exact client command. This corroborates the corrected owner account.
- `FluvialGeomorph-toolbox` commit
  `11cc5323e8a64d2ef2a12129c61bfcdd37e33717` (2020-05-14) changed Channel Slope's
  hard-coded `z_factor = 0.3048` into an analyst-supplied parameter. The predecessor
  therefore used an international-foot conversion factor in that calculation.
  [Current tool documentation](../../../FluvialGeomorph-toolbox/tools/_09_ChannelSlope.py)
  retains the 0.3048 example; it does not enforce that value for every run.
- Field-derived DEM code interpolates the supplied Elevation field and uses
  `z_factor = 1` for its TIN-to-raster path. That path does not independently resolve
  the source elevation's foot variant.

**Inference:** international feet are supported by the historic slope calculation
and Esri raster-conversion guidance; this is not evidence that all archive DEM
values were created or converted to that exact standard.

**Unknown:** the retained expression, ArcGIS version and conversion history for
each project. The owner now identifies Raster Calculator and 0.3048 by recollection;
the previous question about the general workflow is answered. No licensed
historical ArcGIS execution was performed here.

## Intake consequence and next qualification step

The owner's subsequent workflow clarification distinguishes point-cloud source
CRS from the deliberately chosen analysis DEM CRS. Analysts often prepared DEMs
in a common project reference framework before deriving FG products, with the
expertise and support to manage transformations. Source units or datum therefore
cannot simply fill a missing derived-DEM declaration. Recover the preparation
path (including any 0.3048 conversion), chosen analysis reference and exceptions.
Different input/output CRSs are not themselves contradictory metadata. See
[ADR-0026](../decisions/adr-0026-vertical-reference-recovery-and-preservation.md).

Retain `feet` as the corrected owner assertion and international feet as the
interpretation of the recalled meter-to-foot calculation. Resolve an exact foot definition
from the actual conversion factor, source product metadata, explicit VCS units or
reproducible tool/version behavior before precise conversion. Retain the evidence
basis separately from the source's raw wording; do not silently map generic feet
to either variant merely to complete intake fields.

No additional platform test is needed to determine the unit defined by division
by 0.3048. If a different or uncertain tool path needs verification, an authorized ArcGIS workstation can test the identified raster
conversion operation on a constant Float64 raster, recording full-precision
output and tool/version: one meter is about 3.280839895 international feet versus
3.280833333 U.S. survey feet. A display-unit change must not be mistaken for a
pixel-value conversion. This is a proposed diagnostic, not a completed test.

The difference is approximately two parts per million (about 0.61 mm for a value
of 1,000 feet). It is important for explicit contracts but does not by itself
demonstrate scientifically material error in historic elevation analyses. Do not
confuse it with larger errors from missing vertical datums or meter/foot confusion.

This correction changes documentation/evidence only, not manifests, raster values,
source rights, Survey Events or production tooling. The previously identified
2013/2022 source-access and metadata qualification requirements still apply.
