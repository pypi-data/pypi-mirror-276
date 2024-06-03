import numpy as np

def roc_curve(y_true, y_score):
    desc_score_indices = np.argsort(y_score, kind="mergesort")[::-1]
    y_true = y_true[desc_score_indices]
    y_score = y_score[desc_score_indices]
    distinct_value_indices = np.where(np.diff(y_score))[0]
    threshold_idxs = np.r_[distinct_value_indices, y_true.size - 1]
    tps = np.cumsum(y_true)[threshold_idxs]
    fps = 1 + threshold_idxs - tps
    thresholds = y_score[threshold_idxs]
    tps = np.r_[0, tps]
    fps = np.r_[0, fps]
    thresholds = np.r_[thresholds[0] + 1, thresholds]
    tpr = tps / tps[-1]
    fpr = fps / fps[-1]
    return fpr, tpr, thresholds


