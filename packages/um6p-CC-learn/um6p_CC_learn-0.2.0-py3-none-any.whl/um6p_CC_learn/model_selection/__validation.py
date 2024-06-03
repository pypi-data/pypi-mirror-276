from utils.__clone import clone
import numpy as np


from model_selection.__split import KFold, StratifiedKFold



def cross_val_predict(estimator, X, y, method="predict"):
    if estimator._estimator_type == "regressor":
        cv = KFold()
    else:  # estimator._estimator_type == "classifier"
        cv = StratifiedKFold()
    predictions = []
    indices = []
    for train, test in cv.split(X, y):
        est = clone(estimator)
        est.fit(X[train], y[train])
        predictions.extend(getattr(est, method)(X[test]))
        indices.extend(test)
    inv_indices = np.empty(len(indices), dtype=int)
    inv_indices[indices] = np.arange(len(indices))
    return np.array(predictions)[inv_indices]
