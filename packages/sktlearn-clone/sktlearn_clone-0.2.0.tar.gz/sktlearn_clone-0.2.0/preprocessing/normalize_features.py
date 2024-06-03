
#     norms = np.linalg.norm(X, axis=1)
#     X_normalized = X / norms[:, None]

import numpy as np

def normalize_features(X, norm='l2', axis=1):
    """
    Normalize features in X to have unit norm.

    Parameters:
    - X: Input array.
    - norm: Type of norm to use ('l1', 'l2', or 'max').
    - axis: Axis along which to compute the norm.

    Returns:
    - X_normalized: Normalized array.
    """
    if norm == 'l1':
        ord = 1
    elif norm == 'l2':
        ord = 2
    elif norm == 'max':
        ord = - np.inf
    else:
        raise ValueError("Invalid norm. Supported norms are 'l1', 'l2', and 'max'.")

    norms = np.linalg.norm(X, ord=ord, axis=axis, keepdims=True)
    X_normalized = X / norms
    return X_normalized

