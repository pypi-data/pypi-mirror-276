import unittest
import numpy as np
from sklearn.preprocessing import OneHotEncoder as SklearnOneHotEncoder
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from preprocessing.one_hot_encoder import OneHotEncoder

class TestOneHotEncoder(unittest.TestCase):
    def setUp(self):
        # Example data setup
        self.data = np.array([
            ['Male', 1],
            ['Female', 3],
            ['Female', 2]
        ])

    def test_fit_transform(self):
        # Initialize both encoders
        custom_encoder = OneHotEncoder()
        sklearn_encoder = SklearnOneHotEncoder()

        # Fit and transform the data
        custom_encoded = custom_encoder.fit_transform(self.data)
        sklearn_encoded = sklearn_encoder.fit_transform(self.data)

        # Check if both outputs are identical
        np.testing.assert_array_almost_equal(custom_encoded, sklearn_encoded.toarray())

    def test_inverse_transform(self):
        # Initialize the encoder
        custom_encoder = OneHotEncoder()
        sklearn_encoder = SklearnOneHotEncoder()

        # Fit and transform the data
        custom_encoder.fit(self.data)
        sklearn_encoder.fit(self.data)
        custom_encoded = custom_encoder.transform(self.data)
        sklearn_encoded = sklearn_encoder.transform(self.data)

        # Inverse transform the data
        custom_decoded = custom_encoder.inverse_transform(custom_encoded)
        sklearn_decoded = sklearn_encoder.inverse_transform(sklearn_encoded)

        # Check if both outputs are identical
        np.testing.assert_array_equal(custom_decoded, sklearn_decoded)

if __name__ == '__main__':
    unittest.main()
