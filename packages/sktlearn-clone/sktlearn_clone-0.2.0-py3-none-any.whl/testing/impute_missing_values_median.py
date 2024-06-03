# Testing/test_impute_missing_values_median.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from preprocessing.impute_missing_values_median import impute_missing_values_median

class TestImputeMissingValuesMedian(unittest.TestCase):

    def test_impute_missing_values_median_custom(self):
        X = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
        X_imputed_custom = impute_missing_values_median(X)
        expected_custom = np.array([[1., 2., 7.5], [4., 5., 6.], [7., 8., 9.]])
        self.assertTrue(np.allclose(X_imputed_custom, expected_custom, equal_nan=True))

    def test_impute_missing_values_median_sklearn(self):
        from sklearn.impute import SimpleImputer
        X = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
        imputer_sklearn = SimpleImputer(strategy='median')
        X_imputed_sklearn = imputer_sklearn.fit_transform(X)
        expected_sklearn = np.array([[1., 2., 7.5], [4., 5., 6.], [7., 8., 9.]])
        self.assertTrue(np.allclose(X_imputed_sklearn, expected_sklearn, equal_nan=True))

if __name__ == '__main__':
    unittest.main()
