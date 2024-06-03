import numpy as np

def auc(x, y):
    """Compute Area Under the Curve (AUC) using the trapezoidal rule.

    Parameters
    ----------
    x : array-like of shape (n,)
        X coordinates. These must be either monotonic increasing or monotonic
        decreasing.
    y : array-like of shape (n,)
        Y coordinates.

    Returns
    -------
    auc : float
        Area Under the Curve.

    Raises
    ------
    ValueError
        If x is neither increasing nor decreasing.

    Notes
    -----
    This function assumes that x is sorted in increasing order.
    """
    # Check for consistent length of x and y
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")

    # Check if x is monotonic
    if not np.all(np.diff(x) >= 0) and not np.all(np.diff(x) <= 0):
        raise ValueError("x must be monotonic increasing or decreasing")

    # Calculate the area under the curve using the trapezoidal rule
    auc_value = np.trapz(y, x)

    return auc_value
