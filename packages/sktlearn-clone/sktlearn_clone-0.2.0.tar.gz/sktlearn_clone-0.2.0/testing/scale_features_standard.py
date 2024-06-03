# Testing/test_scale_features_standard.py
import sys
sys.path.append('C:\\Users\\Pc\\Downloads\\scikit-learn-clone')
import unittest
import numpy as np
from preprocessing.scale_features_standard import scale_features


from sklearn.preprocessing import StandardScaler

class TestScaleFeatures(unittest.TestCase):
    def test_scale_features(self):
        X = np.array([[1, 2], [3, 4], [5, 6]])
        # Your scale_features function
        X_scaled_custom = scale_features(X)
        # Scikit-learn's MinMaxScaler
        scaler = StandardScaler()
        X_scaled_sklearn = scaler.fit_transform(X)

        # Compare the results
        np.testing.assert_array_almost_equal(X_scaled_custom, X_scaled_sklearn)

if __name__ == '__main__':
    unittest.main()
