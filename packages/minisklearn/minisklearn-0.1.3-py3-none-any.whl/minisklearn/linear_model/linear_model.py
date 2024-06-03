import numpy as np
from numpy.linalg import inv

class LinearRegression:
    """
    A simple linear regression model.

    Attributes:
        coef_: array-like, shape (n_features,)
            Coefficients of the linear regression model.
        intercept_: float
            Intercept of the linear regression model.
    """

    def fit(self, X, y):
        """
        Fit the linear regression model to the training data.

        Parameters:
            X : array-like, shape (n_samples, n_features)
                Training data.
            y : array-like, shape (n_samples,)
                Target values.

        Returns:
            self : object
                Returns self.
        """
        # Compute mean of features and target
        X_mean = np.mean(X, axis=0)
        y_mean = np.mean(y)
        
        # Center the data
        X_train = X - X_mean
        y_train = y - y_mean
        
        # Compute dot product of centered features
        A = np.dot(X_train.T, X_train)
        
        # Compute dot product of centered features and target
        Xy = np.dot(X_train.T, y_train)
        
        # Compute coefficients and intercept
        self.coef_ = np.dot(inv(A), Xy).ravel()
        self.intercept_ = y_mean - np.dot(X_mean, self.coef_)
        
        return self

    def predict(self, X):
        """
        Predict target values for the given data.

        Parameters:
            X : array-like, shape (n_samples, n_features)
                Data to predict.

        Returns:
            y_pred : array-like, shape (n_samples,)
                Predicted target values.
        """
        y_pred = np.dot(X, self.coef_) + self.intercept_
        return y_pred
