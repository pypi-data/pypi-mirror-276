# File: preprocessing/ordinal_encoder.py

import numpy as np
import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.encoder import Encoder
import numpy as np

class OrdinalEncoder(Encoder):
    """
    Encode categorical features as an integer array.

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
        Fit OrdinalEncoder to X.

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
        Transform X using ordinal encoding.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to encode.

        Returns
        -------
        X_out : ndarray of shape (n_samples, n_features)
            Transformed input.
        """
        X_out = np.empty(X.shape, dtype=int)
        for i in range(X.shape[1]):
            categories = self.categories_[i]
            X_out[:, i] = np.searchsorted(categories, X[:, i])
        return X_out

    def fit_transform(self, X, y=None):
        """
        Fit to data, then transform it.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to fit and transform.

        Returns
        -------
        X_out : ndarray of shape (n_samples, n_features)
            Transformed input.
        """
        return self.fit(X).transform(X)

    def inverse_transform(self, X):
        """
        Transform ordinal encoded data back to original feature values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The ordinal encoded data.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Inverse transformed array.
        """
        X_out = np.empty(X.shape, dtype=object)
        for i in range(X.shape[1]):
            categories = self.categories_[i]
            X_out[:, i] = categories[X[:, i]]
        return X_out
