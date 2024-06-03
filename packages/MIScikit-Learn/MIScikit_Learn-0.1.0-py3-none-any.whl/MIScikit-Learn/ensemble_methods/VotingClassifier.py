import numpy as np

class VotingClassifier:
    """
    Voting Classifier.

    Parameters
    ----------
    estimators : list of (str, estimator) tuples
        List of (name, estimator) tuples.
    voting : str, {'hard', 'soft'}, default='hard'
        If 'hard', uses predicted class labels for majority rule voting.
        If 'soft', predicts the class label based on the argmax of the sums of the predicted probabilities.
    """
    def __init__(self, estimators, voting='hard'):
        self.estimators = estimators
        self.voting = voting

    def fit(self, X, y):
        """
        Fit the estimators.

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
        for _, estimator in self.estimators:
            estimator.fit(X, y)
        return self

    def predict(self, X):
        """
        Predict using the voting classifier.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test data.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted class labels.
        """
        if self.voting == 'soft':
            predictions = np.argmax(np.mean([estimator.predict_proba(X) for _, estimator in self.estimators], axis=0), axis=1)
        else:  # 'hard' voting
            predictions = np.mean([estimator.predict(X) for _, estimator in self.estimators], axis=0)
            predictions = np.round(predictions).astype(int)
        return predictions
