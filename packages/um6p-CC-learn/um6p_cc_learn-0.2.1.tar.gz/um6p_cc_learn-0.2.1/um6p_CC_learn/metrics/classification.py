import numpy as np
from scipy.sparse import coo_matrix


def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)

def fbeta_score(y_true, y_pred, beta, average="binary"):

    n_labels = len(set(y_true) | set(y_pred))
    true_sum = np.bincount(y_true, minlength=n_labels)
    pred_sum = np.bincount(y_pred, minlength=n_labels)
    tp = np.bincount(y_true[y_true == y_pred], minlength=n_labels)
    
    if average == "binary":
        tp = np.array([tp[1]])
        true_sum = np.array([true_sum[1]])
        pred_sum = np.array([pred_sum[1]])
    elif average == "micro":
        tp = np.array([np.sum(tp)])
        true_sum = np.array([np.sum(true_sum)])
        pred_sum = np.array([np.sum(pred_sum)])
        
    precision = np.zeros(len(pred_sum))
    mask = pred_sum != 0
    precision[mask] = tp[mask] / pred_sum[mask]
    
    recall = np.zeros(len(true_sum))
    mask = true_sum != 0
    recall[mask] = tp[mask] / true_sum[mask]
    
    denom = (beta ** 2) * precision + recall
    denom[denom == 0.] = 1
    
    fscore = (1 + np.square(beta)) * precision * recall / denom
    
    if average == "weighted":
        fscore = np.average(fscore, weights=true_sum)
    elif average is not None:
        fscore = np.mean(fscore)
    
    return fscore


def f1_score(y_true, y_pred, average="binary"):
    return fbeta_score(y_true, y_pred, 1.0, average)


def recall_score(y_true, y_pred, average):
    n_labels = len(set(y_true) | set(y_pred))
    true_sum = np.bincount(y_true, minlength=n_labels)
    tp = np.bincount(y_true[y_true == y_pred], minlength=n_labels)
    
    if average == "binary":
        tp = np.array([tp[1]])
        true_sum = np.array([true_sum[1]])
    elif average == "micro":
        tp = np.array([np.sum(tp)])
        true_sum = np.array([np.sum(true_sum)])
    
    recall = np.zeros(len(true_sum))
    mask = true_sum != 0
    recall[mask] = tp[mask] / true_sum[mask]
    
    if average == "weighted":
        recall = np.average(recall, weights=true_sum)
    elif average is not None:
        recall = np.mean(recall)
    
    return recall



def precision_score(y_true, y_pred, average = "binary"):

    n_labels = len(set(y_true) | set(y_pred))
    true_sum = np.bincount(y_true, minlength=n_labels)
    pred_sum = np.bincount(y_pred, minlength=n_labels)
    tp = np.bincount(y_true[y_true == y_pred], minlength=n_labels)

    if average == "binary":
        tp = np.array([tp[1]])
        pred_sum = np.array([pred_sum[1]])
    elif average == "micro":
        tp = np.array([np.sum(tp)])
        pred_sum = np.array([np.sum(pred_sum)])
    
    precision = np.zeros(len(pred_sum))
    mask = pred_sum != 0
    precision[mask] = tp[mask] / pred_sum[mask]

    if average == "weighted":
        precision = np.average(precision, weights=true_sum)
    elif average is not None:
        precision = np.mean(precision)
    return precision


def confusion_matrix(y_true, y_pred):
    labels = np.unique(np.concatenate([y_true, y_pred]))
    n_labels = len(labels)
    label_to_ind = {label: i for i, label in enumerate(labels)}
    
    true_inds = np.array([label_to_ind[label] for label in y_true])
    pred_inds = np.array([label_to_ind[label] for label in y_pred])
    
    cm = np.bincount(n_labels * true_inds + pred_inds, minlength=np.square(n_labels)).reshape(n_labels, n_labels)
    
    return cm


