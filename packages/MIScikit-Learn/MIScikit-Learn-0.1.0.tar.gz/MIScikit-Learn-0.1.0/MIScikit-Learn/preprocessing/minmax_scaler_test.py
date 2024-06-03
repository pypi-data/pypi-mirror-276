import numpy as np
from sklearn.preprocessing import MinMaxScaler as SklearnMinMaxScaler
from minmax_scaler import MinMaxScaler

# Generate sample data
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 100], [10, 11, 12]])

# Custom MinMaxScaler
custom_minmax_scaler = MinMaxScaler()
X_custom_minmax_scaled = custom_minmax_scaler.fit_transform(X)
X_custom_minmax_inversed = custom_minmax_scaler.inverse_transform(X_custom_minmax_scaled)

# Scikit-learn MinMaxScaler
sklearn_minmax_scaler = SklearnMinMaxScaler()
X_sklearn_minmax_scaled = sklearn_minmax_scaler.fit_transform(X)
X_sklearn_minmax_inversed = sklearn_minmax_scaler.inverse_transform(X_sklearn_minmax_scaled)

# Print results for comparison
print("Original Data:\n", X)

print("\nCustom MinMaxScaler - Scaled Data:\n", X_custom_minmax_scaled)
print("Scikit-Learn MinMaxScaler - Scaled Data:\n", X_sklearn_minmax_scaled)
print("\nCustom MinMaxScaler - Inverse Scaled Data:\n", X_custom_minmax_inversed)
print("Scikit-Learn MinMaxScaler - Inverse Scaled Data:\n", X_sklearn_minmax_inversed)

# Assertions to ensure they are almost equal
np.testing.assert_almost_equal(X_custom_minmax_scaled, X_sklearn_minmax_scaled, decimal=6)
np.testing.assert_almost_equal(X_custom_minmax_inversed, X_sklearn_minmax_inversed, decimal=6)

print("\nCustom MinMaxScaler matches Scikit-Learn MinMaxScaler!")
