import unittest
import numpy as np
from common import compare_arrays, all_checks, grid_check, contained, LAB


class OracleTests(unittest.TestCase):
    def test_exact(self):
        a = np.array([[0., -1., .125, -9999.]])
        m = a == -9999
        self.assertTrue(all_checks(compare_arrays(a, m, a.copy(), m.copy())))

    def test_corruption(self):
        a = np.array([[0., .125]])
        m = np.zeros(a.shape, bool)
        self.assertFalse(all_checks(compare_arrays(a, m, a + .001, m)))
        self.assertFalse(all_checks(compare_arrays(a, m, a, ~m)))
        self.assertFalse(all_checks(compare_arrays(a, m, a.T, m.T)))

    def test_grid_shift(self):
        self.assertFalse(grid_check([0, 1, 0, 2, 0, -1], [.5, 1, 0, 2, 0, -1])['grid'])

    def test_path_escape(self):
        with self.assertRaises(ValueError): contained(LAB, '../outside')


if __name__ == '__main__': unittest.main()
