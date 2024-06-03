# Testing/test_select_features.py
import sys
sys.path.append('C:\\Users\\Pc\\Downloads\\scikit-learn-clone')
import unittest
import numpy as np
from preprocessing.select_features import select_features

from sklearn.feature_selection import SelectKBest, f_regression

class TestSelectFeatures(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.X = np.random.rand(100, 10)
        self.y = np.random.rand(100)
        self.k = 5

    def test_correlation(self):
        X_selected = select_features(self.X, self.y, k=self.k, method='correlation')
        selector = SelectKBest(score_func=f_regression, k=self.k)
        X_selected_sklearn = selector.fit_transform(self.X, self.y)

        # Sort the selected features for comparison
        X_selected_sorted = np.sort(X_selected, axis=1)
        X_selected_sklearn_sorted = np.sort(X_selected_sklearn, axis=1)
        
        np.testing.assert_array_equal(X_selected_sorted, X_selected_sklearn_sorted)

if __name__ == '__main__':
    unittest.main()
