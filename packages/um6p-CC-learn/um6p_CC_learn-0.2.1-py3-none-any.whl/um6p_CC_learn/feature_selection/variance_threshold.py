import numpy as np
from base.base import TransformerMixin, BaseEstimator

class VarianceThreshold(TransformerMixin, BaseEstimator):
    """Feature selector that removes low-variance features.

    This transformer removes features whose variance does not meet a certain
    threshold. By default, it removes features with zero variance.

    Parameters:
    threshold : float, default=0
        The variance threshold below which features will be removed.

    Attributes:
    variances_ : array of shape (n_features,)
        The variance of each feature in the training data.
    """

    def __init__(self, threshold=0):
        self.threshold = threshold

    def fit(self, X, y=None):
        """Compute the variance of each feature in X.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,), default=None
            Target values (ignored).

        Returns:
        self : VarianceThreshold
            The fitted VarianceThreshold instance.
        """
        self.variances_ = np.var(X, axis=0)
        return self

    def transform(self, X):
        """Remove features with variance below the threshold.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Data to transform.

        Returns:
        X_transformed : array-like of shape (n_samples, n_features)
            Transformed data with low-variance features removed.
        """
        return X[:, self.variances_ > self.threshold]