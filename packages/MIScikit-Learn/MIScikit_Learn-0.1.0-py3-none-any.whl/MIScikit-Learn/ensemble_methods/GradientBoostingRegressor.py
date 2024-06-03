import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.tree import DecisionTreeRegressor

class GradientBoostingRegressor(BaseEstimator, RegressorMixin):
    """
    Gradient Boosting Regressor.

    Parameters
    ----------
    n_estimators : int, default=100
        The number of boosting stages to be run.
    learning_rate : float, default=0.1
        Learning rate shrinks the contribution of each tree.
    max_depth : int, default=3
        Maximum depth of the individual regression estimators.
    """
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.models = []
        self.initial_model = None

    def fit(self, X, y):
        """
        Fit the Gradient Boosting Regressor model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : object
        """
        self.models = []
        
        residuals = y.copy()
        self.initial_model = np.mean(y)
        residuals -= self.initial_model

        for _ in range(self.n_estimators):
            model = DecisionTreeRegressor(max_depth=self.max_depth)
            model.fit(X, residuals)
            predictions = model.predict(X)
            residuals -= self.learning_rate * predictions
            self.models.append(model)

        return self

    def predict(self, X):
        """
        Predict using the Gradient Boosting Regressor model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test data.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted values.
        """
        predictions = np.full(X.shape[0], self.initial_model)
        for model in self.models:
            predictions += self.learning_rate * model.predict(X)
        return predictions

    def score(self, X, y):
        """
        Calculate the R^2 score.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test data.
        y : array-like of shape (n_samples,)
            True values for X.

        Returns
        -------
        score : float
            R^2 score.
        """
        y_pred = self.predict(X)
        u = ((y - y_pred) ** 2).sum()
        v = ((y - y.mean()) ** 2).sum()
        return 1 - u / v
