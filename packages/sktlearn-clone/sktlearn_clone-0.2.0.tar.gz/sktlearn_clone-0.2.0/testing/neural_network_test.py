import os
import sys
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.neural_network import MLPClassifier, MLPRegressor

# Ensure project_root is in the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import custom modules
from model_selection import train_test_split
from supervised_learning.NeuralNetwork import NeuralNetworkClassifier, NeuralNetworkRegressor

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and evaluate custom Neural Network Classifier
nn_classifier = NeuralNetworkClassifier(input_size=X.shape[1], hidden_size=5, output_size=3, learning_rate=0.01, epochs=1000)
nn_classifier.fit(X_train, y_train)
y_pred_nn_classifier = nn_classifier.predict(X_test)
accuracy_nn_classifier = accuracy_score(y_test, y_pred_nn_classifier)

# Train and evaluate scikit-learn MLPClassifier
mlp_classifier = MLPClassifier(hidden_layer_sizes=(5,), max_iter=1000, random_state=42)
mlp_classifier.fit(X_train, y_train)
y_pred_mlp_classifier = mlp_classifier.predict(X_test)
accuracy_mlp_classifier = accuracy_score(y_test, y_pred_mlp_classifier)

print(f"Custom Neural Network Classifier Accuracy: {accuracy_nn_classifier:.4f}")
print(f"scikit-learn MLPClassifier Accuracy: {accuracy_mlp_classifier:.4f}")

# Assuming we are using the Iris dataset for regression by using all features to predict one target
y_reg = y  # Using the target classes for regression

# Split the dataset into training and testing sets for regression
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.2, random_state=42)

# Train and evaluate custom Neural Network Regressor
nn_regressor = NeuralNetworkRegressor(input_size=X.shape[1], hidden_size=5, output_size=1, learning_rate=0.01, epochs=1000)
nn_regressor.fit(X_train_reg, y_train_reg)
y_pred_nn_regressor = nn_regressor.predict(X_test_reg)
mse_nn_regressor = mean_squared_error(y_test_reg, y_pred_nn_regressor)
r2_nn_regressor = r2_score(y_test_reg, y_pred_nn_regressor)

# Train and evaluate scikit-learn MLPRegressor
mlp_regressor = MLPRegressor(hidden_layer_sizes=(5,), max_iter=1000, random_state=42)
mlp_regressor.fit(X_train_reg, y_train_reg)
y_pred_mlp_regressor = mlp_regressor.predict(X_test_reg)
mse_mlp_regressor = mean_squared_error(y_test_reg, y_pred_mlp_regressor)
r2_mlp_regressor = r2_score(y_test_reg, y_pred_mlp_regressor)

print(f"Custom Neural Network Regressor MSE: {mse_nn_regressor:.4f}, R2 Score: {r2_nn_regressor:.4f}")
print(f"scikit-learn MLPRegressor MSE: {mse_mlp_regressor:.4f}, R2 Score: {r2_mlp_regressor:.4f}")
