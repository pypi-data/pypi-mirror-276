

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from model_selection.cross_validation import cross_val_score
from model_selection.kfold import KFold
import numpy as np
import unittest

class TestCrossValidation(unittest.TestCase):

    def test_cross_val_score(self):
        iris = load_iris()
        X = iris.data
        y = iris.target

        estimator = LogisticRegression(max_iter=200)

        # Testing your implementation
        custom_scores = cross_val_score(estimator, X, y, cv=KFold(n_splits=3))
        # Testing scikit-learn's implementation
        sk_scores = cross_val_score(estimator, X, y, cv=KFold(n_splits=3))

        # Assert that both implementations produce similar results
        np.testing.assert_array_almost_equal(custom_scores, sk_scores)

if __name__ == '__main__':
    unittest.main()
