"""Run here after retrieving a committed ArcGIS run; independently reads exports."""
import argparse
from open_source import check
from common import LAB, load_json, save_json, verify_payload, contained, digest, all_checks, safe_error


def main(run_name):
    manifest = verify_payload()
    cases = {c['id']: c for c in manifest['cases']}
    run = contained(LAB / 'results', run_name)
    if load_json(run / 'runtime.json')['payload_manifest_sha256'] != digest(LAB / 'payload/manifest.json'):
        raise ValueError('ArcGIS run used another payload manifest')
    if not load_json(run / 'completion.json')['completed']:
        raise ValueError('Incomplete ArcGIS run')
    for relative, expected in load_json(run / 'artifact-checksums.json').items():
        if digest(contained(run, relative)) != expected:
            raise ValueError('Returned artifact changed: ' + relative)
    destination = run / 'independent-gdal-review.json'
    if destination.exists(): raise FileExistsError(destination)
    rows = []
    for output in load_json(run / 'outputs.json'):
        path = contained(run, output['path'])
        if output.get('format') == 'OpenFileGDB':
            path = 'OpenFileGDB:"%s":%s' % (path, output['layer'])
        elif output.get('format') == 'GPKG':
            path = 'GPKG:%s:%s' % (path, output['layer'])
        try:
            checks = check(cases[output['case']], path)
            row = dict(output, status='PASS' if all_checks(checks) else 'FAIL', checks=checks)
        except Exception as error:
            row = dict(output, status='ERROR', error=safe_error(error))
        rows.append(row)
    save_json(destination, rows)
    print('Independent review saved:', destination.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--run', required=True)
    main(parser.parse_args().run)
