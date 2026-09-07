"""Shared numerical oracle; no GIS runtime dependency. Not a production adapter."""
import hashlib
import json
from pathlib import Path
import numpy as np

LAB = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=True,
                                   allow_nan=False) + '\n', encoding='utf-8')


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def contained(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Path escapes declared root')
    return path


def verify_payload():
    manifest = load_json(LAB / 'payload/manifest.json')
    if manifest['schema'] != 'FG_RASTER_EXPERIMENT_1':
        raise ValueError('Unknown experiment schema')
    for relative, expected in manifest['sha256'].items():
        if digest(contained(LAB / 'payload', relative)) != expected:
            raise ValueError('Payload checksum mismatch: ' + relative)
    return manifest


def oracle(case):
    with np.load(contained(LAB / 'payload', case['oracle']), allow_pickle=False) as d:
        return d['values'].copy(), d['mask'].copy()


def compare_arrays(expected, expected_mask, actual, actual_mask):
    result = {'shape': list(expected.shape) == list(actual.shape)}
    if not result['shape']:
        return result
    result['nodata_mask'] = bool(np.array_equal(expected_mask, actual_mask))
    # Compare all originally valid cells, even if a candidate mislabels one NoData.
    valid = ~expected_mask
    result['exact_valid_values'] = bool(np.array_equal(expected[valid], actual[valid]))
    differences = np.abs(expected[valid].astype('float64') - actual[valid].astype('float64'))
    maximum = float(np.max(differences)) if differences.size else 0.0
    result['max_abs_difference'] = maximum if np.isfinite(maximum) else None
    result['valid_zero_count'] = int(np.count_nonzero(valid & (expected == 0)))
    return result


def grid_check(expected, actual):
    expected = np.asarray(expected, dtype='float64')
    actual = np.asarray(actual, dtype='float64')
    # Representation allowance only, not permission to shift or resample a grid.
    tolerance = 32 * np.finfo('float64').eps * max(1., float(np.max(np.abs(expected))))
    difference = float(np.max(np.abs(expected - actual)))
    return {'grid': bool(difference <= tolerance), 'grid_max_difference': difference,
            'grid_tolerance': float(tolerance)}


def all_checks(result):
    checks = [v for v in result.values() if isinstance(v, bool)]
    return bool(checks) and all(checks)


def safe_error(error):
    text = str(error)
    for root in (str(LAB), str(LAB).replace('\\', '/'), str(LAB).replace('\\', '\\\\')):
        text = text.replace(root, '<experiment>')
    return text[:3000]


def new_run(name):
    if not name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in name):
        raise ValueError('Run ID must contain only letters, numbers, hyphens or underscores')
    path = LAB / 'results' / name
    path.mkdir(parents=True, exist_ok=False)
    return path
