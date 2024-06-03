import numpy as np
from scipy import sparse

class Binarizer:
    """
    Binarize data (set feature values to 0 or 1) according to a threshold.

    Values greater than the threshold map to 1, while values less than
    or equal to the threshold map to 0. With the default threshold of 0,
    only positive values map to 1.

    Parameters
    ----------
    threshold : float, default=0.0
        Feature values below or equal to this are replaced by 0, above it by 1.

    copy : bool, default=True
        Set to False to perform inplace binarization and avoid a copy (if
        the input is already a numpy array or a scipy.sparse CSR matrix).

    Attributes
    ----------
    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during fit.
    """

    def __init__(self, threshold=0.0, copy=True):
        self.threshold = threshold
        self.copy = copy
        self.n_features_in_ = None
        self.feature_names_in_ = None

    def fit(self, X, y=None):
        """
        Validate the parameters and the input data.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data to validate.

        y : None
            Ignored.

        Returns
        -------
        self : object
            Fitted transformer.
        """
        X = self._validate_data(X, reset=True)
        self.n_features_in_ = X.shape[1]
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)
        return self

    def transform(self, X, copy=None):
        """
        Binarize each element of X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data to binarize, element by element.

        copy : bool, default=None
            Copy the input X or not.

        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Transformed array.
        """
        copy = self.copy if copy is None else copy
        X = self._validate_data(X, copy=copy)
        if sparse.issparse(X):
            return self._transform_sparse(X, copy=copy)
        else:
            return self._transform_dense(X, copy=copy)

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
        return self.fit(X, y).transform(X, copy=self.copy)

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
        return {"threshold": self.threshold, "copy": self.copy}

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

    def _validate_data(self, X, reset=False, copy=True):
        """
        Validate input data.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data to validate.

        reset : bool, default=False
            Whether to reset the internal attributes or not.

        copy : bool, default=True
            Copy the input X or not.

        Returns
        -------
        X : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Validated data.
        """
        if sparse.issparse(X):
            if not sparse.isspmatrix_csr(X) and not sparse.isspmatrix_csc(X):
                X = X.tocsr() if copy else X
        else:
            X = np.array(X, copy=copy)
        return X

    def _transform_dense(self, X, copy=True):
        """
        Binarize dense matrix.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Dense data to binarize.

        Returns
        -------
        X_bin : ndarray of shape (n_samples, n_features)
            Binarized data.
        """
        if copy:
            X = X.copy()
        return np.where(X > self.threshold, 1, 0)

    def _transform_sparse(self, X, copy=True):
        """
        Binarize sparse matrix.

        Parameters
        ----------
        X : sparse matrix of shape (n_samples, n_features)
            Sparse data to binarize.

        Returns
        -------
        X_bin : sparse matrix of shape (n_samples, n_features)
            Binarized data.
        """
        if copy:
            X = X.copy()
        X.data = np.where(X.data > self.threshold, 1, 0)
        return X
