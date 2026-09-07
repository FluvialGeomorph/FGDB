"""Licensed workstation runner. Requires ArcGIS Pro Python + NumPy, not R/GDAL."""
import argparse
import sys
import shutil
from pathlib import Path
import numpy as np
from common import (LAB, new_run, save_json, verify_payload, oracle, compare_arrays,
                    grid_check, all_checks, safe_error, digest)


def main(run_id):
    # Licensing/import failures happen before creating a result directory.
    import arcpy
    manifest = verify_payload()
    run = new_run(run_id)
    info = arcpy.GetInstallInfo()
    save_json(run / 'runtime.json', {'engine': 'ArcGIS Pro',
              'version': info.get('Version'), 'build': info.get('BuildNumber'),
              'python': sys.version.split()[0], 'numpy': np.__version__,
              'payload_manifest_sha256': digest(LAB / 'payload/manifest.json')})
    arcpy.ResetEnvironments()
    arcpy.env.overwriteOutput = False
    # ArcGIS may create statistics/auxiliary files on read. Use disposable
    # input copies, never the committed reference payload itself.
    input_copy = run / 'input-copy'; input_copy.mkdir()
    for path in (LAB / 'payload').iterdir():
        if path.suffix in ('.tif', '.gpkg') or path.name.endswith('.tif.aux.xml'):
            shutil.copyfile(path, input_copy / path.name)
    rows, outputs = [], []
    def attempt(case, route, operation):
        try:
            checks = operation()
            rows.append({'case': case['id'], 'route': route,
                         'status': 'PASS' if all_checks(checks) else 'FAIL', 'checks': checks})
        except Exception as error:
            rows.append({'case': case['id'], 'route': route,
                         'status': 'ERROR', 'error': safe_error(error)})
        save_json(run / 'checks.json', rows)
        save_json(run / 'outputs.json', outputs)
    def inspect(case, path):
        raster = arcpy.Raster(str(path))
        expected, expected_mask = oracle(case)
        # Two distinct substitutions expose NoData without assuming a sentinel
        # is absent from valid data. No Spatial Analyst extension is required.
        a = arcpy.RasterToNumPyArray(raster, nodata_to_value=123)
        b = arcpy.RasterToNumPyArray(raster, nodata_to_value=124)
        mask = a != b
        result = compare_arrays(expected, expected_mask, a, mask)
        result.update(grid_check(case['geotransform'], [raster.extent.XMin,
                      raster.meanCellWidth, 0., raster.extent.YMax, 0., -raster.meanCellHeight]))
        result['pixel_type'] = raster.pixelType == {'Float32': 'F32', 'Float64': 'F64', 'Int16': 'S16'}[case['pixel_type']]
        source_crs = arcpy.SpatialReference(); source_crs.loadFromString(case['wkt'])
        # ArcPy CRS equality is provisional; retain WKT for independent review.
        result['crs_arcpy_equal'] = bool(raster.spatialReference == source_crs)
        result['band_count'] = raster.bandCount == 1
        result['observed_crs_wkt'] = raster.spatialReference.exportToString()
        result['metadata_scope'] = 'band units/vertical meaning reviewed on returned exports; not certified here'
        return result
    for case in manifest['cases']:
        case_dir = run / case['id']; case_dir.mkdir()
        control = input_copy / case['tif']
        gpkg = input_copy / case['gpkg']
        # Documented ArcGIS path to a named raster in a GeoPackage.
        candidate = str(gpkg) + '\\' + case['layer']
        attempt(case, 'arcgis_geotiff_control', lambda: inspect(case, control))
        attempt(case, 'arcgis_gdal_gpkg_read', lambda: inspect(case, candidate))
        def export_candidate():
            dest = case_dir / 'from_gdal_gpkg.tif'
            arcpy.management.CopyRaster(candidate, str(dest), format='TIFF')
            outputs.append({'case': case['id'], 'route': 'arcgis_gpkg_to_tiff', 'path': dest.relative_to(run).as_posix()})
            return inspect(case, dest)
        attempt(case, 'arcgis_gpkg_to_tiff', export_candidate)
        def to_filegdb():
            arcpy.management.CreateFileGDB(str(case_dir), 'roundtrip.gdb')
            dest = case_dir / 'roundtrip.gdb' / 'terrain'
            arcpy.management.CopyRaster(str(control), str(dest))
            outputs.append({'case': case['id'], 'route': 'arcgis_tiff_to_filegdb',
                            'path': (case_dir / 'roundtrip.gdb').relative_to(run).as_posix(), 'layer': 'terrain', 'format': 'OpenFileGDB'})
            return inspect(case, dest)
        attempt(case, 'arcgis_tiff_to_filegdb', to_filegdb)
        def from_filegdb():
            dest = case_dir / 'arcgis_created.gpkg'
            arcpy.management.CreateSQLiteDatabase(str(dest), 'GEOPACKAGE_1.3')
            arcpy.conversion.AddRasterToGeoPackage(str(case_dir / 'roundtrip.gdb' / 'terrain'), str(dest), 'terrain', 'TILED')
            outputs.append({'case': case['id'], 'route': 'arcgis_filegdb_to_gpkg',
                            'path': dest.relative_to(run).as_posix(), 'layer': 'terrain', 'format': 'GPKG'})
            return inspect(case, str(dest) + '\\terrain')
        attempt(case, 'arcgis_filegdb_to_gpkg', from_filegdb)
        def back_to_filegdb():
            dest = case_dir / 'roundtrip.gdb' / 'from_gpkg'
            arcpy.management.CopyRaster(candidate, str(dest))
            outputs.append({'case': case['id'], 'route': 'arcgis_gdal_gpkg_to_filegdb',
                            'path': (case_dir / 'roundtrip.gdb').relative_to(run).as_posix(), 'layer': 'from_gpkg', 'format': 'OpenFileGDB'})
            return inspect(case, dest)
        attempt(case, 'arcgis_gdal_gpkg_to_filegdb', back_to_filegdb)
        def own_back_to_filegdb():
            dest = case_dir / 'roundtrip.gdb' / 'from_arcgis_gpkg'
            arcpy.management.CopyRaster(str(case_dir / 'arcgis_created.gpkg') + '\\terrain', str(dest))
            outputs.append({'case': case['id'], 'route': 'arcgis_own_gpkg_to_filegdb',
                            'path': (case_dir / 'roundtrip.gdb').relative_to(run).as_posix(), 'layer': 'from_arcgis_gpkg', 'format': 'OpenFileGDB'})
            return inspect(case, dest)
        attempt(case, 'arcgis_own_gpkg_to_filegdb', own_back_to_filegdb)
    arcpy.management.ClearWorkspaceCache()
    verify_payload()
    save_json(run / 'artifact-checksums.json', {p.relative_to(run).as_posix(): digest(p)
              for p in run.rglob('*') if p.is_file() and not p.is_relative_to(input_copy)
              and p.suffix not in ('.lock', '.json')})
    save_json(run / 'completion.json', {'completed': True, 'checks': len(rows),
              'counts': {s: sum(r['status'] == s for r in rows) for s in ('PASS', 'FAIL', 'ERROR')},
              'meaning': 'Execution completed, not scientific acceptance. Review errors and exports.'})
    print('Completed', run.name, 'with', len(rows), 'observations. Failures are retained; do not delete them.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True, help='New unique run ID, e.g. arcgis-pro-01')
    main(parser.parse_args().run)
