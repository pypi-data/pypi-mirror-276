import numpy as np
from scipy import sparse

import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.scaler import Scaler


class MaxAbsScaler(Scaler):
    """
    Scale each feature by its maximum absolute value.

    Attributes
    ----------
    scale_ : ndarray of shape (n_features,)
        Per feature maximum absolute value.
    """

    def __init__(self):
        self.scale_ = None

    def fit(self, X):
        """
        Compute the maximum absolute value to be used for later scaling.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data used to compute the per-feature maximum absolute value.

        Returns
        -------
        self : object
            Fitted scaler.
        """
        X = np.asarray(X)
        self.scale_ = np.abs(X).max(axis=0)
        return self

    def transform(self, X):
        """
        Scale features of X by maximum absolute value.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data that will be transformed.

        Returns
        -------
        X_tr : ndarray of shape (n_samples, n_features)
            Transformed array.
        """
        X = np.asarray(X, dtype=np.float64)
        X_tr = X / self.scale_
        return X_tr

    def fit_transform(self, X, y=None):
        """
        Fit to data, then transform it.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input samples.

        y : array-like of shape (n_samples,) or (n_samples, n_outputs), default=None
            Target values (None for unsupervised transformations).

        Returns
        -------
        X_new : ndarray of shape (n_samples, n_features_new)
            Transformed array.
        """
        return self.fit(X).transform(X)

    def inverse_transform(self, X):
        """
        Undo the scaling of X according to maximum absolute value.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data that will be inverse-transformed.

        Returns
        -------
        X_tr : ndarray of shape (n_samples, n_features)
            Inverse-transformed array.
        """
        X = np.asarray(X, dtype=np.float64)
        X_tr = X * self.scale_
        return X_tr
