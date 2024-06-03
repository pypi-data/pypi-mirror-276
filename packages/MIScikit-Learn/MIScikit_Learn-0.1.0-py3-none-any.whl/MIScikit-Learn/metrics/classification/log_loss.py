import numpy as np

def log_loss(y_true, y_pred, eps=1e-15, normalize=True, sample_weight=None, labels=None):
    """
    Compute log loss, aka logistic loss or cross-entropy loss, from scratch.

    Args:
    y_true (array-like): True labels.
    y_pred (array-like): Predicted probabilities.
    eps (float, optional): Small value to clip probabilities to avoid log(0) error. Defaults to 1e-15.
    normalize (bool, optional): If true, return the mean loss per sample. Otherwise, return the sum. Defaults to True.
    sample_weight (array-like, optional): Sample weights. Defaults to None.
    labels (array-like, optional): List of labels. Defaults to None.

    Returns:
    float: Log loss.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    if labels is None:
        labels = np.unique(y_true)
    else:
        labels = np.array(labels)
    
    # Clipping probabilities to avoid log(0) error
    y_pred = np.clip(y_pred, eps, 1 - eps)
    
    # Ensure y_pred is of shape (n_samples, n_classes)
    if y_pred.ndim == 1:
        y_pred = np.vstack([1 - y_pred, y_pred]).T
    
    # Transform y_true to a binary matrix in case of multiclass (one-hot encoding)
    y_true_encoded = np.zeros_like(y_pred)
    for i, label in enumerate(labels):
        y_true_encoded[:, i] = (y_true == label).astype(int)

    # Compute log loss
    log_losses = -np.sum(y_true_encoded * np.log(y_pred) + (1 - y_true_encoded) * np.log(1 - y_pred), axis=1)
    
    if sample_weight is not None:
        log_losses *= sample_weight
    
    if normalize:
        return np.mean(log_losses)
    else:
        return np.sum(log_losses)

from sklearn.metrics import log_loss as sklearn_log_loss

# Test data
y_true = ["spam", "ham", "ham", "spam"]
y_pred = [[.1, .9], [.9, .1], [.8, .2], [.35, .65]]

# Convert string labels to integers for custom function
label_map = {"spam": 0, "ham": 1}
y_true_numeric = [label_map[label] for label in y_true]


# Using the revised implementation
our_log_loss = log_loss(y_true, y_pred)

# Using sklearn's implementation
sklearn_log_loss_value = sklearn_log_loss(y_true, y_pred)

print("Our Log Loss:", our_log_loss)
print("Sklearn Log Loss:", sklearn_log_loss_value)
