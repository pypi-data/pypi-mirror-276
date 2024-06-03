import numpy as np
from sklearn.metrics import precision_score as sklearn_precision_score

def precision_score(y_true, y_pred):
    """
    Compute the precision score.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True binary labels.
    y_pred : array-like of shape (n_samples,)
        Predicted binary labels.

    Returns
    -------
    precision : float
        Precision score.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    true_positive = np.sum((y_true == 1) & (y_pred == 1))
    false_positive = np.sum((y_true == 0) & (y_pred == 1))
    
    if true_positive + false_positive == 0:
        return 0.0  # Avoid division by zero
    
    precision = true_positive / (true_positive + false_positive)
    return precision

# Example usage
y_true = [0, 1, 1, 0, 1, 1, 0, 0, 0, 1]
y_pred = [0, 1, 0, 0, 1, 1, 0, 0, 1, 1]

precision = precision_score(y_true, y_pred)
print(f"Precision: {precision:.4f}")

sklearn_precision = sklearn_precision_score(y_true, y_pred)
print(f"Scikit-Learn Precision: {sklearn_precision:.4f}")
