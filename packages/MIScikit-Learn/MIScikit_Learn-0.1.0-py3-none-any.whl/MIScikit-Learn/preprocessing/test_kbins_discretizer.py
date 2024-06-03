import unittest
import numpy as np
from kbins_discretizer import KBinsDiscretizer

class TestKBinsDiscretizer(unittest.TestCase):
    def setUp(self):
        self.X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
            [13, 14, 15]
        ])
        self.discretizer_uniform = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
        self.discretizer_quantile = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile')
        self.discretizer_kmeans = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='kmeans', random_state=42)

    def test_uniform_strategy(self):
        self.discretizer_uniform.fit(self.X)
        X_trans = self.discretizer_uniform.transform(self.X)
        expected_trans = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 1, 1],
            [2, 2, 2],
            [2, 2, 2]
        ])
        np.testing.assert_array_equal(X_trans, expected_trans)

    def test_quantile_strategy(self):
        self.discretizer_quantile.fit(self.X)
        X_trans = self.discretizer_quantile.transform(self.X)
        expected_trans = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 1, 1],
            [2, 2, 2],
            [2, 2, 2]
        ])
        np.testing.assert_array_equal(X_trans, expected_trans)

    def test_kmeans_strategy(self):
        self.discretizer_kmeans.fit(self.X)
        X_trans = self.discretizer_kmeans.transform(self.X)
        expected_trans = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 1, 1],
            [2, 2, 2],
            [2, 2, 2]
        ])
        np.testing.assert_array_equal(X_trans, expected_trans)

    def test_inverse_transform(self):
        self.discretizer_uniform.fit(self.X)
        X_trans = self.discretizer_uniform.transform(self.X)
        X_inv = self.discretizer_uniform.inverse_transform(X_trans)
        np.testing.assert_array_almost_equal(self.X, X_inv, decimal=1)

    def test_get_set_params(self):
        discretizer = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
        params = discretizer.get_params()
        self.assertEqual(params['n_bins'], 3)
        self.assertEqual(params['encode'], 'ordinal')

        discretizer.set_params(n_bins=5, strategy='quantile')
        self.assertEqual(discretizer.n_bins, 5)
        self.assertEqual(discretizer.strategy, 'quantile')

if __name__ == "__main__":
    unittest.main()
