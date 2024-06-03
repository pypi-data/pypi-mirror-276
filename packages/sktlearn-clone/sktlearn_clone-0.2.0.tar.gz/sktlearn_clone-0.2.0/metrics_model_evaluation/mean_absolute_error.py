def mean_absolute_error(y_true, y_pred):
    """
    Calculate mean absolute error (MAE).
    
    Parameters:
        y_true : array-like of shape (n_samples,)
            True labels.
        y_pred : array-like of shape (n_samples,)
            Predicted labels.
    
    Returns:
        mae : float
            Mean absolute error.
    """
    # TODO: add case where inpute data is of shape (n_samples, n_outputs)
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    absolute_errors = [abs(true - pred) for true, pred in zip(y_true, y_pred)]
    mae = sum(absolute_errors) / len(y_true)
    return mae
