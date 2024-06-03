import numpy as np
from base import Predictor
from .nodes import ClassifierTreeNode, RegressionTreeNode

class DecisionTreeClassifier(Predictor):
    """
    A simple implementation of a decision tree classifier with entropy-based information gain.
    """
    
    def __init__(self, max_depth=2):
        """
        Initialize the decision tree classifier.

        Parameters:
        max_depth (int): The maximum depth of the tree.
        """
        self.max_depth = max_depth

    def _calculate_entropy(self, counts):
        """ Calculate the entropy of a distribution for the given counts. """
        probabilities = counts / np.sum(counts)
        probabilities = probabilities[probabilities > 0]
        return -np.sum(probabilities * np.log2(probabilities))

    def _split(self, features, targets, depth, parent_index, is_left_child):
        """ Recursively split the data to build the tree. """
        if depth == self.max_depth:
            node = ClassifierTreeNode()
            node.sample_count = features.shape[0]
            node.class_counts = np.bincount(targets, minlength=self.num_classes)
            node.impurity = self._calculate_entropy(node.class_counts)
            node_id = len(self.tree_structure)
            self.tree_structure.append(node)
            if parent_index is not None:
                if is_left_child:
                    self.tree_structure[parent_index].left_child = node_id
                else:
                    self.tree_structure[parent_index].right_child = node_id
            return
        
        best_gain = float('-inf')
        best_split = None
        target_counts = np.bincount(targets, minlength=self.num_classes)
        for feature_index in range(0, self.num_classes): 
            sorted_indices = np.argsort(features[:, feature_index])
            left_counts = np.zeros(self.num_classes, dtype=int)
            right_counts = target_counts.copy()
            left_size = 0
            right_size = features.shape[0]

            for idx in range(len(sorted_indices) - 1):
                target = targets[sorted_indices[idx]]
                left_counts[target] += 1
                right_counts[target] -= 1
                left_size += 1
                right_size -= 1
                if idx + 1 < len(sorted_indices) - 1 and np.isclose(features[sorted_indices[idx], feature_index], features[sorted_indices[idx + 1], feature_index]):
                    continue
                gain = -left_size * self._calculate_entropy(left_counts) - right_size * self._calculate_entropy(right_counts)
                if gain > best_gain:
                    best_gain = gain
                    best_split = (feature_index, features[sorted_indices[idx], feature_index], sorted_indices[:idx + 1], sorted_indices[idx + 1:])
        
        if best_split:
            feature_index, threshold, left_indices, right_indices = best_split
            node = ClassifierTreeNode()
            node.feature = feature_index
            node.threshold = threshold
            node.sample_count = features.shape[0]
            node.class_counts = target_counts
            node.impurity = self._calculate_entropy(target_counts)
            node_id = len(self.tree_structure)
            self.tree_structure.append(node)
            if parent_index is not None:
                if is_left_child:
                    self.tree_structure[parent_index].left_child = node_id
                else:
                    self.tree_structure[parent_index].right_child = node_id
            self._split(features[left_indices], targets[left_indices], depth + 1, node_id, True)
            self._split(features[right_indices], targets[right_indices], depth + 1, node_id, False)

    def fit(self, features, targets):
        """ Fit the decision tree model. """
        self.num_features = features.shape[1]
        self.classes_, targets_encoded = np.unique(targets, return_inverse=True)
        self.num_classes = len(self.classes_)
        self.tree_structure = []
        self._split(features, targets_encoded, 0, None, None)
        return self

    def apply(self, features):
        """ Apply the model to the given features. """
        predictions = np.zeros(features.shape[0], dtype=int)
        for i in range(features.shape[0]):
            node_id = 0
            while self.tree_structure[node_id].left_child != -1:
                if features[i][self.tree_structure[node_id].feature] <= self.tree_structure[node_id].threshold:
                    node_id = self.tree_structure[node_id].left_child
                else:
                    node_id = self.tree_structure[node_id].right_child
            predictions[i] = node_id
        return predictions

    def predict_proba(self, features):
        """ Predict class probabilities for the given features. """
        node_indices = self.apply(features)
        probabilities = np.array([self.tree_structure[node].class_counts for node in node_indices])
        return probabilities / np.sum(probabilities, axis=1, keepdims=True)

    def predict(self, features):
        """ Predict class labels for the given features. """
        node_indices = self.apply(features)
        return np.array([self.classes_[np.argmax(self.tree_structure[node].class_counts)] for node in node_indices])

    @property
    def feature_importances(self):
        """ Calculate feature importances based on impurity reduction. """
        importances = np.zeros(self.num_features)
        for node in self.tree_structure:
            if node.left_child != -1:
                left_node = self.tree_structure[node.left_child]
                right_node = self.tree_structure[node.right]
                importances[node.feature] += (node.sample_count * node.impurity -
                                              left_node.sample_count * left_node.impurity -
                                              right_node.sample_count * right_node.impurity)
        return importances / np.sum(importances)




