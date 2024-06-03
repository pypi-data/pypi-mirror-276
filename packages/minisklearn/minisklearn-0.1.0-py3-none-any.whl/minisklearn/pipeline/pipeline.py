from meta import MetaEstimator
from base import Predictor

class Pipeline(MetaEstimator, Predictor):
    def __init__(self, steps):
        super().__init__(estimators=steps[:-1])
        self.final_estimator = steps[-1]

    def fit(self, X, y=None):
        for step in self.estimators:
            X = step.fit_transform(X, y)
        self.final_estimator.fit(X, y)
        return self

    def predict(self, X):
        for step in self.estimators:
            X = step.transform(X)
        return self.final_estimator.predict(X)
