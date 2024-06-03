from sklearn.base import clone
from sklearn.model_selection import KFold, StratifiedKFold
from itertools import product
import numpy as np
from base import Estimator, Predictor

class ModelSelector(Estimator, Predictor):
    def __init__(self, models, scoring_function):
        super().__init__()
        self.models = models
        self.scoring_function = scoring_function
        self.best_score_ = None
        self.best_params_ = None
        self.best_estimator_ = None

    def fit(self, X, y):
        best_score = -float('inf')
        for model in self.models:
            model.fit(X, y)
            score = self.scoring_function(model, X, y)
            if score > best_score:
                best_score = score
                self.best_score_ = score
                self.best_params_ = model.get_params()
                self.best_estimator_ = model
        return self

    def predict(self, X):
        return self.best_estimator_.predict(X)

class GridSearchCV:
    def __init__(self, estimator, param_grid):
        """
        Initialize the GridSearchCV with the estimator and parameter grid.

        Parameters:
        - estimator: The machine learning algorithm to use.
        - param_grid: Dictionary with parameters names (`str`) as keys and lists of parameter settings to try as values.
        """
        self.estimator = estimator
        self.param_grid = param_grid

    def fit(self, X, y):
        """
        Perform grid search and fit the estimator with the best found parameters.

        Parameters:
        - X: Training data.
        - y: Target values.

        Returns:
        - self: The fitted GridSearchCV object.
        """
        # Choose cross-validation method based on the type of estimator
        if self.estimator._estimator_type == "regressor":
            cv = KFold()
        else:  # Assuming it's a classifier if not a regressor
            cv = StratifiedKFold()

        train_scores, test_scores, param_combinations = [], [], []

        items = sorted(self.param_grid.items())
        keys, values = zip(*items)
        param_combinations = [dict(zip(keys, combination)) for combination in product(*values)]

        # Iterate over all parameter combinations
        for params in param_combinations:
            cur_train_scores, cur_test_scores = [], []

            # Perform cross-validation
            for train_index, test_index in cv.split(X, y):
                est_clone = clone(self.estimator)
                est_clone.set_params(**params)
                est_clone.fit(X[train_index], y[train_index])

                cur_train_scores.append(est_clone.score(X[train_index], y[train_index]))
                cur_test_scores.append(est_clone.score(X[test_index], y[test_index]))

            param_combinations.append(params)
            train_scores.append(cur_train_scores)
            test_scores.append(cur_test_scores)

        # Convert scores to numpy arrays for easier manipulation
        train_scores = np.array(train_scores)
        test_scores = np.array(test_scores)

        # Collect results into a dictionary
        self.cv_results_ = {}
        for split_idx in range(cv.get_n_splits()):
            self.cv_results_[f"split{split_idx}_train_score"] = train_scores[:, split_idx]
            self.cv_results_[f"split{split_idx}_test_score"] = test_scores[:, split_idx]

        self.cv_results_["mean_train_score"] = np.mean(train_scores, axis=1)
        self.cv_results_["std_train_score"] = np.std(train_scores, axis=1)
        self.cv_results_["mean_test_score"] = np.mean(test_scores, axis=1)
        self.cv_results_["std_test_score"] = np.std(test_scores, axis=1)
        self.cv_results_['params'] = param_combinations

        # Determine the best parameters and refit the best estimator
        best_idx = np.argmax(self.cv_results_['mean_test_score'])
        self.best_params_ = self.cv_results_['params'][best_idx]
        self.best_estimator_ = clone(self.estimator).set_params(**self.best_params_)
        self.best_estimator_.fit(X, y)

        return self

    def decision_function(self, X):
        """
        Compute the decision function of the best estimator.

        Parameters:
        - X: Input data.

        Returns:
        - Decision function scores.
        """
        return self.best_estimator_.decision_function(X)

    def predict(self, X):
        """
        Predict using the best estimator.

        Parameters:
        - X: Input data.

        Returns:
        - Predicted values.
        """
        return self.best_estimator_.predict(X)


class KFold:
    def __init__(self, n_splits=5, shuffle=False, random_state=0):
        """
        Initialize the KFold cross-validator.

        Parameters:
        - n_splits: Number of folds. Must be at least 2.
        - shuffle: Whether to shuffle the data before splitting into batches.
        - random_state: When shuffle is True, this ensures reproducibility.
        """
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

    def _iter_test_indices(self, X, y):
        """
        Generate test set indices for each fold.

        Parameters:
        - X: Training data.
        - y: Target values (not used but kept for compatibility).

        Yields:
        - Indices for the test set for each fold.
        """
        indices = np.arange(X.shape[0])
        if self.shuffle:
            rng = np.random.RandomState(self.random_state)
            rng.shuffle(indices)

        # Calculate the sizes of each fold
        fold_sizes = np.full(self.n_splits, X.shape[0] // self.n_splits)
        fold_sizes[:X.shape[0] % self.n_splits] += 1

        current = 0
        for fold_size in fold_sizes:
            yield indices[current:current + fold_size]
            current += fold_size

    def _iter_test_masks(self, X, y):
        """
        Generate boolean masks for the test set for each fold.

        Parameters:
        - X: Training data.
        - y: Target values (not used but kept for compatibility).

        Yields:
        - Boolean array where True indicates the test set and False indicates the train set.
        """
        for test_index in self._iter_test_indices(X, y):
            test_mask = np.zeros(X.shape[0], dtype=bool)
            test_mask[test_index] = True
            yield test_mask

    def split(self, X, y):
        """
        Generate indices to split data into training and test set for each fold.

        Parameters:
        - X: Training data.
        - y: Target values.

        Yields:
        - The training and test set indices for each fold.
        """
        indices = np.arange(X.shape[0])
        for test_mask in self._iter_test_masks(X, y):
            yield indices[~test_mask], indices[test_mask]
