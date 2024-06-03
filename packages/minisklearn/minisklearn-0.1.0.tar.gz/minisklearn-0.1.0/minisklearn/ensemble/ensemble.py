import numpy as np
from base import Predictor
# from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score

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
