import numpy as np

class EmpiricalCovariance():
    def fit(self, X):
        self.covariance_ = np.cov(X.T, bias=True)
        return self
