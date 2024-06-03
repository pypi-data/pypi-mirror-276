import numpy as np
from sklearn.preprocessing import MaxAbsScaler as SklearnMaxAbsScaler
from maxabs_scaler import MaxAbsScaler

# Generate sample data
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 100], [10, 11, 12]])

# Custom MaxAbsScaler
custom_maxabs_scaler = MaxAbsScaler()
X_custom_maxabs_scaled = custom_maxabs_scaler.fit_transform(X)
X_custom_maxabs_inversed = custom_maxabs_scaler.inverse_transform(X_custom_maxabs_scaled)

# Scikit-learn MaxAbsScaler
sklearn_maxabs_scaler = SklearnMaxAbsScaler()
X_sklearn_maxabs_scaled = sklearn_maxabs_scaler.fit_transform(X)
X_sklearn_maxabs_inversed = sklearn_maxabs_scaler.inverse_transform(X_sklearn_maxabs_scaled)

# Print results for comparison
print("Original Data:\n", X)

print("\nCustom MaxAbsScaler - Scaled Data:\n", X_custom_maxabs_scaled)
print("Scikit-Learn MaxAbsScaler - Scaled Data:\n", X_sklearn_maxabs_scaled)
print("\nCustom MaxAbsScaler - Inverse Scaled Data:\n", X_custom_maxabs_inversed)
print("Scikit-Learn MaxAbsScaler - Inverse Scaled Data:\n", X_sklearn_maxabs_inversed)

# Assertions to ensure they are almost equal
np.testing.assert_almost_equal(X_custom_maxabs_scaled, X_sklearn_maxabs_scaled, decimal=6)
np.testing.assert_almost_equal(X_custom_maxabs_inversed, X_sklearn_maxabs_inversed, decimal=6)

print("\nCustom MaxAbsScaler matches Scikit-Learn MaxAbsScaler!")
