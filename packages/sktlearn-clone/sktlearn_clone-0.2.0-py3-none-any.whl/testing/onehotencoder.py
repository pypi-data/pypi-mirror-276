import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import unittest
import numpy as np
from preprocessing.onehotencoder import OneHotEncoder

class TestOneHotEncoder(unittest.TestCase):
    def test_fit_transform(self):
        # Sample input data
        X = np.array([[1, 2, 1],
                       [3, 1, 2],
                       [2, 2, 3],
                       [1, 3, 2]])

        # Initialize encoder
        encoder = OneHotEncoder()
        
        # Fit and transform data
        encoder.fit(X)
        X_encoded = encoder.transform(X)

        # Check if the transformation is correct
        expected_output = np.array([[1., 0., 0., 0., 1., 0., 1., 0., 0.],
                             [0., 0., 1., 1., 0., 0., 0., 1., 0.],
                             [0., 1., 0., 0., 1., 0., 0., 0., 1.],
                             [1., 0., 0., 0., 0., 1., 0., 1., 0.]])
        np.testing.assert_array_equal(X_encoded, expected_output)

if __name__ == '__main__':
    unittest.main()
