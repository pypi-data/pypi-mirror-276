#testgrid search 
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from sklearn.datasets import load_iris
from model_selection.train_test_split import TrainTestSplitter
from supervised_learning.knn import KNNClassifier
from metrics_model_evaluation.accuracy import accuracy_score
from model_selection.grid_search import GridSearchCV
from model_selection.kfold import KFold



# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target
# from sklearn.model_selection import KFold
kf = KFold(n_splits=3, shuffle=True, random_state=42)

# Split the dataset into training and test sets
splitter = TrainTestSplitter(random_state=42)
X_train, X_test, y_train, y_test = splitter.split(X, y)
# Define the parameter grid

param_grid = {
    'n_neighbors': [1, 3, 5, 7, 9],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

kf = KFold(n_splits=3, shuffle=True, random_state=42)
def accuracy_scorer(estimator, X, y):
    y_pred = estimator.predict(X)
    return accuracy_score(y, y_pred)

# Create an instance of your GridSearchCV class
grid_search = GridSearchCV(KNNClassifier(), param_grid, scoring=accuracy_scorer, cv=kf)
# Create an instance of your GridSearchCV class
# grid_search = GridSearchCV(KNNClassifier(), param_grid, scoring='accuracy', cv=kf)

# Perform the grid search
grid_search.fit(X_train, y_train)

# Get the best parameters and best score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

# Use the best estimator to make predictions
y_pred = grid_search.best_estimator_.predict(X_test)

# Calculate the accuracy of the best estimator on the test set
accuracy = accuracy_score(y_test, y_pred)

print("Best Parameters:", best_params)
print("Best Score:", best_score)
print("Test Set Accuracy:", accuracy)

