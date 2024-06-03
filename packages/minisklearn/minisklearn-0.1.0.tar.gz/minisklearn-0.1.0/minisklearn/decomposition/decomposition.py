import numpy as np
from base import Transformer
from scipy.linalg import svd

class PCA(Transformer):
    """
    Principal Component Analysis (PCA) for dimensionality reduction.

    This class performs dimensionality reduction using PCA.

    Parameters:
    n_components : int, default=2
        Number of components to keep.

    Attributes:
    mean_ : array-like, shape (n_features,)
        Mean of each feature in the training data.
    components_ : array-like, shape (n_components, n_features)
        Principal axes in feature space, representing the directions of maximum variance.
    explained_variance_ratio_ : array-like, shape (n_components,)
        Percentage of variance explained by each of the selected components.

    Methods:
    fit(X): Fit the model with the training data X.
    transform(X): Apply dimensionality reduction to X.
    inverse_transform(X): Transform data back to its original space.
    """

    def __init__(self, n_components=2):
        # Initialize number of components
        self.n_components = n_components

    def fit(self, X):
        """
        Fit the model with the training data X.

        Parameters:
        X : array-like, shape (n_samples, n_features)
            Training data.

        Returns:
        self : object
            Returns the instance itself.
        """
        # Compute mean of each feature
        self.mean_ = np.mean(X, axis=0)
        # Center data
        X_train = X - self.mean_
        # Perform Singular Value Decomposition (SVD)
        U, S, V = svd(X_train, full_matrices=False)
        # Extract principal components
        self.components_ = V[:self.n_components]
        # Calculate explained variance ratio
        self.explained_variance_ratio_ = np.square(S[:self.n_components]) / np.sum(np.square(S))
        return self

    def transform(self, X):
        """
        Apply dimensionality reduction to X.

        Parameters:
        X : array-like, shape (n_samples, n_features)
            Data to transform.

        Returns:
        array-like, shape (n_samples, n_components)
            Transformed data.
        """
        # Center data
        X_train = X - self.mean_
        # Project data onto principal components
        return np.dot(X_train, self.components_.T)

    def inverse_transform(self, X):
        """
        Transform data back to its original space.

        Parameters:
        X : array-like, shape (n_samples, n_components)
            Data to transform.

        Returns:
        array-like, shape (n_samples, n_features)
            Original data.
        """
        # Transform data back to original space
        return np.dot(X, self.components_) + self.mean_
