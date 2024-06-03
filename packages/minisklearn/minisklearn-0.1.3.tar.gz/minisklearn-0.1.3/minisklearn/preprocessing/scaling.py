import numpy as np
from base import Transformer

class MaxAbsScaler(Transformer):
    """
    Scale features by their maximum absolute value.

    Usage:
    scaler = MaxAbsScaler()
    scaler.fit(data)  # Fit the scaler to the data
    scaled_data = scaler.transform(data)  # Scale the data by maximum absolute value
    """
    def fit(self, data):
        """
        Fit the scaler to the data by computing the maximum absolute value of each feature.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - self: Fitted MaxAbsScaler instance.
        """
        # Compute the maximum absolute value of each feature and store it in 'scale_'
        self.scale_ = np.max(np.abs(data), axis=0)
        return self

    def transform(self, data):
        """
        Scale the input data by dividing each feature by its maximum absolute value.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - array: Scaled data.
        """
        # Scale the data by dividing each feature by its corresponding maximum absolute value
        return data / self.scale_

class MinMaxScaler(Transformer):
    """
    Scale features to a given range using min-max scaling.

    Usage:
    scaler = MinMaxScaler(feature_range=(min_value, max_value))
    scaler.fit(data)  # Fit the scaler to the data
    scaled_data = scaler.transform(data)  # Scale the data to the specified range
    """
    def __init__(self, feature_range=(0, 1)):
        """
        Initialize the MinMaxScaler instance.

        Parameters:
        - feature_range (tuple, optional): Desired range of transformed data. Default is (0, 1).
        """
        self.feature_range = feature_range

    def fit(self, data):
        """
        Fit the scaler to the data by computing data range and scale.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - self: Fitted MinMaxScaler instance.
        """
        # Compute minimum and maximum values of each feature
        self.data_min_ = data.min(axis=0)
        self.data_max_ = data.max(axis=0)

        # Compute data range and scale for each feature
        self.data_range_ = self.data_max_ - self.data_min_
        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / self.data_range_
        return self

    def transform(self, data):
        """
        Transform the input data by scaling it to the specified range.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - array: Scaled data.
        """
        # Scale the data to the specified range
        return self.feature_range[0] + (data - self.data_min_) * self.scale_

class Normalizer(Transformer):
    """
    Normalize samples along the specified axis using different norms.

    Parameters:
    - norm_type (str, optional): Type of normalization ('l1', 'l2', or 'max'). Default is 'l2'.
    """

    def __init__(self, norm_type='l2'):
        """
        Initialize the Normalizer instance.

        Parameters:
        - norm_type (str, optional): Type of normalization ('l1', 'l2', or 'max'). Default is 'l2'.
        """
        self.norm_type = norm_type

    def fit(self, data):
        """
        Fit the normalizer to the data.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - self: Fitted Normalizer instance.
        """
        # No computations needed for fitting, return self directly
        return self

    def transform(self, data):
        """
        Transform the input data by normalizing it using the specified norm.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - array: Normalized data.
        """
        # Compute norms based on the specified norm type ('l1', 'l2', or 'max')
        if self.norm_type == 'l1':
            norms = np.sum(np.abs(data), axis=1)
        elif self.norm_type == 'l2':
            norms = np.sqrt(np.sum(np.square(data), axis=1))
        elif self.norm_type == 'max':
            norms = np.max(data, axis=1)

        # Normalize the data using the computed norms
        return data / norms[:, np.newaxis]


class RobustScaler(Transformer):
    """
    Scale features using robust scaling based on quantiles.

    Parameters:
    - quant_range (tuple, optional): Custom quantile range for robust scaling. Default is (25, 75).
    """

    def __init__(self, quant_range=(25, 75)):
        """
        Initialize the RobustScaler instance.

        Parameters:
        - quant_range (tuple, optional): Custom quantile range for robust scaling. Default is (25, 75).
        """
        self.quant_range = quant_range

    def fit(self, X):
        """
        Fit the robust scaler to the data.

        Parameters:
        - X (array-like): Input data.

        Returns:
        - self: Fitted RobustScaler instance.
        """
        # Compute the center (median) and scale based on the custom quantile range
        self.center_ = np.median(X, axis=0)
        quantiles = np.percentile(X, self.quant_range, axis=0)
        self.scale_ = quantiles[1] - quantiles[0]
        return self

    def transform(self, X):
        """
        Transform the input data using robust scaling.

        Parameters:
        - X (array-like): Input data.

        Returns:
        - array: Robust-scaled data.
        """
        # Scale the data using robust scaling based on the fitted center and scale
        return (X - self.center_) / self.scale_

class StandardScaler(Transformer):
    """
    Standardize features by removing the mean and scaling to unit variance.

    """

    def fit(self, data):
        """
        Fit the standard scaler to the data.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - self: Fitted StandardScaler instance.
        """
        # Compute the mean and standard deviation for each feature
        self.mean_ = np.mean(data, axis=0)
        self.std_ = np.std(data, axis=0)
        return self

    def transform(self, data):
        """
        Transform the input data using standard scaling.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - array: Standard-scaled data.
        """
        # Scale the data using standard scaling based on the fitted mean and standard deviation
        return (data - self.mean_) / self.std_

