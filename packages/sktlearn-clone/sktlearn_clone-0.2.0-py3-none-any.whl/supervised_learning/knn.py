import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Predictor import Predictor
import numpy as np

class KNNClassifier(Predictor):
    """
    k-Nearest Neighbors (KNN) classifier.

    Attributes:
    ----------
    k : int, default=5
        Number of neighbors to consider.

    Methods:
    --------
    __init__(k=5):
        Initialize KNN classifier with the number of neighbors.
    fit(X, y):
        Fit the model according to the given training data.
    predict(X):
        Predict the class labels for the provided data.
    """

    def __init__(self, k=5):
        """
        Initialize KNN classifier with the number of neighbors.

        Parameters:
        ----------
        k : int, default=5
            Number of neighbors to consider.
        """
        super().__init__()
        self.k = k
        self.X_train = None
        self.y_train = None

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
        self : KNNClassifier
            Fitted KNN classifier.
        """
        self.X_train = X
        self.y_train = y
        return self

    def predict(self, X):
        """
        Predict the class labels for the provided data.

        Parameters:
        ----------
        X : array-like, shape (n_samples, n_features)
            Data samples.

        Returns:
        -------
        y_pred : array-like, shape (n_samples,)
            Predicted class labels.
        """
        y_pred = []
        X = np.array(X)
        for sample in X:
            distances = np.sqrt(np.sum((self.X_train - sample)**2, axis=1))
            nearest_indices = np.argsort(distances)[:self.k]
            nearest_labels = self.y_train[nearest_indices]
            unique_labels, counts = np.unique(nearest_labels, return_counts=True)
            if len(unique_labels) == 1:
                y_pred.append(unique_labels[0])
            else:
                max_count_indices = np.where(counts == np.max(counts))[0]
                if len(max_count_indices) == 1:
                    y_pred.append(unique_labels[max_count_indices[0]])
                else:
                    # Break ties randomly
                    selected_index = np.random.choice(max_count_indices)
                    y_pred.append(unique_labels[selected_index])
        return np.array(y_pred)

