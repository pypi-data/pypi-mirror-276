# File: preprocessing/test/label_encoder_test.py

import unittest
import numpy as np
from sklearn.preprocessing import LabelEncoder as SklearnLabelEncoder
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from preprocessing.label_encoder import LabelEncoder

class TestLabelEncoder(unittest.TestCase):
    def setUp(self):
        # Example data setup
        self.data_numeric = [1, 2, 2, 6]
        self.data_categorical = ["paris", "paris", "tokyo", "amsterdam"]

    def test_numeric_labels(self):
        # Initialize both encoders
        custom_encoder = LabelEncoder()
        sklearn_encoder = SklearnLabelEncoder()

        # Fit and transform the data
        custom_encoded = custom_encoder.fit_transform(self.data_numeric)
        sklearn_encoded = sklearn_encoder.fit_transform(self.data_numeric)

        # Check if both outputs are identical
        np.testing.assert_array_equal(custom_encoded, sklearn_encoded)
        print("Numeric Labels: OK" if np.array_equal(custom_encoded, sklearn_encoded) else "Numeric Labels: WRONG")

        # Check inverse transform
        custom_decoded = custom_encoder.inverse_transform(custom_encoded)
        sklearn_decoded = sklearn_encoder.inverse_transform(sklearn_encoded)
        np.testing.assert_array_equal(custom_decoded, sklearn_decoded)
        print("Inverse Numeric Labels: OK" if np.array_equal(custom_decoded, sklearn_decoded) else "Inverse Numeric Labels: WRONG")

    def test_categorical_labels(self):
        # Initialize both encoders
        custom_encoder = LabelEncoder()
        sklearn_encoder = SklearnLabelEncoder()

        # Fit and transform the data
        custom_encoded = custom_encoder.fit_transform(self.data_categorical)
        sklearn_encoded = sklearn_encoder.fit_transform(self.data_categorical)

        # Check if both outputs are identical
        np.testing.assert_array_equal(custom_encoded, sklearn_encoded)
        print("Categorical Labels: OK" if np.array_equal(custom_encoded, sklearn_encoded) else "Categorical Labels: WRONG")

        # Check inverse transform
        custom_decoded = custom_encoder.inverse_transform(custom_encoded)
        sklearn_decoded = sklearn_encoder.inverse_transform(sklearn_encoded)
        np.testing.assert_array_equal(custom_decoded, sklearn_decoded)
        print("Inverse Categorical Labels: OK" if np.array_equal(custom_decoded, sklearn_decoded) else "Inverse Categorical Labels: WRONG")

if __name__ == '__main__':
    unittest.main()
