
from sklearn.ensemble import RandomForestRegressor as SklearnRandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from RandomForestRegressor import RandomForestRegressor

data = load_diabetes()
X, y = data.data, data.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

custom_rf = RandomForestRegressor(n_estimators=100, random_state=42)
custom_rf.fit(X_train, y_train)

# Predictions and evaluation
custom_pred_train = custom_rf.predict(X_train)
custom_pred_test = custom_rf.predict(X_test)
custom_mse_train = mean_squared_error(y_train, custom_pred_train)
custom_mse_test = mean_squared_error(y_test, custom_pred_test)
print(f"Custom RandomForestRegressor Train MSE: {custom_mse_train:.4f}")
print(f"Custom RandomForestRegressor Test MSE: {custom_mse_test:.4f}")

# Initialize and train the scikit-learn RandomForestRegressor
sklearn_rf = SklearnRandomForestRegressor(n_estimators=100, random_state=42)
sklearn_rf.fit(X_train, y_train)

# Predictions and evaluation for the scikit-learn RandomForestRegressor
sklearn_pred_train = sklearn_rf.predict(X_train)
sklearn_pred_test = sklearn_rf.predict(X_test)
sklearn_mse_train = mean_squared_error(y_train, sklearn_pred_train)
sklearn_mse_test = mean_squared_error(y_test, sklearn_pred_test)
print(f"Scikit-Learn RandomForestRegressor Train MSE: {sklearn_mse_train:.4f}")
print(f"Scikit-Learn RandomForestRegressor Test MSE: {sklearn_mse_test:.4f}")

