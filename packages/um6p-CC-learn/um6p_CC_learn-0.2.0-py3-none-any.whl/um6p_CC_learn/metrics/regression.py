import numpy as np


def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def mean_squared_error(y_true, y_pred):
    return np.mean(np.square((y_true - y_pred)))

def r2_score(y_true, y_pred):
    numerator = np.sum(np.square((y_true - y_pred)))
    denominator = np.sum(np.square((y_true - np.mean(y_true))))
    return 1 - numerator / denominator
