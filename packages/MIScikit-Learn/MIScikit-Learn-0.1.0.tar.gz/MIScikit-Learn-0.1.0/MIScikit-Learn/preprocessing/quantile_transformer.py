# File: preprocessing/quantile_transformer.py

import numpy as np
from scipy import sparse
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted

class QuantileTransformer:
    """
    Transform features using quantiles information.

    Parameters
    ----------
    n_quantiles : int, default=1000
        Number of quantiles to be computed.

    output_distribution : {'uniform', 'normal'}, default='uniform'
        Marginal distribution for the transformed data.

    ignore_implicit_zeros : bool, default=False
        Only applies to sparse matrices. If True, sparse entries are discarded to compute quantile statistics.

    subsample : int or None, default=10000
        Maximum number of samples used to estimate the quantiles for computational efficiency.

    random_state : int, RandomState instance or None, default=None
        Seed used by the random number generator for reproducibility.

    copy : bool, default=True
        Set to False to perform in-place transformation and avoid a copy.

    Attributes
    ----------
    n_quantiles_ : int
        The actual number of quantiles used to discretize the cumulative distribution function.

    quantiles_ : ndarray of shape (n_quantiles, n_features)
        The values corresponding to the quantiles of reference.

    references_ : ndarray of shape (n_quantiles, )
        Quantiles of references.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during fit.
    """

    def __init__(self, n_quantiles=1000, output_distribution='uniform', ignore_implicit_zeros=False, subsample=10000, random_state=None, copy=True):
        self.n_quantiles = n_quantiles
        self.output_distribution = output_distribution
        self.ignore_implicit_zeros = ignore_implicit_zeros
        self.subsample = subsample
        self.random_state = random_state
        self.copy = copy

    def fit(self, X, y=None):
        """
        Compute the quantiles used for transforming.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to scale along the features axis.

        y : None
            Ignored.

        Returns
        -------
        self : object
            Fitted transformer.
        """
        X = check_array(X, accept_sparse='csc')
        n_samples, n_features = X.shape

        if self.subsample is None:
            subsample = n_samples
        else:
            subsample = min(self.subsample, n_samples)

        if self.n_quantiles > subsample:
            self.n_quantiles = subsample

        rng = np.random.RandomState(self.random_state)
        self.references_ = np.linspace(0, 1, self.n_quantiles, endpoint=True)

        self.quantiles_ = np.zeros((self.n_quantiles, n_features))

        for feature_idx in range(n_features):
            column = X[:, feature_idx].toarray().ravel() if sparse.issparse(X) else X[:, feature_idx]
            if self.ignore_implicit_zeros:
                column = column[column != 0]
            if subsample < n_samples:
                column = rng.choice(column, size=subsample, replace=False)
            self.quantiles_[:, feature_idx] = np.percentile(column, self.references_ * 100)

        self.n_features_in_ = n_features
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)

        return self

    def transform(self, X):
        """
        Feature-wise transformation of the data.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to scale along the features axis.

        Returns
        -------
        Xt : {ndarray, sparse matrix} of shape (n_samples, n_features)
            The projected data.
        """
        check_is_fitted(self, ['quantiles_', 'references_'])
        X = check_array(X, accept_sparse='csc', copy=self.copy)

        n_samples, n_features = X.shape
        Xt = np.zeros_like(X)

        for feature_idx in range(n_features):
            column = X[:, feature_idx].toarray().ravel() if sparse.issparse(X) else X[:, feature_idx]
            ranks = np.searchsorted(self.quantiles_[:, feature_idx], column, side='right') - 1
            ranks = np.clip(ranks, 0, self.n_quantiles - 1)
            cdf_values = self.references_[ranks]

            if self.output_distribution == 'uniform':
                Xt[:, feature_idx] = cdf_values
            elif self.output_distribution == 'normal':
                Xt[:, feature_idx] = np.percentile(np.random.randn(1000000), cdf_values * 100)

        return Xt

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
        X_new : ndarray of shape (n_samples, n_features_new)
            Transformed array.
        """
        return self.fit(X, y).transform(X)

    def inverse_transform(self, X):
        """
        Back-projection to the original space.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to scale along the features axis.

        Returns
        -------
        Xt : {ndarray, sparse matrix} of (n_samples, n_features)
            The projected data.
        """
        check_is_fitted(self, ['quantiles_', 'references_'])
        X = check_array(X, accept_sparse='csc', copy=self.copy)

        n_samples, n_features = X.shape
        Xt = np.zeros_like(X)

        for feature_idx in range(n_features):
            column = X[:, feature_idx].toarray().ravel() if sparse.issparse(X) else X[:, feature_idx]
            if self.output_distribution == 'uniform':
                quantile_values = np.percentile(self.quantiles_[:, feature_idx], column * 100)
            elif self.output_distribution == 'normal':
                quantile_values = np.percentile(np.random.randn(1000000), column * 100)

            Xt[:, feature_idx] = quantile_values

        return Xt

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
        check_is_fitted(self, ['n_features_in_'])
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
        return {"n_quantiles": self.n_quantiles, "output_distribution": self.output_distribution, 
                "ignore_implicit_zeros": self.ignore_implicit_zeros, "subsample": self.subsample, 
                "random_state": self.random_state, "copy": self.copy}

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
