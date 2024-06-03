
#     X_min = X.min(axis=0)
#     X_max = X.max(axis=0)

import numpy as np

def scale_features(X, axis=0):
    """
    Scale features in X using Min-Max scaling.

    Parameters:
    - X: Input array.
    - axis: Axis along which to scale the features.

    Returns:
    - X_scaled: Scaled array.
    """
    X_min = X.min(axis=axis, keepdims=True)
    X_max = X.max(axis=axis, keepdims=True)
    X_scaled = (X - X_min) / (X_max - X_min)
    return X_scaled
