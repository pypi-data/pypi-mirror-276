import numpy as np
from base import Predictor

class KNeighborsClassifier(Predictor):
    """
    K-Nearest Neighbors classifier.
    """

    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors

    def fit(self, X, y):
        self._fit_X = X
        self.classes_, self._y = np.unique(y, return_inverse=True)
        return self

    def predict(self, X):
        dist_mat = np.linalg.norm(X[:, np.newaxis] - self._fit_X, axis=2)
        neigh_ind = np.argsort(dist_mat, axis=1)[:, :self.n_neighbors]
        mode = lambda x: np.argmax(np.bincount(x))
        return self.classes_[np.apply_along_axis(mode, axis=1, arr=self._y[neigh_ind])]

    def predict_proba(self, X):
        dist_mat = np.linalg.norm(X[:, np.newaxis] - self._fit_X, axis=2)
        neigh_ind = np.argsort(dist_mat, axis=1)[:, :self.n_neighbors]
        proba = np.zeros((X.shape[0], len(self.classes_)))
        pred_labels = self._y[neigh_ind]
        for idx in range(pred_labels.shape[1]):
            proba[np.arange(X.shape[0]), pred_labels[:, idx]] += 1
        proba /= np.sum(proba, axis=1)[:, np.newaxis]
        return proba

class KNeighborsRegressor(Predictor):
    """
    K-Nearest Neighbors regressor.
    """

    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors

    def fit(self, X, y):
        self._fit_X = X
        self._y = y
        return self

    def predict(self, X):
        dist_mat = np.linalg.norm(X[:, np.newaxis] - self._fit_X, axis=2)
        neigh_ind = np.argsort(dist_mat, axis=1)[:, :self.n_neighbors]
        return np.mean(self._y[neigh_ind], axis=1)

class NearestCentroid(Predictor):
    """
    Nearest Centroid classifier.
    """

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.centroids_ = np.array([np.mean(X[y == c], axis=0) for c in self.classes_])
        return self

    def predict(self, X):
        return self.classes_[np.argmin(np.linalg.norm(X[:, np.newaxis] - self.centroids_, axis=2), axis=1)]
