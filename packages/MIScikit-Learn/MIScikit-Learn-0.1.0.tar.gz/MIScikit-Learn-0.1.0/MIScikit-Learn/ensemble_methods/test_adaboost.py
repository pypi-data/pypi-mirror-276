import numpy as np
from adaboost import AdaBoostClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier as SklearnAdaBoost

# Sample data for testing
X, y = load_iris(return_X_y=True)
y = (y == 0).astype(int)  # Convert to binary classification problem

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the custom AdaBoostClassifier
custom_ada = AdaBoostClassifier(n_estimators=50, learning_rate=1.0)
custom_ada.fit(X_train, y_train)

# Predictions
custom_y_pred = custom_ada.predict(X_test)

# Calculate accuracy
custom_accuracy = accuracy_score(y_test, custom_y_pred)

# Initialize and fit the scikit-learn AdaBoostClassifier
sklearn_ada = SklearnAdaBoost(n_estimators=50, learning_rate=1.0, random_state=42)
sklearn_ada.fit(X_train, y_train)

# Predictions
sklearn_y_pred = sklearn_ada.predict(X_test)

# Calculate accuracy
sklearn_accuracy = accuracy_score(y_test, sklearn_y_pred)

# Display results
print(f"Custom AdaBoostClassifier accuracy: {custom_accuracy:.4f}")
print(f"Scikit-learn AdaBoostClassifier accuracy: {sklearn_accuracy:.4f}")

# Simple unit test
assert abs(custom_accuracy - sklearn_accuracy) < 0.1, "Accuracy difference between custom and sklearn implementations is too high!"
print("Unit test passed!")
