import numpy as np
from variance_threshold import VarianceThreshold
from sklearn.feature_selection import VarianceThreshold as SklearnVarianceThreshold

# Sample data
X = np.array([
    [0, 2, 0, 3],
    [0, 1, 4, 3],
    [0, 1, 1, 3]
])

# Initialize the VarianceThreshold from our implementation
vt = VarianceThreshold(threshold=0.1)
vt.fit(X)
X_transformed = vt.transform(X)

# Initialize the VarianceThreshold from scikit-learn
sklearn_vt = SklearnVarianceThreshold(threshold=0.1)
sklearn_vt.fit(X)
sklearn_X_transformed = sklearn_vt.transform(X)

# Display variances
print("Custom VarianceThreshold variances:", vt.variances_)
print("Scikit-learn VarianceThreshold variances:", sklearn_vt.variances_)

# Display transformed datasets
print("Custom VarianceThreshold transformed X:\n", X_transformed)
print("Scikit-learn VarianceThreshold transformed X:\n", sklearn_X_transformed)