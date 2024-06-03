import numpy as np
from base import Predictor

class KMeans(Predictor):
    """
    K-Means clustering algorithm.

    This class implements the K-Means clustering algorithm, which partitions data into k clusters
    based on similarity.

    Parameters:
    n_clusters : int, default=8
        The number of clusters to form as well as the number of centroids to generate.
    max_iter : int, default=300
        The maximum number of iterations.
    tol : float, default=1e-4
        The relative tolerance with regards to inertia to declare convergence.
    random_state : int, RandomState instance or None, default=0
        Determines random number generation for centroid initialization.
        Pass an int for reproducible results across multiple function calls.

    Attributes:
    cluster_centers_ : array-like, shape (n_clusters, n_features)
        Coordinates of cluster centers.
    labels_ : array-like, shape (n_samples,)
        Labels of each point.
    inertia_ : float
        Sum of squared distances of samples to their closest cluster center.
    n_iter_ : int
        Number of iterations run.

    Methods:
    fit(X): Compute k-means clustering.
    predict(X): Predict the closest cluster each sample in X belongs to.
    """

    def __init__(self, n_clusters=8, max_iter=300, tol=1e-4, random_state=0):
        # Initialize parameters
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state

    def _labels_inertia(self, X, centers):
        """
        Assign labels and compute inertia.

        Parameters:
        X : array-like, shape (n_samples, n_features)
            Training instances to cluster.
        centers : array-like, shape (n_clusters, n_features)
            Cluster centers.

        Returns:
        labels : array-like, shape (n_samples,)
            Index of the cluster each sample belongs to.
        inertia : float
            Sum of squared distances of samples to their closest cluster center.
        """
        # Initialize labels and inertia
        labels = np.zeros(X.shape[0])
        inertia = 0
        # Loop through each sample
        for sample_idx in range(X.shape[0]):
            min_dis = np.inf
            # Loop through each cluster center
            for center_idx in range(self.n_clusters):
                # Calculate squared Euclidean distance
                d = np.sum(np.square(X[sample_idx] - centers[center_idx]))
                # Update label if closer
                if d < min_dis:
                    min_dis = d
                    labels[sample_idx] = center_idx
            # Accumulate inertia
            inertia += min_dis
        return labels, inertia

    def fit(self, X):
        """
        Compute k-means clustering.

        Parameters:
        X : array-like, shape (n_samples, n_features)
            Training instances to cluster.

        Returns:
        self : object
            Returns the instance itself.
        """
        # Initialize random number generator
        rng = np.random.RandomState(self.random_state)
        # Calculate tolerance
        tol = np.mean(np.var(X, axis=0)) * self.tol
        # Initialize cluster centers randomly
        centers = X[rng.permutation(X.shape[0])[:self.n_clusters]]
        # Iterate until convergence or max iterations reached
        for i in range(self.max_iter):
            # Store previous centers for convergence check
            centers_old = centers.copy()
            # Assign labels and compute inertia
            labels, inertia = self._labels_inertia(X, centers)
            # Update cluster centers
            for center_idx in range(self.n_clusters):
                centers[center_idx] = np.mean(X[labels == center_idx], axis=0)
            # Calculate total shift of cluster centers
            center_shift_total = np.sum(np.square(centers_old - centers))
            # Check convergence
            if center_shift_total <= tol:
                break
        # Re-assign labels and inertia if there was any update after the last iteration
        if center_shift_total > 0:
            labels, inertia = self._labels_inertia(X, centers)
        # Save attributes
        self.cluster_centers_ = centers
        self.labels_ = labels
        self.inertia_ = inertia
        self.n_iter_ = i + 1
        return self

    def predict(self, X):
        """
        Predict the closest cluster each sample in X belongs to.

        Parameters:
        X : array-like, shape (n_samples, n_features)
            New data to predict.

        Returns:
        array-like, shape (n_samples,)
            Index of the cluster each sample belongs to.
        """
        return self._labels_inertia(X, self.cluster_centers_)[0]
