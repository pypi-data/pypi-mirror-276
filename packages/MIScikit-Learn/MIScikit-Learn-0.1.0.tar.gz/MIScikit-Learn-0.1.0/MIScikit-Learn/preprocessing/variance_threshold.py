import numpy as np

class VarianceThreshold:
    """
    Feature selector that removes all low-variance features.

    Parameters
    ----------
    threshold : float, default=0.0
        Features with a training-set variance lower than this threshold will be removed.

    Attributes
    ----------
    variances_ : ndarray of shape (n_features,)
        Variance of each feature.
    """

    def __init__(self, threshold=0.0):
        self.threshold = threshold
        self.variances_ = None

    def fit(self, X, y=None):
        """
        Fit to data, then transform it.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data to fit.

        y : None
            Ignored. This parameter exists only for compatibility with Pipeline.

        Returns
        -------
        self : object
            Fitted transformer.
        """
        X = np.asarray(X)
        self.variances_ = np.var(X, axis=0, ddof=0)
        return self

    def transform(self, X):
        """
        Transform the data to retain only selected features.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data to transform.

        Returns
        -------
        X_r : {ndarray, sparse matrix} of shape (n_samples, n_selected_features)
            The input samples with only the selected features.
        """
        X = np.asarray(X)
        if self.variances_ is None:
            raise RuntimeError("The model must be fitted before transforming data.")
        return X[:, self.variances_ > self.threshold]

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
        X_new : ndarray of shape (n_samples, n_selected_features)
            Transformed array.
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
        return {"threshold": self.threshold}

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
