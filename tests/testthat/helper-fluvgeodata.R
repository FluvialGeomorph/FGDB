fluvgeodata_extdata <- function(...) {
  testthat::skip_if_not_installed("fluvgeodata")
  testthat::skip_if_not_installed("sf")

  path <- system.file("extdata", ..., package = "fluvgeodata")
  if (!nzchar(path)) {
    testthat::fail(
      paste(
        "The requested test data was not found in the installed",
        "fluvgeodata package."
      )
    )
  }

  path
}

expect_gdb_layers <- function(gdb, expected) {
  layers <- sf::st_layers(gdb)$name
  testthat::expect_setequal(intersect(layers, expected), expected)
  invisible(layers)
}
