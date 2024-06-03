from sklearn.linear_model import RidgeCV
from sklearn.svm import LinearSVR
from sklearn.ensemble import RandomForestRegressor as SklearnRandomForestRegressor
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from StackingRegressor import StackingRegressor
import warnings 
warnings.filterwarnings("ignore")

data = load_diabetes()
X, y = data.data, data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

estimators = [
    ('ridge', RidgeCV()),
    ('svr', LinearSVR(random_state=42))
]
final_estimator = SklearnRandomForestRegressor(n_estimators=10, random_state=42)

custom_sr = StackingRegressor(estimators=estimators, final_estimator=final_estimator, cv=5)
custom_sr.fit(X_train, y_train)


custom_pred_train = custom_sr.predict(X_train)
custom_pred_test = custom_sr.predict(X_test)
custom_mse_train = mean_squared_error(y_train, custom_pred_train)
custom_mse_test = mean_squared_error(y_test, custom_pred_test)
print(f"Custom StackingRegressor Train MSE: {custom_mse_train:.4f}")
print(f"Custom StackingRegressor Test MSE: {custom_mse_test:.4f}")

# Initialize and train the scikit-learn StackingRegressor
from sklearn.ensemble import StackingRegressor as SklearnStackingRegressor

sklearn_sr = SklearnStackingRegressor(
    estimators=estimators,
    final_estimator=final_estimator,
    cv=5
)
sklearn_sr.fit(X_train, y_train)

# Predictions and evaluation for the scikit-learn StackingRegressor
sklearn_pred_train = sklearn_sr.predict(X_train)
sklearn_pred_test = sklearn_sr.predict(X_test)
sklearn_mse_train = mean_squared_error(y_train, sklearn_pred_train)
sklearn_mse_test = mean_squared_error(y_test, sklearn_pred_test)
print(f"Scikit-Learn StackingRegressor Train MSE: {sklearn_mse_train:.4f}")
print(f"Scikit-Learn StackingRegressor Test MSE: {sklearn_mse_test:.4f}")

