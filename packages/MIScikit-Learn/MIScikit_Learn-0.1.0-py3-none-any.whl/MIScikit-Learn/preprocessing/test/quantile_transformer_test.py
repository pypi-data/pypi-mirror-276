# File: preprocessing/test/quantile_transformer_test.py

import numpy as np
from sklearn.preprocessing import QuantileTransformer as SklearnQuantileTransformer
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from preprocessing.quantile_transformer import QuantileTransformer

def test_quantile_transformer():
    # Sample data
    rng = np.random.RandomState(0)
    X = np.sort(rng.normal(loc=0.5, scale=0.25, size=(25, 1)), axis=0)

    # Parameters for the quantile transformer
    n_quantiles = 10
    output_distribution = 'uniform'
    ignore_implicit_zeros = False
    subsample = 10000
    random_state = 0
    copy = True

    # Scikit-learn's QuantileTransformer
    sklearn_qt = SklearnQuantileTransformer(n_quantiles=n_quantiles, output_distribution=output_distribution, 
                                            ignore_implicit_zeros=ignore_implicit_zeros, subsample=subsample, 
                                            random_state=random_state, copy=copy)
    sklearn_result = sklearn_qt.fit_transform(X)

    # Custom QuantileTransformer
    custom_qt = QuantileTransformer(n_quantiles=n_quantiles, output_distribution=output_distribution, 
                                    ignore_implicit_zeros=ignore_implicit_zeros, subsample=subsample, 
                                    random_state=random_state, copy=copy)
    custom_result = custom_qt.fit_transform(X)

    # Print results for comparison
    print("Scikit-learn QuantileTransformer result:")
    print(sklearn_result)
    print("\nCustom QuantileTransformer result:")
    print(custom_result)

    # Check if the results are the same
    assert np.allclose(sklearn_result, custom_result), "The results are not the same!"

if __name__ == "__main__":
    test_quantile_transformer()
