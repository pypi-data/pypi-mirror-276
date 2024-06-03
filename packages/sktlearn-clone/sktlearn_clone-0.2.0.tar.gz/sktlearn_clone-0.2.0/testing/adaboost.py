import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import unittest
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from ensemble_methods.adaBoost import AdaBoostClassifier

class TestAdaBoostClassifier(unittest.TestCase):
    def setUp(self):
        self.data = load_iris()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data.data, self.data.target, test_size=0.3, random_state=42)
        self.base_estimator = DecisionTreeClassifier(max_depth=1)

    def test_fit(self):
        ada_boost = AdaBoostClassifier(base_estimator=self.base_estimator, n_estimators=10, random_state=42)
        ada_boost.fit(self.X_train, self.y_train)
        self.assertTrue(hasattr(ada_boost, 'estimators_'))
        self.assertTrue(hasattr(ada_boost, 'estimator_weights'))

    def test_predict(self):
        ada_boost = AdaBoostClassifier(base_estimator=self.base_estimator, n_estimators=10, random_state=42)
        ada_boost.fit(self.X_train, self.y_train)
        y_pred = ada_boost.predict(self.X_test)
        self.assertEqual(y_pred.shape[0], self.X_test.shape[0])

    def test_score(self):
        ada_boost = AdaBoostClassifier(base_estimator=self.base_estimator, n_estimators=10, random_state=42)
        ada_boost.fit(self.X_train, self.y_train)
        score = ada_boost.score(self.X_test, self.y_test)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

if __name__ == '__main__':
    unittest.main()

