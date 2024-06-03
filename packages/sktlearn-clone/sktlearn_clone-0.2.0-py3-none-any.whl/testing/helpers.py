import pandas as pd
from sklearn.datasets import load_iris
import sys

# Add the path to your custom library
sys.path.append('C:\\Users\\Pc\\Downloads\\scikit-learn-clone')

# Load the HelperFunctions class
from utilities.helpers import HelperFunctions

# Load sample data
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['target'] = iris.target

# Use the split_features_labels method
X, y = HelperFunctions.split_features_labels(data, 'target')

# Print the results to verify
print("Features (X):")
print(X.head())

print("\nLabels (y):")
print(y.head())
