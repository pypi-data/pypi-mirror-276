import numpy as np
from sklearn.preprocessing import StandardScaler as SklearnStandardScaler
from standard_scaler import StandardScaler

# Generate sample data
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])

# Custom StandardScaler
custom_scaler = StandardScaler()
X_custom_scaled = custom_scaler.fit_transform(X)
X_custom_inversed = custom_scaler.inverse_transform(X_custom_scaled)

# Scikit-learn StandardScaler
sklearn_scaler = SklearnStandardScaler()
X_sklearn_scaled = sklearn_scaler.fit_transform(X)
X_sklearn_inversed = sklearn_scaler.inverse_transform(X_sklearn_scaled)

# Print results for comparison
print("Original Data:\n", X)
print("\nCustom Scaler - Scaled Data:\n", X_custom_scaled)
print("Scikit-Learn Scaler - Scaled Data:\n", X_sklearn_scaled)

print("\nCustom Scaler - Inverse Scaled Data:\n", X_custom_inversed)
print("Scikit-Learn Scaler - Inverse Scaled Data:\n", X_sklearn_inversed)

# Assertions to ensure they are almost equal
np.testing.assert_almost_equal(X_custom_scaled, X_sklearn_scaled, decimal=6)
np.testing.assert_almost_equal(X_custom_inversed, X_sklearn_inversed, decimal=6)

print("\nCustom scaler matches Scikit-Learn scaler!")
