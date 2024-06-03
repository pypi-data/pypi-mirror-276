import numpy as np
from sklearn.base import clone

class VotingRegressor:
    """
    Voting Regressor.

    Parameters
    ----------
    estimators : list of (str, estimator) tuples
        List of (name, estimator) tuples.
    weights : array-like of shape (n_estimators,), default=None
        Sequence of weights (float or int) to weight the occurrences of predicted values before averaging.
    n_jobs : int, default=None
        The number of jobs to run in parallel for fit. None means 1.
    verbose : bool, default=False
        If True, print information while fitting.
    """
    def __init__(self, estimators, weights=None, n_jobs=None, verbose=False):
        self.estimators = estimators
        self.weights = weights
        self.n_jobs = n_jobs
        self.verbose = verbose

    def fit(self, X, y, sample_weight=None):
        """
        Fit the estimators.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights.

        Returns
        -------
        self : object
        """
        self.estimators_ = []
        self.named_estimators_ = {}
        
        for name, estimator in self.estimators:
            if estimator == 'drop':
                continue
            cloned_estimator = clone(estimator)
            cloned_estimator.fit(X, y, sample_weight=sample_weight)
            self.estimators_.append(cloned_estimator)
            self.named_estimators_[name] = cloned_estimator
        
        return self

    def predict(self, X):
        """
        Predict using the voting regressor.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test data.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted values.
        """
        predictions = np.asarray([estimator.predict(X) for estimator in self.estimators_]).T
        if self.weights is not None:
            avg = np.average(predictions, axis=1, weights=self.weights)
        else:
            avg = np.mean(predictions, axis=1)
        return avg

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
        return {
            'estimators': self.estimators,
            'weights': self.weights,
            'n_jobs': self.n_jobs,
            'verbose': self.verbose
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
        for param, value in params.items():
            setattr(self, param, value)
        return self
