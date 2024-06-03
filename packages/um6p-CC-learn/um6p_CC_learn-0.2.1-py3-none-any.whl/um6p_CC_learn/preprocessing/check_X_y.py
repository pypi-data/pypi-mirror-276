import numpy as np
def check_X_y(X, y):
    """Validate and return X and y arrays."""
    X = np.asarray(X)
    y = np.asarray(y)
    if X.shape[0] != y.shape[0]:
        raise ValueError("Number of samples in X and y does not match.")
    return X, y