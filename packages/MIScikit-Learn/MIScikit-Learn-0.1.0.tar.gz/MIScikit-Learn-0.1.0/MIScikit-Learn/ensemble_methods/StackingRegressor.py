import numpy as np
from sklearn.model_selection import cross_val_predict, KFold

class StackingRegressor:
    """
    Stacking Regressor.

    Parameters
    ----------
    estimators : list of (str, estimator) tuples
        Base estimators which will be stacked.
    final_estimator : estimator, default=None
        The final estimator to fit on the blended predictions.
    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
    n_jobs : int, default=None
        The number of jobs to run in parallel for cross_val_predict.
    passthrough : bool, default=False
        When True, the original training data is added to the meta-features.
    verbose : int, default=0
        Verbosity level.
    """
    def __init__(self, estimators, final_estimator=None, cv=None, n_jobs=None, passthrough=False, verbose=0):
        self.estimators = estimators
        self.final_estimator = final_estimator
        self.cv = cv
        self.n_jobs = n_jobs
        self.passthrough = passthrough
        self.verbose = verbose

    def fit(self, X, y):
        """
        Fit the stacking regressor.

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
        self.estimators_ = []
        self.named_estimators_ = {}
        
        for name, estimator in self.estimators:
            if estimator == 'drop':
                continue
            estimator.fit(X, y)
            self.estimators_.append(estimator)
            self.named_estimators_[name] = estimator

        if self.cv is None:
            self.cv = 5
        cv = KFold(n_splits=self.cv) if isinstance(self.cv, int) else self.cv
        
        meta_features = np.column_stack([
            cross_val_predict(estimator, X, y, cv=cv, method='predict', n_jobs=self.n_jobs)
            for estimator in self.estimators_
        ])
        
        if self.passthrough:
            meta_features = np.hstack((X, meta_features))

        self.final_estimator_ = self.final_estimator
        self.final_estimator_.fit(meta_features, y)
        
        return self

    def predict(self, X):
        """
        Predict using the stacking regressor.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test data.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted values.
        """
        meta_features = np.column_stack([estimator.predict(X) for estimator in self.estimators_])
        
        if self.passthrough:
            meta_features = np.hstack((X, meta_features))
        
        return self.final_estimator_.predict(meta_features)

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
            'final_estimator': self.final_estimator,
            'cv': self.cv,
            'n_jobs': self.n_jobs,
            'passthrough': self.passthrough,
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
