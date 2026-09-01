test_that("fluvgeodata provides retained network outputs", {
  retained_outputs <- c(
    "AntelopeCreek_2013.gdb",
    "testing_data.gdb",
    "y2006_R1.gdb"
  )

  for (dataset in retained_outputs) {
    gdb <- fluvgeodata_extdata(dataset)
    expect_gdb_layers(gdb, c("stream_network", "flowline"))

    network <- suppressWarnings(
      sf::st_read(gdb, layer = "stream_network", quiet = TRUE)
    )

    expect_s3_class(network, "sf")
    expect_gt(nrow(network), 0L)
    expect_true(
      all(as.character(sf::st_geometry_type(network)) %in%
        c("LINESTRING", "MULTILINESTRING"))
    )
  }
})

test_that("fluvgeodata provides flowline-only legacy outputs", {
  flowline_only_outputs <- c(
    "AntelopeCreek_2017.gdb",
    "y2010_R1.gdb",
    "y2016_R1.gdb"
  )

  for (dataset in flowline_only_outputs) {
    gdb <- fluvgeodata_extdata(dataset)
    layers <- sf::st_layers(gdb)$name

    expect_true("flowline" %in% layers)
    expect_false("stream_network" %in% layers)

    flowline <- suppressWarnings(
      sf::st_read(gdb, layer = "flowline", quiet = TRUE)
    )

    expect_s3_class(flowline, "sf")
    expect_gt(nrow(flowline), 0L)
    expect_true(
      all(as.character(sf::st_geometry_type(flowline)) %in%
        c("LINESTRING", "MULTILINESTRING"))
    )
  }
})
