import unittest
import numpy as np

import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from preprocessing.iterative_imputer import IterativeImputer

class TestIterativeImputer(unittest.TestCase):
    def setUp(self):
        self.data_with_nan = np.array([
            [1, 2, np.nan],
            [3, np.nan, 6],
            [7, 8, 9]
        ])
        self.complete_data = np.array([
            [1, 2, 3],
            [3, 4, 6],
            [7, 8, 9]
        ])

    def test_imputation(self):
        imputer = IterativeImputer(max_iter=10, random_state=0)
        imputed_data = imputer.fit_transform(self.data_with_nan)
        expected_result = self.complete_data  # assuming this is the expected imputed result
        np.testing.assert_array_almost_equal(imputed_data, expected_result, decimal=1)

    def test_transform_without_fit(self):
        imputer = IterativeImputer(max_iter=10, random_state=0)
        with self.assertRaises(ValueError):
            imputer.transform(self.data_with_nan)

if __name__ == '__main__':
    unittest.main()
