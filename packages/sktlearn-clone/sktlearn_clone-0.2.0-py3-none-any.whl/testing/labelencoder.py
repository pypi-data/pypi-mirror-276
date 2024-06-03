
# Testing/test_labelencoder.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from preprocessing.labelencoder import LabelEncoder


class TestLabelEncoder(unittest.TestCase):

    def test_fit_transform(self):
        y = np.array(['a', 'b', 'a', 'c', 'b'])
        encoder = LabelEncoder()
        encoder.fit(y)
        y_encoded = encoder.transform(y)

        self.assertTrue(np.array_equal(y_encoded, np.array([0, 1, 0, 2, 1])))

    def test_inverse_transform(self):
        y_encoded = np.array([0, 1, 0, 2, 1])
        encoder = LabelEncoder()
        encoder.classes_ = np.array(['a', 'b', 'c'])
        y_original = encoder.inverse_transform(y_encoded)

        self.assertTrue(np.array_equal(y_original, np.array(['a', 'b', 'a', 'c', 'b'])))

if __name__ == '__main__':
    unittest.main()