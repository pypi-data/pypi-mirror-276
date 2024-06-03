import numpy as np

def accuracy_score(y_true, y_pred, normalize=True, sample_weight=None):
    """
    Calculate accuracy classification score.
    
    Args:
    y_true (array-like): Ground truth (correct) labels.
    y_pred (array-like): Predicted labels, as returned by a classifier.
    normalize (bool, optional): If True, return the fraction of correctly classified samples. Defaults to True.
    sample_weight (array-like, optional): Sample weights. Defaults to None.
    
    Returns:
    float: If normalize is True, return the fraction of correctly classified samples; otherwise, return the number of correctly classified samples.
    """
    # Ensure input is numpy arrays for consistency
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Check if sample weights are provided
    if sample_weight is not None:
        sample_weight = np.array(sample_weight)
        correct = sample_weight * (y_true == y_pred)
        correct_sum = correct.sum()
    else:
        correct_sum = np.sum(y_true == y_pred)
    
    if normalize:
        total = len(y_true)
        if sample_weight is not None:
            total = sample_weight.sum()
        return correct_sum / total
    else:
        return correct_sum


def balanced_accuracy_score(y_true, y_pred, sample_weight=None, adjusted=False):
    """
    Calculate the balanced accuracy score.
    
    Args:
    y_true (array-like): Ground truth (correct) target values.
    y_pred (array-like): Estimated targets as returned by a classifier.
    sample_weight (array-like, optional): Sample weights. Defaults to None.
    adjusted (bool, optional): Adjust for chance to make random performance score 0. Defaults to False.
    
    Returns:
    float: Balanced accuracy score.
    """
    # Convert inputs to numpy arrays
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Unique classes in y_true
    classes = np.unique(y_true)
    recalls = []
    
    # Compute recall for each class
    for cls in classes:
        cls_mask = (y_true == cls)
        cls_true = np.sum(cls_mask)
        if sample_weight is not None:
            cls_pred_correct = np.sum((y_pred == cls) & cls_mask * sample_weight)
            cls_true_weighted = np.sum(cls_mask * sample_weight)
            recall = cls_pred_correct / cls_true_weighted if cls_true_weighted > 0 else 0
        else:
            cls_pred_correct = np.sum((y_pred == cls) & cls_mask)
            recall = cls_pred_correct / cls_true if cls_true > 0 else 0
        recalls.append(recall)
    
    balanced_acc = np.mean(recalls)
    
    if adjusted:
        random_acc = 1 / len(classes)
        balanced_acc = (balanced_acc - random_acc) / (1 - random_acc)
    
    return balanced_acc


def top_k_accuracy_score(y_true, y_score, k=2, normalize=True, sample_weight=None, labels=None):
    """
    Calculate the top-k accuracy classification score.
    
    Args:
    y_true (array-like): True labels.
    y_score (array-like): Target scores. These can be probability estimates or non-thresholded decision values.
    k (int, optional): Number of most likely outcomes considered to find the correct label. Defaults to 2.
    normalize (bool, optional): If True, return the fraction of correctly classified samples. Defaults to True.
    sample_weight (array-like, optional): Sample weights. Defaults to None.
    labels (array-like, optional): List of labels indexing the classes in y_score. Defaults to None.
    
    Returns:
    float: The top-k accuracy score.
    """
    # Ensure input is numpy arrays for consistency
    y_true = np.array(y_true)
    y_score = np.array(y_score)
    
    if labels is not None:
        labels = np.array(labels)
        label_order = np.argsort(labels)
    else:
        labels = np.unique(y_true)
        label_order = np.argsort(labels)
    
    # Index the scores according to the label order
    y_score = y_score[:, label_order]

    # Get the indices of the top k scores
    top_k_predictions = np.argsort(y_score, axis=1)[:, -k:]
    
    # Check if true labels are in top k predictions
    correct = np.any(top_k_predictions == y_true[:, None], axis=1)
    
    if sample_weight is not None:
        sample_weight = np.array(sample_weight)
        correct = sample_weight * correct
        score = correct.sum()
    else:
        score = correct.sum()
    
    if normalize:
        total = sample_weight.sum() if sample_weight is not None else len(y_true)
        return score / total
    else:
        return score


