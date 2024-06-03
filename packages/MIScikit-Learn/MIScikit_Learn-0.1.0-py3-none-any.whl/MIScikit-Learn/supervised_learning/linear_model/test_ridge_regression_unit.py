import unittest
import numpy as np
from ridge_regression import RidgeRegression


class TestRidgeRegression(unittest.TestCase):
    def setUp(self):
        self.model = RidgeRegression(alpha=1.0, fit_intercept=True, copy_X=True)

    def test_fit(self):
        # Simple linear relationship
        X = np.array([[1, 2], [2, 3], [3, 4]])
        y = np.array([8, 13, 18])  # y = 2*x1 + 3*x2
        self.model.fit(X, y)
        self.assertIsNotNone(self.model.coef_)
        self.assertIsNotNone(self.model.intercept_)

    def test_predict(self):
        # Simple linear relationship
        X = np.array([[1, 2], [2, 3], [3, 4]])
        y = np.array([8, 13, 18])  # y = 2*x1 + 3*x2
        self.model.fit(X, y)
        predictions = self.model.predict(X)
        self.assertEqual(predictions.shape, (3,))
        np.testing.assert_almost_equal(predictions, y, decimal=0)

    def test_score(self):
        # Simple linear relationship
        X = np.array([[1, 2], [2, 3], [3, 4]])
        y = np.array([8, 13, 18])  # y = 2*x1 + 3*x2
        self.model.fit(X, y)
        score = self.model.score(X, y)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
        self.assertAlmostEqual(score, 1.0, places=1)


if __name__ == "__main__":
    unittest.main()