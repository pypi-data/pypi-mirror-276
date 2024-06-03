import numpy as np
import os
import sys
from copy import deepcopy

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Estimator import Estimator
from metrics_model_evaluation.accuracy import accuracy_score

class ClassifierMixin:
    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

class RegressorMixin:
    def score(self, X, y):
        y_pred = self.predict(X)
        return 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)

def clone(estimator):
    return deepcopy(estimator)

def check_is_fitted(estimator, attributes):
    if isinstance(attributes, str):
        attributes = [attributes]
    for attr in attributes:
        if not hasattr(estimator, attr):
            raise ValueError(f"This {type(estimator)._name_} instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.")

def resample(X, y, random_state=None):
    if random_state is not None:
        np.random.seed(random_state)
    n_samples = X.shape[0]
    indices = np.random.choice(n_samples, size=n_samples, replace=True)
    return X[indices], y[indices]

class BaggingClassifier(Estimator, ClassifierMixin):
    def __init__(self, base_estimator, n_estimators=10, random_state=None):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.random_state = random_state

    def fit(self, X, y):
        self.estimators_ = []
        
        for i in range(self.n_estimators):
            estimator = clone(self.base_estimator)
            X_resampled, y_resampled = resample(X, y, random_state=self.random_state + i)  # Use different random states
            estimator.fit(X_resampled, y_resampled)
            self.estimators_.append(estimator)
        
        print(f"Fit {len(self.estimators_)} estimators.")
        return self

    def predict(self, X):
        print("Checking if fitted...")
        check_is_fitted(self, ['estimators_'])
        predictions = np.array([estimator.predict(X) for estimator in self.estimators_])
        print(f"Made predictions with {len(self.estimators_)} estimators.")
        return np.array([np.bincount(predictions[:, i]).argmax() for i in range(predictions.shape[1])])
    
class BaggingRegressor(Estimator, RegressorMixin):
    def __init__(self, base_estimator, n_estimators=10, random_state=None):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.random_state = random_state

    def fit(self, X, y):
        self.estimators_ = []

        for i in range(self.n_estimators):
            estimator = clone(self.base_estimator)
            X_resampled, y_resampled = resample(X, y, random_state=self.random_state + i)  # Use different random states
            estimator.fit(X_resampled, y_resampled)
            self.estimators_.append(estimator)

        print(f"Fit {len(self.estimators_)} estimators.")
        return self

    def predict(self, X):
        print("Checking if fitted...")
        check_is_fitted(self, ['estimators_'])
        predictions = np.array([estimator.predict(X) for estimator in self.estimators_])
        print(f"Made predictions with {len(self.estimators_)} estimators.")
        return np.mean(predictions, axis=0)

    def score(self, X, y):
        y_pred = self.predict(X)
        return 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)

