# File: preprocessing/test/test_standard_scaler.py

import unittest
import numpy as np
from sklearn.preprocessing import StandardScaler as SklearnStandardScaler
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from preprocessing.standard_scaler import StandardScaler  # Ensure you have your implementation in the scalers module

class TestStandardScaler(unittest.TestCase):
    def test_standard_scaler(self):
        # Test data
        X = np.array([[1, 2], [3, 4], [5, 6]])

        # Our implementation
        scaler = StandardScaler()
        our_scaled = scaler.fit_transform(X)

        # Scikit-Learn implementation
        sk_scaler = SklearnStandardScaler()
        sk_scaled = sk_scaler.fit_transform(X)

        # Compare results
        np.testing.assert_almost_equal(our_scaled, sk_scaled)
        print("StandardScaler: OK" if np.allclose(our_scaled, sk_scaled) else "StandardScaler: WRONG")

if __name__ == '__main__':
    unittest.main()
