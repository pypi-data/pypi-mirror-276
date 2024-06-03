def scale_features(X, axis=0):
    """
    Scale features in X using Standard scaling.

    Parameters:
    - X: Input array.
    - axis: Axis along which to scale the features.

    Returns:
    - X_scaled: Scaled array.
    """
    X_mean = X.mean(axis=axis, keepdims=True)
    X_std = X.std(axis=axis, keepdims=True)
    X_scaled = (X - X_mean) / X_std
    return X_scaled
