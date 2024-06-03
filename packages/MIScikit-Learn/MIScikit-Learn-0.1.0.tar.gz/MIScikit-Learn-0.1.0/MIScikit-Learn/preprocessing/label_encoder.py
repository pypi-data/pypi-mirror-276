# File: preprocessing/label_encoder.py

import numpy as np

import os
import sys

# Add the base module to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base.encoder import Encoder

class LabelEncoder(Encoder):
    """
    Encode target labels with value between 0 and n_classes-1.

    This transformer should be used to encode target values, i.e. y, and not the input X.

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        Holds the label for each class.

    See Also
    --------
    OrdinalEncoder : Encode categorical features using an ordinal encoding scheme.
    OneHotEncoder : Encode categorical features as a one-hot numeric array.

    Examples
    --------
    >>> from preprocessing.label_encoder import LabelEncoder
    >>> le = LabelEncoder()
    >>> le.fit([1, 2, 2, 6])
    LabelEncoder()
    >>> le.classes_
    array([1, 2, 6])
    >>> le.transform([1, 1, 2, 6])
    array([0, 0, 1, 2])
    >>> le.inverse_transform([0, 0, 1, 2])
    array([1, 1, 2, 6])

    It can also be used to transform non-numerical labels (as long as they are hashable and comparable) to numerical labels.

    >>> le = LabelEncoder()
    >>> le.fit(["paris", "paris", "tokyo", "amsterdam"])
    LabelEncoder()
    >>> list(le.classes_)
    ['amsterdam', 'paris', 'tokyo']
    >>> le.transform(["tokyo", "tokyo", "paris"])
    array([2, 2, 1])
    >>> list(le.inverse_transform([2, 2, 1]))
    ['tokyo', 'tokyo', 'paris']
    """

    def __init__(self):
        self.classes_ = None

    def fit(self, y):
        """
        Fit label encoder.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : object
            Fitted label encoder.
        """
        y = np.array(y)
        self.classes_ = np.unique(y)
        return self

    def fit_transform(self, y):
        """
        Fit label encoder and return encoded labels.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        y : array-like of shape (n_samples,)
            Encoded labels.
        """
        return self.fit(y).transform(y)

    def transform(self, y):
        """
        Transform labels to normalized encoding.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        y : array-like of shape (n_samples,)
            Labels as normalized encodings.
        """
        y = np.array(y)
        return np.searchsorted(self.classes_, y)

    def inverse_transform(self, y):
        """
        Transform labels back to original encoding.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        y : array-like of shape (n_samples,)
            Original encoding.
        """
        y = np.array(y)
        return self.classes_[y]

    def get_params(self, deep=True):
        """
        Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, optional, default=True
            If True, will return the parameters for this estimator and contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.
        """
        return {"classes_": self.classes_}

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
