import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.utils import check_random_state, check_array, Bunch
from sklearn.metrics import pairwise_distances
from scipy import stats

class KNNImputer:
    def __init__(self, n_neighbors=5, weights='uniform', metric='nan_euclidean', missing_values=np.nan, copy=True, add_indicator=False):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.metric = metric
        self.missing_values = missing_values
        self.copy = copy
        self.add_indicator = add_indicator
        self.output_format = 'default'  # 'pandas' or 'polars' could be other options

    def fit(self, X, y=None):
        X = check_array(X, accept_sparse=False, dtype=np.float64, force_all_finite=False, copy=self.copy)
        self.X_fit_ = X
        self.n_features_in_ = X.shape[1]
        self.feature_names_in_ = ['x{}'.format(i) for i in range(X.shape[1])]
        return self

    def transform(self, X):
        X = check_array(X, accept_sparse=False, dtype=np.float64, force_all_finite=False, copy=self.copy)
        return self._impute(X)

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X).transform(X)

    def _impute(self, X):
        for i in range(X.shape[1]):
            missing = np.isnan(X[:, i])
            if np.any(missing):
                distances = pairwise_distances(X[missing, :], self.X_fit_, metric=self.metric)
                ind = np.argsort(distances, axis=1)[:, :self.n_neighbors]
                weights = np.ones_like(ind) if self.weights == 'uniform' else 1 / (distances[:, ind] + 1e-5)
                values = self.X_fit_[ind, i]
                X[missing, i] = np.sum(weights * values, axis=1) / np.sum(weights, axis=1)
        return X

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return np.array(self.feature_names_in_)
        elif isinstance(input_features, (list, np.ndarray)):
            if len(input_features) != len(self.feature_names_in_):
                raise ValueError("input_features length must match number of features during fit.")
            return np.array(input_features)
        else:
            raise TypeError("input_features must be list or numpy ndarray.")

    def get_params(self, deep=True):
        return {'n_neighbors': self.n_neighbors, 'weights': self.weights, 'metric': self.metric, 'missing_values': self.missing_values, 'copy': self.copy, 'add_indicator': self.add_indicator}

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self

    def set_output(self, transform=None):
        valid_outputs = ['default', 'pandas', 'polars']
        if transform in valid_outputs:
            self.output_format = transform
        else:
            raise ValueError("transform must be one of: {}".format(', '.join(valid_outputs)))
        return self