class Estimator:
    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        pass

    def set_params(self, **params):
        """Set the parameters of this estimator."""
        pass

    def fit(self, X, y=None):
        """Fit the model according to the given training data."""
        pass

class Predictor(Estimator):
    def predict(self, X):
        """Make predictions using the learned model."""
        pass

    def fit(self, X, y):
        """Fit the model according to the given training data."""
        super().fit(X, y)

    def fit_predict(self, X, y):
        """Fit the model and predict on the same dataset."""
        self.fit(X, y)
        return self.predict(X)

    def score(self, X, y):
        """Returns the score of the prediction."""
        pass

class Transformer(Estimator):
    def transform(self, X, y=None):
        """Transform the data based on the learned parameters."""
        pass

    def fit(self, X, y=None):
        """Fit to data, then transform it."""
        super().fit(X, y)

    def fit_transform(self, X, y=None):
        """Fit to data, then transform it."""
        self.fit(X, y)
        return self.transform(X)