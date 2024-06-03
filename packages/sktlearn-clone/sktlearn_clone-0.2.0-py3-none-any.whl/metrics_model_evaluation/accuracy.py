def accuracy_score(y_true, y_pred):
    """
    Calculate accuracy score.
    
    Parameters:
        y_true : array-like of shape (n_samples,)
            True labels.
        y_pred : array-like of shape (n_samples,)
            Predicted labels.
    
    Returns:
        accuracy : float
            Accuracy score.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    total = len(y_true)
    accuracy = correct / total
    return accuracy
