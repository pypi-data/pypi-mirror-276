import numpy as np

class DecisionTreeRegressor:
    """
    Decision Tree Regressor.

    Parameters
    ----------
    criterion : str, optional, default: "squared_error"
        The function to measure the quality of a split. Supported criteria are "squared_error" for the mean squared error.
    splitter : str, optional, default: "best"
        The strategy used to choose the split at each node. Supported strategies are "best" to choose the best split and "random" to choose the best random split.
    max_depth : int or None, optional, default: None
        The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.
    min_samples_split : int, optional, default: 2
        The minimum number of samples required to split an internal node.
    min_samples_leaf : int, optional, default: 1
        The minimum number of samples required to be at a leaf node.
    min_weight_fraction_leaf : float, optional, default: 0.0
        The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node.
    max_features : int, float, str or None, optional, default: None
        The number of features to consider when looking for the best split.
    random_state : int or None, optional, default: None
        Controls the randomness of the estimator.
    max_leaf_nodes : int or None, optional, default: None
        Grow a tree with max_leaf_nodes in best-first fashion.
    min_impurity_decrease : float, optional, default: 0.0
        A node will be split if this split induces a decrease of the impurity greater than or equal to this value.
    ccp_alpha : float, optional, default: 0.0
        Complexity parameter used for Minimal Cost-Complexity Pruning.
    """
    def __init__(self, criterion='squared_error', splitter='best', max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None,
                 max_leaf_nodes=None, min_impurity_decrease=0.0, ccp_alpha=0.0):
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.ccp_alpha = ccp_alpha
        self.tree_ = None

    def fit(self, X, y):
        """
        Build a decision tree regressor from the training set (X, y).

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values.
        """
        self.n_features_ = X.shape[1]
        self.tree_ = self._build_tree(X, y)

    def predict(self, X):
        """
        Predict regression value for X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : array, shape (n_samples,)
            The predicted values.
        """
        return np.array([self._predict(inputs) for inputs in X])

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

    def _build_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        if (self.max_depth and depth >= self.max_depth) or num_samples < self.min_samples_split or len(np.unique(y)) == 1:
            leaf_value = self._mean_of_values(y)
            return Node(value=leaf_value)

        best_feat, best_thresh = self._best_split(X, y, num_features)
        if best_feat is None:
            leaf_value = self._mean_of_values(y)
            return Node(value=leaf_value)

        left_idxs, right_idxs = self._split(X[:, best_feat], best_thresh)
        left = self._build_tree(X[left_idxs, :], y[left_idxs], depth + 1)
        right = self._build_tree(X[right_idxs, :], y[right_idxs], depth + 1)
        return Node(best_feat, best_thresh, left, right)

    def _best_split(self, X, y, num_features):
        best_gain = -1
        split_idx, split_thresh = None, None

        for feat_idx in range(num_features):
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)
            for threshold in thresholds:
                gain = self._variance_reduction(y, X_column, threshold)
                if gain > best_gain:
                    best_gain = gain
                    split_idx = feat_idx
                    split_thresh = threshold

        return split_idx, split_thresh

    def _variance_reduction(self, y, X_column, split_thresh):
        parent_variance = np.var(y)

        left_idxs, right_idxs = self._split(X_column, split_thresh)
        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0

        num_samples = len(y)
        num_left, num_right = len(left_idxs), len(right_idxs)
        left_variance, right_variance = np.var(y[left_idxs]), np.var(y[right_idxs])
        weighted_variance = (num_left / num_samples) * left_variance + (num_right / num_samples) * right_variance

        reduction = parent_variance - weighted_variance
        return reduction

    def _split(self, X_column, split_thresh):
        left_idxs = np.argwhere(X_column <= split_thresh).flatten()
        right_idxs = np.argwhere(X_column > split_thresh).flatten()
        return left_idxs, right_idxs

    def _mean_of_values(self, y):
        return np.mean(y)

    def _predict(self, inputs):
        node = self.tree_
        while node.left:
            if inputs[node.feature_index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

class Node:
    """
    Node class for the Decision Tree.

    Parameters
    ----------
    feature_index : int or None
        Index of the feature to split on.
    threshold : float or None
        Threshold value to split on.
    left : Node or None
        Left child node.
    right : Node or None
        Right child node.
    value : int or None
        Predicted value (for leaf nodes).
    """
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, *, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

# Testing the DecisionTreeRegressor with additional datasets

from sklearn.datasets import fetch_california_housing, load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor as SklearnDecisionTreeRegressor

def test():
    # Load the California housing dataset
    data = fetch_california_housing()
    X, y = data.data, data.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train our Decision Tree Regressor
    dt = DecisionTreeRegressor(max_depth=3)
    dt.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = dt.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Custom Decision Tree Regressor MSE on California housing dataset: {mse:.4f}")

    # Compare with Scikit-Learn's Decision Tree Regressor
    sklearn_dt = SklearnDecisionTreeRegressor(max_depth=3)
    sklearn_dt.fit(X_train, y_train)
    y_pred_sklearn = sklearn_dt.predict(X_test)
    mse_sklearn = mean_squared_error(y_test, y_pred_sklearn)
    print(f"Scikit-Learn Decision Tree Regressor MSE on California housing dataset: {mse_sklearn:.4f}")

def test2():
    # Load the Diabetes dataset
    data = load_diabetes()
    X, y = data.data, data.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train our Decision Tree Regressor
    dt = DecisionTreeRegressor(max_depth=3)
    dt.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = dt.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Custom Decision Tree Regressor MSE on Diabetes dataset: {mse:.4f}")

    # Compare with Scikit-Learn's Decision Tree Regressor
    sklearn_dt = SklearnDecisionTreeRegressor(max_depth=3)
    sklearn_dt.fit(X_train, y_train)
    y_pred_sklearn = sklearn_dt.predict(X_test)
    mse_sklearn = mean_squared_error(y_test, y_pred_sklearn)
    print(f"Scikit-Learn Decision Tree Regressor MSE on Diabetes dataset: {mse_sklearn:.4f}")

if __name__ == "__main__":
    test()
    test2()
