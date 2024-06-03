import os
import sys
import numpy as np
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Predictor import Predictor

def sigmoid(x):
    """
    Compute the sigmoid of x.
    """
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """
    Compute the derivative of the sigmoid function.
    """
    s = sigmoid(x)
    return s * (1 - s)

def softmax(x):
    """
    Compute the softmax of x.
    """
    exp_values = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_values / np.sum(exp_values, axis=1, keepdims=True)

def one_hot_encode(y, num_classes):
    """
    One-hot encode the labels.
    """
    return np.eye(num_classes)[y]

class NeuralNetworkClassifier(Predictor):
    def __init__(self, input_size, hidden_size=100, output_size=3, learning_rate=0.01, epochs=1000):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.epochs = epochs

        # Initialize weights and biases
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * 0.01
        self.bias_hidden = np.zeros(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * 0.01
        self.bias_output = np.zeros(output_size)

    def fit(self, X, y):
        """
        Train the neural network on the provided data.
        """
        y_one_hot = one_hot_encode(y, self.output_size)

        for epoch in range(self.epochs):
            # Forward pass
            hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
            hidden_output = sigmoid(hidden_input)
            output_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
            output_output = softmax(output_input)

            # Compute the loss
            loss = -np.sum(y_one_hot * np.log(output_output)) / y.shape[0]  # Cross-entropy loss

            # Backward pass
            error = output_output - y_one_hot
            dW_hidden_output = np.dot(hidden_output.T, error) / y.shape[0]
            db_output = np.sum(error, axis=0) / y.shape[0]
            hidden_error = np.dot(error, self.weights_hidden_output.T) * sigmoid_derivative(hidden_input)
            dW_input_hidden = np.dot(X.T, hidden_error) / y.shape[0]
            db_hidden = np.sum(hidden_error, axis=0) / y.shape[0]

            # Update weights and biases
            self.weights_hidden_output -= self.learning_rate * dW_hidden_output
            self.bias_output -= self.learning_rate * db_output
            self.weights_input_hidden -= self.learning_rate * dW_input_hidden
            self.bias_hidden -= self.learning_rate * db_hidden

            # Print loss every 100 epochs
            if epoch % 100 == 0:
                print(f"Epoch {epoch}/{self.epochs}, Loss: {loss:.4f}")

    def predict(self, X):
        """
        Predict class labels for samples in X.
        """
        hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        hidden_output = sigmoid(hidden_input)
        output_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        output_output = softmax(output_input)
        return np.argmax(output_output, axis=1)

class NeuralNetworkRegressor(Predictor):
    def __init__(self, input_size, hidden_size=100, output_size=1, learning_rate=0.01, epochs=1000):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.epochs = epochs

        # Initialize weights and biases
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * 0.01
        self.bias_hidden = np.zeros(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * 0.01
        self.bias_output = np.zeros(output_size)

    def fit(self, X, y):
        """
        Train the neural network on the provided data.
        """
        y = y.reshape(-1, 1)  # Ensure y is a column vector

        for epoch in range(self.epochs):
            # Forward pass
            hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
            hidden_output = sigmoid(hidden_input)
            output = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output

            # Compute the loss
            error = output - y
            loss = np.mean(error ** 2)  # Mean squared error loss

            # Backward pass
            dW_hidden_output = np.dot(hidden_output.T, error) / y.shape[0]
            db_output = np.sum(error, axis=0) / y.shape[0]
            hidden_error = np.dot(error, self.weights_hidden_output.T) * sigmoid_derivative(hidden_input)
            dW_input_hidden = np.dot(X.T, hidden_error) / y.shape[0]
            db_hidden = np.sum(hidden_error, axis=0) / y.shape[0]

            # Update weights and biases
            self.weights_hidden_output -= self.learning_rate * dW_hidden_output
            self.bias_output -= self.learning_rate * db_output
            self.weights_input_hidden -= self.learning_rate * dW_input_hidden
            self.bias_hidden -= self.learning_rate * db_hidden

            # Print loss every 100 epochs
            if epoch % 100 == 0:
                print(f"Epoch {epoch}/{self.epochs}, Loss: {loss:.4f}")

    def predict(self, X):
        """
        Predict regression targets for samples in X.
        """
        hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        hidden_output = sigmoid(hidden_input)
        output = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        return output
