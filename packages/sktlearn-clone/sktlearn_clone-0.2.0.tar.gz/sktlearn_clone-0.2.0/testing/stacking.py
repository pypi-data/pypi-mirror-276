import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import numpy as np
import unittest
import os
import sys
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

# Ensure the project root is in the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import your custom GradientBoosting implementations
from ensemble_methods.stacking import StackingClassifier as CustomStackingClassifier
from ensemble_methods.stacking import StackingRegressor as CustomStackingRegressor

# Import scikit-learn's implementations for comparison
from sklearn.ensemble import StackingClassifier as SKStackingClassifier
from sklearn.ensemble import StackingRegressor as SKStackingRegressor
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


class TestStacking(unittest.TestCase):
    def test_stacking_regressor(self):
        X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        base_models = [LinearRegression(), DecisionTreeRegressor()]
        meta_model = Ridge()

        custom_model = CustomStackingRegressor(base_models, meta_model)
        custom_model.fit(X_train, y_train)
        custom_preds = custom_model.predict(X_test)
        custom_mse = mean_squared_error(y_test, custom_preds)
        print("Custom Stacking Regressor MSE:", custom_mse)

        sk_model = SKStackingRegressor(estimators=[('lr', LinearRegression()), ('dt', DecisionTreeRegressor())], final_estimator=Ridge(), cv=5)
        sk_model.fit(X_train, y_train)
        sk_preds = sk_model.predict(X_test)
        sk_mse = mean_squared_error(y_test, sk_preds)
        print("Sklearn Stacking Regressor MSE:", sk_mse)

        self.assertAlmostEqual(custom_mse, sk_mse, places=2)

    def test_stacking_classifier(self):
        X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        base_models = [LogisticRegression(random_state=42), DecisionTreeClassifier(random_state=42)]
        meta_model = RandomForestClassifier(random_state=42)

        custom_model = CustomStackingClassifier(base_models, meta_model)
        custom_model.fit(X_train, y_train)
        custom_preds = custom_model.predict(X_test)
        custom_acc = accuracy_score(y_test, custom_preds)
        print("Custom Stacking Classifier Accuracy:", custom_acc)

        sk_model = SKStackingClassifier(estimators=[('lr', LogisticRegression(random_state=42)), ('dt', DecisionTreeClassifier(random_state=42))], final_estimator=RandomForestClassifier(random_state=42), cv=5)
        sk_model.fit(X_train, y_train)
        sk_preds = sk_model.predict(X_test)
        sk_acc = accuracy_score(y_test, sk_preds)
        print("Sklearn Stacking Classifier Accuracy:", sk_acc)

        self.assertAlmostEqual(custom_acc, sk_acc, delta=0.07)

if __name__ == '__main__':
    unittest.main()