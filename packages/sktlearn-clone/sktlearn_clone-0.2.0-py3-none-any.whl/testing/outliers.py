# Testing/test_outliers.py
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from preprocessing.outliers import detect_outliers
from sklearn.ensemble import IsolationForest

class TestOutliers(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.data = np.random.randn(100, 5)  # Generate random data with 5 features
    
    def test_outliers(self):
        outliers, outlier_indices = detect_outliers(self.data)
        
        # Using IsolationForest from scikit-learn to detect outliers
        iso_forest = IsolationForest(contamination=0.1, random_state=0)
        preds = iso_forest.fit_predict(self.data)
        
        # IsolationForest labels outliers as -1
        sk_outliers_indices = np.where(preds == -1)[0]

        # Print outliers indices for comparison
        print("Outlier indices from IQR method:", outlier_indices)
        print("Outlier indices from IsolationForest:", sk_outliers_indices)
        
        # Calculate the intersection of outlier indices
        intersection = np.intersect1d(outlier_indices[0], sk_outliers_indices)
        
        # Check for a reasonable overlap
        self.assertTrue(len(intersection) > 0, "No overlap in detected outliers")

if __name__ == '__main__':
    unittest.main()
