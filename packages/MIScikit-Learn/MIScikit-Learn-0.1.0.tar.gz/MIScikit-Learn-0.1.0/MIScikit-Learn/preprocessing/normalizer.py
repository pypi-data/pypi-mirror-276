# File: preprocessing/normalizer.py

import numpy as np
from scipy import sparse

import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.normalizer import Normalizer as BaseNormalizer

class Normalizer(BaseNormalizer):
    """
    Normalize samples individually to unit norm.

    Each sample (i.e. each row of the data matrix) with at least one non-zero component is rescaled independently of other samples so that its norm (l1 or l2) equals one.

    Parameters
    ----------
    norm : 'l1' or 'l2', optional, default='l2'
        The norm to use to normalize each non-zero sample.

    copy : bool, optional, default=True
        Set to False to perform inplace row normalization and avoid a copy (if the input is already a numpy array or a scipy.sparse CSR matrix).

    See Also
    --------
    sklearn.preprocessing.normalize : Equivalent function without the estimator API.
    """

    def __init__(self, norm='l2', copy=True):
        self.norm = norm
        self.copy = copy

    def fit(self, X, y=None):
        """
        Do nothing and return the estimator unchanged.

        This method is just there to implement the usual API and hence work in pipelines.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            Fitted transformer.
        """
        return self

    def transform(self, X, y=None, copy=None):
        """
        Scale each non-zero row of X to unit norm.

        Parameters
        ----------
        X : array or scipy.sparse matrix with shape (n_samples, n_features)
            The data to normalize, row by row. scipy.sparse matrices should be in CSR format to avoid an un-necessary copy.

        y : Ignored
            Not used, present here for API consistency by convention.

        copy : bool, optional, default=None
            Set to False to perform inplace normalization and avoid a copy (if the input is already a numpy array or a scipy.sparse CSR matrix). Overrides the copy parameter passed to the constructor.

        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Transformed array.
        """
        if copy is None:
            copy = self.copy

        if sparse.issparse(X):
            if self.norm == 'l1':
                norms = sparse.linalg.norm(X, axis=1, ord=1)
            elif self.norm == 'l2':
                norms = sparse.linalg.norm(X, axis=1, ord=2)
            else:
                raise ValueError("'%s' is not a supported norm" % self.norm)

            if copy:
                X = X.copy()

            non_zero_norms = norms != 0
            if self.norm == 'l1':
                X[non_zero_norms] = X[non_zero_norms].multiply(1.0 / norms[non_zero_norms])
            elif self.norm == 'l2':
                X[non_zero_norms] = X[non_zero_norms].multiply(1.0 / norms[non_zero_norms])

            return X
        else:
            X = np.asarray(X)
            if self.norm == 'l1':
                norms = np.sum(np.abs(X), axis=1)
            elif self.norm == 'l2':
                norms = np.sqrt(np.sum(X ** 2, axis=1))
            else:
                raise ValueError("'%s' is not a supported norm" % self.norm)

            if copy:
                X = X.copy()

            non_zero_norms = norms != 0
            X[non_zero_norms] /= norms[non_zero_norms][:, np.newaxis]

            return X

    def fit_transform(self, X, y=None, **fit_params):
        """
        Fit to data, then transform it.

        Fits transformer to X and y with optional parameters fit_params and returns a transformed version of X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training set.

        y : Ignored
            Not used, present here for API consistency by convention.

        **fit_params : dict
            Additional fit parameters.

        Returns
        -------
        X_new : ndarray of shape (n_samples, n_features)
            Transformed array.
        """
        return self.fit(X, y).transform(X)

    def get_params(self, deep=True):
        """
        Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, optional, default=True
            If True, will return the parameters for this estimator and contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.
        """
        return {"norm": self.norm, "copy": self.copy}

    def set_params(self, **params):
        """
        Set the parameters of this estimator.

        Parameters
        ----------
        **params : dict
            Estimator parameters.

        Returns
        -------
        self : object
            Estimator instance.
        """
        for key, value in params.items():
            setattr(self, key, value)
        return self
