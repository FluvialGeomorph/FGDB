"""Create a portable raster experiment and exercise GDAL and native QGIS reads."""
import argparse
import os
from pathlib import Path
import shutil
import sqlite3
import sys
from contextlib import nullcontext

# Configure only this process. Keep DLL-directory handles alive on Windows.
_dll_handles = []
if os.environ.get('FG_PROJ_DATA'):
    os.environ['PROJ_DATA'] = os.environ['FG_PROJ_DATA']
    os.environ['PROJ_LIB'] = os.environ['FG_PROJ_DATA']
if os.name == 'nt' and os.environ.get('OSGEO4W_ROOT'):
    root = Path(os.environ['OSGEO4W_ROOT'])
    prefix = Path(os.environ['QGIS_PREFIX_PATH'])
    qt = 'Qt5' if prefix.name == 'qgis-ltr' else 'Qt6'
    _dll_handles = [os.add_dll_directory(str(p)) for p in
                    [root / 'bin', root / 'apps' / qt / 'bin', prefix / 'bin'] if p.is_dir()]

from osgeo import gdal, ogr, osr
import numpy as np
from common import (LAB, save_json, load_json, digest, oracle, compare_arrays,
                    grid_check, all_checks, new_run, verify_payload, safe_error)
gdal.UseExceptions()
osr.UseExceptions()
if os.environ.get('PROJ_DATA'):
    osr.SetPROJSearchPaths([os.environ['PROJ_DATA']])


def read(path):
    ds = gdal.Open(str(path))
    if ds.RasterCount != 1:
        raise ValueError('Expected one analytical band; found ' + str(ds.RasterCount))
    b = ds.GetRasterBand(1)
    return ds, b.ReadAsArray(), b.GetMaskBand().ReadAsArray() == 0


def check(case, path):
    ds, values, mask = read(path)
    expected, expected_mask = oracle(case)
    result = compare_arrays(expected, expected_mask, values, mask)
    result.update(grid_check(case['geotransform'], ds.GetGeoTransform()))
    reference = osr.SpatialReference(wkt=case['wkt'])
    result['crs_semantic'] = bool(reference.IsSame(ds.GetSpatialRef()))
    result['pixel_type'] = gdal.GetDataTypeName(ds.GetRasterBand(1).DataType) == case['pixel_type']
    result['unit_preserved'] = ds.GetRasterBand(1).GetUnitType() == case['band_unit']
    scale = ds.GetRasterBand(1).GetScale()
    offset = ds.GetRasterBand(1).GetOffset()
    result['scale_preserved'] = (1. if scale is None else scale) == case['scale']
    result['offset_preserved'] = (0. if offset is None else offset) == case['offset']
    return result


