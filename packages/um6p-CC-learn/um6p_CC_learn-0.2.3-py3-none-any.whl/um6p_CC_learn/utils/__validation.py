# mini_sklearn/utils/validation.py

import numpy as np
import warnings
import numbers


def _check_sample_weight(sample_weight, X):
    """Validate sample weights.

    Parameters
    ----------
    sample_weight : array-like of shape (n_samples,)
        Sample weights.

    X : array-like of shape (n_samples, n_features)
        Training data.

    Returns
    -------
    sample_weight : ndarray of shape (n_samples,)
        Validated sample weights.
    """
    if sample_weight is None:
        return np.ones(X.shape[0], dtype=np.float64)
    else:
        sample_weight = np.asarray(sample_weight)
        if np.any(sample_weight < 0):
            raise ValueError("Sample weights must be non-negative.")
        if len(sample_weight) != X.shape[0]:
            raise ValueError("Sample weights length must be equal to the number of samples.")
        return sample_weight



def _check_partial_fit_first_call(estimator, classes):
    """Check if partial_fit is called for the first time.

    Parameters
    ----------
    estimator : object
        Estimator instance.

    classes : array-like of shape (n_classes,)
        Unique class labels.

    Returns
    -------
    bool
        True if partial_fit is called for the first time, False otherwise.
    """
    if getattr(estimator, "classes_", None) is None and classes is None:
        raise ValueError(
            "classes must be passed on the first call to partial_fit."
        )
    return getattr(estimator, "classes_", None) is None


def column_or_1d(y, *, dtype=None, warn=False):
    """Convert input data to a 1d numpy array.

    Parameters
    ----------
    y : array-like
        Input data.

    dtype : data-type, default=None
        Data type for `y`.

    warn : bool, default=False
        Whether to display warnings.

    Returns
    -------
    y : ndarray
        Output data.

    Raises
    ------
    ValueError
        If `y` is not a 1D array or a 2D array with a single row or column.

    Examples
    --------
    >>> column_or_1d([1, 1])
    array([1, 1])
    """
    y = np.asarray(y, dtype=dtype)

    if y.ndim == 1:
        return y.ravel()
    elif y.ndim == 2 and (y.shape[0] == 1 or y.shape[1] == 1):
        if warn:
            warnings.warn("A column-vector y was passed when a 1d array was expected. Please change the shape of y to (n_samples, ).", UserWarning, stacklevel=2)
        return y.ravel()

    raise ValueError(f"y should be a 1d array, got an array of shape {y.shape} instead.")



def _num_samples(x):
    """Return number of samples in array-like x."""
    if hasattr(x, "__len__"):
        return len(x)
    elif hasattr(x, "shape") and x.shape is not None:
        if len(x.shape) == 0:
            raise TypeError("Singleton array %r cannot be considered a valid collection." % x)
        elif isinstance(x.shape[0], numbers.Integral):
            return x.shape[0]
    raise TypeError("Expected sequence or array-like, got %s" % type(x))



def check_array(array, *, ensure_2d=True, ensure_min_samples=1, ensure_min_features=1):
    if ensure_2d and array.ndim < 2:
        raise ValueError("Expected 2D array, got array with ndim=%d" % array.ndim)

    if ensure_min_samples > 0 and len(array) < ensure_min_samples:
        raise ValueError(
            "Found array with %d sample(s) while a minimum of %d is required"
            % (len(array), ensure_min_samples)
        )

    if ensure_min_features > 0 and array.ndim == 2 and array.shape[1] < ensure_min_features:
        raise ValueError(
            "Found array with %d feature(s) while a minimum of %d is required"
            % (array.shape[1], ensure_min_features)
        )

    return array
