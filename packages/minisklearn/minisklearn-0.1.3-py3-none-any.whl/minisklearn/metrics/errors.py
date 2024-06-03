import numpy as np

def mean_absolute_error(y_true, y_pred):
    """
    Compute the mean absolute error between true labels and predicted labels.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: Mean absolute error.
    """
    return np.mean(np.abs(y_true - y_pred))

def mean_squared_error(y_true, y_pred):
    """
    Compute the mean squared error between true labels and predicted labels.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: Mean squared error.
    """
    return np.mean((y_true - y_pred) ** 2)

def median_absolute_error(y_true, y_pred):
    """
    Compute the median absolute error between true labels and predicted labels.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: Median absolute error.
    """
    return np.median(np.abs(y_true - y_pred))

def r2_score(y_true, y_pred):
    """
    Compute the R-squared score between true labels and predicted labels.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: R-squared score.
    """
    rss = np.sum((y_true - y_pred) ** 2)
    tss = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - rss / tss




