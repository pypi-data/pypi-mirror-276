import numpy as np
from scipy.optimize import minimize
from base import Predictor

class LinearSVC(Predictor):
    """
    A simplified implementation of a Linear Support Vector Classification.
    """
    def __init__(self, penalty_factor=1.0):
        """
        Initializes the SimplifiedLinearSVC with a penalty factor.
        
        Parameters:
        penalty_factor (float): The regularization strength inversely proportional to C.
        """
        self.penalty_factor = penalty_factor

    def _compute_cost_and_gradient(self, weights, X, targets, penalty_factor):
        """
        Computes the cost and gradient for optimization.

        Parameters:
        weights (array-like): Current weights of the SVM.
        X (array-like): Feature dataset.
        targets (array-like): Binary encoded target values.
        penalty_factor (float): The regularization strength.

        Returns:
        tuple: (cost, gradient)
        """
        extended_X = np.hstack([X, np.ones((X.shape[0], 1))])
        predictions = np.dot(extended_X, weights)
        margins = targets * predictions
        violations = margins <= 1
        cost = penalty_factor * np.sum(np.square(1 - margins[violations])) + 0.5 * np.dot(weights, weights)
        gradient = weights + 2 * penalty_factor * np.dot(extended_X[violations].T, predictions[violations] - targets[violations])
        return cost, gradient

    def fit(self, X, y):
        """
        Fits the model using the given dataset.

        Parameters:
        X (array-like): Feature dataset.
        y (array-like): Target values.

        Returns:
        SimplifiedLinearSVC: The instance itself.
        """
        classes = np.unique(y)
        encoded_targets = np.full((y.shape[0], len(classes)), -1)
        for i, cls in enumerate(classes):
            encoded_targets[y == cls, i] = 1
        if len(classes) == 2:
            encoded_targets = encoded_targets[:, 1].reshape(-1, 1)
        self.classes_ = classes
        encoded_y = encoded_targets

        num_features = X.shape[1]
        weights = np.zeros((encoded_y.shape[1], num_features + 1))
        for i in range(encoded_y.shape[1]):
            initial_weights = np.zeros(num_features + 1)
            res = minimize(fun=self._compute_cost_and_gradient, jac=True, x0=initial_weights,
                           args=(X, encoded_y[:, i], self.penalty_factor), method='L-BFGS-B')
            weights[i] = res.x

        self.coef_ = weights[:, :-1]
        self.intercept_ = weights[:, -1]
    
        return self

    def decision_function(self, X):
        """
        Computes the decision function for the samples in X.

        Parameters:
        X (array-like): Feature dataset.

        Returns:
        array: Scores of the samples.
        """
        scores = np.dot(X, self.coef_.T) + self.intercept_
        return scores.ravel() if scores.shape[1] == 1 else scores

    def predict(self, X):
        """
        Predict class labels for samples in X.

        Parameters:
        X (array-like): Feature dataset.

        Returns:
        array: Predicted class labels.
        """
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            return self.classes_[(scores > 0).astype(int)]
        return self.classes_[np.argmax(scores, axis=1)]
