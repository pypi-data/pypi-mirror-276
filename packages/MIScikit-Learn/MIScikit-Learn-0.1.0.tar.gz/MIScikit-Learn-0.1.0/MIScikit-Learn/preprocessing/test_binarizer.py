import unittest
import numpy as np
from scipy.sparse import csr_matrix
from binarizer import Binarizer

class TestBinarizer(unittest.TestCase): 
    def setUp(self):
        self.X_dense = np.array([[1.0, -1.0, 2.0],
                                 [2.0, 0.0, 0.5],
                                 [0.0, 1.0, -0.5]])
        self.X_sparse = csr_matrix(self.X_dense)

    def test_binarize_dense(self):
        binarizer = Binarizer(threshold=0.5)
        X_bin = binarizer.fit_transform(self.X_dense)
        expected_output = np.array([[1, 0, 1],
                                    [1, 0, 0],
                                    [0, 1, 0]])
        np.testing.assert_array_equal(X_bin, expected_output)

    def test_binarize_sparse(self):
        binarizer = Binarizer(threshold=0.5)
        X_bin = binarizer.fit_transform(self.X_sparse)
        expected_output = csr_matrix([[1, 0, 1],
                                      [1, 0, 0],
                                      [0, 1, 0]])
        np.testing.assert_array_equal(X_bin.toarray(), expected_output.toarray())

    def test_binarize_dense_copy(self):
        binarizer = Binarizer(threshold=0.5, copy=False)
        X_bin = binarizer.fit_transform(self.X_dense)
        expected_output = np.array([[1, 0, 1],
                                    [1, 0, 0],
                                    [0, 1, 0]])
        np.testing.assert_array_equal(X_bin, expected_output)
        np.testing.assert_array_equal(self.X_dense, expected_output)

    def test_binarize_sparse_copy(self):
        binarizer = Binarizer(threshold=0.5, copy=False)
        X_bin = binarizer.fit_transform(self.X_sparse)
        expected_output = csr_matrix([[1, 0, 1],
                                      [1, 0, 0],
                                      [0, 1, 0]])
        np.testing.assert_array_equal(X_bin.toarray(), expected_output.toarray())
        np.testing.assert_array_equal(self.X_sparse.toarray(), expected_output.toarray())

    def test_get_feature_names_out(self):
        binarizer = Binarizer()
        binarizer.fit(self.X_dense)
        feature_names_out = binarizer.get_feature_names_out()
        expected_feature_names = np.array(["x0", "x1", "x2"])
        np.testing.assert_array_equal(feature_names_out, expected_feature_names)

if __name__ == "__main__":
    unittest.main()
