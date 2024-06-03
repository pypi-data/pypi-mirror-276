import numpy as np
import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.scaler import Scaler

class StandardScaler(Scaler):
    """
    Standardize features by removing the mean and scaling to unit variance.

    Parameters
    ----------
    copy : bool, default=True
        If False, try to avoid a copy and do inplace scaling instead.

    with_mean : bool, default=True
        If True, center the data before scaling.

    with_std : bool, default=True
        If True, scale the data to unit variance.

    Attributes
    ----------
    scale_ : ndarray of shape (n_features,) or None
        Per feature scaling factor to achieve zero mean and unit variance.

    mean_ : ndarray of shape (n_features,) or None
        The mean value for each feature in the training set.

    var_ : ndarray of shape (n_features,) or None
        The variance for each feature in the training set.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during fit.
    """

    def __init__(self, copy=True, with_mean=True, with_std=True):
        self.copy = copy
        self.with_mean = with_mean
        self.with_std = with_std
        self.scale_ = None
        self.mean_ = None
        self.var_ = None
        self.n_features_in_ = None
        self.feature_names_in_ = None
        self.n_samples_seen_ = 0

    def fit(self, X, y=None, sample_weight=None):
        """
        Compute the mean and std to be used for later scaling.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to compute the mean and standard deviation.

        y : None
            Ignored.

        sample_weight : array-like of shape (n_samples,), default=None
            Individual weights for each sample.

        Returns
        -------
        self : object
            Fitted scaler.
        """
        X = np.asarray(X)
        if self.with_mean:
            self.mean_ = np.average(X, axis=0, weights=sample_weight)
        if self.with_std:
            self.var_ = np.average((X - self.mean_) ** 2, axis=0, weights=sample_weight)
            self.scale_ = np.sqrt(self.var_)
        self.n_features_in_ = X.shape[1]
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)
        return self

    def transform(self, X, copy=None):
        """
        Perform standardization by centering and scaling.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to scale along the features axis.

        copy : bool, default=None
            Copy the input X or not.

        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Transformed array.
        """
        copy = self.copy if copy is None else copy
        X = np.asarray(X, dtype=np.float64)  # Ensure X is float64
        if copy:
            X = X.copy()
        if self.with_mean:
            X -= self.mean_
        if self.with_std:
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

    def inverse_transform(self, X, copy=None):
        """
        Scale back the data to the original representation.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to scale along the features axis.

        copy : bool, default=None
            Copy the input X or not.

        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Transformed array.
        """

        copy = self.copy if copy is None else copy
        X = np.asarray(X, dtype=np.float64)  # Ensure X is float64
        if copy:
            X = X.copy()
        if self.with_std:
            X *= self.scale_
        if self.with_mean:
            X += self.mean_
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
        return {"copy": self.copy, "with_mean": self.with_mean, "with_std": self.with_std}

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

    def partial_fit(self, X, y=None, sample_weight=None):
        """
        Online computation of mean and std on X for later scaling.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to compute the mean and standard deviation.

        y : None
            Ignored.

        sample_weight : array-like of shape (n_samples,), default=None
            Individual weights for each sample.

        Returns
        -------
        self : object
            Fitted scaler.
        """
        X = np.asarray(X)
        n_samples, n_features = X.shape

        if self.n_samples_seen_ == 0:
            self.mean_ = np.zeros(n_features)
            self.var_ = np.zeros(n_features)

        if sample_weight is None:
            sample_weight = np.ones(n_samples)

        last_mean = self.mean_.copy()
        last_var = self.var_.copy()

        self.n_samples_seen_ += sample_weight.sum()

        weighted_mean = np.average(X, axis=0, weights=sample_weight)
        self.mean_ = (last_mean * (self.n_samples_seen_ - sample_weight.sum()) + weighted_mean * sample_weight.sum()) / self.n_samples_seen_

        weighted_var = np.average((X - weighted_mean) ** 2, axis=0, weights=sample_weight)
        self.var_ = (last_var * (self.n_samples_seen_ - sample_weight.sum()) + weighted_var * sample_weight.sum()) / self.n_samples_seen_

        if self.with_std:
            self.scale_ = np.sqrt(self.var_)

        return self
