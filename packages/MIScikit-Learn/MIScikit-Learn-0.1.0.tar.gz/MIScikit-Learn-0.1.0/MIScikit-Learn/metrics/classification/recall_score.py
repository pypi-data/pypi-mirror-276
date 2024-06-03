import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score as sklearn_recall_score

def recall_score(y_true, y_pred):
    """
    Compute the recall score.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True binary labels.
    y_pred : array-like of shape (n_samples,)
        Predicted binary labels.

    Returns
    -------
    recall : float
        Recall score.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    true_positive = np.sum((y_true == 1) & (y_pred == 1))
    false_negative = np.sum((y_true == 1) & (y_pred == 0))
    
    if true_positive + false_negative == 0:
        return 0.0  # Avoid division by zero
    
    recall = true_positive / (true_positive + false_negative)
    return recall

# Load the Breast Cancer Wisconsin dataset
data = load_breast_cancer()
X, y = data.data, data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train the Logistic Regression model
model = LogisticRegression(max_iter=10000)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Custom recall score
custom_recall = recall_score(y_test, y_pred)
print(f"Custom Recall: {custom_recall:.4f}")

# Scikit-Learn recall score
sklearn_recall = sklearn_recall_score(y_test, y_pred)
print(f"Scikit-Learn Recall: {sklearn_recall:.4f}")

# Ensure they are the same
assert np.isclose(custom_recall, sklearn_recall), "The recall scores do not match!"
