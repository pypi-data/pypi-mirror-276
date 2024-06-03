import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from supervised_learning.decision_trees.decision_tree_regressor import DecisionTreeRegressor

class RandomForestRegressor:
    def __init__(self, n_estimators=100, criterion='squared_error', max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=1.0, max_leaf_nodes=None,
                 min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=None,
                 verbose=0, warm_start=False, ccp_alpha=0.0, max_samples=None, monotonic_cst=None):
        self.n_estimators = n_estimators
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose
        self.warm_start = warm_start
        self.ccp_alpha = ccp_alpha
        self.max_samples = max_samples
        self.monotonic_cst = monotonic_cst
        self.estimators_ = []
        self.estimators_samples_ = []
        self.oob_prediction_ = None
        self.oob_score_ = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.estimators_ = []
        self.estimators_samples_ = []
        random_state = np.random.RandomState(self.random_state)

        for _ in range(self.n_estimators):
            estimator = DecisionTreeRegressor(
                criterion=self.criterion, max_depth=self.max_depth,
                min_samples_split=self.min_samples_split, min_samples_leaf=self.min_samples_leaf,
                random_state=random_state.randint(np.iinfo(np.int32).max)
            )
            
            if self.bootstrap:
                if self.max_samples:
                    if isinstance(self.max_samples, float):
                        n_bootstrap_samples = int(self.max_samples * n_samples)
                    else:
                        n_bootstrap_samples = self.max_samples
                else:
                    n_bootstrap_samples = n_samples
                
                indices = random_state.choice(n_samples, n_bootstrap_samples, replace=True)
            else:
                indices = np.arange(n_samples)
            
            X_sample = X[indices]
            y_sample = y[indices]
            
            estimator.fit(X_sample, y_sample)
            self.estimators_.append(estimator)
            self.estimators_samples_.append(indices)

        if self.oob_score:
            self._set_oob_score(X, y)
        
        return self

    def _set_oob_score(self, X, y):
        n_samples = X.shape[0]
        oob_predictions = np.zeros(n_samples)
        oob_counts = np.zeros(n_samples)
        
        for estimator, indices in zip(self.estimators_, self.estimators_samples_):
            mask = np.ones(n_samples, dtype=bool)
            mask[indices] = False
            oob_predictions[mask] += estimator.predict(X[mask])
            oob_counts[mask] += 1
        
        oob_counts[oob_counts == 0] = 1
        self.oob_prediction_ = oob_predictions / oob_counts
        self.oob_score_ = np.mean((y - self.oob_prediction_) ** 2)

    def predict(self, X):
        predictions = np.zeros(X.shape[0])
        for estimator in self.estimators_:
            predictions += estimator.predict(X)
        return predictions / self.n_estimators

    def score(self, X, y):
        y_pred = self.predict(X)
        return np.mean((y - y_pred) ** 2)

    def get_params(self, deep=True):
        return {
            'n_estimators': self.n_estimators,
            'criterion': self.criterion,
            'max_depth': self.max_depth,
            'min_samples_split': self.min_samples_split,
            'min_samples_leaf': self.min_samples_leaf,
            'min_weight_fraction_leaf': self.min_weight_fraction_leaf,
            'max_features': self.max_features,
            'max_leaf_nodes': self.max_leaf_nodes,
            'min_impurity_decrease': self.min_impurity_decrease,
            'bootstrap': self.bootstrap,
            'oob_score': self.oob_score,
            'n_jobs': self.n_jobs,
            'random_state': self.random_state,
            'verbose': self.verbose,
            'warm_start': self.warm_start,
            'ccp_alpha': self.ccp_alpha,
            'max_samples': self.max_samples,
            'monotonic_cst': self.monotonic_cst,
        }

    def set_params(self, **params):
        for param, value in params.items():
            setattr(self, param, value)
        return self

