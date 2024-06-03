# Testing/test_numerical_categorical_variables.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
import pandas as pd
from preprocessing.numerical_categorical_variables  import ColumnClassifier

class TestNumericalCategoricalVariables(unittest.TestCase):
    def setUp(self):
        data = {
            'A': [1, 2, 3, 4],
            'B': ['a', 'b', 'c', 'd'],
            'C': [1.1, 2.2, 3.3, 4.4],
            'D': ['x', 'y', 'z', 'w']
        }
        self.df = pd.DataFrame(data)
        self.classifier = ColumnClassifier(self.df)

    def test_numerical_columns(self):
        expected_numerical_columns = ['A', 'C']
        self.assertListEqual(self.classifier.numerical_columns, expected_numerical_columns)

    def test_categorical_columns(self):
        expected_categorical_columns = ['B', 'D']
        self.assertListEqual(self.classifier.categorical_columns, expected_categorical_columns)

if __name__ == '__main__':
    unittest.main()
