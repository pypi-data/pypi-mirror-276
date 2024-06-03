# File: preprocessing/min_max_scaler.py

import numpy as np

class MinMaxScaler:
    """
    Transform features by scaling each feature to a given range.

    Parameters
    ----------
    feature_range : tuple (min, max), default=(0, 1)
        Desired range of transformed data.

    copy : bool, default=True
        Set to False to perform inplace row normalization and avoid a copy.

    clip : bool, default=False
        Set to True to clip transformed values of held-out data to provided feature range.

    Attributes
    ----------
    min_ : ndarray of shape (n_features,)
        Per feature adjustment for minimum. Equivalent to min - X.min(axis=0) * self.scale_

    scale_ : ndarray of shape (n_features,)
        Per feature relative scaling of the data. Equivalent to (max - min) / (X.max(axis=0) - X.min(axis=0))

    data_min_ : ndarray of shape (n_features,)
        Per feature minimum seen in the data.

    data_max_ : ndarray of shape (n_features,)
        Per feature maximum seen in the data.

    data_range_ : ndarray of shape (n_features,)
        Per feature range (data_max_ - data_min_) seen in the data.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during fit.
    """

    def __init__(self, feature_range=(0, 1), copy=True, clip=False):
        self.feature_range = feature_range
        self.copy = copy
        self.clip = clip
        self.min_ = None
        self.scale_ = None
        self.data_min_ = None
        self.data_max_ = None
        self.data_range_ = None
        self.n_features_in_ = None
        self.feature_names_in_ = None

    def fit(self, X, y=None):
        """
        Compute the minimum and maximum to be used for later scaling.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data used to compute the per-feature minimum and maximum used for later scaling along the features axis.

        y : None
            Ignored.

        Returns
        -------
        self : object
            Fitted scaler.
        """
        X = np.asarray(X)
        self.data_min_ = np.min(X, axis=0)
        self.data_max_ = np.max(X, axis=0)
        self.data_range_ = self.data_max_ - self.data_min_
        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / self.data_range_
        self.min_ = self.feature_range[0] - self.data_min_ * self.scale_
        self.n_features_in_ = X.shape[1]
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)
        return self

    def transform(self, X):
        """
        Scale features of X according to feature_range.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data that will be transformed.

        Returns
        -------
        Xt : ndarray of shape (n_samples, n_features)
            Transformed data.
        """
        X = np.asarray(X, dtype=np.float64)  # Ensure X is float64
        if self.copy:
            X = X.copy()
        X *= self.scale_
        X += self.min_
        if self.clip:
            X = np.clip(X, self.feature_range[0], self.feature_range[1])
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
        return self.fit(X, y).transform(X)

    def inverse_transform(self, X):
        """
        Undo the scaling of X according to feature_range.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data that will be transformed. It cannot be sparse.

        Returns
        -------
        Xt : ndarray of shape (n_samples, n_features)
            Transformed data.
        """
        X = np.asarray(X, dtype=np.float64)  # Ensure X is float64
        if self.copy:
            X = X.copy()
        X -= self.min_
        X /= self.scale_
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
        return {"feature_range": self.feature_range, "copy": self.copy, "clip": self.clip}

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

    def partial_fit(self, X, y=None):
        """
        Online computation of min and max on X for later scaling.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data used to compute the min and max used for later scaling along the features axis.

        y : None
            Ignored.

        Returns
        -------
        self : object
            Fitted scaler.
        """
        X = np.asarray(X)
        if self.data_min_ is None:
            self.data_min_ = np.min(X, axis=0)
            self.data_max_ = np.max(X, axis=0)
        else:
            self.data_min_ = np.minimum(self.data_min_, np.min(X, axis=0))
            self.data_max_ = np.maximum(self.data_max_, np.max(X, axis=0))

        self.data_range_ = self.data_max_ - self.data_min_
        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / self.data_range_
        self.min_ = self.feature_range[0] - self.data_min_ * self.scale_
        self.n_features_in_ = X.shape[1]
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)
        return self