def create_payload(source):
    payload = LAB / 'payload'
    payload.mkdir(exist_ok=False)
    cases = []
    provenance = []
    # Independent synthetic values: fractions, signs, zeros, boundary and internal NoData.
    y, x = np.indices((33, 35))
    a = (x - 17) * .125 + (y - 16) * .25
    mask = (x == 0) | ((x == 12) & (y > 8) & (y < 15))
    synthetic = [('float32_m', a.astype('float32'), 26914, 'm'),
                 ('float32_ft', a.astype('float32'), 2276, 'ft'),
                 ('float64_precision', (a + 0.1234567890123).astype('float64'), 26914, 'm'),
                 ('int16_signed', (a * 8).astype('int16'), 26914, '')]
    for name, values, epsg, unit in synthetic:
        values[mask] = -9999
        code = {'float32': gdal.GDT_Float32, 'float64': gdal.GDT_Float64, 'int16': gdal.GDT_Int16}[str(values.dtype)]
        ds = gdal.GetDriverByName('GTiff').Create(str(payload / (name + '.tif')), 35, 33, 1, code,
                                               options=['COMPRESS=DEFLATE'])
        s = osr.SpatialReference(); s.ImportFromEPSG(epsg)
        ds.SetSpatialRef(s); ds.SetGeoTransform((500000.25, 1., 0., 4500000.75, 0., -1.))
        b = ds.GetRasterBand(1); b.SetNoDataValue(-9999); b.SetUnitType(unit); b.WriteArray(values)
        ds = None
        _, written, written_mask = read(payload / (name + '.tif'))
        if not all_checks(compare_arrays(values, mask, written, written_mask)):
            raise ValueError('Synthetic GeoTIFF differs from generated oracle')
        cases.append((name, {'kind': 'synthetic', 'vertical_reference': 'unspecified synthetic reference',
                             'horizontal_epsg': epsg}))
    for year in (2006, 2010, 2016):
        archive = source / ('y%d_R1.gdb' % year)
        hashes = {p.relative_to(source).as_posix(): digest(p) for p in archive.rglob('*') if p.is_file()}
        datasets = gdal.Open(str(archive)).GetSubDatasets()
        if len(datasets) != 2:
            raise ValueError('Expected two retained rasters per Cole Creek event')
        for index, (uri, _) in enumerate(datasets):
            ds = gdal.Open(uri)
            name = 'cole_%d_%d' % (year, index)
            result = gdal.Translate(str(payload / (name + '.tif')), ds, format='GTiff',
                                    creationOptions=['COMPRESS=DEFLATE'])
            original, original_mask = ds.ReadAsArray(), ds.GetRasterBand(1).GetMaskBand().ReadAsArray() == 0
            extracted, extracted_mask = result.ReadAsArray(), result.GetRasterBand(1).GetMaskBand().ReadAsArray() == 0
            if not all_checks(compare_arrays(original, original_mask, extracted, extracted_mask)):
                raise ValueError('Archive extraction changed numerical data')
            if not ds.GetSpatialRef().IsSame(result.GetSpatialRef()) or ds.GetGeoTransform() != result.GetGeoTransform():
                raise ValueError('Archive extraction changed CRS/grid')
            result = None
            cases.append((name, {'kind': 'retained', 'source': archive.name,
                                 'source_layer': uri.rsplit(':', 1)[-1],
                                 'vertical_reference': 'unknown; names are not evidence of datum/units'}))
        after = {p.relative_to(source).as_posix(): digest(p) for p in archive.rglob('*') if p.is_file()}
        if hashes != after:
            raise ValueError('Source archive changed')
        provenance.append({'source': archive.name, 'sha256': hashes, 'unchanged': True})
    manifest = {'schema': 'FG_RASTER_EXPERIMENT_1', 'cases': [], 'sources': provenance,
                'creation': {'gpkg_version': '1.3', 'tile_format': 'TIFF for float; PNG for integer',
                             'resampling': 'none', 'pixel_cast': 'none requested'}, 'sha256': {}}
    for name, context in cases:
        tif = payload / (name + '.tif')
        ds, values, nodata_mask = read(tif)
        np.savez_compressed(payload / (name + '.npz'), values=values, mask=nodata_mask)
        b = ds.GetRasterBand(1)
        case = dict(id=name, tif=tif.name, oracle=name + '.npz', gpkg=name + '.gpkg', layer='terrain',
                    pixel_type=gdal.GetDataTypeName(b.DataType), wkt=ds.GetProjection(),
                    geotransform=ds.GetGeoTransform(), band_unit=b.GetUnitType(),
                    scale=b.GetScale() or 1., offset=b.GetOffset() or 0., **context)
        fmt = 'PNG' if case['pixel_type'] == 'Int16' else 'TIFF'
        notices = []
        gdal.PushErrorHandler(lambda level, code, message: notices.append({'level': level, 'code': code, 'message': safe_error(message)}))
        try:
            gdal.Translate(str(payload / case['gpkg']), ds, format='GPKG',
                           creationOptions=['VERSION=1.3', 'RASTER_TABLE=terrain', 'TILE_FORMAT=' + fmt])
        except Exception as error:
            case['creation_error'] = safe_error(error)
        finally:
            gdal.PopErrorHandler()
        case['creation_notices'] = notices
        manifest['cases'].append(case)
    for p in sorted(payload.iterdir()):
        if p.is_file(): manifest['sha256'][p.name] = digest(p)
    save_json(payload / 'manifest.json', manifest)


