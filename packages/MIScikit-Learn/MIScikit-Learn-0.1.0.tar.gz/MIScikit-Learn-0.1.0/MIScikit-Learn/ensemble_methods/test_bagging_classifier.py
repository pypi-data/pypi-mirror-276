import numpy as np
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import BaggingClassifier as SklearnBaggingClassifier
from bagging_classifier import BaggingClassifier

# Load dataset
X, y = load_iris(return_X_y=True)
y = (y == 0).astype(int)  # Convert to binary classification problem

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize base estimator
base_estimator = DecisionTreeClassifier()

# Initialize and fit the custom BaggingClassifier
custom_bagging = BaggingClassifier(base_estimator=base_estimator, n_estimators=10, max_samples=0.8, random_state=42)
custom_bagging.fit(X_train, y_train)

# Predictions
custom_y_pred = custom_bagging.predict(X_test)

# Calculate accuracy
custom_accuracy = accuracy_score(y_test, custom_y_pred)

# Initialize and fit the scikit-learn BaggingClassifier
sklearn_bagging = SklearnBaggingClassifier(base_estimator=base_estimator, n_estimators=10, max_samples=0.8, random_state=42)
sklearn_bagging.fit(X_train, y_train)

# Predictions
sklearn_y_pred = sklearn_bagging.predict(X_test)

# Calculate accuracy
sklearn_accuracy = accuracy_score(y_test, sklearn_y_pred)

# Display results
print(f"Custom BaggingClassifier accuracy: {custom_accuracy:.4f}")
print(f"Scikit-learn BaggingClassifier accuracy: {sklearn_accuracy:.4f}")

# Simple unit test
assert abs(custom_accuracy - sklearn_accuracy) < 0.1, "Accuracy difference between custom and sklearn implementations is too high!"
print("Unit test passed!")
