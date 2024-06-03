# import unittest
# import numpy as np
# from scalers import StandardScaler, MinMaxScaler
# from sklearn.preprocessing import StandardScaler as SklearnStandardScaler, MinMaxScaler as SklearnMinMaxScaler

# class TestStandardScaler(unittest.TestCase):
#     def test_standard_scaler(self):
#         # Test data
#         X = np.array([[1, 2], [3, 4], [5, 6]])

#         # Our implementation
#         scaler = StandardScaler()
#         our_scaled = scaler.fit_transform(X)

#         # Scikit-Learn implementation
#         sk_scaler = SklearnStandardScaler()
#         sk_scaled = sk_scaler.fit_transform(X)

#         # Compare results
#         np.testing.assert_almost_equal(our_scaled, sk_scaled)
#         print("StandardScaler: OK" if np.allclose(our_scaled, sk_scaled) else "StandardScaler: WRONG")

# class TestMinMaxScaler(unittest.TestCase):
#     def test_min_max_scaler(self):
#         # Test data
#         X = np.array([[1, 2], [3, 4], [5, 6]])

#         # Our implementation
#         scaler = MinMaxScaler()
#         our_scaled = scaler.fit_transform(X)

#         # Scikit-Learn implementation
#         sk_scaler = SklearnMinMaxScaler()
#         sk_scaled = sk_scaler.fit_transform(X)

#         # Compare results
#         np.testing.assert_almost_equal(our_scaled, sk_scaled)
#         print("MinMaxScaler: OK" if np.allclose(our_scaled, sk_scaled) else "MinMaxScaler: WRONG")

# if __name__ == '__main__':
#     unittest.main()

import unittest
import numpy as np
from sklearn.preprocessing import OrdinalEncoder as SklearnOrdinalEncoder
from encoders import OrdinalEncoder  

class TestOrdinalEncoder(unittest.TestCase):
    def setUp(self):
        # Example data setup
        self.data = np.array([
            ['low', 'medium', 'high'],
            ['medium', 'high', 'low'],
            ['high', 'low', 'medium']
        ]).T  # Transpose to align samples along the first axis as expected

    def test_fit_transform(self):
        # Initialize both encoders
        custom_encoder = OrdinalEncoder()
        sklearn_encoder = SklearnOrdinalEncoder()

        # Fit and transform the data
        custom_encoded = custom_encoder.fit_transform(self.data)
        sklearn_encoded = sklearn_encoder.fit_transform(self.data)

        # Check if both outputs are identical
        np.testing.assert_array_equal(custom_encoded, sklearn_encoded, "Custom encoder results differ from Sklearn's OrdinalEncoder")

    def test_handle_unknown_error(self):
        # Test handling of unknown categories
        custom_encoder = OrdinalEncoder(handle_unknown='error')
        sklearn_encoder = SklearnOrdinalEncoder(handle_unknown='error')

        # Fit the encoder
        custom_encoder.fit(self.data[:-1])  # Fit without the last sample
        sklearn_encoder.fit(self.data[:-1])

        # Attempt to transform all data and expect an error for the unknown category
        with self.assertRaises(ValueError):
            custom_encoded = custom_encoder.transform(self.data)

        with self.assertRaises(ValueError):
            sklearn_encoded = sklearn_encoder.transform(self.data)

    def test_handle_unknown_use_encoded(self):
        # Initialize both encoders to use a specific unknown value
        unknown_value = -1
        custom_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=unknown_value)
        sklearn_encoder = SklearnOrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=unknown_value)

        # Fit the encoder
        custom_encoder.fit(self.data[:-1])  # Fit without the last sample
        sklearn_encoder.fit(self.data[:-1])

        # Transform the data, should use `unknown_value` for unknown categories
        custom_encoded = custom_encoder.transform(self.data)
        sklearn_encoded = sklearn_encoder.transform(self.data)

        # Check if both outputs are identical and correctly use the unknown value
        np.testing.assert_array_equal(custom_encoded, sklearn_encoded, "Handling of unknown values differs between custom and Sklearn implementations")

if __name__ == '__main__':
    unittest.main()

