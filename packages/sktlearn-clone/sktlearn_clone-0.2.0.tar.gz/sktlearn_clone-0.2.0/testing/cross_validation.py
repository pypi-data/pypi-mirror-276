# Testing/test_crossval.py

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import unittest
import numpy as np
from model_selection.cross_validation import cross_val_score
from model_selection.kfold import KFold

from sklearn.model_selection import cross_val_score as sk_cross_val_score
from sklearn.linear_model import LogisticRegression

class TestCrossValidation(unittest.TestCase):

    def test_cross_val_score(self):
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
        y = np.array([0, 1, 0, 1, 0])

        estimator = LogisticRegression()

        # Testing your implementation
        custom_scores = cross_val_score(estimator, X, y, cv=KFold(n_splits=3))
        # Testing scikit-learn's implementation
        sk_scores = sk_cross_val_score(estimator, X, y, cv=3)

        # Assert that both implementations produce similar results
        np.testing.assert_array_almost_equal(custom_scores, sk_scores)

if __name__ == '__main__':
    unittest.main()
