import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from supervised_learning.decision_trees.decision_tree_classifier import DecisionTreeClassifier

class StackingClassifier:
    """
    Stacking Classifier.

    Parameters
    ----------
    base_classifiers : list of classifiers, default=None
        The base classifiers to be used. If None, default to two DecisionTreeClassifiers with different depths.
    meta_classifier : classifier, default=None
        The meta-classifier to be used for stacking. If None, default to a DecisionTreeClassifier.
    """
    def __init__(self, base_classifiers=None, meta_classifier=None):
        self.base_classifiers = base_classifiers if base_classifiers else [DecisionTreeClassifier(max_depth=1), DecisionTreeClassifier(max_depth=3)]
        self.meta_classifier = meta_classifier if meta_classifier else DecisionTreeClassifier(max_depth=1)
        self.base_predictions = None

    def fit(self, X, y):
        """
        Fit the stacking classifier.

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
        self.base_predictions = []
        for clf in self.base_classifiers:
            clf.fit(X, y)
            predictions = clf.predict(X)
            self.base_predictions.append(predictions)
        self.base_predictions = np.array(self.base_predictions).T
        self.meta_classifier.fit(self.base_predictions, y)

    def predict(self, X):
        """
        Predict using the stacking classifier.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test data.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted values.
        """
        base_preds = []
        for clf in self.base_classifiers:
            predictions = clf.predict(X)
            base_preds.append(predictions)
        base_preds = np.array(base_preds).T
        return self.meta_classifier.predict(base_preds)
