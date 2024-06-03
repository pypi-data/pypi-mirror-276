import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from model_selection.grid_search import GridSearchCV
import sklearn.model_selection 
from model_selection.kfold import KFold


class TestGridSearchCV(unittest.TestCase):
    def test_grid_search_cv(self):
        # Define the parameter grid
        param_grid = {
            'a': [1, 2, 3],
            'b': ['x', 'y'],
            'c': [0.1, 0.2]
        }

        # Define the estimator (you can use a simple one for testing purposes)
        class DummyEstimator:
            def __init__(self, a=None, b=None, c=None):
                self.params = {'a': a, 'b': b, 'c': c}

            def set_params(self, **params):
                self.params.update(params)
                return self

            def get_params(self, deep=True):
                return self.params

            def fit(self, X, y):
                return self

            def predict(self, X):
                return np.zeros(len(X))  # Dummy predictions



        estimator = DummyEstimator()

        # Define scoring function (you can use a simple one for testing purposes)
        def dummy_scoring(estimator, X, y):
            return np.mean(estimator.predict(X) == y)  # Dummy scoring

        # Define cross-validation strategy
        cv = sklearn.model_selection.KFold(n_splits=3)
        # cv = KFold(n_splits=3)


        # Create GridSearchCV instances
        custom_grid_search = GridSearchCV(estimator, param_grid, scoring=dummy_scoring, cv=cv)
        sklearn_grid_search = sklearn.model_selection.GridSearchCV(estimator, param_grid, scoring=dummy_scoring, cv=cv)

        # Generate some dummy data
        X = np.random.rand(100, 3)
        y = np.random.randint(0, 2, size=100)

        # Fit both models
        custom_grid_search.fit(X, y)
        sklearn_grid_search.fit(X, y)

        # Check if the best parameters and best score are the same
        self.assertEqual(custom_grid_search.best_params_, sklearn_grid_search.best_params_)
        self.assertEqual(custom_grid_search.best_score_, sklearn_grid_search.best_score_)


if __name__ == '__main__':
    unittest.main()
