import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Predictor import Predictor
import numpy as np

class LinearRegression(Predictor):
    """
    Linear regression predictor.

    Attributes:
    ----------
    learning_rate : float, default=0.01
        Learning rate for gradient descent.
    n_iterations : int, default=1000
        Number of iterations for gradient descent.
    regularization : {'l1', 'l2', None}, default=None
        Type of regularization to apply. If None, no regularization is applied.
    reg_strength : float, default=0.01
        Regularization strength parameter.

    Methods:
    --------
    __init__(learning_rate=0.01, n_iterations=1000, regularization=None, reg_strength=0.01):
        Initialize linear regression predictor.
    fit(X, y):
        Fit the model according to the given training data.
    predict(X):
        Predict the target for the provided data.
    score(X, y):
        Return the coefficient of determination R^2 of the prediction.
    """

    def __init__(self, learning_rate=0.01, n_iterations=1000, regularization=None, reg_strength=0.01):
        """
        Initialize linear regression predictor.

        Parameters:
        ----------
        learning_rate : float, default=0.01
            Learning rate for gradient descent.
        n_iterations : int, default=1000
            Number of iterations for gradient descent.
        regularization : {'l1', 'l2', None}, default=None
            Type of regularization to apply. If None, no regularization is applied.
        reg_strength : float, default=0.01
            Regularization strength parameter.
        """
        super().__init__()
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
        self.regularization = regularization
        self.reg_strength = reg_strength
    
    def fit(self, X, y):
        """
        Fit the model according to the given training data.

        Parameters:
        ----------
        X : array-like, shape (n_samples, n_features)
            Training samples.
        y : array-like, shape (n_samples,)
            Target values.

        Returns:
        -------
        self : LinearRegression
            Fitted linear regression predictor.
        """
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iterations):
            model = np.dot(X, self.weights) + self.bias
            dw = (1 / n_samples) * np.dot(X.T, (model - y))
            db = (1 / n_samples) * np.sum(model - y)
            
            if self.regularization == 'l1':
                dw += self.reg_strength * np.sign(self.weights)
            elif self.regularization == 'l2':
                dw += self.reg_strength * self.weights
            
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
        
        return self
    
    def predict(self, X):
        """
        Predict the target for the provided data.

        Parameters:
        ----------
        X : array-like, shape (n_samples, n_features)
            Data samples.

        Returns:
        -------
        y_pred : array-like, shape (n_samples,)
            Predicted targets.
        """
        return np.dot(X, self.weights) + self.bias
    
