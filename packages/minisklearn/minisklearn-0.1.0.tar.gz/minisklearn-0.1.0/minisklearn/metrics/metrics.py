import numpy as np
from scipy.sparse import coo_matrix

def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)


def average_precision_score(y_true, y_score):
    """
    Compute the average precision score given the true labels and predicted scores.

    Parameters:
    - y_true (array-like): True binary labels (0 or 1).
    - y_score (array-like): Predicted scores.

    Returns:
    - float: Average precision score.
    """
    # Sort scores in descending order
    desc_score_indices = np.argsort(y_score, kind="mergesort")[::-1]
    y_true_sorted = y_true[desc_score_indices]
    y_score_sorted = y_score[desc_score_indices]

    # Find indices where scores change
    distinct_value_indices = np.where(np.diff(y_score_sorted))[0]
    threshold_idxs = np.r_[distinct_value_indices, y_true_sorted.size - 1]

    # Calculate true positives and false positives at each threshold
    tps = np.cumsum(y_true_sorted)[threshold_idxs]
    fps = 1 + threshold_idxs - tps
    thresholds = y_score_sorted[threshold_idxs]

    # Compute precision and recall
    precision = tps / (tps + fps)
    recall = tps / tps[-1]

    # Add points for perfect precision-recall curve
    precision = np.r_[1, precision]
    recall = np.r_[0, recall]

    # Compute average precision using trapezoidal rule
    average_precision = np.sum(np.diff(recall) * np.array(precision)[1:])
    return average_precision



def confusion_matrix(y_true, y_pred):
    """
    Compute the confusion matrix given the true labels and predicted labels.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - array: Confusion matrix.
    """
    # Determine the number of unique labels
    n_labels = len(set(y_true) | set(y_pred))

    # Create a sparse matrix using COO format and convert it to a dense array
    cm = coo_matrix((np.ones(len(y_true)), (y_true, y_pred)), shape=(n_labels, n_labels)).toarray()
    return cm

def f1_score(y_true, y_pred, average='binary'):
    """
    Compute the F1 score given the true labels, predicted labels, and averaging method.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.
    - average (str, optional): Averaging method ('binary', 'micro', 'weighted', or None).

    Returns:
    - float: F1 score.
    """
    # Determine the number of unique labels
    n_labels = len(set(y_true) | set(y_pred))

    # Compute true positives, true sums, and predicted sums
    true_sum = np.bincount(y_true, minlength=n_labels)
    pred_sum = np.bincount(y_pred, minlength=n_labels)
    tp = np.bincount(y_true[y_true == y_pred], minlength=n_labels)

    # Adjust calculations based on the averaging method
    if average == "binary":
        tp = np.array([tp[1]])
        true_sum = np.array([true_sum[1]])
        pred_sum = np.array([pred_sum[1]])
    elif average == "micro":
        tp = np.array([np.sum(tp)])
        true_sum = np.array([np.sum(true_sum)])
        pred_sum = np.array([np.sum(pred_sum)])

    # Compute precision, recall, and F1 score
    precision = np.zeros(len(pred_sum))
    mask = pred_sum != 0
    precision[mask] = tp[mask] / pred_sum[mask]

    recall = np.zeros(len(true_sum))
    mask = true_sum != 0
    recall[mask] = tp[mask] / true_sum[mask]

    denom = precision + recall
    denom[denom == 0.] = 1
    fscore = 2 * precision * recall / denom

    # Compute final F1 score based on the averaging method
    if average == "weighted":
        fscore = np.average(fscore, weights=true_sum)
    elif average is not None:
        fscore = np.mean(fscore)

    return fscore


def precision_recall_curve(y_true, y_score):
    """
    Compute precision-recall pairs for different thresholds.

    Parameters:
    - y_true (array-like): True binary labels (0 or 1).
    - y_score (array-like): Predicted scores.

    Returns:
    - tuple: (precision, recall, thresholds)
      precision (array): Precision values.
      recall (array): Recall values.
      thresholds (array): Thresholds used.
    """
    # Sort scores in descending order
    desc_score_indices = np.argsort(y_score, kind="mergesort")[::-1]
    y_true_sorted = y_true[desc_score_indices]
    y_score_sorted = y_score[desc_score_indices]

    # Find indices where scores change
    distinct_value_indices = np.where(np.diff(y_score_sorted))[0]
    threshold_idxs = np.r_[distinct_value_indices, y_true_sorted.size - 1]

    # Calculate true positives and false positives at each threshold
    tps = np.cumsum(y_true_sorted)[threshold_idxs]
    fps = 1 + threshold_idxs - tps
    thresholds = y_score_sorted[threshold_idxs]

    # Compute precision and recall
    precision = tps / (tps + fps)
    recall = tps / tps[-1]

    # Reverse arrays for descending order
    last_ind = tps.searchsorted(tps[-1])
    sl = slice(last_ind, None, -1)

    return np.r_[precision[sl], 1], np.r_[recall[sl], 0], thresholds[sl]

