# Independent installed R/GDAL lane. Run from any directory using absolute script path.
arguments <- commandArgs(trailingOnly = TRUE)
if (length(arguments) != 2L) stop("Supply experiment directory and new run ID")
lab <- normalizePath(arguments[[1]], winslash = "/", mustWork = TRUE)
id <- arguments[[2]]
if (!grepl("^[A-Za-z0-9_-]+$", id)) stop("Invalid run ID")
out <- file.path(lab, "results", id)
if (file.exists(out)) stop("Run already exists")
manifest <- jsonlite::read_json(file.path(lab, "payload/manifest.json"), simplifyVector = FALSE)
for (name in names(manifest$sha256)) {
  if (grepl("[/\\\\]", name)) stop("Unexpected payload path")
  stopifnot(digest::digest(file = file.path(lab, "payload", name), algo = "sha256") == manifest$sha256[[name]])
}
dir.create(out, recursive = TRUE)
rows <- list()
for (case in manifest$cases) {
  warnings <- character()
  row <- tryCatch(withCallingHandlers({
    a <- terra::rast(file.path(lab, "payload", case$tif))
    b <- terra::rast(file.path(lab, "payload", case$gpkg))
    x <- terra::values(a, mat = FALSE); y <- terra::values(b, mat = FALSE)
    tolerance <- 32 * .Machine$double.eps * max(1, abs(as.vector(terra::ext(a))))
    checks <- c(dimensions = identical(dim(a), dim(b)),
      nodata_mask = identical(is.na(x), is.na(y)),
      exact_valid_values = identical(x[!is.na(x)], y[!is.na(x)]),
      pixel_type = identical(terra::datatype(a), terra::datatype(b)),
      crs_semantic = isTRUE(sf::st_crs(terra::crs(a)) == sf::st_crs(terra::crs(b))),
      resolution = identical(terra::res(a), terra::res(b)),
      extent = max(abs(as.vector(terra::ext(a)) - as.vector(terra::ext(b)))) <= tolerance,
      band_units = identical(terra::units(a), terra::units(b)))
    list(case = case$id, status = if (all(checks)) "PASS" else "FAIL", checks = as.list(checks))
  }, warning = function(w) {
    warnings <<- c(warnings, conditionMessage(w)); invokeRestart("muffleWarning")
  }), error = function(e) list(case = case$id, status = "ERROR", error = conditionMessage(e)))
  clean <- function(text) gsub(lab, "<experiment>", text, fixed = TRUE)
  if (!is.null(row$error)) row$error <- clean(row$error)
  row$warnings <- clean(warnings)
  rows[[length(rows) + 1L]] <- row
}
jsonlite::write_json(rows, file.path(out, "checks.json"), auto_unbox = TRUE, pretty = TRUE)
jsonlite::write_json(list(R = as.character(getRversion()), sf = as.character(packageVersion("sf")),
  terra = as.character(packageVersion("terra")), gdal = terra::gdal(),
  spatial_versions = as.list(sf::sf_extSoftVersion()),
  payload_manifest_sha256 = digest::digest(file = file.path(lab, "payload/manifest.json"), algo = "sha256")),
  file.path(out, "runtime.json"), auto_unbox = TRUE, pretty = TRUE)
jsonlite::write_json(list(completed = TRUE, checks = length(rows)),
  file.path(out, "completion.json"), auto_unbox = TRUE, pretty = TRUE)
print(table(vapply(rows, `[[`, character(1), "status")))
