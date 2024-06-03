# Testing/test_kfold.py

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import unittest
import numpy as np
from model_selection import KFold

class TestKFold(unittest.TestCase):
    def test_split(self):
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        kf = KFold(n_splits=2, shuffle=False)
        
        train_indices_list = []
        test_indices_list = []
        for train_index, test_index in kf.split(X):
            train_indices_list.append(train_index)
            test_indices_list.append(test_index)

        self.assertEqual(len(train_indices_list), 2)
        self.assertEqual(len(test_indices_list), 2)

        # Check if indices are valid and cover all data points
        train_indices_concat = np.concatenate(train_indices_list)
        test_indices_concat = np.concatenate(test_indices_list)
        self.assertEqual(len(train_indices_concat), len(X))
        self.assertEqual(len(test_indices_concat), len(X))
        self.assertTrue(np.array_equal(np.sort(train_indices_concat), np.arange(len(X))))
        self.assertTrue(np.array_equal(np.sort(test_indices_concat), np.arange(len(X))))

        # Check if train/test indices are disjoint
        for train_index, test_index in zip(train_indices_list, test_indices_list):
            intersection = np.intersect1d(train_index, test_index)
            self.assertEqual(len(intersection), 0)

if __name__ == '__main__':
    unittest.main()
