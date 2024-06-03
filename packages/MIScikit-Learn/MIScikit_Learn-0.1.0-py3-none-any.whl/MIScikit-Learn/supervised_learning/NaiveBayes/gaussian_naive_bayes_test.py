import unittest
import numpy as np
from gaussian_naive_bayes import GaussianNaiveBayes
from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class TestGaussianNaiveBayes(unittest.TestCase):
    def setUp(self):
        self.iris = load_iris()
        self.wine = load_wine()
        self.clf = GaussianNaiveBayes()

    def test_fit_predict_iris(self):
        X_train, X_test, y_train, y_test = train_test_split(self.iris.data, self.iris.target, test_size=0.3, random_state=42)
        self.clf.fit(X_train, y_train)
        predictions = self.clf.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        self.assertGreaterEqual(accuracy, 0.9)

    def test_fit_predict_wine(self):
        X_train, X_test, y_train, y_test = train_test_split(self.wine.data, self.wine.target, test_size=0.3, random_state=42)
        self.clf.fit(X_train, y_train)
        predictions = self.clf.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        self.assertGreaterEqual(accuracy, 0.9)

    def test_predict_single_sample(self):
        X_train, X_test, y_train, y_test = train_test_split(self.iris.data, self.iris.target, test_size=0.3, random_state=42)
        self.clf.fit(X_train, y_train)
        prediction = self.clf.predict([X_test[0]])
        self.assertEqual(prediction.shape, (1,))

if __name__ == "__main__":
    unittest.main()
