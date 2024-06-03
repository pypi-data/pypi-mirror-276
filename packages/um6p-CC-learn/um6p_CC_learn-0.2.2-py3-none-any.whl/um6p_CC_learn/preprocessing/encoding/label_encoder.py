
from utils._encode import _encode, _unique
from utils.__validation import column_or_1d, _num_samples

from base.base import BaseEstimator, TransformerMixin

import numpy as np



class LabelEncoder(TransformerMixin, BaseEstimator):
    """Encode target labels with value between 0 and n_classes-1.

    This transformer should be used to encode target values, *i.e.* `y`, and
    not the input `X`.

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        Holds the label for each class.
    """

    def fit(self, y):
        """Fit label encoder.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : returns an instance of self.
            Fitted label encoder.
        """
        y = column_or_1d(y, warn=True)
        self.classes_ = _unique(y)
        self._is_fitted = True
        return self

    def fit_transform(self, y):
        """Fit label encoder and return encoded labels.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        y : array-like of shape (n_samples,)
            Encoded labels.
        """
        y = column_or_1d(y, warn=True)
        self.classes_, y = _unique(y, return_inverse=True)
        return y

    def transform(self, y):
        """Transform labels to normalized encoding.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        y : array-like of shape (n_samples,)
            Labels as normalized encodings.
        """
        self.check_is_fitted()
        y = column_or_1d(y, dtype=self.classes_.dtype, warn=True)
        # transform of empty array is empty array
        if _num_samples(y) == 0:
            return np.array([])

        return _encode(y, uniques=self.classes_)