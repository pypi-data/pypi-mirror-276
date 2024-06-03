# Testing/test_param_grid.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from model_selection.param_grid import ParameterGrid
import sklearn.model_selection 



class TestParameterGrid(unittest.TestCase):
    def test_parameter_grid_iteration(self):
        param_grid = {
            'a': [1, 2, 3],
            'b': ['x', 'y'],
            'c': [0.1, 0.2]
        }
        custom_grid = ParameterGrid(param_grid)
        sklearn_grid = sklearn.model_selection.ParameterGrid(param_grid)

        custom_params_list = list(custom_grid)
        sklearn_params_list = list(sklearn_grid)

        # Check the number of parameter combinations
        self.assertEqual(len(custom_params_list), len(sklearn_params_list))

        # Check each parameter combination
        for idx, (custom_params, sklearn_params) in enumerate(zip(custom_params_list, sklearn_params_list)):
            # print(f"Custom params {idx}: {custom_params}")
            # print(f"Sklearn params {idx}: {sklearn_params}")
            for key in param_grid.keys():
                self.assertEqual(custom_params[key], sklearn_params[key])


    def test_parameter_grid_length(self):
        param_grid = {
            'a': [1, 2, 3],
            'b': ['x', 'y'],
            'c': [0.1, 0.2]
        }
        custom_grid = ParameterGrid(param_grid)
        sklearn_grid = sklearn.model_selection.ParameterGrid(param_grid)

        self.assertEqual(len(custom_grid), len(sklearn_grid))

if __name__ == '__main__':
    unittest.main()
