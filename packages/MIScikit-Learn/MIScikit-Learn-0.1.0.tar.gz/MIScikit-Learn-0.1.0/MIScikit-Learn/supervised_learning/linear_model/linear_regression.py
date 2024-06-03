import numpy as np
from numpy.linalg import svd


class LinearRegression:
    """
    Linear Regression model.

    Parameters
    ----------
    fit_intercept : bool, optional, default: True
        Whether to calculate the intercept for this model. If set to False,
        no intercept will be used in calculations.
    copy_X : bool, optional, default: True
        If True, X will be copied; else, it may be overwritten.
    n_jobs : int, optional, default: None
        The number of jobs to use for the computation. This will only provide
        a speedup for n_targets > 1 and sufficiently large problems.
    positive : bool, optional, default: False
        When set to True, forces the coefficients to be positive.

    Attributes
    ----------
    coef_ : array, shape (n_features,)
        Estimated coefficients for the linear regression problem.
    intercept_ : float
        Independent term in the linear model.
    """

    def __init__(self, fit_intercept=True, copy_X=True, n_jobs=None, positive=False):
        self.fit_intercept = fit_intercept
        self.copy_X = copy_X
        self.n_jobs = n_jobs
        self.positive = positive
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        """
        Fit linear model.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data.
        y : array-like, shape (n_samples,)
            Target values.

        Returns
        -------
        self : returns an instance of self.
        """
        if self.copy_X:
            X = X.copy()

        if self.fit_intercept:
            # Add a column of ones for the intercept
            X = np.hstack([np.ones((X.shape[0], 1)), X])

        # Compute the SVD of X for the solution
        U, s, Vt = svd(X, full_matrices=False)
        s_inv = np.diag(1 / s)
        X_pinv = Vt.T @ s_inv @ U.T
        self.coef_ = X_pinv @ y

        if self.fit_intercept:
            self.intercept_ = self.coef_[0]
            self.coef_ = self.coef_[1:]
        else:
            self.intercept_ = 0

        return self

    def predict(self, X):
        """
        Predict using the linear model.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Samples.

        Returns
        -------
        C : array, shape (n_samples,)
            Returns predicted values.
        """
        if self.fit_intercept:
            return np.dot(X, self.coef_) + self.intercept_
        else:
            return np.dot(X, self.coef_)

    def score(self, X, y):
        """
        Return the coefficient of determination R^2 of the prediction.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Test samples.
        y : array-like, shape (n_samples,)
            True values for X.

        Returns
        -------
        score : float
            R^2 of self.predict(X) wrt. y.
        """
        y_pred = self.predict(X)
        u = ((y - y_pred) ** 2).sum()
        v = ((y - y.mean()) ** 2).sum()
        return 1 - u / v

    def get_params(self, deep=True):
        """
        Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, optional, default: True
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.
        """
        return {
            'fit_intercept': self.fit_intercept,
            'copy_X': self.copy_X,
            'n_jobs': self.n_jobs,
            'positive': self.positive,
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
