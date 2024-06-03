import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from GradientBoostingRegressor import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor as SklearnGradientBoostingRegressor

# Generate a random regression problem
X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the custom and sklearn GradientBoostingRegressors
custom_gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
sklearn_gbr = SklearnGradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Fit the models
custom_gbr.fit(X_train, y_train)
sklearn_gbr.fit(X_train, y_train)

# Make predictions
custom_preds = custom_gbr.predict(X_test)
sklearn_preds = sklearn_gbr.predict(X_test)

# Calculate Mean Squared Error
custom_mse = mean_squared_error(y_test, custom_preds)
sklearn_mse = mean_squared_error(y_test, sklearn_preds)

# Print the results
print(f"Custom GradientBoostingRegressor MSE: {custom_mse:.4f}")
print(f"Scikit-Learn GradientBoostingRegressor MSE: {sklearn_mse:.4f}")
