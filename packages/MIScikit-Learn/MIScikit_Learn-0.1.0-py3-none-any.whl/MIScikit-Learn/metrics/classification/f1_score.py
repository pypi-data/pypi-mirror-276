import numpy as np

def f1_score(y_true, y_pred, labels=None, pos_label=1, average='binary', sample_weight=None, zero_division='warn'):
    """
    Compute the F1 score from scratch.
    
    Args:
    y_true (array-like): True labels.
    y_pred (array-like): Predicted labels.
    labels (array-like, optional): Labels to include in F1 calculation.
    pos_label (int/float/bool/str, optional): Positive class label for binary classification.
    average (str, optional): Type of averaging ('binary', 'micro', 'macro', 'weighted').
    sample_weight (array-like, optional): Sample weights.
    zero_division (str/float, optional): Handle division by zero as 'warn', 0, 1, or np.nan.
    
    Returns:
    float or ndarray: F1 score or array of F1 scores.
    """
    # Convert labels to a sorted array if they're provided, otherwise use the unique values in y_true
    if labels is None:
        labels = np.unique(np.concatenate([y_true, y_pred]))
    else:
        labels = np.array(labels)
        labels.sort()

    # Compute true positives, false positives, false negatives
    tp = np.zeros(len(labels))
    fp = np.zeros(len(labels))
    fn = np.zeros(len(labels))

    for i, label in enumerate(labels):
        tp[i] = np.sum((y_true == label) & (y_pred == label))
        fp[i] = np.sum((y_true != label) & (y_pred == label))
        fn[i] = np.sum((y_true == label) & (y_pred != label))

    if average == 'micro':
        tp_sum = np.sum(tp)
        fp_sum = np.sum(fp)
        fn_sum = np.sum(fn)
        precision = tp_sum / (tp_sum + fp_sum) if tp_sum + fp_sum > 0 else 0
        recall = tp_sum / (tp_sum + fn_sum) if tp_sum + fn_sum > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        return f1

    # Individual F1 scores per label
    f1_scores = 2 * tp / (2 * tp + fp + fn)
    f1_scores[np.isnan(f1_scores)] = 0.0  # Handle division by zero

    if average == 'binary':
        # Binary classification case: Only consider the F1 score for pos_label
        idx = np.where(labels == pos_label)[0][0]
        return f1_scores[idx]
    elif average == 'macro':
        return np.mean(f1_scores)
    elif average == 'weighted':
        weights = np.array([np.sum(y_true == label) for label in labels])
        return np.average(f1_scores, weights=weights)

    # Default: return F1 scores for each label
    return f1_scores