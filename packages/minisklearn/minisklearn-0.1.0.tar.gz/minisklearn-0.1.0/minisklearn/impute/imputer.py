from base import Transformer
import numpy as np
from scipy.stats import mode

class MissingIndicator(Transformer):
    """
    Create a binary indicator for missing values in the input data.

    """

    def fit(self, data):
        """
        Fit the missing indicator to the data.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - self: Fitted MissingIndicator instance.
        """
        # Create a mask for missing values and count the number of missing values per feature
        missing_mask = np.isnan(data)
        n_missing_per_feature = np.sum(missing_mask, axis=0)

        # Identify features with missing values and store their indices
        self.features_with_missing_ = np.flatnonzero(n_missing_per_feature)
        return self

    def transform(self, data):
        """
        Transform the input data by creating a binary indicator for missing values.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - array: Binary indicator for missing values.
        """
        # Create a binary indicator for missing values in the identified features
        return np.isnan(data[:, self.features_with_missing_])


class SimpleImputer:
    """
    Impute missing values in the input data using different strategies.

    Parameters:
    - strategy (str, optional): Imputation strategy ('mean', 'median', 'most_frequent', or 'constant').
    - fill_value (scalar, optional): Value to use for imputation when strategy is 'constant'.
    """

    def __init__(self, strategy='mean', fill_value=None):
        """
        Initialize the SimpleImputer instance.

        Parameters:
        - strategy (str, optional): Imputation strategy ('mean', 'median', 'most_frequent', or 'constant').
        - fill_value (scalar, optional): Value to use for imputation when strategy is 'constant'.
        """
        self.strategy = strategy
        self.fill_value = fill_value  # Only used when strategy == 'constant'

    def fit(self, data):
        """
        Fit the imputer to the data.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - self: Fitted SimpleImputer instance.
        """
        # Create a mask for missing values
        missing_mask = np.isnan(data)

        # Mask the data array using the missing values mask
        masked_data = np.ma.masked_array(data, mask=missing_mask)

        # Compute the statistics based on the imputation strategy
        if self.strategy == "mean":
            self.statistics_ = np.array(np.ma.mean(masked_data, axis=0))
        elif self.strategy == "median":
            self.statistics_ = np.array(np.ma.median(masked_data, axis=0))
        elif self.strategy == "most_frequent":
            self.statistics_ = np.array(mode(masked_data, axis=0)[0])
        elif self.strategy == "constant":
            self.statistics_ = np.full(data.shape[1], self.fill_value)

        return self

    def transform(self, data):
        """
        Transform the input data by imputing missing values.

        Parameters:
        - data (array-like): Input data.

        Returns:
        - array: Data with missing values imputed.
        """
        # Create a mask for missing values in the input data
        missing_mask = np.isnan(data)

        # Compute the number of missing values per feature
        n_missing_per_feature = np.sum(missing_mask, axis=0)

        # Repeat the imputed statistics for each missing value
        imputed_values = np.repeat(self.statistics_, n_missing_per_feature)

        # Determine the coordinates of missing values in the transposed masked array
        coordinates = np.where(missing_mask.T)[::-1]

        # Create a copy of the input data and replace missing values with imputed values
        imputed_data = data.copy()
        imputed_data[coordinates] = imputed_values

        return imputed_data
