"""Forensic return analysis; never overrides the strict handoff integrity gate.

Reads with GDAL auxiliary metadata disabled and reports every integrity discrepancy.
Outputs are diagnostic evidence, not an accepted compatibility profile.
"""
import argparse
import sqlite3
import sys
from collections import Counter
import numpy as np
from open_source import gdal, osr, check
from common import (LAB, contained, digest, load_json, save_json, verify_payload,
                    oracle, compare_arrays, all_checks, safe_error)


def main(run_name):
    manifest = verify_payload()
    run = contained(LAB / 'results', run_name)
    destination = run / 'return-analysis.json'
    if destination.exists():
        raise FileExistsError(destination)
    runtime = load_json(run / 'runtime.json')
    if runtime['payload_manifest_sha256'] != digest(LAB / 'payload/manifest.json'):
        raise ValueError('Payload manifest mismatch')
    if not load_json(run / 'completion.json')['completed']:
        raise ValueError('Incomplete ArcGIS run')
    cases = {c['id']: c for c in manifest['cases']}
    hashes = load_json(run / 'artifact-checksums.json')
    before = {p: digest(contained(run, p)) if contained(run, p).is_file() else None
              for p in hashes}
    mismatches = [{'path': p, 'expected': h, 'observed': before[p]}
                  for p, h in hashes.items() if before[p] != h]
    # Do not consult or regenerate potentially changed .aux.xml sidecars.
    gdal.SetConfigOption('GDAL_PAM_ENABLED', 'NO')
    reconciliation = []
    for row in load_json(run / 'checks.json'):
        result = {k: row[k] for k in ('case', 'route', 'status')}
        if 'checks' in row:
            checks = row['checks']
            result['original_false_checks'] = [k for k, v in checks.items() if v is False]
            # ArcGIS appends coordinate-domain settings after the CRS WKT.
            # Compare the horizontal CRS, not those storage precision settings.
            expected = osr.SpatialReference(wkt=cases[row['case']]['wkt'])
            observed = osr.SpatialReference()
            observed.ImportFromESRI([checks['observed_crs_wkt'].split(';', 1)[0]])
            result['horizontal_crs_semantic'] = bool(expected.IsSame(observed))
            result['other_recorded_checks_pass'] = all_checks({
                k: v for k, v in checks.items() if k != 'crs_arcpy_equal'})
        else:
            result['error'] = row['error']
        reconciliation.append(result)
    exports = []
    for output in load_json(run / 'outputs.json'):
        path = contained(run, output['path'])
        uri = str(path)
        if output.get('format') == 'OpenFileGDB':
            uri = 'OpenFileGDB:"%s":%s' % (path, output['layer'])
        elif output.get('format') == 'GPKG':
            uri = 'GPKG:%s:%s' % (path, output['layer'])
        record = dict(output)
        related = [p for p in hashes if p == output['path'] or
                   p.startswith(output['path'] + '/') or p.startswith(output['path'] + '.')]
        record['related_artifact_hashes_match'] = bool(related) and all(before[p] == hashes[p] for p in related)
        record['mismatched_related_files'] = [p for p in related if before[p] != hashes[p]]
        try:
            ds = gdal.Open(uri)
            record['bands'] = ds.RasterCount
            record['shape'] = [ds.RasterYSize, ds.RasterXSize]
            record['band_types'] = [gdal.GetDataTypeName(ds.GetRasterBand(i).DataType)
                                    for i in range(1, ds.RasterCount + 1)]
            record['band_units'] = [ds.GetRasterBand(i).GetUnitType()
                                    for i in range(1, ds.RasterCount + 1)]
            b = ds.GetRasterBand(1)
            a = b.ReadAsArray(); mask = b.GetMaskBand().ReadAsArray() == 0
            valid = a[~mask]
            record['band1_valid_range'] = [float(valid.min()), float(valid.max())] if valid.size else []
            record['band1_nodata_cells'] = int(mask.sum())
            expected, emask = oracle(cases[output['case']])
            record['band1_diagnostic_comparison'] = compare_arrays(expected, emask, a, mask)
            ds = None
            try:
                comparisons = check(cases[output['case']], uri)
                record['comparisons'] = comparisons
                record['comparison_status'] = 'PASS' if all_checks(comparisons) else 'FAIL'
            except Exception as error:
                record['comparison_status'] = 'ERROR'
                record['comparison_error'] = safe_error(error)
            if output.get('format') == 'GPKG':
                with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as con:
                    record['contents'] = con.execute('SELECT table_name,data_type,srs_id FROM gpkg_contents').fetchall()
                    record['extensions'] = con.execute('SELECT extension_name FROM gpkg_extensions').fetchall() if con.execute("SELECT 1 FROM sqlite_master WHERE name='gpkg_extensions'").fetchone() else []
                    record['terrain_tile_signature'] = con.execute('SELECT hex(substr(tile_data,1,12)) FROM terrain LIMIT 1').fetchone()
        except Exception as error:
            record['comparison_status'] = 'ERROR'
            record['comparison_error'] = safe_error(error)
        exports.append(record)
    after = {p: digest(contained(run, p)) if contained(run, p).is_file() else None
             for p in hashes}
    if before != after:
        raise ValueError('Returned artifacts changed during inspection')
    result = {
        'scope': 'Diagnostic reconciliation, not strict integrity acceptance; auxiliary metadata disabled',
        'runtime': {'gdal': gdal.VersionInfo('--version'), 'python': sys.version.split()[0],
                    'numpy': np.__version__, 'proj': '.'.join(str(f()) for f in
                    (osr.GetPROJVersionMajor, osr.GetPROJVersionMinor, osr.GetPROJVersionMicro))},
        'payload_manifest_sha256': digest(LAB / 'payload/manifest.json'),
        'input_record_sha256': {p: digest(run / p) for p in
                               ('runtime.json', 'checks.json', 'outputs.json', 'completion.json', 'artifact-checksums.json')},
        'artifact_count': len(hashes), 'matching_artifacts': len(hashes) - len(mismatches),
        'integrity_mismatches': mismatches, 'raw_artifacts_unchanged_by_review': before == after,
        'arcgis_reconciliation': reconciliation, 'export_comparisons': exports,
        'export_comparison_counts': dict(Counter(r['comparison_status'] for r in exports))}
    save_json(destination, result)
    print('Diagnostic return analysis:', result['export_comparison_counts'],
          'integrity discrepancies:', len(mismatches))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--run', required=True)
    main(parser.parse_args().run)
