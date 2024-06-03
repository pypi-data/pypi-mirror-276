import numpy as np


class RidgeRegression:
    """
    Ridge Regression model.

    Parameters
    ----------
    alpha : float, optional, default: 1.0
        Regularization strength; must be a positive float.
    fit_intercept : bool, optional, default: True
        Whether to calculate the intercept for this model. If set to False,
        no intercept will be used in calculations.
    copy_X : bool, optional, default: True
        If True, X will be copied; else, it may be overwritten.

    Attributes
    ----------
    coef_ : array, shape (n_features,)
        Estimated coefficients for the linear regression problem.
    intercept_ : float
        Independent term in the linear model.
    """

    def __init__(self, alpha=1.0, fit_intercept=True, copy_X=True):
        if alpha <= 0:
            raise ValueError("Regularization strength alpha must be positive")
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.copy_X = copy_X
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        """
        Fit Ridge regression model.

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
            X = np.hstack([np.ones((X.shape[0], 1)), X])

        # Ridge regression closed-form solution
        A = X.T @ X + self.alpha * np.eye(X.shape[1])
        b = X.T @ y
        self.coef_ = np.linalg.solve(A, b)

        if self.fit_intercept:
            self.intercept_ = self.coef_[0]
            self.coef_ = self.coef_[1:]
        else:
            self.intercept_ = 0

        return self

    def predict(self, X):
        """
        Predict using the ridge regression model.

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
            'alpha': self.alpha,
            'fit_intercept': self.fit_intercept,
            'copy_X': self.copy_X,
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
