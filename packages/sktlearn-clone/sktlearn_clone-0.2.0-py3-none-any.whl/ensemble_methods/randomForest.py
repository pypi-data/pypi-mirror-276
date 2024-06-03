
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Predictor import Predictor
from supervised_learning.DecisionTree import DecisionTreeClassifier, DecisionTreeRegressor

import numpy as np

class RandomForestClassifier(Predictor):
    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=None):
        super().__init__()
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.estimators_ = []

    def fit(self, X, y):
        for _ in range(self.n_estimators):
            tree = DecisionTreeClassifier(max_depth=self.max_depth, min_samples_split=self.min_samples_split,
                                           min_samples_leaf=self.min_samples_leaf, random_state=self.random_state)
            tree.fit(X, y)
            self.estimators_.append(tree)

    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.estimators_])
        # Calculate the most common prediction for each sample
        return np.array([np.argmax(np.bincount(tree_predictions)) for tree_predictions in predictions.T])


    def score(self, X, y):
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


class RandomForestRegressor(Predictor):
    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2, min_samples_leaf=1, random_state=None):
        super().__init__()
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.estimators_ = []

    def fit(self, X, y):
        for _ in range(self.n_estimators):
            tree = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_split=self.min_samples_split,
                                          min_samples_leaf=self.min_samples_leaf, random_state=self.random_state)
            tree.fit(X, y)
            self.estimators_.append(tree)

    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.estimators_])
        return np.mean(predictions, axis=0)

    def score(self, X, y):
        y_pred = self.predict(X)
        return 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)
