# File: preprocessing/label_binarizer.py

import numpy as np
from scipy import sparse
from sklearn.utils.multiclass import type_of_target

class LabelBinarizer:
    """
    Binarize labels in a one-vs-all fashion.

    Parameters
    ----------
    neg_label : int, default=0
        Value with which negative labels must be encoded.

    pos_label : int, default=1
        Value with which positive labels must be encoded.

    sparse_output : bool, default=False
        True if the returned array from transform is desired to be in sparse CSR format.

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        Holds the label for each class.

    y_type_ : str
        Represents the type of the target data as evaluated by type_of_target.

    sparse_input_ : bool
        True if the input data to transform is given as a sparse matrix, False otherwise.
    """

    def __init__(self, neg_label=0, pos_label=1, sparse_output=False):
        self.neg_label = neg_label
        self.pos_label = pos_label
        self.sparse_output = sparse_output

    def fit(self, y):
        """
        Fit label binarizer.

        Parameters
        ----------
        y : ndarray of shape (n_samples,) or (n_samples, n_classes)
            Target values. The 2-d matrix should only contain 0 and 1, represents multilabel classification.

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        self.y_type_ = type_of_target(y)
        if 'multilabel' in self.y_type_:
            self.classes_ = np.arange(y.shape[1])
        else:
            self.classes_ = np.unique(y)
        return self

    def transform(self, y):
        """
        Transform multi-class labels to binary labels.

        Parameters
        ----------
        y : {array, sparse matrix} of shape (n_samples,) or (n_samples, n_classes)
            Target values. The 2-d matrix should only contain 0 and 1, represents multilabel classification.

        Returns
        -------
        Y : {ndarray, sparse matrix} of shape (n_samples, n_classes)
            Shape will be (n_samples, 1) for binary problems. Sparse matrix will be of CSR format.
        """
        if self.y_type_ == 'multiclass':
            Y = np.zeros((len(y), len(self.classes_)), dtype=int)
            for i, label in enumerate(self.classes_):
                Y[:, i] = np.where(y == label, self.pos_label, self.neg_label)
        elif 'multilabel' in self.y_type_:
            Y = y.copy()
            Y = Y.astype(int)
            Y[Y == 0] = self.neg_label
            Y[Y == 1] = self.pos_label
        else:
            Y = np.array([self.pos_label if i == y else self.neg_label for i in self.classes_]).reshape(1, -1)

        if self.sparse_output:
            return sparse.csr_matrix(Y)
        else:
            return Y

    def fit_transform(self, y):
        """
        Fit label binarizer/transform multi-class labels to binary labels.

        Parameters
        ----------
        y : {ndarray, sparse matrix} of shape (n_samples,) or (n_samples, n_classes)
            Target values. The 2-d matrix should only contain 0 and 1, represents multilabel classification.

        Returns
        -------
        Y : {ndarray, sparse matrix} of shape (n_samples, n_classes)
            Shape will be (n_samples, 1) for binary problems. Sparse matrix will be of CSR format.
        """
        return self.fit(y).transform(y)

    def inverse_transform(self, Y, threshold=None):
        """
        Transform binary labels back to multi-class labels.

        Parameters
        ----------
        Y : {ndarray, sparse matrix} of shape (n_samples, n_classes)
            Target values. All sparse matrices are converted to CSR before inverse transformation.

        threshold : float, default=None
            Threshold used in the binary and multi-label cases.
            Use 0 when Y contains the output of decision_function (classifier).
            Use 0.5 when Y contains the output of predict_proba.
            If None, the threshold is assumed to be half way between neg_label and pos_label.

        Returns
        -------
        y : {ndarray, sparse matrix} of shape (n_samples,)
            Target values. Sparse matrix will be of CSR format.
        """
        if threshold is None:
            threshold = (self.neg_label + self.pos_label) / 2.

        if sparse.issparse(Y):
            Y = Y.toarray()

        if self.y_type_ == 'multiclass':
            y = np.array([self.classes_[np.argmax(Y[i, :])] for i in range(Y.shape[0])])
        elif 'multilabel' in self.y_type_:
            y = (Y > threshold).astype(int)
        else:
            y = (Y > threshold).astype(int).ravel()

        return y

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
        return {"neg_label": self.neg_label, "pos_label": self.pos_label, "sparse_output": self.sparse_output}

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
            Estimator instance.
        """
        for key, value in params.items():
            setattr(self, key, value)
        return self
