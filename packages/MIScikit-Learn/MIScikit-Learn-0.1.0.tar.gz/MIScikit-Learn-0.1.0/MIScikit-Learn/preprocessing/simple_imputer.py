import numpy as np

import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.imputer import Imputer

from sklearn.utils import check_array

class SimpleImputer(Imputer):
    """
    SimpleImputer for completing missing values.

    Parameters
    ----------
    missing_values : scalar, string, np.nan (default), or None
        The placeholder for the missing values. All occurrences of
        `missing_values` will be imputed.

    strategy : string, default='mean'
        The imputation strategy.
        - If "mean", then replace missing values using the mean along
          each column. Can only be used with numeric data.
        - If "median", then replace missing values using the median along
          each column. Can only be used with numeric data.
        - If "most_frequent", then replace missing using the most frequent
          value along each column. Can be used with strings or numeric data.
        - If "constant", then replace missing values with fill_value. Can be
          used with strings or numeric data.

    fill_value : string or numerical value, default=None
        When strategy == "constant", fill_value is used to replace all
        occurrences of missing_values. If left to the default, fill_value
        will be 0 when imputing numerical data and "missing_value" for strings
        or object data types.

    Attributes
    ----------
    statistics_ : array of shape (n_features,)
        The imputation fill value for each feature.
    """

    def __init__(self, missing_values=np.nan, strategy="mean", fill_value=None):
        self.missing_values = missing_values
        self.strategy = strategy
        self.fill_value = fill_value
        self.statistics_ = None

    def fit(self, X, y=None):
        """
        Fit the imputer on X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input data to complete.

        y : Ignored

        Returns
        -------
        self : object
            Fitted imputer.
        """
        X = check_array(X, dtype=np.float64, force_all_finite=False)

        if self.strategy == "mean":
            self.statistics_ = np.nanmean(X, axis=0)
        elif self.strategy == "median":
            self.statistics_ = np.nanmedian(X, axis=0)
        elif self.strategy == "most_frequent":
            self.statistics_ = [np.nan if np.isnan(col).all() else np.bincount(col[~np.isnan(col)].astype(int)).argmax() for col in X.T]
        elif self.strategy == "constant":
            if self.fill_value is not None:
                self.statistics_ = np.full(X.shape[1], self.fill_value)
            else:
                self.statistics_ = np.zeros(X.shape[1]) if np.issubdtype(X.dtype, np.number) else np.full(X.shape[1], "missing_value")
        else:
            raise ValueError(f"Invalid strategy '{self.strategy}'")

        return self

    def transform(self, X):
        """
        Impute all missing values in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input data to complete.

        Returns
        -------
        X_imputed : array of shape (n_samples, n_features)
            The imputed dataset.
        """
        X = check_array(X, dtype=np.float64, force_all_finite=False)
        X_imputed = X.copy()

        for i, stat in enumerate(self.statistics_):
            mask = np.isnan(X[:, i])
            X_imputed[mask, i] = stat

        return X_imputed

    def fit_transform(self, X, y=None):
        """
        Fit the imputer on X, then transform X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input data to complete.

        y : Ignored

        Returns
        -------
        X_imputed : array of shape (n_samples, n_features)
            The imputed dataset.
        """
        return self.fit(X, y).transform(X)

    def get_params(self, deep=True):
        """
        Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, default=True
            If True, will return the parameters for this estimator and contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.
        """
        return {
            "missing_values": self.missing_values,
            "strategy": self.strategy,
            "fill_value": self.fill_value
        }

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
        """
        for key, value in params.items():
            setattr(self, key, value)
        return self
