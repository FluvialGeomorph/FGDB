# R package development

FGDB is an R package. Read the workspace-level `.agents/workstation.md` before
running R because the active R installation is not assumed to be on `PATH`.

## Ownership and dependencies

- Package code belongs in `R/` and is documented with roxygen2.
- Automated tests belong in `tests/testthat/` and use testthat edition 3.
- Direct geospatial tool outputs used across repositories belong in
  `fluvgeodata`; do not duplicate them in FGDB.
- Reproducible derivation of a needed data artifact uses an R script in the
  owning repository, following that repository's data-raw conventions.
- Reusable scientific derivation and topology algorithms belong in `fluvgeo`.
  FGDB owns contract validation, reconciliation, enterprise mapping, loading,
  and database management.

## Test-data pattern

Locate shared evidence with `system.file("extdata", ..., package =
"fluvgeodata")`. A test of invalid input starts from a direct tool output and
creates only the invalid condition under examination in memory or in a
testthat-managed temporary directory. Do not commit manufactured geospatial
datasets or introduce a separate Python conformance runner.

## Verification

Using the configured development R installation with the package dependencies
installed, run:

```r
devtools::document()
devtools::test()
devtools::check(args = "--no-manual")
```

Inspect `git status --short` and `git diff --check` after generation and checks.
