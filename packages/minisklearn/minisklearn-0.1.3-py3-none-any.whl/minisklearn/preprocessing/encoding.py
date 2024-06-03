import numpy as np
from base import Transformer

class Binarizer(Transformer):
    """
    Binarize data by setting values greater than 0 to 1 and 0 otherwise.
    """
    def fit(self, X):
        """
        Fit the binarizer to the data (no operation performed).

        Parameters:
        - X (array-like): Input data.

        Returns:
        - self: Instance of the Binarizer class.
        """
        return self

    def transform(self, X):
        """
        Transform input data by binarizing it.

        Parameters:
        - X (array-like): Input data.

        Returns:
        - array: Binarized data.
        """
        Xt = np.zeros_like(X)
        Xt[X > 0] = 1
        return Xt


class KBinsDiscretizer(Transformer):
    """
    Discretize continuous data into bins using different strategies.

    Parameters:
    - num_bins (int, optional): Number of bins to create. Default is 5.
    - method (str, optional): Discretization strategy ("quantile" or "uniform"). Default is "quantile".
    """
    def __init__(self, num_bins=5, method="quantile"):
        """
        Initialize the KBinsDiscretizer instance.

        Parameters:
        - num_bins (int, optional): Number of bins to create. Default is 5.
        - method (str, optional): Discretization strategy ("quantile" or "uniform"). Default is "quantile".
        """
        self.num_bins = num_bins
        self.method = method

    def fit(self, data):
        """
        Fit the discretizer to the data.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - self: Fitted KBinsDiscretizer instance.
        """
        # Initialize attributes for storing bin edges
        self.num_bins_ = np.full(data.shape[1], self.num_bins)
        self.bin_edges_ = np.empty(data.shape[1], dtype=object)

        # Compute bin edges based on the chosen method
        for feature_index in range(data.shape[1]):
            if self.method == "uniform":
                self.bin_edges_[feature_index] = np.linspace(data[:, feature_index].min(),
                                                              data[:, feature_index].max(),
                                                              self.num_bins_[feature_index] + 1)
            elif self.method == "quantile":
                quantiles = np.linspace(0, 100, self.num_bins_[feature_index] + 1)
                self.bin_edges_[feature_index] = np.percentile(data[:, feature_index], quantiles)
        return self

    def transform(self, data):
        """
        Transform the input data by binning.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - array: Binned data.
        """
        # Initialize array for storing transformed data
        transformed_data = np.empty_like(data)

        # Bin data based on the computed bin edges
        for feature_index in range(data.shape[1]):
            # Bin data using digitize function
            transformed_data[:, feature_index] = np.digitize(data[:, feature_index] +
                                                              np.finfo(float).eps,
                                                              self.bin_edges_[feature_index][1:])
        
        # Clip transformed data to ensure it falls within bin boundaries
        transformed_data = np.clip(transformed_data, 0, self.num_bins_ - 1)
        return transformed_data

class LabelBinarizer(Transformer):
    """
    Binarize labels into a one-hot encoded matrix.

    Parameters:
    - positive_label (int or str, optional): Positive label. Default is 1.
    - negative_label (int or str, optional): Negative label. Default is 0.
    """
    def __init__(self, positive_label=1, negative_label=0):
        """
        Initialize the LabelBinarizer instance.

        Parameters:
        - positive_label (int or str, optional): Positive label. Default is 1.
        - negative_label (int or str, optional): Negative label. Default is 0.
        """
        self.positive_label = positive_label
        self.negative_label = negative_label

    def fit(self, labels):
        """
        Fit the binarizer to the labels.

        Parameters:
        - labels (array-like): Input labels.

        Returns:
        - self: Fitted LabelBinarizer instance.
        """
        # Find unique classes in the labels
        self.classes_ = np.unique(labels)
        return self

    def transform(self, labels):
        """
        Transform the input labels into a one-hot encoded matrix.

        Parameters:
        - labels (array-like): Input labels.

        Returns:
        - array: One-hot encoded matrix.
        """
        # Initialize an array for storing the one-hot encoded labels
        encoded_labels = np.full((labels.shape[0], len(self.classes_)), self.negative_label)
        
        # Iterate over each class and set the corresponding column to positive label
        for i, c in enumerate(self.classes_):
            encoded_labels[labels == c, i] = self.positive_label
        
        # If there are only two classes, reshape the output to a column vector
        if len(self.classes_) == 2:
            encoded_labels = encoded_labels[:, 1].reshape(-1, 1)
        
        return encoded_labels


class LabelEncoder(Transformer):
    """
    Encode labels into numerical values using searchsorted.

    Usage:
    encoder = LabelEncoder()
    encoder.fit(labels)  # Fit the encoder to the labels
    encoded_labels = encoder.transform(labels)  # Transform labels into numerical values
    """
    def fit(self, labels):
        """
        Fit the encoder to the labels.

        Parameters:
        - labels (array-like): Input labels.

        Returns:
        - self: Fitted LabelEncoder instance.
        """
        # Find unique classes in the labels and store them in 'classes_'
        self.classes_ = np.unique(labels)
        return self

    def transform(self, labels):
        """
        Transform labels into numerical values.

        Parameters:
        - labels (array-like): Input labels.

        Returns:
        - array: Numerical encoded labels.
        """
        # Use searchsorted to find the indices of labels in 'classes_'
        return np.searchsorted(self.classes_, labels)