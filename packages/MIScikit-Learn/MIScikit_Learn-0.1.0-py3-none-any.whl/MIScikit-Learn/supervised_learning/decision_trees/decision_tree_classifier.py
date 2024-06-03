import numpy as np

class DecisionTreeClassifier:
    """
    Decision Tree Classifier.

    Parameters
    ----------
    criterion : str, optional, default: "gini"
        The function to measure the quality of a split. Supported criteria are "gini" for the Gini impurity and "entropy" for the information gain.
    max_depth : int or None, optional, default: None
        The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.
    min_samples_split : int, optional, default: 2
        The minimum number of samples required to split an internal node.
    min_samples_leaf : int, optional, default: 1
        The minimum number of samples required to be at a leaf node.
    random_state : int or None, optional, default: None
        Controls the randomness of the estimator.
    """
    def __init__(self, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=None):
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.tree_ = None
        self.classes_ = None

    def fit(self, X, y):
        """
        Build a decision tree classifier from the training set (X, y).

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values (class labels).
        """
        self.classes_ = np.unique(y)
        self.tree_ = self._build_tree(X, y)

    def predict(self, X):
        """
        Predict class for X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : array, shape (n_samples,)
            The predicted classes.
        """
        return np.array([self._predict(inputs) for inputs in X])

    def predict_proba(self, X):
        """
        Predict class probabilities for X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        p : array, shape (n_samples, n_classes)
            The class probabilities of the input samples.
        """
        class_counts = np.array([self._predict_proba(inputs) for inputs in X])
        return class_counts / class_counts.sum(axis=1, keepdims=True)

    def score(self, X, y):
        """
        Return the mean accuracy on the given test data and labels.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Test samples.
        y : array-like, shape (n_samples,)
            True labels for X.

        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) wrt. y.
        """
        predictions = self.predict(X)
        return np.mean(predictions == y)

    def _build_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        if (self.max_depth and depth >= self.max_depth) or num_samples < self.min_samples_split or len(np.unique(y)) == 1:
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        best_feat, best_thresh = self._best_split(X, y, num_features)
        if best_feat is None:
            leaf_value = self._most_common_label(y)
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
                gain = self._information_gain(y, X_column, threshold)
                if gain > best_gain:
                    best_gain = gain
                    split_idx = feat_idx
                    split_thresh = threshold

        return split_idx, split_thresh

    def _information_gain(self, y, X_column, split_thresh):
        parent_entropy = self._entropy(y)

        left_idxs, right_idxs = self._split(X_column, split_thresh)
        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0

        num_samples = len(y)
        num_left, num_right = len(left_idxs), len(right_idxs)
        left_entropy, right_entropy = self._entropy(y[left_idxs]), self._entropy(y[right_idxs])
        child_entropy = (num_left / num_samples) * left_entropy + (num_right / num_samples) * right_entropy

        ig = parent_entropy - child_entropy
        return ig

    def _split(self, X_column, split_thresh):
        left_idxs = np.argwhere(X_column <= split_thresh).flatten()
        right_idxs = np.argwhere(X_column > split_thresh).flatten()
        return left_idxs, right_idxs

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log2(p) for p in ps if p > 0])

    def _most_common_label(self, y):
        return np.bincount(y).argmax()

    def _predict(self, inputs):
        node = self.tree_
        while node.left:
            if inputs[node.feature_index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

    def _predict_proba(self, inputs):
        node = self.tree_
        while node.left:
            if inputs[node.feature_index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return [1 if node.value == cls else 0 for cls in self.classes_]

    def get_params(self, deep=True):
        return {
            "criterion": self.criterion,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "min_samples_leaf": self.min_samples_leaf,
            "random_state": self.random_state
        }

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self

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
        Predicted class label (for leaf nodes).
    """
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, *, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

# Testing the DecisionTreeClassifier with additional datasets

from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier as SklearnDecisionTreeClassifier

def test():
    # Load the Iris dataset
    data = load_iris()
    X, y = data.data, data.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train our Decision Tree Classifier
    dt = DecisionTreeClassifier(max_depth=3)
    dt.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = dt.predict(X_test)
    accuracy = dt.score(X_test, y_test)
    print(f"Custom Decision Tree Classifier Accuracy: {accuracy:.4f}")

    # Compare with Scikit-Learn's Decision Tree Classifier
    sklearn_dt = SklearnDecisionTreeClassifier(max_depth=3)
    sklearn_dt.fit(X_train, y_train)
    y_pred_sklearn = sklearn_dt.predict(X_test)
    accuracy_sklearn = accuracy_score(y_test, y_pred_sklearn)
    print(f"Scikit-Learn Decision Tree Classifier Accuracy: {accuracy_sklearn:.4f}")

def test2():
    # Load the Wine dataset
    data = load_wine()
    X, y = data.data, data.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train our Decision Tree Classifier
    dt = DecisionTreeClassifier(max_depth=3)
    dt.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = dt.predict(X_test)
    accuracy = dt.score(X_test, y_test)
    print(f"Custom Decision Tree Classifier Accuracy on Wine dataset: {accuracy:.4f}")

    # Compare with Scikit-Learn's Decision Tree Classifier
    sklearn_dt = SklearnDecisionTreeClassifier(max_depth=3)
    sklearn_dt.fit(X_train, y_train)
    y_pred_sklearn = sklearn_dt.predict(X_test)
    accuracy_sklearn = accuracy_score(y_test, y_pred_sklearn)
    print(f"Scikit-Learn Decision Tree Classifier Accuracy on Wine dataset: {accuracy_sklearn:.4f}")

def test3():
    # Load the Breast Cancer Wisconsin dataset
    data = load_breast_cancer()
    X, y = data.data, data.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train our Decision Tree Classifier
    dt = DecisionTreeClassifier(max_depth=5)
    dt.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = dt.predict(X_test)
    accuracy = dt.score(X_test, y_test)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print(f"Custom Decision Tree Classifier Accuracy on Breast Cancer dataset: {accuracy:.4f}")
    print(f"Custom Decision Tree Classifier Precision: {precision:.4f}")
    print(f"Custom Decision Tree Classifier Recall: {recall:.4f}")
    print(f"Custom Decision Tree Classifier F1 Score: {f1:.4f}")

    # Compare with Scikit-Learn's Decision Tree Classifier
    sklearn_dt = SklearnDecisionTreeClassifier(max_depth=5)
    sklearn_dt.fit(X_train, y_train)
    y_pred_sklearn = sklearn_dt.predict(X_test)
    accuracy_sklearn = accuracy_score(y_test, y_pred_sklearn)
    precision_sklearn = precision_score(y_test, y_pred_sklearn)
    recall_sklearn = recall_score(y_test, y_pred_sklearn)
    f1_sklearn = f1_score(y_test, y_pred_sklearn)
    print(f"Scikit-Learn Decision Tree Classifier Accuracy on Breast Cancer dataset: {accuracy_sklearn:.4f}")
    print(f"Scikit-Learn Decision Tree Classifier Precision: {precision_sklearn:.4f}")
    print(f"Scikit-Learn Decision Tree Classifier Recall: {recall_sklearn:.4f}")
    print(f"Scikit-Learn Decision Tree Classifier F1 Score: {f1.sklearn:.4f}")

if __name__ == "__main__":
    test()
    test2()
    test3()
