import numpy as np

def confusion_matrix(y_true, y_pred):
    """
    Compute confusion matrix to evaluate the accuracy of a classification.

    Parameters:
    y_true: array-like of shape (n_samples,)
        Ground truth (correct) target values.
    y_pred: array-like of shape (n_samples,)
        Estimated targets as returned by a classifier.

    Returns:
    C: ndarray of shape (n_classes, n_classes)
        Confusion matrix whose i-th row and j-th column entry indicates the number of samples with true label being i-th class and predicted label being j-th class.
    """
    labels = np.unique(np.concatenate((y_true, y_pred)))
    n_classes = len(labels)
    C = np.zeros((n_classes, n_classes), dtype=int)

    for i in range(len(y_true)):
        true_label = np.where(labels == y_true[i])[0][0]
        pred_label = np.where(labels == y_pred[i])[0][0]
        C[true_label, pred_label] += 1

    return C

