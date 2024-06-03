import numpy as np
from sklearn.impute import SimpleImputer as SklearnSimpleImputer
from simple_imputer import SimpleImputer

# Generate sample data with missing values
X = np.array([[1, 2, np.nan], [np.nan, 5, 6], [7, np.nan, 9], [10, 11, 12]])

# Custom SimpleImputer with strategy 'mean'
custom_imputer_mean = SimpleImputer(strategy='mean')
X_custom_imputed_mean = custom_imputer_mean.fit_transform(X)

# Scikit-learn SimpleImputer with strategy 'mean'
sklearn_imputer_mean = SklearnSimpleImputer(strategy='mean')
X_sklearn_imputed_mean = sklearn_imputer_mean.fit_transform(X)

# Print results for comparison
print("Original Data:\n", X)

print("\nCustom SimpleImputer (Mean) - Imputed Data:\n", X_custom_imputed_mean)
print("Scikit-Learn SimpleImputer (Mean) - Imputed Data:\n", X_sklearn_imputed_mean)

# Assertions to ensure they are almost equal
np.testing.assert_almost_equal(X_custom_imputed_mean, X_sklearn_imputed_mean, decimal=6)

print("\nCustom SimpleImputer (Mean) matches Scikit-Learn SimpleImputer (Mean)!")


# Custom SimpleImputer with strategy 'median'
custom_imputer_median = SimpleImputer(strategy='median')
X_custom_imputed_median = custom_imputer_median.fit_transform(X)

# Scikit-learn SimpleImputer with strategy 'median'
sklearn_imputer_median = SklearnSimpleImputer(strategy='median')
X_sklearn_imputed_median = sklearn_imputer_median.fit_transform(X)

# Print results for comparison
print("\nCustom SimpleImputer (Median) - Imputed Data:\n", X_custom_imputed_median)
print("Scikit-Learn SimpleImputer (Median) - Imputed Data:\n", X_sklearn_imputed_median)

# Assertions to ensure they are almost equal
np.testing.assert_almost_equal(X_custom_imputed_median, X_sklearn_imputed_median, decimal=6)

print("\nCustom SimpleImputer (Median) matches Scikit-Learn SimpleImputer (Median)!")
