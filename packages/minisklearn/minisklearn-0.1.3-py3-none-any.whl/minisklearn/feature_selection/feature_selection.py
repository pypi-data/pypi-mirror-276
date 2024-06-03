from sklearn.base import clone
from base import Transformer
import numpy as np

class FeatureSelector:
    """
    Feature selector that selects features based on importance weights from a fitted model.

    The class uses an estimator from scikit-learn and selects features which are deemed important
    based on a computed threshold.
    """

    def __init__(self, model):
        """
        Initializes the FeatureSelector with a model (estimator).

        Parameters:
        model (estimator): The base estimator from which the feature importances or coefficients
                           will be obtained.
        """
        self.model = model

    def fit(self, X, y):
        """
        Fit the model and determine which features meet the threshold criterion for importance.

        Parameters:
        X (array-like): The training input samples.
        y (array-like): The target values (class labels in classification, real numbers in regression).

        Returns:
        FeatureSelector: The instance itself.
        """
        # Clone the model to ensure that fitting the selector does not change the original model
        self.fitted_model = clone(self.model)
        self.fitted_model.fit(X, y)

        # Determine the feature importances or coefficients depending on the model
        if hasattr(self.fitted_model, "feature_importances_"):
            self.importances_ = self.fitted_model.feature_importances_
        elif hasattr(self.fitted_model, "coef_"):
            # Handle both single and multiple coefficient cases
            if self.fitted_model.coef_.ndim == 1:
                self.importances_ = np.abs(self.fitted_model.coef_)
            else:
                self.importances_ = np.linalg.norm(self.fitted_model.coef_, ord=1, axis=0)
        
        # Set the threshold for feature selection to the mean importance
        self.threshold_ = np.mean(self.importances_)

        return self

    def transform(self, X):
        """
        Reduce X to the selected features.

        Parameters:
        X (array-like): The input samples.

        Returns:
        ndarray: The transformed array with only the selected features.
        """
        # Select features where the importances are above the threshold
        return X[:, self.importances_ >= self.threshold_]
