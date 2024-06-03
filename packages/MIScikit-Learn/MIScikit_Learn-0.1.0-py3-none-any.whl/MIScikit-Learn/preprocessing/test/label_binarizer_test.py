# File: preprocessing/test/label_binarizer_test.py

import numpy as np
from sklearn.preprocessing import LabelBinarizer as SklearnLabelBinarizer
import sys
import os

# Ensure the parent directory is in the system path to allow package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from preprocessing.label_binarizer import LabelBinarizer

def test_label_binarizer():
    # Sample data
    y = [1, 2, 6, 4, 2]

    # Parameters for the binarizer
    neg_label = 0
    pos_label = 1
    sparse_output = False

    # Scikit-learn's LabelBinarizer
    sklearn_binarizer = SklearnLabelBinarizer(neg_label=neg_label, pos_label=pos_label, sparse_output=sparse_output)
    sklearn_result = sklearn_binarizer.fit_transform(y)

    # Custom LabelBinarizer
    custom_binarizer = LabelBinarizer(neg_label=neg_label, pos_label=pos_label, sparse_output=sparse_output)
    custom_result = custom_binarizer.fit_transform(y)

    # Print results for comparison
    print("Scikit-learn LabelBinarizer result:")
    print(sklearn_result)
    print("\nCustom LabelBinarizer result:")
    print(custom_result)

    # Check if the results are the same
    assert np.array_equal(sklearn_result, custom_result), "The results are not the same!"

if __name__ == "__main__":
    test_label_binarizer()
