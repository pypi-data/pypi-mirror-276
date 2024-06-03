import unittest
import numpy as np
import sys
import os
from sklearn.impute import SimpleImputer as SklearnSimpleImputer

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from preprocessing.simple_imputer import SimpleImputer

class TestSimpleImputer:
    def __init__(self):
        self.data_with_nan = np.array([
            [1, 2, np.nan],
            [3, np.nan, 6],
            [7, 8, 9]
        ])
        self.strategies = ["mean", "median", "most_frequent", "constant"]

    def run_tests(self):
        for strategy in self.strategies:
            self.plot_imputed_data(strategy)

    def plot_imputed_data(self, strategy):
      custom_imputer = SimpleImputer(strategy=strategy, fill_value=0)
      sklearn_imputer = SklearnSimpleImputer(strategy=strategy, fill_value=0)
      
      custom_imputed = custom_imputer.fit_transform(self.data_with_nan)
      sklearn_imputed = sklearn_imputer.fit_transform(self.data_with_nan)

      np.testing.assert_array_almost_equal(custom_imputed, sklearn_imputed, decimal=1)
      print(f"{strategy.capitalize()} Imputer: OK" if np.allclose(custom_imputed, sklearn_imputed) else f"{strategy.capitalize()} Imputer: WRONG")

      


if __name__ == '__main__':
    tester = TestSimpleImputer()
    tester.run_tests()