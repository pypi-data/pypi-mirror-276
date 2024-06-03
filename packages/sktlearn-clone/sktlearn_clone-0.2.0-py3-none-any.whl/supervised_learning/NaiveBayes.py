import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Predictor import Predictor
import numpy as np

class GaussianNB(Predictor):
    """
    Gaussian Naive Bayes classifier.

    Attributes:
    ----------
    None

    Methods:
    --------
    __init__(priors=None, var_smoothing=1e-09):
        Initialize Gaussian Naive Bayes classifier.
    fit(X, y):
        Fit the model according to the given training data.
    predict(X):
        Predict the class labels for the provided data.
    """
    def __init__(self, priors=None, var_smoothing=1e-09):
        """
        Initialize Gaussian Naive Bayes classifier.

        Parameters:
        ----------
        priors : array-like of shape (n_classes,), default=None
            Prior probabilities of the classes.
        var_smoothing : float, default=1e-9
            Portion of the largest variance of all features that is added to variances for calculation stability.
        """
        super().__init__()
        self.priors = priors
        self.var_smoothing = var_smoothing
        self.class_count = None
        self.class_prior = None
        self.classes = None
        self.epsilon = None
        self.n_features_in_ = None
        self.feature_names_in_ = None
        self.var = None
        self.theta = None

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
        self : GaussianNB
            Fitted Gaussian Naive Bayes classifier.
        """
        self.classes, y = np.unique(y, return_inverse=True)
        self.class_count = np.bincount(y)
        if self.priors is None:
            self.class_prior = self.class_count / len(y)
        else:
            self.class_prior = np.asarray(self.priors)
        self.epsilon = self.var_smoothing * np.var(X, axis=0).max()
        self.n_features_in_ = X.shape[1]
        self.feature_names_in_ = np.array(range(self.n_features_in_))
        self.var = []
        self.theta = []
        for i in range(len(self.classes)):
            X_class = X[y == i, :]
            self.var.append(self.epsilon + np.var(X_class, axis=0))
            self.theta.append(np.mean(X_class, axis=0))
        return self

    def _joint_log_likelihood(self, X):
        """
        Compute the unnormalized posterior log probability of X.

        Parameters:
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns:
        -------
        jll : array-like, shape (n_samples, n_classes)
            The unnormalized log posterior probabilities of the samples.
        """
        joint_log_likelihood = []
        for i in range(len(self.classes)):
            jointi = np.log(self.class_prior[i])
            n_ij = - 0.5 * np.sum(np.log(2. * np.pi * self.var[i]))
            n_ij -= 0.5 * np.sum(((X - self.theta[i]) ** 2) /
                                  (self.var[i]), 1)
            joint_log_likelihood.append(jointi + n_ij)

        return np.array(joint_log_likelihood).T

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
        jll = self._joint_log_likelihood(X)
        return self.classes[np.argmax(jll, axis=1)]
