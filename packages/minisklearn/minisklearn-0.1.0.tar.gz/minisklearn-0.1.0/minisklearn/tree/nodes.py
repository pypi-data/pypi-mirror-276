class ClassifierTreeNode:
    """
    A node in the decision tree, representing a split point or a leaf.

    Attributes:
    left_child (int): Index of the left child node in the tree structure array. 
                      A value of -1 indicates that this node is a leaf on the left side.
    right_child (int): Index of the right child node in the tree structure array.
                       A value of -1 indicates that this node is a leaf on the right side.
    feature (int or None): The feature index used for the split. None if this node is a leaf.
    threshold (float or None): The threshold value for the split. None if this node is a leaf.
    impurity (float or None): The impurity measure of this node (e.g., Gini, entropy). None if not calculated.
    sample_count (int or None): The number of samples at this node. None if not calculated.
    class_counts (array or None): The count of each class's samples at this node. None for uninitialized nodes.
    """
    def __init__(self):
        """
        Initialize a tree node with default values indicating an uninitialized or leaf node.
        """
        self.left_child = -1  # Initialize as -1, meaning no left child (leaf node)
        self.right_child = -1  # Initialize as -1, meaning no right child (leaf node)
        self.feature = None  # No feature assigned yet
        self.threshold = None  # No threshold assigned yet
        self.impurity = None  # Impurity not calculated yet
        self.sample_count = None  # Number of samples at this node not set
        self.class_counts = None  # Class counts not initialized yet

class RegressionTreeNode:
    """
    Node for the regression decision tree, holding data specific to each split or leaf node.
    """
    def __init__(self):
        self.left_child = -1  # Index of the left child node
        self.right_child = -1  # Index of the right child node
        self.feature = None  # Feature index used for splitting
        self.threshold = None  # Value of the feature used as the threshold for splitting
        self.impurity = None  # Impurity measure at this node
        self.sample_count = None  # Number of samples at this node
        self.value = None  # Predicted output value for this node (used at leaf nodes)