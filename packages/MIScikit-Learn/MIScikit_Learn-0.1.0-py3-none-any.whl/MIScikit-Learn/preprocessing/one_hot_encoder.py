import numpy as np
from scipy import sparse

import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.encoder import Encoder


class OneHotEncoder(Encoder):
    """
    Encode categorical integer features as a one-hot numeric array.

    Parameters
    ----------
    categories : 'auto' or list of array-like, default='auto'
        Categories (unique values) per feature:
        - 'auto' : Determine categories automatically from the training data.
        - list : `categories[i]` holds the categories expected in the ith column.

    Attributes
    ----------
    categories_ : list of arrays
        The categories of each feature determined during fitting.
    """

    def __init__(self, categories='auto'):
        self.categories = categories

    def fit(self, X, y=None):
        """
        Fit OneHotEncoder to X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to determine the categories of each feature.

        Returns
        -------
        self
        """
        if self.categories == 'auto':
            self.categories_ = [np.unique(X[:, i]) for i in range(X.shape[1])]
        else:
            self.categories_ = self.categories
        return self

    def transform(self, X):
        """
        Transform X using one-hot encoding.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to encode.

        Returns
        -------
        X_out : sparse matrix of shape (n_samples, n_encoded_features)
            Transformed input.
        """
        n_samples, n_features = X.shape
        X_out = []
        for i in range(n_features):
            feature = X[:, i]
            categories = self.categories_[i]
            X_out.append(np.array([np.isin(categories, v).astype(int) for v in feature]))

        return np.hstack(X_out)

    def fit_transform(self, X, y=None):
        """
        Fit to data, then transform it.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to fit and transform.

        Returns
        -------
        X_out : sparse matrix of shape (n_samples, n_encoded_features)
            Transformed input.
        """
        return self.fit(X).transform(X)

    def inverse_transform(self, X):
        """
        Transform one-hot encoded data back to original feature values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_encoded_features)
            The one-hot encoded data.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Inverse transformed array.
        """
        n_samples = X.shape[0]
        n_features = len(self.categories_)
        X_out = np.empty((n_samples, n_features), dtype=object)

        start_idx = 0
        for i, categories in enumerate(self.categories_):
            end_idx = start_idx + len(categories)
            one_hot_features = X[:, start_idx:end_idx]
            X_out[:, i] = categories[np.argmax(one_hot_features, axis=1)]
            start_idx = end_idx

        return X_out
