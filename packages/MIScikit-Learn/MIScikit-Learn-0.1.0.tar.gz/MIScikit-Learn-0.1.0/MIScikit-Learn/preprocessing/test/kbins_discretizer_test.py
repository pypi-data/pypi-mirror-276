# File: preprocessing/test/kbins_discretizer_test.py

import numpy as np
from sklearn.preprocessing import KBinsDiscretizer as SklearnKBinsDiscretizer
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from preprocessing.kbins_discretizer import KBinsDiscretizer

def test_kbins_discretizer():
    # Sample data
    X = np.array([[-2, 1, -4, -1],
                  [-1, 2, -3, -0.5],
                  [0, 3, -2, 0.5],
                  [1, 4, -1, 2]])

    # Parameters for the discretizer
    n_bins = 3
    encode = 'ordinal'
    strategy = 'uniform'

    # Scikit-learn's KBinsDiscretizer
    sklearn_discretizer = SklearnKBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy)
    sklearn_result = sklearn_discretizer.fit_transform(X)

    # Custom KBinsDiscretizer
    custom_discretizer = KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy)
    custom_result = custom_discretizer.fit_transform(X)

    # Print results for comparison
    print("Scikit-learn KBinsDiscretizer result:")
    print(sklearn_result)
    print("\nCustom KBinsDiscretizer result:")
    print(custom_result)

    # Check if the results are the same
    assert np.array_equal(sklearn_result, custom_result), "The results are not the same!"

if __name__ == "__main__":
    test_kbins_discretizer()
