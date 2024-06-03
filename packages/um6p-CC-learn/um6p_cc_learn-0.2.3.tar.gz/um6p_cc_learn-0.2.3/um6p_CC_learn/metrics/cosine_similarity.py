import numpy as np


def cosine_similarity(X, Y=None):
    # Normalize input data
    X_normalized = _normalize(X, copy=True)
    if Y is None:
        Y_normalized = X_normalized
    else:
        Y_normalized = _normalize(Y, copy=True)
    # Compute dot product
    dot_product = np.dot(X_normalized, Y_normalized.T)
    return dot_product


def _normalize(X, copy=False):
    X = np.asarray(X)
    if np.issubdtype(X.dtype, np.floating):
        norm = np.sqrt(np.sum(np.square(X), axis=1, keepdims=True))
        X_normalized = X / norm
        if copy:
            return X_normalized.copy()
        else:
            return X_normalized
    else:
        raise ValueError("Unsupported dtype for input array. Only floating-point arrays are supported.")
