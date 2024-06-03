import numpy as np
from collections import Counter

def pairwise_distances(X, Y=None, metric='euclidean'):
    """
    Compute pairwise distances between X and Y using the specified metric.

    Parameters
    ----------
    X : array-like, shape (n_samples_1, n_features)
        An array of samples.
    Y : array-like, shape (n_samples_2, n_features), optional, default: None
        An array of samples. If None, Y is set to X.
    metric : str, optional, default: 'euclidean'
        The distance metric to use. Supported metrics: 'euclidean', 'manhattan'.

    Returns
    -------
    distances : array, shape (n_samples_1, n_samples_2)
        An array of pairwise distances.
    """
    X = np.array(X)
    Y = np.array(Y) if Y is not None else X
    if metric == 'euclidean':
        return euclidean_distances(X, Y)
    elif metric == 'manhattan':
        return manhattan_distances(X, Y)
    else:
        raise ValueError(f"Unsupported metric: {metric}")

def euclidean_distances(X, Y):
    """
    Compute the Euclidean distances between X and Y.

    Parameters
    ----------
    X : array-like, shape (n_samples_1, n_features)
        An array of samples.
    Y : array-like, shape (n_samples_2, n_features)
        An array of samples.

    Returns
    -------
    distances : array, shape (n_samples_1, n_samples_2)
        An array of Euclidean distances.
    """
    XX = np.sum(X ** 2, axis=1)[:, np.newaxis]
    YY = np.sum(Y ** 2, axis=1)[np.newaxis, :]
    distances = np.sqrt(XX + YY - 2 * np.dot(X, Y.T))
    return distances

def manhattan_distances(X, Y):
    """
    Compute the Manhattan distances between X and Y.

    Parameters
    ----------
    X : array-like, shape (n_samples_1, n_features)
        An array of samples.
    Y : array-like, shape (n_samples_2, n_features)
        An array of samples.

    Returns
    -------
    distances : array, shape (n_samples_1, n_samples_2)
        An array of Manhattan distances.
    """
    return np.sum(np.abs(X[:, np.newaxis] - Y[np.newaxis, :]), axis=2)

class KNeighborsClassifier:
    """
    Classifier implementing the k-nearest neighbors vote.

    Parameters
    ----------
    n_neighbors : int, optional, default: 5
        Number of neighbors to use by default for kneighbors queries.
    algorithm : {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional, default: 'auto'
        Algorithm used to compute the nearest neighbors.
    leaf_size : int, optional, default: 30
        Leaf size passed to BallTree or KDTree.
    p : int, optional, default: 2
        Power parameter for the Minkowski metric.
    metric : str, optional, default: 'minkowski'
        The distance metric to use.
    metric_params : dict, optional, default: None
        Additional keyword arguments for the metric function.
    n_jobs : int, optional, default: None
        The number of parallel jobs to run for neighbors search.

    Attributes
    ----------
    X_train : array-like, shape (n_samples, n_features)
        The input samples.
    y_train : array-like, shape (n_samples,)
        The input labels.
    """

    def __init__(self, n_neighbors=5, algorithm='auto', leaf_size=30, p=2,
                 metric='minkowski', metric_params=None, n_jobs=None):
        self.n_neighbors = n_neighbors
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.metric = metric
        self.metric_params = metric_params
        self.n_jobs = n_jobs
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        """
        Fit the k-nearest neighbors classifier from the training dataset.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values.
        """
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def kneighbors(self, X, n_neighbors=None, return_distance=True):
        """
        Find the K-neighbors of a point.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The query point or points.
        n_neighbors : int, optional, default: None
            Number of neighbors to get (default is the value passed to the constructor).
        return_distance : bool, optional, default: True
            Whether to return distances.

        Returns
        -------
        distances : array, shape (n_samples, n_neighbors)
            Array representing the lengths to point.
        indices : array, shape (n_samples, n_neighbors)
            Indices of the nearest points in the population matrix.
        """
        if n_neighbors is None:
            n_neighbors = self.n_neighbors

        metric = 'euclidean' if self.metric == 'minkowski' and self.p == 2 else 'manhattan'
        distances = pairwise_distances(X, self.X_train, metric=metric)
        neighbors_indices = np.argsort(distances, axis=1)[:, :n_neighbors]

        if return_distance:
            neighbors_distances = np.sort(distances, axis=1)[:, :n_neighbors]
            return neighbors_distances, neighbors_indices
        else:
            return neighbors_indices

    def predict(self, X):
        """
        Predict the class labels for the provided data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Test samples.

        Returns
        -------
        y_pred : array, shape (n_samples,)
            Class labels for each data sample.
        """
        neighbors_indices = self.kneighbors(X, return_distance=False)
        neighbor_votes = self.y_train[neighbors_indices]
        y_pred = [
            Counter(neighbor_votes[i]).most_common(1)[0][0]
            for i in range(len(neighbor_votes))
        ]
        return np.array(y_pred)

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
        y_pred = self.predict(X)
        return np.mean(y_pred == y)

    def get_params(self, deep=True):
        """
        Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, optional, default: True
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.
        """
        return {
            'n_neighbors': self.n_neighbors,
            'algorithm': self.algorithm,
            'leaf_size': self.leaf_size,
            'p': self.p,
            'metric': self.metric,
            'metric_params': self.metric_params,
            'n_jobs': self.n_jobs,
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
        for key, value in params.items():
            setattr(self, key, value)
        return self
