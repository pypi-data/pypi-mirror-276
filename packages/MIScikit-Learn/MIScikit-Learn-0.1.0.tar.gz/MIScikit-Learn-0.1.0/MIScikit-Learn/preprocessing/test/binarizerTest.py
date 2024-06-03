# File: preprocessing/test/binarizerTest.py

import numpy as np
from sklearn.preprocessing import Binarizer as SklearnBinarizer
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from preprocessing.binarizer import Binarizer

def test_binarizer():
    # Sample data
    X = np.array([[1.0, -1.0, 2.0],
                  [2.0, 0.0, 0.0],
                  [0.0, 1.0, -1.0]])

    # Threshold value
    threshold = 0.0

    # Scikit-learn's binarizer
    sklearn_binarizer = SklearnBinarizer(threshold=threshold)
    sklearn_result = sklearn_binarizer.fit_transform(X)

    # Custom binarizer
    custom_binarizer = Binarizer(threshold=threshold)
    custom_result = custom_binarizer.fit_transform(X)

    # Print results for comparison
    print("Scikit-learn Binarizer result:")
    print(sklearn_result)
    print("\nCustom Binarizer result:")
    print(custom_result)

    # Check if the results are the same
    assert np.array_equal(sklearn_result, custom_result), "The results are not the same!"

if __name__ == "__main__":
    test_binarizer()
