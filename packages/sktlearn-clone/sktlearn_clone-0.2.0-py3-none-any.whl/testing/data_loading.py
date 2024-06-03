import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from utilities.data_loading import load_csv
from utilities.data_loading import load_csv_as_array
import pandas as pd





class TestDataLoading(unittest.TestCase):

    def test_load_csv(self):
        # Create a test CSV file
        test_data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
        test_df = pd.DataFrame(test_data)
        test_csv_path = 'test_load_csv.csv'
        test_df.to_csv(test_csv_path, index=False)

        # Test loading the CSV file
        loaded_df = load_csv(test_csv_path)
        self.assertTrue(isinstance(loaded_df, pd.DataFrame))
        self.assertEqual(len(loaded_df), 3)
        self.assertListEqual(list(loaded_df.columns), ['A', 'B'])

        # Clean up
        os.remove(test_csv_path)

    def test_load_csv_as_array(self):
        # Create a test CSV file
        test_data = '1,2,3\n4,5,6\n'
        test_csv_path = 'test_load_csv_as_array.csv'
        with open(test_csv_path, 'w') as f:
            f.write(test_data)

        # Test loading the CSV file as a NumPy array
        loaded_array = load_csv_as_array(test_csv_path)
        self.assertTrue(isinstance(loaded_array, np.ndarray))
        self.assertEqual(loaded_array.shape, (2, 3))
        self.assertTrue(np.array_equal(loaded_array, np.array([[1, 2, 3], [4, 5, 6]])))

        # Clean up
        os.remove(test_csv_path)

if __name__ == '__main__':
    unittest.main()
