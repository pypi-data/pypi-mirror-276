import numpy as np
from scipy.special import logsumexp
from base import Predictor

class GaussianNB(Predictor):
    """
    A simplified implementation of Gaussian Naive Bayes for classification.
    """
    
    def fit(self, X, y):
        """
        Fit the Gaussian Naive Bayes model according to the given training data.

        Parameters:
        X (array-like): Feature dataset with shape (n_samples, n_features).
        y (array-like): Target values with shape (n_samples,).

        Returns:
        SimplifiedGaussianNB: The instance itself.
        """
        self.classes_ = np.unique(y)
        num_features = X.shape[1]
        num_classes = len(self.classes_)
        
        # Initialize parameters
        self.theta_ = np.zeros((num_classes, num_features))
        self.sigma_ = np.zeros((num_classes, num_features))
        self.class_count_ = np.zeros(num_classes)
        
        # Calculate parameters for each class
        for idx, class_val in enumerate(self.classes_):
            X_class = X[y == class_val]
            self.theta_[idx] = np.mean(X_class, axis=0)
            self.sigma_[idx] = np.var(X_class, axis=0)
            self.class_count_[idx] = X_class.shape[0]
        
        self.class_prior_ = self.class_count_ / np.sum(self.class_count_)
        return self

    def predict(self, X):
        """
        Perform classification on an array of test vectors X.

        Parameters:
        X (array-like): Feature dataset to predict.

        Returns:
        array: Predicted class labels for each sample in X.
        """
        joint_log_likelihood = []
        for idx in range(len(self.classes_)):
            prior_log_prob = np.log(self.class_prior_[idx])
            n_ij = -0.5 * np.sum(np.log(2 * np.pi * self.sigma_[idx]))
            n_ij -= 0.5 * np.sum(((X - self.theta_[idx]) ** 2) / self.sigma_[idx], axis=1)
            joint_log_likelihood.append(prior_log_prob + n_ij)
        
        joint_log_likelihood = np.array(joint_log_likelihood).T
        return self.classes_[np.argmax(joint_log_likelihood, axis=1)]

    def predict_proba(self, X):
        """
        Return probability estimates for the test vector X.

        Parameters:
        X (array-like): Feature dataset to predict probabilities for.

        Returns:
        array: Returns the probability of the sample for each class in the model.
        """
        joint_log_likelihood = []
        for idx in range(len(self.classes_)):
            prior_log_prob = np.log(self.class_prior_[idx])
            n_ij = -0.5 * np.sum(np.log(2 * np.pi * self.sigma_[idx]))
            n_ij -= 0.5 * np.sum(((X - self.theta_[idx]) ** 2) / self.sigma_[idx], axis=1)
            joint_log_likelihood.append(prior_log_prob + n_ij)
        
        joint_log_likelihood = np.array(joint_log_likelihood).T
        log_prob = joint_log_likelihood - logsumexp(joint_log_likelihood, axis=1)[:, np.newaxis]
        return np.exp(log_prob)
