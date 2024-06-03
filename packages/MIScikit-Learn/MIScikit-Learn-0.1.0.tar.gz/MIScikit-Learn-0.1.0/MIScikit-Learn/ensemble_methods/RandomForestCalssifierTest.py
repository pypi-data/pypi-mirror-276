from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier as SklearnRandomForestClassifier
from RandomForestClassifier import RandomForestClassifier

data = load_iris()
X, y = data.data, data.target

# Split the data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
rf.fit(X_train, y_train)

# Predictions and evaluation
y_pred = rf.predict(X_test)
accuracy = rf.score(X_test, y_test)
print(f"Custom Random Forest Classifier Accuracy on Iris dataset: {accuracy:.4f}")

# Compare with Scikit-Learn's Random Forest Classifier
sklearn_rf = SklearnRandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
sklearn_rf.fit(X_train, y_train)
y_pred_sklearn = sklearn_rf.predict(X_test)
accuracy_sklearn = accuracy_score(y_test, y_pred_sklearn)
print(f"Scikit-Learn Random Forest Classifier Accuracy on Iris dataset: {accuracy_sklearn:.4f}")

data = load_wine()
X, y = data.data, data.target

# Split the data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train our Random Forest Classifier
rf = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
rf.fit(X_train, y_train)

# Predictions and evaluation
y_pred = rf.predict(X_test)
accuracy = rf.score(X_test, y_test)
print(f"Custom Random Forest Classifier Accuracy on Wine dataset: {accuracy:.4f}")

# Compare with Scikit-Learn's Random Forest Classifier
sklearn_rf = SklearnRandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
sklearn_rf.fit(X_train, y_train)
y_pred_sklearn = sklearn_rf.predict(X_test)
accuracy_sklearn = accuracy_score(y_test, y_pred_sklearn)
print(f"Scikit-Learn Random Forest Classifier Accuracy on Wine dataset: {accuracy_sklearn:.4f}")
