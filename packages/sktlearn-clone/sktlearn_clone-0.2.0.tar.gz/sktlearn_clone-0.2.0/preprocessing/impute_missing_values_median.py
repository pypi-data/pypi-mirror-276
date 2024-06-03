import numpy as np

def impute_missing_values_median(X):
    """
    Impute missing values in X using median.
    """
    missing_mask = np.isnan(X)
    X_imputed = np.where(missing_mask, np.nanmedian(X, axis=0), X)
    return X_imputed
