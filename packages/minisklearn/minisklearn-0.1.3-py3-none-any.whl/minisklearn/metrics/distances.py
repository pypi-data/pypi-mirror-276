import numpy as np

def cosine_similarity(X, Y=None):
    """
    Compute the cosine similarity between arrays X and Y.

    Parameters:
    - X (array-like): First input array.
    - Y (array-like, optional): Second input array. If not provided, Y is set to X.

    Returns:
    - array: Cosine similarity between X and Y.
    """
    # Normalize X
    X_normalized = X / np.sqrt(np.sum(np.square(X), axis=1))[:, np.newaxis]

    if Y is None:
        # If Y is not provided, use X_normalized for Y_normalized
        Y_normalized = X_normalized
    else:
        # Normalize Y
        Y_normalized = Y / np.sqrt(np.sum(np.square(Y), axis=1))[:, np.newaxis]

    # Compute cosine similarity
    similarity = np.dot(X_normalized, Y_normalized.T)
    return similarity

def cosine_distances(X, Y=None):
    """
    Compute the cosine distances between arrays X and Y.

    Parameters:
    - X (array-like): First input array.
    - Y (array-like, optional): Second input array. If not provided, Y is set to X.

    Returns:
    - array: Cosine distances between X and Y.
    """
    return 1 - cosine_similarity(X,Y)

def euclidean_distances(X, Y=None):
    """
    Compute the Euclidean distances between arrays X and Y.

    Parameters:
    - X (array-like): First input array.
    - Y (array-like, optional): Second input array. If not provided, Y is set to X.

    Returns:
    - array: Euclidean distances between X and Y.
    """
    # Compute XX which is the sum of squares of elements in X
    XX = np.sum(np.square(X), axis=1)[:, np.newaxis]

    if Y is None:
        # If Y is not provided, set YY to be the transpose of XX and compute XY as dot product of X with its transpose
        YY = XX.T
        XY = np.dot(X, X.T)
    else:
        # Compute YY which is the sum of squares of elements in Y and XY as dot product of X and Y transposed
        YY = np.sum(np.square(Y), axis=1)[np.newaxis, :]
        XY = np.dot(X, Y.T)

    # Compute the squared Euclidean distances
    dist_squared = -2 * XY + XX + YY

    # Set any negative values in dist_squared to 0 (this can happen due to numerical precision)
    dist_squared[dist_squared < 0] = 0

    # Take the square root to obtain the Euclidean distances
    distances = np.sqrt(dist_squared)

    return distances