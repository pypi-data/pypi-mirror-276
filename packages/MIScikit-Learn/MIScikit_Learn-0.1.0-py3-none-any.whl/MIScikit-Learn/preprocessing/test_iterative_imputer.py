import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer as SklearnIterativeImputer
from iterative_imputer import IterativeImputer

# Generate sample data with missing values
X = np.array([[1, 2, np.nan], [np.nan, 5, 6], [7, np.nan, 9], [10, 11, 12]])

# Custom IterativeImputer
custom_iterative_imputer = IterativeImputer()
X_custom_imputed = custom_iterative_imputer.fit_transform(X)

# Scikit-learn IterativeImputer
sklearn_iterative_imputer = SklearnIterativeImputer()
X_sklearn_imputed = sklearn_iterative_imputer.fit_transform(X)

# Print results for comparison
print("Original Data:\n", X)

print("\nCustom IterativeImputer - Imputed Data:\n", X_custom_imputed)
print("Scikit-Learn IterativeImputer - Imputed Data:\n", X_sklearn_imputed)

# Assertions to ensure they are almost equal
np.testing.assert_almost_equal(X_custom_imputed, X_sklearn_imputed, decimal=6)

print("\nCustom IterativeImputer matches Scikit-Learn IterativeImputer!")
