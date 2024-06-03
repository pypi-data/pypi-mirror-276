import unittest
import numpy as np
from decision_tree_regressor import DecisionTreeRegressor
from sklearn.datasets import fetch_california_housing, load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class TestDecisionTreeRegressor(unittest.TestCase):
    def setUp(self):
        self.california = fetch_california_housing()
        self.diabetes = load_diabetes()
        self.regressor = DecisionTreeRegressor(max_depth=3, random_state=42)

    def test_fit_predict_california(self):
        X_train, X_test, y_train, y_test = train_test_split(self.california.data, self.california.target, test_size=0.3, random_state=42)
        self.regressor.fit(X_train, y_train)
        predictions = self.regressor.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        self.assertLessEqual(mse, 1)
        self.assertGreaterEqual(r2, 0.5)

    def test_fit_predict_diabetes(self):
        X_train, X_test, y_train, y_test = train_test_split(self.diabetes.data, self.diabetes.target, test_size=0.3, random_state=42)
        self.regressor.fit(X_train, y_train)
        predictions = self.regressor.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        self.assertLessEqual(mse, 4000)
        self.assertGreaterEqual(r2, 0.3)

    def test_predict_single_sample(self):
        X_train, X_test, y_train, y_test = train_test_split(self.california.data, self.california.target, test_size=0.3, random_state=42)
        self.regressor.fit(X_train, y_train)
        prediction = self.regressor.predict([X_test[0]])
        self.assertEqual(prediction.shape, (1,))

if __name__ == "__main__":
    unittest.main()
