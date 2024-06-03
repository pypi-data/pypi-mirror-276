import numpy as np
from sklearn.tree import DecisionTreeClassifier

import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.base_predictor import BasePredictor


class AdaBoostClassifier(BasePredictor):
    """
    AdaBoost classifier.

    Parameters
    ----------
    n_estimators : int, default=50
        The maximum number of estimators at which boosting is terminated.

    learning_rate : float, default=1.0
        Weight applied to each classifier at each boosting iteration.

    Attributes
    ----------
    models : list of estimators
        The collection of fitted base estimators.

    alphas : list of floats
        The weights for each base estimator.
    """

    def __init__(self, n_estimators=50, learning_rate=1.0):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.models = []
        self.alphas = []

    def fit(self, X, y):
        """
        Build a boosted classifier from the training set (X, y).

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        y : array-like of shape (n_samples,)
            The target values (class labels).
        
        Returns
        -------
        self : object
            Fitted estimator.
        """
        n_samples, n_features = X.shape
        w = np.ones(n_samples) / n_samples

        for _ in range(self.n_estimators):
            model = DecisionTreeClassifier(max_depth=1)
            model.fit(X, y, sample_weight=w)
            y_pred = model.predict(X)

            error = np.sum(w * (y_pred != y)) / np.sum(w)
            alpha = self.learning_rate * np.log((1 - error) / (error + 1e-10)) / 2

            w *= np.exp(-alpha * y * y_pred)
            w /= np.sum(w)

            self.models.append(model)
            self.alphas.append(alpha)

        return self

    def predict(self, X):
        """
        Predict classes for X.

        The predicted class of an input sample is computed as the weighted mean 
        prediction of the classifiers in the ensemble.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : array of shape (n_samples,)
            The predicted classes.
        """
        y_pred = np.zeros(X.shape[0])
        for model, alpha in zip(self.models, self.alphas):
            y_pred += alpha * model.predict(X)
        return np.sign(y_pred)

    def score(self, X, y):
        """
        Return the mean accuracy on the given test data and labels.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.

        y : array-like of shape (n_samples,)
            True labels for X.

        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) wrt. y.
        """
        y_pred = self.predict(X)
        return np.mean(y == y_pred)
