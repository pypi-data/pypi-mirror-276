import numpy as np

def impute_missing_values_mean(X):
    """
    Impute missing values in X using mean.
    """
    missing_mask = np.isnan(X)
    X_imputed = np.where(missing_mask, np.nanmean(X, axis=0), X)
    return X_imputed
