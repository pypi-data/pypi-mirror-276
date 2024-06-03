import os
import sys
import numpy as np
import unittest
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Ensure the project root is in the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import your custom GradientBoosting implementations
from ensemble_methods.gradient_boosting import GradientBoostingRegressor as CustomGradientBoostingRegressor
from ensemble_methods.gradient_boosting import GradientBoostingClassifier as CustomGradientBoostingClassifier

# Import scikit-learn's implementations for comparison
from sklearn.ensemble import GradientBoostingRegressor as SKGradientBoostingRegressor
from sklearn.ensemble import GradientBoostingClassifier as SKGradientBoostingClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier

class TestGradientBoosting(unittest.TestCase):
    def test_gradient_boosting_regressor(self):
        X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        custom_model = CustomGradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
        custom_model.fit(X_train, y_train)
        custom_preds = custom_model.predict(X_test)
        custom_mse = mean_squared_error(y_test, custom_preds)
        print("Custom Gradient Boosting Regressor MSE:", custom_mse)

        sk_model = SKGradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        sk_model.fit(X_train, y_train)
        sk_preds = sk_model.predict(X_test)
        sk_mse = mean_squared_error(y_test, sk_preds)
        print("Sklearn Gradient Boosting Regressor MSE:", sk_mse)

        self.assertAlmostEqual(custom_mse, sk_mse, delta=10)

    def test_gradient_boosting_classifier(self):
        X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convert continuous labels to discrete classes
        label_encoder = LabelEncoder()
        y_train_cls_encoded = label_encoder.fit_transform(y_train)
        y_test_cls_encoded = label_encoder.transform(y_test)

        custom_model = CustomGradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
        custom_model.fit(X_train, y_train_cls_encoded)
        custom_preds = custom_model.predict(X_test)
        custom_acc = accuracy_score(y_test_cls_encoded, custom_preds)
        print("Custom Gradient Boosting Classifier Accuracy:", custom_acc)

        sk_model = SKGradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        sk_model.fit(X_train, y_train)
        sk_preds = sk_model.predict(X_test)
        sk_acc = accuracy_score(y_test, sk_preds)
        print("Sklearn Gradient Boosting Classifier Accuracy:", sk_acc)

        self.assertAlmostEqual(custom_acc, sk_acc, delta=0.07)

if __name__ == '__main__':
    unittest.main()
