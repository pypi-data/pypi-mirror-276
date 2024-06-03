# Testing/test_normalize_features.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from preprocessing.normalize_features import normalize_features
from sklearn.preprocessing import normalize as sk_normalize

class TestNormalizeFeatures(unittest.TestCase):

    def test_normalize_features_custom(self):
        X = np.array([[1, 2, 3], [4, 5, 6]])
        X_normalized_custom = normalize_features(X, norm='l2', axis=1)

        expected_custom = np.array([[0.26726124, 0.53452248, 0.80178373],
                                     [0.45584231, 0.56980288, 0.68376346]])
        np.testing.assert_array_almost_equal(X_normalized_custom, expected_custom)

    def test_normalize_features_sklearn(self):
        X = np.array([[1, 2, 3], [4, 5, 6]])
        X_normalized_sklearn = sk_normalize(X, norm='l2', axis=1)

        expected_sklearn = np.array([[0.26726124, 0.53452248, 0.80178373],
                                      [0.45584231, 0.56980288, 0.68376346]])
        np.testing.assert_array_almost_equal(X_normalized_sklearn, expected_sklearn)

if __name__ == '__main__':
    unittest.main()