# File: preprocessing/robust_scaler.py

import numpy as np

import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.scaler import Scaler

class RobustScaler(Scaler):
    """
    Scale features using statistics that are robust to outliers.

    Parameters
    ----------
    with_centering : bool, default=True
        If True, center the data before scaling.

    with_scaling : bool, default=True
        If True, scale the data to interquartile range.

    quantile_range : tuple (q_min, q_max), default=(25.0, 75.0)
        Quantile range used to calculate scale_.

    copy : bool, default=True
        If False, try to avoid a copy and do inplace scaling instead.

    unit_variance : bool, default=False
        If True, scale data so that normally distributed features have a variance of 1.

    Attributes
    ----------
    center_ : array of floats
        The median value for each feature in the training set.

    scale_ : array of floats
        The (scaled) interquartile range for each feature in the training set.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during fit.
    """

    def __init__(self, with_centering=True, with_scaling=True, quantile_range=(25.0, 75.0), copy=True, unit_variance=False):
        self.with_centering = with_centering
        self.with_scaling = with_scaling
        self.quantile_range = quantile_range
        self.copy = copy
        self.unit_variance = unit_variance
        self.center_ = None
        self.scale_ = None
        self.n_features_in_ = None
        self.feature_names_in_ = None

    def fit(self, X, y=None):
        """
        Compute the median and quantiles to be used for scaling.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to compute the median and quantiles used for later scaling.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            Fitted scaler.
        """
        X = np.asarray(X)
        self.n_features_in_ = X.shape[1]
        if self.with_centering:
            self.center_ = np.median(X, axis=0)
        if self.with_scaling:
            q_min, q_max = self.quantile_range
            q_min = np.percentile(X, q_min, axis=0)
            q_max = np.percentile(X, q_max, axis=0)
            self.scale_ = q_max - q_min
            if self.unit_variance:
                self.scale_ /= np.sqrt(2) * 1.349
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)
        return self

    def transform(self, X):
        """
        Center and scale the data.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to scale along the specified axis.

        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Transformed array.
        """
        X = np.asarray(X, dtype=np.float64)  # Ensure X is float64
        if self.copy:
            X = X.copy()
        if self.with_centering:
            X -= self.center_
        if self.with_scaling:
            X /= self.scale_
        return X

    def fit_transform(self, X, y=None, **fit_params):
        """
        Fit to data, then transform it.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input samples.

        y : array-like of shape (n_samples,) or (n_samples, n_outputs), default=None
            Target values (None for unsupervised transformations).

        **fit_params : dict
            Additional fit parameters.

        Returns
        -------
        X_new : ndarray array of shape (n_samples, n_features_new)
            Transformed array.
        """
        return self.fit(X, y, **fit_params).transform(X)

    def inverse_transform(self, X):
        """
        Scale back the data to the original representation.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The rescaled data to be transformed back.

        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Transformed array.
        """
        X = np.asarray(X, dtype=np.float64)  # Ensure X is float64
        if self.copy:
            X = X.copy()
        if self.with_scaling:
            X *= self.scale_
        if self.with_centering:
            X += self.center_
        return X

    def get_feature_names_out(self, input_features=None):
        """
        Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Input features.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Same as input features.
        """
        if input_features is None:
            if self.feature_names_in_ is None:
                input_features = [f"x{i}" for i in range(self.n_features_in_)]
            else:
                input_features = self.feature_names_in_
        return np.array(input_features)

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
        return {"with_centering": self.with_centering, "with_scaling": self.with_scaling, 
                "quantile_range": self.quantile_range, "copy": self.copy, "unit_variance": self.unit_variance}

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
