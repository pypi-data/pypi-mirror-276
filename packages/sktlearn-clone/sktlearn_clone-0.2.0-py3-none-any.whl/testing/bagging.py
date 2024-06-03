
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from metrics_model_evaluation.accuracy import accuracy_score

# Test script
import unittest
from ensemble_methods.bagging import BaggingClassifier
from supervised_learning.DecisionTree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier as SklearnBaggingClassifier
from ensemble_methods.bagging import BaggingRegressor
from supervised_learning.DecisionTree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor as SklearnBaggingRegressor
from sklearn.datasets import load_iris
from model_selection.train_test_split import TrainTestSplitter

class TestBaggingClassifier(unittest.TestCase):
    def setUp(self):
        self.data = load_iris()
        splitter = TrainTestSplitter(random_state=42)
        
        self.X_train, self.X_test, self.y_train, self.y_test = splitter.split(self.data.data, self.data.target)
        self.base_estimator = DecisionTreeClassifier()

    def test_bagging_classifier(self):
        my_bagging = BaggingClassifier(base_estimator=self.base_estimator, n_estimators=10, random_state=42)
        my_bagging.fit(self.X_train, self.y_train)
        my_preds = my_bagging.predict(self.X_test)
        my_accuracy = accuracy_score(self.y_test, my_preds)

        sklearn_bagging = SklearnBaggingClassifier( n_estimators=10)
        sklearn_bagging.fit(self.X_train, self.y_train)
        sklearn_preds = sklearn_bagging.predict(self.X_test)
        sklearn_accuracy = accuracy_score(self.y_test, sklearn_preds)

        print(f"My BaggingClassifier accuracy: {my_accuracy}")
        print(f"Scikit-learn BaggingClassifier accuracy: {sklearn_accuracy}")

        self.assertAlmostEqual(my_accuracy, sklearn_accuracy, places=2)
    
    def test_bagging_regressor(self):
        # Load dataset
        iris = load_iris()
        X = iris.data
        y = iris.target

        # Split dataset
        splitter = TrainTestSplitter(test_size=0.2, random_state=42)
        X_train, X_test, y_train, y_test = splitter.split(X, y)

        # Create and fit BaggingRegressor
        base_estimator = DecisionTreeRegressor(max_depth=3)
        bagging_regressor = BaggingRegressor(base_estimator=base_estimator, n_estimators=5, random_state=42)
        bagging_regressor.fit(X_train, y_train)

        # Evaluate BaggingRegressor
        score = bagging_regressor.score(X_test, y_test)

        # Compare with sklearn's BaggingRegressor
        sk_bagging_regressor = SklearnBaggingRegressor( n_estimators=5, random_state=42)
        sk_bagging_regressor.fit(X_train, y_train)
        sk_score = sk_bagging_regressor.score(X_test, y_test)

        # Assert that the scores are equal
        self.assertAlmostEqual(score, sk_score, places=5)

if __name__ == '__main__':
    unittest.main()
