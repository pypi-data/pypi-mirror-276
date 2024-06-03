import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import numpy as np
import pandas as pd

from preprocessing.impute_missing_values_mean import impute_missing_values_mean
from preprocessing.impute_missing_values_median import impute_missing_values_median
from preprocessing.impute_missing_values_mode import impute_missing_values_mode
from preprocessing.onehotencoder import OneHotEncoder
from preprocessing.labelencoder import LabelEncoder
from preprocessing.normalize_features import normalize_features
from preprocessing.scale_features_min_max import scale_features
from preprocessing.scale_features_standard import scale_features
from preprocessing.select_features import select_features
from utilities.data_loading import load_csv
from preprocessing.outliers import detect_outliers
from preprocessing.numerical_categorical_variables import ColumnClassifier


# Specify the full path to the dataset file
# dataset_path = os.path.join(project_root, 'data', 'titanic_fare.csv')

# titanic_data = pd.read_csv(dataset_path)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dataset_path = os.path.join(project_root, 'data', 'titanic_fare.csv')

titanic_data = load_csv(dataset_path)
# Look for missing values in numeric columns
numeric_columns = titanic_data.select_dtypes(include=[np.number]).columns
print(titanic_data[numeric_columns].isnull().sum())

#impute missing values using mean
# titanic_data[numeric_columns] = impute_missing_values_mean(titanic_data[numeric_columns])
# print(titanic_data[numeric_columns].isnull().sum())

# #impute missing values using median
titanic_data[numeric_columns] = impute_missing_values_median(titanic_data[numeric_columns])
print(titanic_data[numeric_columns].isnull().sum())

#one hot encoder
categorical_columns = titanic_data.select_dtypes(include=[object]).columns


#label encoder

y = titanic_data['sex']

# Initialize and fit the encoder
label_encoder = LabelEncoder()
label_encoder.fit(y)

# Transform the labels
y_encoded = label_encoder.transform(y)
print("Encoded Labels:")
print(y_encoded)

# Inverse transform the labels
y_original = label_encoder.inverse_transform(y_encoded)
print("Original Labels:")
print(y_original)
#normalize features

X = titanic_data[['age', 'fare']]

# Normalize the features
X_normalized = normalize_features(X)
print("Normalized Features:")
print(X_normalized)





#select features
X = titanic_data[['age', 'fare']].to_numpy()
y = titanic_data['survived'].to_numpy()

# Select the top k=1 features based on correlation with y
X_selected = select_features(X, y)
print("Selected Features:")
print(X_selected)


