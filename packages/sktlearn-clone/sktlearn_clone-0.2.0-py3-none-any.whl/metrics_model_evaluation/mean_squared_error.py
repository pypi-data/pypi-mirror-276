def mean_squared_error(y_true, y_pred):
    """
    Calculate mean squared error (MSE).
    
    Parameters:
        y_true : array-like of shape (n_samples,)
            True labels.
        y_pred : array-like of shape (n_samples,)
            Predicted labels.
    
    Returns:
        mse : float
            Mean squared error.
    """
    # TODO: add case where inpute data is of shape (n_samples, n_outputs)
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    squared_errors = [(true - pred) ** 2 for true, pred in zip(y_true, y_pred)]
    mse = sum(squared_errors) / len(y_true)
    return mse
