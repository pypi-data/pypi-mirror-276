# Testing/train_test_split.py
import sys
sys.path.append('C:\\Users\\Pc\\Downloads\\scikit-learn-clone')
# Testing/train_test_split.py
import unittest
import numpy as np
from model_selection.train_test_split import TrainTestSplitter
from sklearn.model_selection import train_test_split as sk_train_test_split

class TestSplitter(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.X = np.random.rand(100, 5)
        self.y = np.random.randint(0, 2, size=100)  # Binary target variable

    def test_splitter(self):
        splitter = TrainTestSplitter(test_size=0.25, random_state=0)
        X_train, X_test, y_train, y_test = splitter.split(self.X, self.y)

        sk_X_train, sk_X_test, sk_y_train, sk_y_test = sk_train_test_split(
            self.X, self.y, test_size=0.25, random_state=0)

        # Check if lengths are the same
        self.assertEqual(len(X_train), len(sk_X_train))
        self.assertEqual(len(X_test), len(sk_X_test))
        self.assertEqual(len(y_train), len(sk_y_train))
        self.assertEqual(len(y_test), len(sk_y_test))

if __name__ == '__main__':
    unittest.main()