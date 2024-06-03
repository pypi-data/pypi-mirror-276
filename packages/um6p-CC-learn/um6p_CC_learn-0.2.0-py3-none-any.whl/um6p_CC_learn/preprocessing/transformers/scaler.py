import numpy as np
from base.base import TransformerMixin, BaseEstimator

class StandardScaler(TransformerMixin, BaseEstimator):
    """Standardize features by removing the mean and scaling to unit variance.

    Standardization of a dataset is a common requirement for many machine learning estimators. 
    StandardScaler implements the Transformer API to compute the mean and standard deviation 
    on a training set so as to be able to later reapply the same transformation on the testing set.

    Parameters:
    None

    Attributes:
    mean_ : array of shape (n_features,)
        The mean value for each feature in the training set.
    scale_ : array of shape (n_features,)
        The standard deviation for each feature in the training set.

    Examples:
    >>> scaler = StandardScaler()
    >>> data = np.array([[0, 0], [0, 0], [1, 1], [1, 1]])
    >>> scaler.fit(data)
    StandardScaler()
    >>> scaler.mean_
    array([0.5, 0.5])
    >>> scaler.scale_
    array([0.5, 0.5])
    >>> scaler.transform(data)
    array([[-1., -1.],
           [-1., -1.],
           [ 1.,  1.],
           [ 1.,  1.]])
    """

    def fit(self, X, y=None):
        """Compute the mean and standard deviation for each feature in X.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Training data.

        Returns:
        self : StandardScaler
            The fitted StandardScaler instance.
        """
        self.mean_ = np.mean(X, axis=0)
        self.scale_ = np.std(X, axis=0)
        return self

    def transform(self, X):
        """Standardize features by removing the mean and scaling to unit variance.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Data to standardize.

        Returns:
        X_scaled : array-like of shape (n_samples, n_features)
            Transformed data.
        """
        return (X - self.mean_) / self.scale_
    


class MinMaxScaler(TransformerMixin, BaseEstimator):
    """Transforms features by scaling each feature to a given range.

    This scaler scales each feature to a given range. This range is determined
    by the `feature_range` parameter, which defaults to (0, 1).

    Parameters:
    feature_range : tuple, default=(0, 1)
        Desired range of transformed data.

    Attributes:
    data_min_ : array of shape (n_features,)
        The minimum value for each feature in the training set.
    data_max_ : array of shape (n_features,)
        The maximum value for each feature in the training set.
    data_range_ : array of shape (n_features,)
        The range of values (max - min) for each feature in the training set.
    scale_ : array of shape (n_features,)
        The scale factor applied to each feature.

    Examples:
    >>> scaler = MinMaxScaler()
    >>> data = np.array([[1, 2], [2, 3], [3, 4]])
    >>> scaler.fit(data)
    MinMaxScaler()
    >>> scaler.data_min_
    array([1, 2])
    >>> scaler.data_max_
    array([3, 4])
    >>> scaler.data_range_
    array([2, 2])
    >>> scaler.scale_
    array([0.5, 0.5])
    >>> scaler.transform(data)
    array([[0. , 0. ],
           [0.5, 0.5],
           [1. , 1. ]])
    """

    def __init__(self, feature_range=(0, 1)):
        self.feature_range = feature_range

    def fit(self, X, y=None):
        """Compute the minimum and maximum values for each feature in X.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Training data.

        Returns:
        self : MinMaxScaler
            The fitted MinMaxScaler instance.
        """
        self.data_min_ = X.min(axis=0)
        self.data_max_ = X.max(axis=0)
        self.data_range_ = self.data_max_ - self.data_min_
        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / self.data_range_
        return self

    def transform(self, X):
        """Transform features by scaling each feature to the given range.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Data to scale.

        Returns:
        X_scaled : array-like of shape (n_samples, n_features)
            Transformed data.
        """
        return self.feature_range[0] + (X - self.data_min_) * self.scale_