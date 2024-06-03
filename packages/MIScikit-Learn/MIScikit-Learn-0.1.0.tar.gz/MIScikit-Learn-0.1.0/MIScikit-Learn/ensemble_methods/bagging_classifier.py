import numpy as np
from sklearn.base import clone
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.base_estimator import BaseEstimator
from sklearn.utils import resample


class BaggingClassifier(BaseEstimator):
    """
    A Bagging classifier.

    Parameters
    ----------
    base_estimator : object
        The base estimator to fit on random subsets of the dataset.

    n_estimators : int, default=10
        The number of base estimators in the ensemble.

    max_samples : float, default=1.0
        The proportion of the dataset to include in each random subset.

    random_state : int, default=None
        Controls the random resampling of the original dataset.
    
    Attributes
    ----------
    estimators_ : list of estimators
        The collection of fitted base estimators.
    """

    def __init__(self, base_estimator, n_estimators=10, max_samples=1.0, random_state=None):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.random_state = random_state
        self.estimators_ = []

    def fit(self, X, y):
        """
        Build a Bagging ensemble of estimators from the training set (X, y).

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
        self.estimators_ = []
        np.random.seed(self.random_state)
        
        n_samples = int(self.max_samples * X.shape[0])
        
        for _ in range(self.n_estimators):
            estimator = clone(self.base_estimator)
            X_resampled, y_resampled = resample(X, y, n_samples=n_samples, random_state=self.random_state)
            estimator.fit(X_resampled, y_resampled)
            self.estimators_.append(estimator)
        
        return self

    def predict(self, X):
        """
        Predict classes for X.

        The predicted class of an input sample is computed as the majority vote
        of the classifiers in the ensemble.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : array of shape (n_samples,)
            The predicted classes.
        """
        predictions = np.array([estimator.predict(X) for estimator in self.estimators_])
        return np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=predictions)

    def predict_proba(self, X):
        """
        Predict class probabilities for X.

        The predicted class probabilities of an input sample are computed as the average
        predicted class probabilities of the classifiers in the ensemble.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        p : array of shape (n_samples, n_classes)
            The class probabilities of the input samples.
        """
        probas = np.array([estimator.predict_proba(X) for estimator in self.estimators_])
        return np.mean(probas, axis=0)