class DecisionTreeRegressor(Predictor):
    """
    A simple decision tree regressor that uses mean squared error reduction for building the tree.
    """
    def __init__(self, max_depth=2):
        """
        Initialize the decision tree regressor with a specified maximum depth.

        Parameters:
        max_depth (int): The maximum depth of the tree.
        """
        self.max_depth = max_depth

    def _build_tree(self, X, y, depth, parent_index, is_left_child):
        """
        Recursive function to build the tree based on reducing the mean squared error (MSE).
        """
        if depth == self.max_depth:
            node = RegressionTreeNode()
            node.impurity = np.var(y) * len(y)  # MSE calculation as total variance
            node.sample_count = X.shape[0]
            node.value = np.mean(y)
            node_index = len(self.tree)
            self.tree.append(node)
            if parent_index is not None:
                if is_left_child:
                    self.tree[parent_index].left_child = node_index
                else:
                    self.tree[parent_index].right_child = node_index
            return
        
        best_improvement = float('-inf')
        best_feature, best_threshold, best_left_indices, best_right_indices = None, None, None, None
        total_sum = np.sum(y)
        total_sum_squared = total_sum * total_sum / len(y)
        
        for feature_index in range(X.shape[1]):
            sorted_indices = np.argsort(X[:, feature_index])
            left_sum, right_sum = 0, total_sum
            left_count, right_count = 0, len(y)
            
            for idx in range(len(sorted_indices) - 1):
                left_sum += y[sorted_indices[idx]]
                right_sum -= y[sorted_indices[idx]]
                left_count += 1
                right_count -= 1
                
                if idx + 1 < len(sorted_indices) - 1 and np.isclose(X[sorted_indices[idx], feature_index], X[sorted_indices[idx + 1], feature_index]):
                    continue
                
                left_mse = left_sum * left_sum / left_count
                right_mse = right_sum * right_sum / right_count
                improvement = left_mse + right_mse - total_sum_squared
                
                if improvement > best_improvement:
                    best_improvement = improvement
                    best_feature = feature_index
                    best_threshold = X[sorted_indices[idx], feature_index]
                    best_left_indices = sorted_indices[:idx + 1]
                    best_right_indices = sorted_indices[idx + 1:]
        
        if best_feature is not None:
            node = RegressionTreeNode()
            node.feature = best_feature
            node.threshold = best_threshold
            node.impurity = np.var(y) * len(y)  # Recalculate impurity for the current node
            node.sample_count = X.shape[0]
            node.value = np.mean(y)
            node_index = len(self.tree)
            self.tree.append(node)
            if parent_index is not None:
                if is_left_child:
                    self.tree[parent_index].left_child = node_index
                else:
                    self.tree[parent_index].right_child = node_index
            self._build_tree(X[best_left_indices], y[best_left_indices], depth + 1, node_index, True)
            self._build_tree(X[best_right_indices], y[best_right_indices], depth + 1, node_index, False)

    def fit(self, X, y):
        """
        Fit the decision tree model on the provided feature matrix X and target vector y.
        """
        self.n_features = X.shape[1]
        self.tree = []
        self._build_tree(X, y, 0, None, None)
        return self

    def apply(self, X):
        """
        Traverse the tree for each instance in X to find the corresponding leaf node.
        """
        predictions = np.zeros(X.shape[0], dtype=int)
        for i in range(X.shape[0]):
            node_index = 0
            while self.tree[node_index].left_child != -1:
                if X[i][self.tree[node_index].feature] <= self.tree[node_index].threshold:
                    node_index = self.tree[node_index].left_child
                else:
                    node_index = self.tree[node_index].right_child
            predictions[i] = node_index
        return predictions

    def predict(self, X):
        """
        Predict the target values for X using the mean values stored at the leaf nodes.
        """
        leaf_indices = self.apply(X)
        return np.array([self.tree[node].value for node in leaf_indices])

    @property
    def feature_importances_(self):
        """
        Calculate the feature importances based on the impurity reduction each feature provides when used in splits.
        """
        importances = np.zeros(self.n_features)
        for node in self.tree:
            if node.left_child != -1:
                left_node = self.tree[node.left_child]
                right_node = self.tree[node.right_child]
                importances[node.feature] += (node.sample_count * node.impurity
                                              - left_node.sample_count * left_node.impurity
                                              - right_node.sample_count * right_node.impurity)
        return importances / np.sum(importances)
