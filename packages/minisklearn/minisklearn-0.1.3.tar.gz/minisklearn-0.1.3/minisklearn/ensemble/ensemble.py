import numpy as np
from base import Predictor
# from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from copy import deepcopy

def clone(estimator):
    """
    Create a deep copy of the estimator.
    
    Parameters:
    - estimator: The estimator to be cloned.
    
    Returns:
    - A deep copy of the estimator.
    """
    return deepcopy(estimator)

def resample(X, y, random_state=None):
    """
    Resample the dataset with replacement.

    Parameters:
    - X (array-like): Feature dataset.
    - y (array-like): Target values.
    - random_state (int, optional): Random seed for reproducibility.

    Returns:
    - X_resampled (array-like): Resampled feature dataset.
    - y_resampled (array-like): Resampled target values.
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    indices = np.random.randint(0, len(X), len(X))
    X_resampled = X[indices]
    y_resampled = y[indices]
    
    return X_resampled, y_resampled



class RandomForestClassifier(Predictor):
    """ Implementation of a Random Forest classifier. """

    def __init__(self, n_trees=100, depth=None, feature_subset="log2", use_oob=False, seed=0):
        """
        Initialize the Random Forest classifier.

        Parameters:
        n_trees (int): Number of trees in the forest.
        depth (int): The maximum depth of the tree.
        feature_subset (str): The number of features to consider when looking for the best split.
        use_oob (bool): Whether to use out-of-bag samples to estimate the generalization accuracy.
        seed (int): Random seed for reproducibility.
        """
        self.n_trees = n_trees
        self.depth = depth
        self.feature_subset = feature_subset
        self.use_oob = use_oob
        self.seed = seed

    def fit(self, X, y):
        """ Fit the Random Forest model. """
        self.num_features_ = X.shape[1]
        self.classes_, y_encoded = np.unique(y, return_inverse=True)
        self.num_classes_ = len(self.classes_)
        max_int = np.iinfo(np.int32).max
        random_generator = np.random.RandomState(self.seed)
        self.trees_ = []

        for _ in range(self.n_trees):
            tree = DecisionTreeClassifier(max_depth=self.depth)#, max_features=self.feature_subset,
                                          #random_state=random_generator.randint(max_int))
            bootstrap_rng = np.random.RandomState(self.seed)
            bootstrap_indices = bootstrap_rng.randint(0, X.shape[0], X.shape[0])
            sample_weights = np.bincount(bootstrap_indices, minlength=X.shape[0])
            tree.fit(X, y_encoded)
            self.trees_.append(tree)
        
        if self.use_oob:
            oob_predictions = np.zeros((X.shape[0], self.num_classes_))
            for tree in self.trees_:
                bootstrap_rng = np.random.RandomState(self.seed)
                bootstrap_indices = bootstrap_rng.randint(0, X.shape[0], X.shape[0])
                oob_mask = np.ones(X.shape[0], dtype=bool)
                oob_mask[bootstrap_indices] = False
                oob_predictions[oob_mask] += tree.predict_proba(X[oob_mask])
            self.oob_decision_function_ = oob_predictions / np.sum(oob_predictions, axis=1, keepdims=True)
            self.oob_score_ = accuracy_score(y_encoded, np.argmax(oob_predictions, axis=1))

        return self

    def predict_proba(self, X):
        """ Predict class probabilities for X. """
        aggregate_proba = np.zeros((X.shape[0], self.num_classes_))
        for tree in self.trees_:
            aggregate_proba += tree.predict_proba(X)
        return aggregate_proba / self.n_trees

    def predict(self, X):
        """ Perform classification on samples in X. """
        probabilities = self.predict_proba(X)
        return self.classes_[np.argmax(probabilities, axis=1)]

    @property
    def feature_importances_(self):
        """ Compute the feature importances. """
        total_importances = np.zeros(self.num_features_)
        for tree in self.trees_:
            total_importances += tree.feature_importances_
        return total_importances / total_importances.sum()


class RandomForestRegressor(Predictor):
    """
    A simple implementation of a random forest regressor.
    """
    def __init__(self, num_trees=100, depth=None, features="log2", use_oob=False, seed=0):
        """
        Initialize the random forest regressor.

        Parameters:
        num_trees (int): Number of trees in the forest.
        depth (int or None): The maximum depth of the trees.
        features (str or int): The number of features to consider when looking for the best split; "log2" for all.
        use_oob (bool): Whether to use out-of-bag samples to estimate the R^2 score.
        seed (int): Random seed for reproducibility.
        """
        self.num_trees = num_trees
        self.depth = depth
        self.features = features
        self.use_oob = use_oob
        self.seed = seed

    def fit(self, X, y):
        """
        Build a random forest of decision trees from the training set (X, y).
        """
        self.feature_count = X.shape[1]
        max_int = np.iinfo(np.int32).max
        random_gen = np.random.RandomState(self.seed)
        self.trees = []

        for _ in range(self.num_trees):
            tree = DecisionTreeRegressor(max_depth=self.depth)#,
            #                              max_features=self.features,
            #                              random_state=random_gen.randint(max_int))
            bootstrap_rng = np.random.RandomState(self.seed)
            bootstrap_indices = bootstrap_rng.randint(0, X.shape[0], X.shape[0])
            tree.fit(X, y)
            self.trees.append(tree)

        if self.use_oob:
            predictions = np.zeros(X.shape[0])
            predictions_count = np.zeros(X.shape[0])

            for tree in self.trees:
                bootstrap_rng = np.random.RandomState(self.seed)
                bootstrap_indices = bootstrap_rng.randint(0, X.shape[0], X.shape[0])
                mask = np.ones(X.shape[0], dtype=bool)
                mask[bootstrap_indices] = False
                predictions[mask] += tree.predict(X[mask])
                predictions_count[mask] += 1

            valid_predictions = predictions_count != 0
            predictions[valid_predictions] /= predictions_count[valid_predictions]
            self.oob_prediction_ = predictions
            self.oob_score_ = r2_score(y[valid_predictions], predictions[valid_predictions])

        return self

    def predict(self, X):
        """
        Predict regression target for X.
        """
        predictions = np.zeros(X.shape[0])
        for tree in self.trees:
            predictions += tree.predict(X)
        return predictions / self.num_trees

    @property
    def feature_importances_(self):
        """
        Compute the importance of each feature.
        """
        importances = np.zeros(self.feature_count)
        for tree in self.trees:
            importances += tree.feature_importances_
        return importances / importances.sum()


import numpy as np
from base import Predictor
from copy import deepcopy

class AdaBoostClassifier(Predictor):
    def __init__(self, base_estimator, n_estimators=50, random_state=0):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.random_state = random_state

    def fit(self, X, y):
        self.classes_, y_train = np.unique(y, return_inverse=True)
        self.n_classes_ = len(self.classes_)
        sample_weight = np.full(X.shape[0], 1 / X.shape[0])
        self.estimators_ = []
        self.estimator_weights_ = np.zeros(self.n_estimators)
        self.estimator_errors_ = np.ones(self.n_estimators)
        MAX_INT = np.iinfo(np.int32).max
        rng = np.random.RandomState(self.random_state)
        for i in range(self.n_estimators):
            est = deepcopy(self.base_estimator)
            est.fit(X, y_train, sample_weight=sample_weight)
            y_predict = est.predict(X)
            incorrect = y_predict != y_train
            estimator_error = np.average(incorrect, weights=sample_weight)

            # To avoid division by zero, ensure estimator_error is not zero
            if estimator_error == 0:
                estimator_error = 1e-10

            estimator_weight = (np.log((1 - estimator_error) / estimator_error) +
                                np.log(self.n_classes_ - 1))
            sample_weight *= np.exp(estimator_weight * incorrect)
            sample_weight_sum = np.sum(sample_weight)

            # Normalize to avoid NaNs
            if sample_weight_sum == 0:
                sample_weight_sum = 1e-10

            sample_weight /= sample_weight_sum
            self.estimators_.append(est)
            self.estimator_errors_[i] = estimator_error
            self.estimator_weights_[i] = estimator_weight
        return self

    def decision_function(self, X):
        pred = np.zeros((X.shape[0], self.n_classes_))
        for i in range(self.n_estimators):
            pred[np.arange(X.shape[0]), self.estimators_[i].predict(X)] += self.estimator_weights_[i]
        pred /= np.sum(self.estimator_weights_)
        if self.n_classes_ == 2:
            return pred[:, 1] - pred[:, 0]
        return pred

    def predict(self, X):
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = np.argmax(scores, axis=1)
        return self.classes_[indices]

import numpy as np
from base import Predictor
from copy import deepcopy

def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)

def resample(X, y, random_state=None):
    if random_state is not None:
        np.random.seed(random_state)
    indices = np.random.randint(0, len(X), len(X))
    X_resampled = X[indices]
    y_resampled = y[indices]
    return X_resampled, y_resampled

class BaggingClassifier(Predictor):
    def __init__(self, base_estimator, n_estimators=10, oob_score=False, random_state=0):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.oob_score = oob_score
        self.random_state = random_state

    def fit(self, X, y):
        self.classes_, y_train = np.unique(y, return_inverse=True)
        self.n_classes_ = len(self.classes_)
        MAX_INT = np.iinfo(np.int32).max
        rng = np.random.RandomState(self.random_state)
        self._seeds = rng.randint(MAX_INT, size=self.n_estimators)
        self.estimators_ = []
        self.estimators_samples_ = []
        for i in range(self.n_estimators):
            est = deepcopy(self.base_estimator)
            rng = np.random.RandomState(self._seeds[i])
            sample_indices = rng.randint(0, X.shape[0], X.shape[0])
            self.estimators_samples_.append(sample_indices)
            est.fit(X[sample_indices], y_train[sample_indices])
            self.estimators_.append(est)
        if self.oob_score:
            self._set_oob_score(X, y_train)
        return self

    def _set_oob_score(self, X, y):
        predictions = np.zeros((X.shape[0], self.n_classes_))
        for i in range(self.n_estimators):
            mask = np.ones(X.shape[0], dtype=bool)
            mask[self.estimators_samples_[i]] = False
            predictions[mask] += self.estimators_[i].predict_proba(X[mask])
        self.oob_decision_function_ = predictions / np.sum(predictions, axis=1)[:, np.newaxis]
        self.oob_score_ = accuracy_score(y, np.argmax(predictions, axis=1))

    def predict_proba(self, X):
        proba = np.zeros((X.shape[0], self.n_classes_))
        for i in range(self.n_estimators):
            proba += self.estimators_[i].predict_proba(X)
        proba /= self.n_estimators
        return proba

    def predict(self, X):
        proba = self.predict_proba(X)
        return self.classes_[np.argmax(proba, axis=1)]

import numpy as np
from copy import deepcopy
from sklearn.model_selection import cross_val_predict

class StackingClassifier():
    def __init__(self, estimators, final_estimator):
        self.estimators = estimators
        self.final_estimator = final_estimator

    def fit(self, X, y):
        self.estimators_ = []
        for est in self.estimators:
            self.estimators_.append(deepcopy(est).fit(X, y))
        predictions = []
        for est in self.estimators:
            cur_prediction = cross_val_predict(est, X, y, method="predict_proba")
            if cur_prediction.shape[1] == 2:
                predictions.append(cur_prediction[:, [1]])
            else:
                predictions.append(cur_prediction)
        X_meta = np.hstack(predictions)
        self.final_estimator_ = deepcopy(self.final_estimator)
        self.final_estimator_.fit(X_meta, y)
        return self

    def transform(self, X):
        predictions = []
        for est in self.estimators_:
            cur_prediction = est.predict_proba(X)
            if cur_prediction.shape[1] == 2:
                predictions.append(cur_prediction[:, [1]])
            else:
                predictions.append(cur_prediction)
        return np.hstack(predictions)

    def predict(self, X):
        return self.final_estimator_.predict(self.transform(X))

    def predict_proba(self, X):
        return self.final_estimator_.predict_proba(self.transform(X))


