import unittest
import numpy as np
from logistic_regression import LogisticRegression


class TestLogisticRegression(unittest.TestCase):
    def setUp(self):
        self.model = LogisticRegression(learning_rate=0.1, max_iter=1000, tol=1e-4)

    def test_fit(self):
        # Simple dataset for binary classification
        X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y = np.array([0, 0, 1, 1])  # Simple binary target
        self.model.fit(X, y)
        self.assertIsNotNone(self.model.weights)
        self.assertIsNotNone(self.model.bias)

    def test_predict_proba(self):
        # Simple dataset for binary classification
        X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y = np.array([0, 0, 1, 1])  # Simple binary target
        self.model.fit(X, y)
        probabilities = self.model.predict_proba(X)
        self.assertEqual(probabilities.shape, (4,))
        self.assertTrue(np.all(probabilities >= 0) and np.all(probabilities <= 1))

    def test_predict(self):
        # Simple dataset for binary classification
        X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y = np.array([0, 0, 1, 1])  # Simple binary target
        self.model.fit(X, y)
        predictions = self.model.predict(X)
        self.assertEqual(predictions.shape, (4,))
        self.assertTrue(set(predictions).issubset({0, 1}))

    def test_score(self):
        # Simple dataset for binary classification
        X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y = np.array([0, 0, 1, 1])  # Simple binary target
        self.model.fit(X, y)
        score = self.model.score(X, y)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
        self.assertAlmostEqual(score, 1.0, places=1)


if __name__ == "__main__":
    unittest.main()
