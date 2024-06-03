import numpy as np

class TrainTestSplitter:
    """
    Split the data into random train and test subsets.

    This implementation shuffles the data randomly and splits it into two portions,
    one for training and the other for testing.

    Attributes:
    ----------
    random_state : int or None, default=None
        Seed for the random number generator.

    Methods:
    --------
    split(X, y, test_size=0.2):
        Split the data into training and testing sets.

    """

    def __init__(self, test_size=0.2, random_state=None):
        """
        Initialize the DataSplitter.

        Parameters:
        ----------
        random_state : int or None, default=None
            Seed for the random number generator.
        """
        self.random_state = random_state
        self.test_size = test_size

    def split(self, X, y):
        """
        Split the data into training and testing sets.

        Parameters:
        ----------
        X : array-like of shape (n_samples, n_features)
            Features.
        y : array-like of shape (n_samples,)
            Target variable.
        test_size : float, default=0.2
            Proportion of the data to include in the test split.

        Returns:
        -------
        X_train : array-like of shape (n_train_samples, n_features)
            Features for training.
        X_test : array-like of shape (n_test_samples, n_features)
            Features for testing.
        y_train : array-like of shape (n_train_samples,)
            Target variable for training.
        y_test : array-like of shape (n_test_samples,)
            Target variable for testing.
        """
        if self.random_state:
            np.random.seed(self.random_state)

        n_samples = len(X)
        test_indices = np.random.choice(n_samples, size=int(self.test_size * n_samples), replace=False)
        train_indices = np.array([i for i in range(n_samples) if i not in test_indices])

        X_train = np.array([X[i] for i in train_indices])
        X_test = np.array([X[i] for i in test_indices])
        y_train = np.array([y[i] for i in train_indices])
        y_test = np.array([y[i] for i in test_indices])

        return X_train, X_test, y_train, y_test
    
