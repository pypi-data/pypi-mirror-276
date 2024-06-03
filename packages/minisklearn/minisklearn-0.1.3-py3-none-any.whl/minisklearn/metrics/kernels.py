import numpy as np

def linear_kernel(X, Y=None):
    """
    Compute the linear kernel between arrays X and Y.

    Parameters:
    - X (array-like): First input array.
    - Y (array-like, optional): Second input array. If not provided, Y is set to X.

    Returns:
    - array: Linear kernel between X and Y.
    """
    if Y is None:
        Y = X

    # Compute the dot product between X and the transpose of Y
    kernel = np.dot(X, Y.T)
    return kernel

def rbf_kernel(X, Y=None, gamma=None):
    """
    Compute the Radial Basis Function (RBF) kernel between arrays X and Y.

    Parameters:
    - X (array-like): First input array.
    - Y (array-like, optional): Second input array. If not provided, Y is set to X.
    - gamma (float, optional): Gamma parameter for the RBF kernel. If not provided, gamma is set to 1 / X.shape[1].

    Returns:
    - array: RBF kernel between X and Y.
    """
    if Y is None:
        Y = X

    if gamma is None:
        gamma = 1 / X.shape[1]

    K = np.zeros((X.shape[0], Y.shape[0]))

    for i in range(X.shape[0]):
        for j in range(Y.shape[0]):
            K[i, j] = np.exp(-gamma * np.sum(np.square(X[i] - Y[j])))

    return K