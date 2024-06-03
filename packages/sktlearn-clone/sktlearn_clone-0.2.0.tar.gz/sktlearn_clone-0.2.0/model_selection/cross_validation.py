import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import numpy as np
from model_selection.kfold import KFold
from Estimator import Estimator

def cross_val_score(estimator: Estimator, X, y, cv=None):
    # TODO: add attribute scoring
    if cv is None:
        cv = KFold(n_splits=5, shuffle=False, random_state=None)

    scores = []
    for train_index, test_index in cv.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train, y_train)
        score = estimator.score(X_test, y_test)
        scores.append(score)
    return np.array(scores)