def run_tests(run_id):
    manifest = verify_payload()
    run = new_run(run_id)
    results = []
    def attempt(case, route, operation):
        try:
            checks = operation()
            results.append({'case': case['id'], 'route': route,
                            'status': 'PASS' if all_checks(checks) else 'FAIL', 'checks': checks})
        except Exception as error:
            results.append({'case': case['id'], 'route': route, 'status': 'ERROR', 'error': safe_error(error)})
        save_json(run / 'checks.json', results)
    # Use a temporary QGIS profile; do not load user plugins or modify their settings.
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    from qgis.core import (QgsApplication, QgsRasterLayer, Qgis, QgsRasterPipe,
                           QgsRasterFileWriter, QgsCoordinateTransformContext)
    from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
    (LAB / 'scratch').mkdir(exist_ok=True)
    profile_path = LAB / 'scratch' / run_id / 'qgis-profile'
    profile_path.mkdir(parents=True, exist_ok=False)
    with nullcontext(str(profile_path)) as profile:
        app = QgsApplication([], False, profile); app.initQgis()
        s = osr.SpatialReference(); s.ImportFromEPSG(26914)
        runtime = {'gdal': gdal.VersionInfo('--version'), 'qgis': Qgis.QGIS_VERSION,
                   'python': sys.version.split()[0], 'numpy': np.__version__,
                   'proj': '.'.join(map(str, (osr.GetPROJVersionMajor(), osr.GetPROJVersionMinor(), osr.GetPROJVersionMicro()))),
                   'payload_manifest_sha256': digest(LAB / 'payload/manifest.json')}
        if os.environ.get('PROJ_DATA'):
            db = Path(os.environ['PROJ_DATA']) / 'proj.db'
            runtime['proj_database_sha256'] = digest(db)
            with sqlite3.connect(db.as_uri() + '?mode=ro', uri=True) as connection:
                runtime['proj_database_metadata'] = dict(connection.execute('select key,value from metadata'))
        save_json(run / 'runtime.json', runtime)
        for case in manifest['cases']:
            attempt(case, 'gdal_geotiff_control', lambda: check(case, LAB / 'payload' / case['tif']))
            attempt(case, 'gdal_gpkg_read', lambda: check(case, LAB / 'payload' / case['gpkg']))
            def roundtrip():
                out = run / (case['id'] + '_roundtrip.tif')
                gdal.Translate(str(out), str(LAB / 'payload' / case['gpkg']), format='GTiff', creationOptions=['COMPRESS=DEFLATE'])
                return check(case, out)
            attempt(case, 'gdal_gpkg_to_geotiff', roundtrip)
            def qgis_read():
                layer = QgsRasterLayer(str(LAB / 'payload' / case['gpkg']), case['id'], 'gdal')
                if not layer.isValid(): raise ValueError('QGIS raster layer invalid')
                provider = layer.dataProvider()
                w, h = layer.width(), layer.height()
                block = provider.block(1, layer.extent(), w, h)
                values = np.fromiter((block.value(r, c) for r in range(h) for c in range(w)), dtype='float64').reshape(h, w)
                mask = np.fromiter((block.isNoData(r, c) for r in range(h) for c in range(w)), dtype=bool).reshape(h, w)
                expected, expected_mask = oracle(case)
                result = compare_arrays(expected, expected_mask, values, mask)
                qcrs = osr.SpatialReference(wkt=layer.crs().toWkt())
                result['crs_semantic'] = bool(osr.SpatialReference(wkt=case['wkt']).IsSame(qcrs))
                extent = layer.extent()
                result.update(grid_check(case['geotransform'], [extent.xMinimum(), layer.rasterUnitsPerPixelX(), 0., extent.yMaximum(), 0., -layer.rasterUnitsPerPixelY()]))
                result['one_band'] = layer.bandCount() == 1
                return result
            attempt(case, 'qgis_native_block_read', qgis_read)
            def qgis_export():
                layer = QgsRasterLayer(str(LAB / 'payload' / case['gpkg']), case['id'], 'gdal')
                if not layer.isValid(): raise ValueError('QGIS raster layer invalid')
                out = run / (case['id'] + '_qgis.tif')
                pipe = QgsRasterPipe(); pipe.set(layer.dataProvider().clone())
                writer = QgsRasterFileWriter(str(out)); writer.setOutputFormat('GTiff')
                writer.setCreationOptions(['COMPRESS=DEFLATE'])
                status = writer.writeRaster(pipe, layer.width(), layer.height(), layer.extent(),
                                            layer.crs(), QgsCoordinateTransformContext())
                if int(status) != 0: raise ValueError('QGIS writer status: ' + str(status))
                return check(case, out)
            attempt(case, 'qgis_export_to_geotiff', qgis_export)
            def qgis_calculate():
                layer = QgsRasterLayer(str(LAB / 'payload' / case['gpkg']), case['id'], 'gdal')
                if not layer.isValid(): raise ValueError('QGIS raster layer invalid')
                entry = QgsRasterCalculatorEntry(); entry.ref = 'terrain@1'; entry.raster = layer; entry.bandNumber = 1
                out = run / (case['id'] + '_calculated.tif')
                calc = QgsRasterCalculator('"terrain@1" * 2', str(out), 'GTiff', layer.extent(),
                                           layer.crs(), layer.width(), layer.height(), [entry], QgsCoordinateTransformContext())
                if int(calc.processCalculation()) != 0: raise ValueError(calc.lastError())
                expected, expected_mask = oracle(case)
                ds, actual, actual_mask = read(out)
                result = compare_arrays(expected.astype('float64') * 2, expected_mask, actual, actual_mask)
                result.update(grid_check(case['geotransform'], ds.GetGeoTransform()))
                result['crs_semantic'] = bool(osr.SpatialReference(wkt=case['wkt']).IsSame(ds.GetSpatialRef()))
                return result
            attempt(case, 'qgis_raster_calculator_times_two', qgis_calculate)
            def validate():
                from osgeo_utils.samples.validate_gpkg import GPKGChecker
                checker = GPKGChecker(str(LAB / 'payload' / case['gpkg']))
                checker.check()
                return {'specification': not checker.errors}
            attempt(case, 'gpkg_structure', validate)
        first = manifest['cases'][0]
        def mixed_container():
            target = run / 'mixed.gpkg'
            for i, case in enumerate(manifest['cases'][:2]):
                options = ['VERSION=1.3', 'RASTER_TABLE=' + case['id'], 'TILE_FORMAT=TIFF']
                if i: options.append('APPEND_SUBDATASET=YES')
                gdal.Translate(str(target), str(LAB / 'payload' / case['tif']), format='GPKG', creationOptions=options)
            vector = ogr.Open(str(target), update=1)
            s = osr.SpatialReference(); s.ImportFromEPSG(26914)
            layer = vector.CreateLayer('stream_fixture', s, ogr.wkbLineString)
            layer.CreateField(ogr.FieldDefn('artifact_id', ogr.OFTString))
            feature = ogr.Feature(layer.GetLayerDefn()); feature.SetField('artifact_id', 'synthetic-stream-1')
            feature.SetGeometry(ogr.CreateGeometryFromWkt('LINESTRING (500001 4499999,500002 4499998)'))
            layer.CreateFeature(feature); feature = None; layer = None; vector = None
            result = {}
            for case in manifest['cases'][:2]:
                result[case['id'] + '_unchanged_after_append'] = all_checks(check(case, 'GPKG:%s:%s' % (target, case['id'])))
                raster = QgsRasterLayer('GPKG:%s:%s' % (target, case['id']), case['id'], 'gdal')
                result[case['id'] + '_qgis_named_layer'] = raster.isValid()
            vector = ogr.Open(str(target))
            layer = vector.GetLayerByName('stream_fixture')
            result['vector_attributes'] = layer.GetNextFeature().GetField('artifact_id') == 'synthetic-stream-1'
            result['two_raster_subdatasets'] = len(gdal.Open(str(target)).GetSubDatasets()) == 2
            with sqlite3.connect(target.as_uri() + '?mode=ro', uri=True) as connection:
                result['sqlite_integrity'] = connection.execute('pragma integrity_check').fetchone()[0] == 'ok'
                result['foreign_keys'] = not connection.execute('pragma foreign_key_check').fetchall()
            return result
        attempt(first, 'mixed_container_append_and_discovery', mixed_container)
    # Move only disposable copies; verify standalone data, not dependent on original path/sidecars.
    relocated = LAB / 'scratch' / run_id / 'relocated with spaces'
    relocated.mkdir(exist_ok=False)
    with nullcontext(str(relocated)) as folder:
        for case in manifest['cases']:
            def relocate():
                target = Path(folder) / case['gpkg']; shutil.copyfile(LAB / 'payload' / case['gpkg'], target)
                return check(case, target)
            attempt(case, 'relocated_gpkg_without_sidecars', relocate)
    verify_payload()
    app.exitQgis()
    save_json(run / 'completion.json', {'completed': True, 'checks': len(results),
              'counts': {s: sum(r['status'] == s for r in results) for s in ('PASS', 'FAIL', 'ERROR')}})
    print('Results:', run.name, {s: sum(r['status'] == s for r in results) for s in ('PASS', 'FAIL', 'ERROR')})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', type=Path, help='fluvgeodata inst/extdata directory; refuses existing payload')
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    preflight = osr.SpatialReference(); preflight.ImportFromEPSG(26914)
    if args.prepare: create_payload(args.prepare.resolve())
    run_tests(args.run)
