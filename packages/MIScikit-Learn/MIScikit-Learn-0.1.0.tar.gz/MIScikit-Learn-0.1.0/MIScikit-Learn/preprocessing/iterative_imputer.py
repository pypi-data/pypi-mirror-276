import numpy as np
from sklearn.linear_model import BayesianRidge
from sklearn.utils import check_array
from simple_imputer import SimpleImputer
from sklearn.base import clone

class IterativeImputer:
    """
    Impute missing values using an iterative approach.

    Parameters
    ----------
    estimator : object, default=BayesianRidge()
        The estimator to use at each step of the imputation.

    max_iter : int, default=10
        The maximum number of imputation iterations.

    tol : float, default=1e-3
        The tolerance to declare convergence.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the estimator.

    Attributes
    ----------
    initial_imputer_ : SimpleImputer
        The initial imputer to fill in the missing values.

    imputation_sequence_ : list of tuples
        The order in which the features will be imputed.

    estimator_ : object
        The estimator used for imputation.
    """

    def __init__(self, estimator=BayesianRidge(), max_iter=10, tol=1e-3, random_state=None):
        self.estimator = estimator
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state

    def fit(self, X, y=None):
        """
        Fit the imputer on X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to fit.

        y : None
            Ignored. This parameter exists only for compatibility with Pipeline.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        self.initial_imputer_ = SimpleImputer(strategy='mean')
        X_initial = self.initial_imputer_.fit_transform(X)

        self.imputation_sequence_ = []
        self.estimator_ = []

        missing_mask = np.isnan(X)

        for i in range(X.shape[1]):
            if missing_mask[:, i].any():
                self.imputation_sequence_.append(i)
                self.estimator_.append(clone(self.estimator))

        X_filled = X_initial.copy()
        for _ in range(self.max_iter):
            X_previous = X_filled.copy()
            for i, estimator in zip(self.imputation_sequence_, self.estimator_):
                missing_idx = missing_mask[:, i]
                if not np.any(missing_idx):
                    continue

                X_train = np.delete(X_filled, i, axis=1)
                y_train = X_filled[:, i]
                X_train = X_train[~missing_idx]
                y_train = y_train[~missing_idx]

                estimator.fit(X_train, y_train)

                X_test = np.delete(X_filled, i, axis=1)
                X_test = X_test[missing_idx]

                X_filled[missing_idx, i] = estimator.predict(X_test)

            if np.linalg.norm(X_filled - X_previous) < self.tol:
                break

        return self

    def transform(self, X):
        """
        Impute all missing values in X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to transform.

        Returns
        -------
        X_new : array-like, shape (n_samples, n_features)
            The imputed data.
        """
        X_initial = self.initial_imputer_.transform(X)

        missing_mask = np.isnan(X)
        X_filled = X_initial.copy()

        for i, estimator in zip(self.imputation_sequence_, self.estimator_):
            missing_idx = missing_mask[:, i]
            if not np.any(missing_idx):
                continue

            X_test = np.delete(X_filled, i, axis=1)
            X_test = X_test[missing_idx]

            X_filled[missing_idx, i] = estimator.predict(X_test)

        return X_filled

    def fit_transform(self, X, y=None):
        """
        Fit the imputer on X and transform X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to fit and transform.

        y : None
            Ignored. This parameter exists only for compatibility with Pipeline.

        Returns
        -------
        X_new : array-like, shape (n_samples, n_features)
            The imputed data.
        """
        return self.fit(X).transform(X)
