def r2_score(y_true, y_pred):
    """
    Calculate R-squared (R2) score.
    
    Parameters:
        y_true : array-like of shape (n_samples,)
            True labels.
        y_pred : array-like of shape (n_samples,)
            Predicted labels.
    
    Returns:
        r2 : float
            R-squared (R2) score.
    """
    # TODO: add case where inpute data is of shape (n_samples, n_outputs)
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    mean_true = sum(y_true) / len(y_true)
    total_variance = sum((true - mean_true) ** 2 for true in y_true)

    residual_variance = sum((true - pred) ** 2 for true, pred in zip(y_true, y_pred))

    r2 = 1 - (residual_variance / total_variance)
    return r2
