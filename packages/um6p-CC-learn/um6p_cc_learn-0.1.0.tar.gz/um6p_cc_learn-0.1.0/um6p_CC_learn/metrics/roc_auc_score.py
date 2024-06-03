
from .roc_curve import roc_curve
from .auc import auc

def roc_auc_score(y_true, y_score):
    """Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC)
       from prediction scores.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True binary labels in binary label indicators.

    y_score : array-like of shape (n_samples,)
        Target scores, can either be probability estimates of the positive
        class, confidence values, or non-thresholded measure of decisions
        (as returned by "decision_function" on some classifiers).

    Returns
    -------
    auc : float
        The Area Under the ROC Curve (ROC AUC) from prediction scores.
    """
    fpr, tpr, _ = roc_curve(y_true, y_score)
    return auc(fpr, tpr)


