# File: preprocessing/polynomial_features.py

import numpy as np
from itertools import combinations_with_replacement
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted

class PolynomialFeatures:
    """
    Generate polynomial and interaction features.

    Parameters
    ----------
    degree : int or tuple (min_degree, max_degree), default=2
        If a single int is given, it specifies the maximal degree of the polynomial features. 
        If a tuple (min_degree, max_degree) is passed, then min_degree is the minimum and 
        max_degree is the maximum polynomial degree of the generated features.

    interaction_only : bool, default=False
        If True, only interaction features are produced.

    include_bias : bool, default=True
        If True, then include a bias column, the feature in which all polynomial powers are zero.

    order : {'C', 'F'}, default='C'
        Order of output array in the dense case.

    Attributes
    ----------
    powers_ : ndarray of shape (n_output_features_, n_features_in_)
        Exponent for each of the inputs in the output.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during fit.
        
    n_output_features_ : int
        The total number of polynomial output features.
    """

    def __init__(self, degree=2, interaction_only=False, include_bias=True, order='C'):
        self.degree = degree
        self.interaction_only = interaction_only
        self.include_bias = include_bias
        self.order = order

    def fit(self, X, y=None):
        """
        Compute number of output features.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            Fitted transformer.
        """
        X = check_array(X, accept_sparse=True)
        self.n_features_in_ = X.shape[1]
        self.powers_ = self._combinations()
        self.n_output_features_ = len(self.powers_)
        if hasattr(X, 'columns'):
            self.feature_names_in_ = np.array(X.columns)
        return self

    def transform(self, X):
        """
        Transform data to polynomial features.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data to transform, row by row.

        Returns
        -------
        XP : {ndarray, sparse matrix} of shape (n_samples, NP)
            The matrix of features, where NP is the number of polynomial features generated 
            from the combination of inputs.
        """
        check_is_fitted(self, 'powers_')
        X = check_array(X, accept_sparse=True)

        if X.shape[1] != self.n_features_in_:
            raise ValueError("Number of features of the input must be equal to the number of features seen during fit.")

        XP = self._transform(X)
        return XP

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
        check_is_fitted(self, 'powers_')
        if input_features is None:
            if self.feature_names_in_ is None:
                input_features = [f"x{i}" for i in range(self.n_features_in_)]
            else:
                input_features = self.feature_names_in_
        feature_names = []
        for power in self.powers_:
            name = " ".join([f"{input_features[i]}^{p}" if p > 1 else input_features[i]
                             for i, p in enumerate(power) if p > 0])
            if name == "":
                name = "1"
            feature_names.append(name)
        return np.array(feature_names)

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
        return {"degree": self.degree, "interaction_only": self.interaction_only, 
                "include_bias": self.include_bias, "order": self.order}

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

    def _combinations(self):
        """
        Generate combinations of feature indices.

        Returns
        -------
        combinations : list of tuples
            Each tuple is a combination of feature indices with their corresponding powers.
        """
        if isinstance(self.degree, int):
            min_degree = 0 if self.include_bias else 1
            max_degree = self.degree
        else:
            min_degree, max_degree = self.degree

        comb = []
        for degree in range(min_degree, max_degree + 1):
            for combination in combinations_with_replacement(range(self.n_features_in_), degree):
                if self.interaction_only and len(set(combination)) < degree:
                    continue
                comb.append(np.bincount(combination, minlength=self.n_features_in_))
        
        return np.array(comb)

    def _transform(self, X):
        """
        Transform data to polynomial features.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data to transform.

        Returns
        -------
        XP : ndarray of shape (n_samples, n_features_new)
            Transformed data.
        """
        n_samples = X.shape[0]
        XP = np.empty((n_samples, self.n_output_features_), order=self.order)

        for i, comb in enumerate(self.powers_):
            XP[:, i] = np.prod(X ** comb, axis=1)

        return XP