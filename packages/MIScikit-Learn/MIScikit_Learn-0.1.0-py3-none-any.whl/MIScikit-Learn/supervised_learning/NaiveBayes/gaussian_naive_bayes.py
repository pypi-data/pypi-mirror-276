import numpy as np

class GaussianNaiveBayes:
    """
    Gaussian Naive Bayes classifier.
    """

    def __init__(self):
        self.classes = None
        self.means = None
        self.variances = None
        self.priors = None

    def fit(self, X, y):
        """
        Fit the Gaussian Naive Bayes model according to the given training data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training vectors.
        y : array-like, shape (n_samples,)
            Target values.
        """
        # Determine the unique classes
        self.classes = np.unique(y)
        # Initialize the means, variances, and priors
        self.means = {}
        self.variances = {}
        self.priors = {}
        for cls in self.classes:
            X_cls = X[y == cls]
            self.means[cls] = np.mean(X_cls, axis=0)
            self.variances[cls] = np.var(X_cls, axis=0)
            self.priors[cls] = X_cls.shape[0] / X.shape[0]

    def _calculate_likelihood(self, class_idx, x):
        """
        Calculate the likelihood of the data for a given class.

        Parameters
        ----------
        class_idx : int
            Class index.
        x : array-like, shape (n_features,)
            Data point.

        Returns
        -------
        likelihood : float
            Likelihood of the data point for the given class.
        """
        mean = self.means[class_idx]
        var = self.variances[class_idx]
        numerator = np.exp(- (x - mean) ** 2 / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator

    def _calculate_posterior(self, x):
        """
        Calculate the posterior probability of the data point for each class.

        Parameters
        ----------
        x : array-like, shape (n_features,)
            Data point.

        Returns
        -------
        class : int
            Class with the highest posterior probability.
        """
        posteriors = []
        for cls in self.classes:
            prior = np.log(self.priors[cls])
            likelihood = np.sum(np.log(self._calculate_likelihood(cls, x)))
            posterior = prior + likelihood
            posteriors.append(posterior)
        return self.classes[np.argmax(posteriors)]

    def predict(self, X):
        """
        Perform classification on an array of test vectors X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Test vectors.

        Returns
        -------
        y_pred : array, shape (n_samples,)
            Predicted target values for X.
        """
        y_pred = [self._calculate_posterior(x) for x in X]
        return np.array(y_pred)

    def score(self, X, y):
        """
        Return the mean accuracy on the given test data and labels.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Test vectors.
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
        return {}

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
