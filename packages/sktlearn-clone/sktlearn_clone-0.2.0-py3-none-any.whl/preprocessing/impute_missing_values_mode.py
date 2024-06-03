import numpy as np
from scipy.stats import mode

def impute_missing_values_mode(X):
    """
    Impute missing values in X using mode.

    Parameters:
    - X: Input array with missing values.

    Returns:
    - X_imputed: Array with missing values imputed using mode.
    """
    mode_values, _ = mode(X, axis=0, nan_policy='omit')  
    mask = np.isnan(X)  
    X_imputed = X.copy()  
    X_imputed[mask] = np.take(mode_values, np.nonzero(mask)[1]) 
    return X_imputed
