import numpy as np
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted

class KBinsDiscretizer:
    """
    Bin continuous data into intervals.

    Parameters
    ----------
    n_bins : int or array-like of shape (n_features,), default=5
        The number of bins to produce. Raises ValueError if n_bins < 2.

    encode : {'onehot', 'onehot-dense', 'ordinal'}, default='onehot'
        Method used to encode the transformed result.

    strategy : {'uniform', 'quantile', 'kmeans'}, default='quantile'
        Strategy used to define the widths of the bins.

    dtype : {np.float32, np.float64}, default=None
        Desired data-type for the output.

    subsample : int or None, default=200000
        Maximum number of samples used to fit the model for computational efficiency.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for subsampling.

    Attributes
    ----------
    bin_edges_ : ndarray of ndarray of shape (n_features,)
        The edges of each bin.

    n_bins_ : ndarray of shape (n_features,), dtype=np.int64
        Number of bins per feature.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during fit.
    """

    def __init__(self, n_bins=5, encode='onehot', strategy='quantile', dtype=None, subsample=200000, random_state=None):
        self.n_bins = n_bins
        self.encode = encode
        self.strategy = strategy
        self.dtype = dtype
        self.subsample = subsample
        self.random_state = random_state

    def fit(self, X, y=None, sample_weight=None):
        """
        Fit the estimator.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Data to be discretized.

        y : None
            Ignored. This parameter exists only for compatibility with Pipeline.

        sample_weight : ndarray of shape (n_samples,)
            Contains weight values to be associated with each sample. Cannot be used when strategy is set to "uniform".

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        X = check_array(X, dtype='numeric', force_all_finite='allow-nan')
        n_samples, n_features = X.shape

        if isinstance(self.n_bins, int):
            self.n_bins_ = np.full(n_features, self.n_bins, dtype=np.int64)
        else:
            self.n_bins_ = np.asarray(self.n_bins, dtype=np.int64)

        if np.any(self.n_bins_ < 2):
            raise ValueError("`n_bins` must be >= 2 for all features.")

        self.bin_edges_ = np.zeros(n_features, dtype=object)

        for i in range(n_features):
            if self.strategy == 'uniform':
                bin_edges = np.linspace(X[:, i].min(), X[:, i].max(), self.n_bins_[i] + 1)
            elif self.strategy == 'quantile':
                quantiles = np.linspace(0, 100, self.n_bins_[i] + 1)
                bin_edges = np.percentile(X[:, i], quantiles)
            elif self.strategy == 'kmeans':
                from sklearn.cluster import KMeans
                kmeans = KMeans(n_clusters=self.n_bins_[i], random_state=self.random_state, n_init='auto')
                kmeans.fit(X[:, [i]])
                bin_edges = np.sort(kmeans.cluster_centers_.flatten())
                bin_edges = np.concatenate(([X[:, i].min()], bin_edges, [X[:, i].max()]))
            else:
                raise ValueError("Invalid strategy: {}".format(self.strategy))
            self.bin_edges_[i] = bin_edges

        self.n_features_in_ = X.shape[1]
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)

        return self

    def transform(self, X):
        """
        Discretize the data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Data to be discretized.

        Returns
        -------
        Xt : {ndarray, sparse matrix}, dtype={np.float32, np.float64}
            Data in the binned space. Will be a sparse matrix if self.encode='onehot' and ndarray otherwise.
        """
        check_is_fitted(self, ['bin_edges_', 'n_bins_', 'n_features_in_'])
        X = check_array(X, dtype='numeric', force_all_finite='allow-nan')

        if X.shape[1] != self.n_features_in_:
            raise ValueError("Number of features of the input must be equal to the number of features seen during fit.")

        bin_indices = np.zeros_like(X, dtype=np.int64)

        for i in range(X.shape[1]):
            bin_indices[:, i] = np.digitize(X[:, i], self.bin_edges_[i][1:-1], right=True)

        if self.encode == 'ordinal':
            return bin_indices.astype(self.dtype)
        elif self.encode in ['onehot', 'onehot-dense']:
            from scipy import sparse
            n_samples, n_features = X.shape
            indices = np.tile(np.arange(n_features), n_samples)
            sample_indices = np.repeat(np.arange(n_samples), n_features)
            feature_indices = bin_indices.ravel()
            data = np.ones(n_samples * n_features)
            onehot = sparse.coo_matrix((data, (sample_indices, feature_indices)), shape=(n_samples, np.sum(self.n_bins_)))
            if self.encode == 'onehot':
                return onehot
            else:
                return onehot.toarray().astype(self.dtype)
        else:
            raise ValueError("Invalid encoding method: {}".format(self.encode))

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

    def inverse_transform(self, X=None, *, Xt=None):
        """
        Transform discretized data back to original feature space.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Transformed data in the binned space.

        Xt : array-like of shape (n_samples, n_features)
            Transformed data in the binned space.

        Returns
        -------
        Xinv : ndarray, dtype={np.float32, np.float64}
            Data in the original feature space.
        """
        check_is_fitted(self, ['bin_edges_', 'n_bins_', 'n_features_in_'])

        if Xt is not None:
            import warnings
            warnings.warn("Xt was deprecated in version 1.5 and will be removed in 1.7. Use X instead.", DeprecationWarning)
            X = Xt

        if X is None:
            raise ValueError("Either X or Xt must be provided.")

        X = check_array(X, dtype='numeric', force_all_finite='allow-nan')

        Xinv = np.zeros_like(X, dtype=self.dtype)

        for i in range(X.shape[1]):
            bin_edges = self.bin_edges_[i]
            midpoints = (bin_edges[:-1] + bin_edges[1:]) / 2
            Xinv[:, i] = midpoints[X[:, i].astype(np.int64)]

        return Xinv

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
            Transformed feature names.
        """
        if input_features is None:
            if self.feature_names_in_ is None:
                return np.array([f"x{i}" for i in range(self.n_features_in_)])
            return self.feature_names_in_
        return np.asarray(input_features)

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
        return {"n_bins": self.n_bins, "encode": self.encode, "strategy": self.strategy, "dtype": self.dtype, "subsample": self.subsample, "random_state": self.random_state}

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
