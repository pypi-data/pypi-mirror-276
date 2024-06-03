# File: preprocessing/test/polynomial_features_test.py

import numpy as np
from sklearn.preprocessing import PolynomialFeatures as SklearnPolynomialFeatures
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from preprocessing.polynomial_features import PolynomialFeatures

def test_polynomial_features():
    # Sample data
    X = np.arange(6).reshape(3, 2)

    # Parameters for the polynomial features
    degree = 2
    interaction_only = False
    include_bias = True
    order = 'C'

    # Scikit-learn's PolynomialFeatures
    sklearn_poly = SklearnPolynomialFeatures(degree=degree, interaction_only=interaction_only, 
                                             include_bias=include_bias, order=order)
    sklearn_result = sklearn_poly.fit_transform(X)

    # Custom PolynomialFeatures
    custom_poly = PolynomialFeatures(degree=degree, interaction_only=interaction_only, 
                                     include_bias=include_bias, order=order)
    custom_result = custom_poly.fit_transform(X)

    # Print results for comparison
    print("Scikit-learn PolynomialFeatures result:")
    print(sklearn_result)
    print("\nCustom PolynomialFeatures result:")
    print(custom_result)

    # Check if the results are the same
    assert np.array_equal(sklearn_result, custom_result), "The results are not the same!"

if __name__ == "__main__":
    test_polynomial_features()
