"""Synthetic handoff/reviewer checks; never represented as ArcGIS evidence."""
import shutil
import unittest
import uuid
from unittest.mock import patch
import common
import inspect_return


class ReturnReviewTests(unittest.TestCase):
    def setUp(self):
        original = common.LAB
        self.lab = original / 'scratch' / ('review-test-' + uuid.uuid4().hex)
        payload = self.lab / 'payload'
        payload.mkdir(parents=True)
        case = common.verify_payload()['cases'][0]
        for name in (case['tif'], case['oracle']):
            shutil.copyfile(original / 'payload' / name, payload / name)
        common.save_json(payload / 'manifest.json', {
            'schema': 'FG_RASTER_EXPERIMENT_1', 'cases': [case],
            'sha256': {p.name: common.digest(p) for p in payload.iterdir()}})
        self.run = self.lab / 'results' / 'simulated'
        self.run.mkdir(parents=True)
        shutil.copyfile(payload / case['tif'], self.run / 'returned.tif')
        common.save_json(self.run / 'runtime.json', {
            'payload_manifest_sha256': common.digest(payload / 'manifest.json')})
        common.save_json(self.run / 'completion.json', {'completed': True})
        common.save_json(self.run / 'artifact-checksums.json', {
            'returned.tif': common.digest(self.run / 'returned.tif')})
        common.save_json(self.run / 'outputs.json', [{
            'case': case['id'], 'route': 'simulated_control', 'path': 'returned.tif'}])
        for module in (common, inspect_return):
            replacement = patch.object(module, 'LAB', self.lab)
            replacement.start()
            self.addCleanup(replacement.stop)

    def test_exact_return_and_no_overwrite(self):
        inspect_return.main('simulated')
        rows = common.load_json(self.run / 'independent-gdal-review.json')
        self.assertEqual(rows[0]['status'], 'PASS')
        with self.assertRaises(FileExistsError):
            inspect_return.main('simulated')

    def test_altered_return_rejected(self):
        # Corrupt only the disposable artifact, not a source or committed file.
        with (self.run / 'returned.tif').open('ab') as stream:
            stream.write(b'changed')
        with self.assertRaisesRegex(ValueError, 'artifact changed'):
            inspect_return.main('simulated')

    def test_incomplete_return_rejected(self):
        common.save_json(self.run / 'completion.json', {'completed': False})
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            inspect_return.main('simulated')


if __name__ == '__main__':
    unittest.main()
