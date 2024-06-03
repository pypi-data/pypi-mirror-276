from base.base import TransformerMixin, BaseEstimator
import numpy as np

class Normalizer(TransformerMixin, BaseEstimator):
    """
    Normalize samples individually to unit norm.

    This transformer normalizes each sample to have unit norm.
    The 'norm' parameter specifies the type of normalization to apply:
    - 'l1': L1 normalization (sum of absolute values)
    - 'l2': L2 normalization (Euclidean norm)
    - 'max': Max normalization (maximum absolute value)

    Parameters:
    -----------
    norm : str, default='l2'
        The normalization method to use. Options are 'l1', 'l2', or 'max'.

    Attributes:
    -----------
    norm : str
        The normalization method used.
    """

    def __init__(self, norm='l2'):
        if norm not in ['l1', 'l2', 'max']:
            raise ValueError('Invalid norm: %s' % norm)
        
        self.norm = norm

    def fit(self, X, y=None):
        """
        Fit the Normalizer to the data.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The input data.

        Returns:
        --------
        self : object
            Returns self.
        """
        return self

    def transform(self, X):
        """
        Transform the input data by normalizing each sample.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The input data.

        Returns:
        --------
        X_normalized : array-like of shape (n_samples, n_features)
            The normalized input data.
        """
        if self.norm == 'l1':
            norms = np.sum(np.abs(X), axis=1)
        elif self.norm == 'l2':
            norms = np.sqrt(np.sum(np.square(X), axis=1))
        elif self.norm == 'max':
            norms = np.max(np.abs(X), axis=1)
        return X / norms[:, np.newaxis]