def precision_score(y_true, y_pred, average='binary'):
    """
    Compute the precision score given the true labels, predicted labels, and averaging method.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.
    - average (str, optional): Averaging method ('binary', 'micro', 'weighted', or None).

    Returns:
    - float: Precision score.
    """
    # Determine the number of unique labels
    n_labels = len(set(y_true) | set(y_pred))

    # Compute true positives, true sums, and predicted sums
    true_sum = np.bincount(y_true, minlength=n_labels)
    pred_sum = np.bincount(y_pred, minlength=n_labels)
    tp = np.bincount(y_true[y_true == y_pred], minlength=n_labels)

    # Adjust calculations based on the averaging method
    if average == "binary":
        tp = np.array([tp[1]])
        pred_sum = np.array([pred_sum[1]])
    elif average == "micro":
        tp = np.array([np.sum(tp)])
        pred_sum = np.array([np.sum(pred_sum)])

    # Compute precision
    precision = np.zeros(len(pred_sum))
    mask = pred_sum != 0
    precision[mask] = tp[mask] / pred_sum[mask]

    # Compute final precision score based on the averaging method
    if average == "weighted":
        precision = np.average(precision, weights=true_sum)
    elif average is not None:
        precision = np.mean(precision)

    return precision


def recall_score(y_true, y_pred, average='binary'):
    """
    Compute the recall score given the true labels, predicted labels, and averaging method.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.
    - average (str, optional): Averaging method ('binary', 'micro', 'weighted', or None).

    Returns:
    - float: Recall score.
    """
    # Determine the number of unique labels
    n_labels = len(set(y_true) | set(y_pred))

    # Compute true positives, true sums, and predicted sums
    true_sum = np.bincount(y_true, minlength=n_labels)
    pred_sum = np.bincount(y_pred, minlength=n_labels)
    tp = np.bincount(y_true[y_true == y_pred], minlength=n_labels)

    # Adjust calculations based on the averaging method
    if average == "binary":
        tp = np.array([tp[1]])
        true_sum = np.array([true_sum[1]])
    elif average == "micro":
        tp = np.array([np.sum(tp)])
        true_sum = np.array([np.sum(true_sum)])

    # Compute recall
    recall = np.zeros(len(true_sum))
    mask = true_sum != 0
    recall[mask] = tp[mask] / true_sum[mask]

    # Compute final recall score based on the averaging method
    if average == "weighted":
        recall = np.average(recall, weights=true_sum)
    elif average is not None:
        recall = np.mean(recall)

    return recall



def roc_auc_score(y_true, y_score):
    """
    Compute the area under the receiver operating characteristic curve (ROC AUC) given true labels and predicted scores.

    Parameters:
    - y_true (array-like): True binary labels (0 or 1).
    - y_score (array-like): Predicted scores.

    Returns:
    - float: ROC AUC score.
    """
    # Sort scores in descending order
    desc_score_indices = np.argsort(y_score, kind="mergesort")[::-1]
    y_true_sorted = y_true[desc_score_indices]
    y_score_sorted = y_score[desc_score_indices]

    # Find indices where scores change
    distinct_value_indices = np.where(np.diff(y_score_sorted))[0]
    threshold_idxs = np.r_[distinct_value_indices, y_true_sorted.size - 1]

    # Calculate true positives and false positives at each threshold
    tps = np.cumsum(y_true_sorted)[threshold_idxs]
    fps = 1 + threshold_idxs - tps

    # Add origin (0, 0) to TPR and FPR arrays
    tps = np.r_[0, tps]
    fps = np.r_[0, fps]

    # Compute true positive rate (TPR) and false positive rate (FPR)
    tpr = tps / tps[-1]
    fpr = fps / fps[-1]

    # Compute ROC AUC using trapezoidal rule
    roc_auc = np.trapz(tpr, fpr)

    return roc_auc



def roc_curve(y_true, y_score):
    """
    Compute the Receiver Operating Characteristic (ROC) curve given true labels and predicted scores.

    Parameters:
    - y_true (array-like): True binary labels (0 or 1).
    - y_score (array-like): Predicted scores.

    Returns:
    - tuple: (fpr, tpr, thresholds)
      fpr (array): False Positive Rate values.
      tpr (array): True Positive Rate values.
      thresholds (array): Thresholds used.
    """
    # Sort scores in descending order
    desc_score_indices = np.argsort(y_score, kind="mergesort")[::-1]
    y_true_sorted = y_true[desc_score_indices]
    y_score_sorted = y_score[desc_score_indices]

    # Find indices where scores change
    distinct_value_indices = np.where(np.diff(y_score_sorted))[0]
    threshold_idxs = np.r_[distinct_value_indices, y_true_sorted.size - 1]

    # Calculate true positives and false positives at each threshold
    tps = np.cumsum(y_true_sorted)[threshold_idxs]
    fps = 1 + threshold_idxs - tps
    thresholds = y_score_sorted[threshold_idxs]

    # Add origin (0, 0) to TPR and FPR arrays
    tps = np.r_[0, tps]
    fps = np.r_[0, fps]
    thresholds = np.r_[thresholds[0] + 1, thresholds]  # Add a threshold just below the lowest score

    # Compute True Positive Rate (TPR) and False Positive Rate (FPR)
    tpr = tps / tps[-1]
    fpr = fps / fps[-1]

    return fpr, tpr, thresholds




