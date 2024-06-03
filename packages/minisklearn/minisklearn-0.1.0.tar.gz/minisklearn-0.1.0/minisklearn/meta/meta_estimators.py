from base import Estimator

class MetaEstimator(Estimator):
    def __init__(self, estimators):
        self.estimators = estimators
