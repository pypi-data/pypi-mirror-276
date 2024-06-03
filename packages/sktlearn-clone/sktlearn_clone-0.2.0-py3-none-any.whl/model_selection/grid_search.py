import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from model_selection.param_grid import ParameterGrid
import numpy as np

class GridSearchCV:
    def __init__(self, estimator, param_grid, scoring=None, cv=None, n_jobs=None, verbose=0):
        self.estimator = estimator
        self.param_grid = param_grid
        self.scoring = scoring
        self.cv = cv
        self.n_jobs = n_jobs
        self.verbose = verbose

    def fit(self, X, y=None):
        if self.scoring is None:
            raise ValueError("Scoring parameter is required")

        if self.cv is None:
            raise ValueError("Cross-validation parameter is required")

        cv = self.cv
        param_grid = list(ParameterGrid(self.param_grid))
        scores = []

        for params in param_grid:
            estimator = self.estimator.set_params(**params)
            fold_scores = []

            for train_idx, test_idx in cv.split(X, y):
                X_train, X_test = X[train_idx], X[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]

                estimator.fit(X_train, y_train)
                score = self.scoring(estimator, X_test, y_test)
                fold_scores.append(score)

            mean_score = np.mean(fold_scores)
            scores.append((params, mean_score))

        best_params, best_score = max(scores, key=lambda x: x[1])
        self.best_params_ = best_params
        self.best_score_ = best_score

        self.best_estimator_ = self.estimator.set_params(**best_params)
        self.best_estimator_.fit(X, y)

        return self

    def score(self, X, y=None):
        cv = self.cv
        param_grid = list(ParameterGrid(self.param_grid))
        scores = []

        for params in param_grid:
            estimator = self.estimator.set_params(**params)
            fold_scores = []

            for train_idx, test_idx in cv.split(X, y):
                X_train, X_test = X[train_idx], X[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]

                estimator.fit(X_train, y_train)
                score = self.scoring(estimator, X_test, y_test)
                fold_scores.append(score)

            mean_score = np.mean(fold_scores)
            scores.append((params, mean_score))

        best_params, best_score = max(scores, key=lambda x: x[1])
        self.best_params_ = best_params
        self.best_score_ = best_score

        self.best_estimator_ = self.estimator.set_params(**best_params)
        self.best_estimator_.fit(X, y)

     
        return self   






# class GridSearchCV:
#     def __init__(self, estimator, param_grid, scoring=None, cv=None, n_jobs=None, verbose=0):
#         self.estimator = estimator
#         self.param_grid = param_grid
#         self.scoring = scoring
#         self.cv = cv
#         self.n_jobs = n_jobs
#         self.verbose = verbose

#     def fit(self, X, y=None):
#         if self.scoring is None:
#             raise ValueError("Scoring parameter is required")

#         if self.cv is None:
#             raise ValueError("Cross-validation parameter is required")

#         cv = self.cv
#         param_grid = list(ParameterGrid(self.param_grid))
#         scores = []

#         if isinstance(self.scoring, str):
#             scoring_func = self._get_scoring_func(self.scoring)
#         else:
#             scoring_func = self.scoring

#         for params in param_grid:
#             estimator = self.estimator.set_params(**params)
#             fold_scores = []

#             for train_idx, test_idx in cv.split(X, y):
#                 X_train, X_test = X[train_idx], X[test_idx]
#                 y_train, y_test = y[train_idx], y[test_idx]

#                 estimator.fit(X_train, y_train)
#                 score = scoring_func(estimator, X_test, y_test)
#                 fold_scores.append(score)

#             mean_score = np.mean(fold_scores)
#             scores.append((params, mean_score))

#         best_params, best_score = max(scores, key=lambda x: x[1])
#         self.best_params_ = best_params
#         self.best_score_ = best_score

#         self.best_estimator_ = self.estimator.set_params(**best_params)
#         self.best_estimator_.fit(X, y)

#         return self

#     def _get_scoring_func(self, scoring):
#         if scoring == 'accuracy':
#             return accuracy_scorer  # Define your accuracy scoring function here
#         # Add other scoring functions as needed
#         else:
#             raise ValueError(f"Scoring method '{scoring}' not supported")

#     def score(self, X, y=None):
#         cv = self.cv
#         param_grid = list(ParameterGrid(self.param_grid))
#         scores = []

#         if isinstance(self.scoring, str):
#             scoring_func = self._get_scoring_func(self.scoring)
#         else:
#             scoring_func = self.scoring

#         for params in param_grid:
#             estimator = self.estimator.set_params(**params)
#             fold_scores = []

#             for train_idx, test_idx in cv.split(X, y):
#                 X_train, X_test = X[train_idx], X[test_idx]
#                 y_train, y_test = y[train_idx], y[test_idx]

#                 estimator.fit(X_train, y_train)
#                 score = scoring_func(estimator, X_test, y_test)
#                 fold_scores.append(score)

#             mean_score = np.mean(fold_scores)
#             scores.append((params, mean_score))

#         best_params, best_score = max(scores, key=lambda x: x[1])
#         self.best_params_ = best_params
#         self.best_score_ = best_score

#         self.best_estimator_ = self.estimator.set_params(**best_params)
#         self.best_estimator_.fit(X, y)

#         return self
