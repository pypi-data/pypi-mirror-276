from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from model_selection.train_test_split import TrainTestSplitter

from supervised_learning.LinearRegression import LinearRegression
from supervised_learning.LogisticRegression import LogisticRegression
from supervised_learning.knn import KNNClassifier
from supervised_learning.NaiveBayes import GaussianNB
from supervised_learning.DecisionTree import DecisionTreeClassifier
from supervised_learning.DecisionTree import DecisionTreeRegressor
# from supervised_learning.NeuralNetwork import NeuralNetworkClassifier
# from supervised_learning.NeuralNetwork import NeuralNetworkRegressor
from ensemble_methods.randomForest import RandomForestClassifier
from ensemble_methods.randomForest import RandomForestRegressor



from metrics_model_evaluation.accuracy import accuracy_score
from metrics_model_evaluation.precision import  precision_score
from metrics_model_evaluation.recall import recall_score
from metrics_model_evaluation.confusion_matrix import confusion_matrix
from metrics_model_evaluation.f1_score import f1_score
from metrics_model_evaluation.mean_absolute_error import mean_absolute_error
from metrics_model_evaluation.mean_squared_error import mean_squared_error
from metrics_model_evaluation.r2_score import r2_score
# from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score, mean_squared_error
# from sklearn.metrics import r2_score


# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
splitter = TrainTestSplitter(random_state=42)
X_train, X_test, y_train, y_test = splitter.split(X, y)
n = X.shape[1]
# Train your custom algorithms
linear_regression = LinearRegression()
linear_regression.fit(X_train, y_train)

logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, y_train)

knn = KNNClassifier()
knn.fit(X_train, y_train)

naive_bayes = GaussianNB()
naive_bayes.fit(X_train, y_train)
custom_classification_metrics ={}


decision_tree_classifier = DecisionTreeClassifier()
decision_tree_classifier.fit(X_train, y_train)

decision_tree_regressor = DecisionTreeRegressor()
decision_tree_regressor.fit(X_train, y_train)

# neural_network_classifier = NeuralNetworkClassifier(input_size=n)
# neural_network_classifier.fit(X_train, y_train)

# neural_network_regressor = NeuralNetworkRegressor(input_size=n)
# neural_network_regressor.fit(X_train, y_train)

random_forest_classifier = RandomForestClassifier()
random_forest_classifier.fit(X_train, y_train)

random_forest_regressor = RandomForestRegressor()
random_forest_regressor.fit(X_train, y_train)


# # Evaluate the performance of each algorithm

# custom_classification_metrics['linear_regression_metrics'] = {
#     'mse': mean_squared_error(y_test, linear_regression.predict(X_test)),
#     'r2_score': r2_score(y_test, linear_regression.predict(X_test))
# }
# custom_classification_metrics['logistic_regression_metrics'] = {
#     'accuracy': accuracy_score(y_test, logistic_regression.predict(X_test)),
#     'precision': precision_score(y_test, logistic_regression.predict(X_test)),
#     'recall': recall_score(y_test, logistic_regression.predict(X_test)),
#     'f1_score': f1_score(y_test, logistic_regression.predict(X_test))
# }
# custom_classification_metrics['knn_metrics'] = {
#     'accuracy': accuracy_score(y_test, knn.predict(X_test)),
#     'precision': precision_score(y_test, knn.predict(X_test)),
#     'recall': recall_score(y_test, knn.predict(X_test)),
#     'f1_score': f1_score(y_test, knn.predict(X_test))
# }
# custom_classification_metrics['naive_bayes_metrics'] = {
#     'accuracy': accuracy_score(y_test, naive_bayes.predict(X_test)),
#     'precision': precision_score(y_test, naive_bayes.predict(X_test)),
#     'recall': recall_score(y_test, naive_bayes.predict(X_test)),
#     'f1_score': f1_score(y_test, naive_bayes.predict(X_test))
# }


# print("\nCustom Classification Metrics:\
#     \nLinear Regression: {}\nLogistic Regression: {}\nKNN: {}\nNaive Bayes: {}".format(
#     custom_classification_metrics['linear_regression_metrics'],
#     custom_classification_metrics['logistic_regression_metrics'],
#     custom_classification_metrics['knn_metrics'],
#     custom_classification_metrics['naive_bayes_metrics']
# ))



# You can also test scikit-learn's implementations for comparison
from sklearn.linear_model import LinearRegression as SklearnLinearRegression
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.neighbors import KNeighborsClassifier as SklearnKNNClassifier
from sklearn.naive_bayes import GaussianNB as SklearnGaussianNB
from sklearn.tree import DecisionTreeClassifier as SklearnDecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor as SklearnDecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier as SklearnRandomForestClassifier
from sklearn.ensemble import RandomForestClassifier as SklearnRandomForestRegressor

# from sklearn.neural_network import mlpclassifier
# from sklearn.neural_network import mlpregressor



sklearn_linear_regression = SklearnLinearRegression()
sklearn_linear_regression.fit(X_train, y_train)

sklearn_logistic_regression = SklearnLogisticRegression()
sklearn_logistic_regression.fit(X_train, y_train)

sklearn_knn = SklearnKNNClassifier()
sklearn_knn.fit(X_train, y_train)

sklearn_naive_bayes = SklearnGaussianNB()
sklearn_naive_bayes.fit(X_train, y_train)

sklearn_decision_tree_classifier = SklearnDecisionTreeClassifier()
sklearn_decision_tree_classifier.fit(X_train, y_train)
sklearn_decision_tree_regressor = SklearnDecisionTreeRegressor()
sklearn_decision_tree_regressor.fit(X_train, y_train)

sklearn_random_forest_classifier = SklearnRandomForestClassifier()
sklearn_random_forest_classifier.fit(X_train, y_train)

sklearn_random_forest_regressor = SklearnRandomForestRegressor()
sklearn_random_forest_regressor.fit(X_train, y_train)

# sklearn_neural_network_classifier = mlpclassifier()
# sklearn_neural_network_classifier.fit(X_train, y_train)

# sklearn_neural_network_regressor = mlpregressor()
# sklearn_neural_network_regressor.fit(X_train, y_train)





sklearn_classification_metrics = {}


# # Evaluate scikit-learn's implementations
# sklearn_classification_metrics['Linear Regression'] = {
#     'mse': mean_squared_error(y_test, sklearn_linear_regression.predict(X_test)),
#     'r2_score': r2_score(y_test, sklearn_linear_regression.predict(X_test))
# }




# sklearn_classification_metrics['Logistic Regression'] = {
#     'accuracy': accuracy_score(y_test, sklearn_logistic_regression.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_logistic_regression.predict(X_test)),
#     'recall': recall_score(y_test, sklearn_logistic_regression.predict(X_test)),
#     'f1_score': f1_score(y_test, sklearn_logistic_regression.predict(X_test))
# }
# sklearn_classification_metrics['KNN'] = {
#     'accuracy': accuracy_score(y_test, sklearn_knn.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_knn.predict(X_test)),
#     'recall': recall_score(y_test, sklearn_knn.predict(X_test)),
#     'f1_score': f1_score(y_test, sklearn_knn.predict(X_test))
# }
# sklearn_classification_metrics['Naive Bayes'] = {
#     'accuracy': accuracy_score(y_test, sklearn_naive_bayes.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_naive_bayes.predict(X_test)),
#     'recall': recall_score(y_test, sklearn_naive_bayes.predict(X_test)),
#     'f1_score': f1_score(y_test, sklearn_naive_bayes.predict(X_test))
# }
# sklearn_classification_metrics['Decision Tree'] = {
#     'accuracy': accuracy_score(y_test, sklearn_decision_tree.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_decision_tree.predict(X_test)),
#     'recall': recall_score(y_test, sklearn_decision_tree.predict(X_test)),
#     'f1_score': f1_score(y_test, sklearn_decision_tree.predict(X_test))
# }
# print("\nSklearn Classification Metrics:\
#     \nLinear Regression: {} \nLogistic Regression: {}\nKNN: {}\nNaive Bayes: {}\nDecision Tree: {}".format(
#     sklearn_classification_metrics['Linear Regression'],
#     sklearn_classification_metrics['Logistic Regression'],
#     sklearn_classification_metrics['KNN'],
#     sklearn_classification_metrics['Naive Bayes'],
#     sklearn_classification_metrics['Decision Tree']

# ))



# custom_classification_metrics['linear_regression_metrics'] = {
#     'mse': mean_squared_error(y_test, linear_regression.predict(X_test)),
#     'r2_score': r2_score(y_test, linear_regression.predict(X_test))
# }
# custom_classification_metrics['logistic_regression_metrics'] = {
#     'accuracy': accuracy_score(y_test, logistic_regression.predict(X_test)),
#     'precision': precision_score(y_test, logistic_regression.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, logistic_regression.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, logistic_regression.predict(X_test), average='macro')
# }
# custom_classification_metrics['knn_metrics'] = {
#     'accuracy': accuracy_score(y_test, knn.predict(X_test)),
#     'precision': precision_score(y_test, knn.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, knn.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, knn.predict(X_test), average='macro')
# }
# custom_classification_metrics['naive_bayes_metrics'] = {
#     'accuracy': accuracy_score(y_test, naive_bayes.predict(X_test)),
#     'precision': precision_score(y_test, naive_bayes.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, naive_bayes.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, naive_bayes.predict(X_test), average='macro')
# }
# custom_classification_metrics['decision_tree_metrics_classifier'] = {
#     'accuracy': accuracy_score(y_test, decision_tree_classifier.predict(X_test)),
#     'precision': precision_score(y_test, decision_tree_classifier.predict(X_test), average='macro'),
#     'recall': recall_score(y_test, decision_tree_classifier.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, decision_tree_classifier.predict(X_test), average='macro')
# }
# custom_classification_metrics['decision_tree_metrics_regressor'] = {
#     'mse': mean_squared_error(y_test, decision_tree_regressor.predict(X_test)),
#     'r2_score': r2_score(y_test, decision_tree_regressor.predict(X_test))
# }

# custom_classification_metrics['random_forest_classifier'] = {
#     'accuracy': accuracy_score(y_test, random_forest_classifier.predict(X_test)),
#     'precision': precision_score(y_test, random_forest_classifier.predict(X_test), average='macro'),
#     'recall': recall_score(y_test, random_forest_classifier.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, random_forest_classifier.predict(X_test), average='macro')
# }
# custom_classification_metrics['random_forest_regressor'] = {
#     'mse': mean_squared_error(y_test, random_forest_regressor.predict(X_test)),
#     'r2_score': r2_score(y_test, random_forest_regressor.predict(X_test))
# }




custom_classification_metrics['linear_regression_metrics'] = {
    'mse': mean_squared_error(y_test, linear_regression.predict(X_test)),
    'r2_score': r2_score(y_test, linear_regression.predict(X_test))
}
custom_classification_metrics['logistic_regression_metrics'] = {
    'accuracy': accuracy_score(y_test, logistic_regression.predict(X_test)),
    'precision': precision_score(y_test, logistic_regression.predict(X_test)),
    'recall': recall_score(y_test, logistic_regression.predict(X_test)),
    'f1_score': f1_score(y_test, logistic_regression.predict(X_test))
}
custom_classification_metrics['knn_metrics'] = {
    'accuracy': accuracy_score(y_test, knn.predict(X_test)),
    'precision': precision_score(y_test, knn.predict(X_test)),
    'recall': recall_score(y_test, knn.predict(X_test)),
    'f1_score': f1_score(y_test, knn.predict(X_test) )
}
custom_classification_metrics['naive_bayes_metrics'] = {
    'accuracy': accuracy_score(y_test, naive_bayes.predict(X_test)),
    'precision': precision_score(y_test, naive_bayes.predict(X_test)),
    'recall': recall_score(y_test, naive_bayes.predict(X_test), ),
    'f1_score': f1_score(y_test, naive_bayes.predict(X_test), )
}
custom_classification_metrics['decision_tree_metrics_classifier'] = {
    'accuracy': accuracy_score(y_test, decision_tree_classifier.predict(X_test)),
    'precision': precision_score(y_test, decision_tree_classifier.predict(X_test), ),
    'recall': recall_score(y_test, decision_tree_classifier.predict(X_test), ),
    'f1_score': f1_score(y_test, decision_tree_classifier.predict(X_test), )
}
custom_classification_metrics['decision_tree_metrics_regressor'] = {
    'mse': mean_squared_error(y_test, decision_tree_regressor.predict(X_test)),
    'r2_score': r2_score(y_test, decision_tree_regressor.predict(X_test))
}

custom_classification_metrics['random_forest_classifier'] = {
    'accuracy': accuracy_score(y_test, random_forest_classifier.predict(X_test)),
    'precision': precision_score(y_test, random_forest_classifier.predict(X_test)),
    'recall': recall_score(y_test, random_forest_classifier.predict(X_test)),
    'f1_score': f1_score(y_test, random_forest_classifier.predict(X_test))
}
custom_classification_metrics['random_forest_regressor'] = {
    'mse': mean_squared_error(y_test, random_forest_regressor.predict(X_test)),
    'r2_score': r2_score(y_test, random_forest_regressor.predict(X_test))
}





# custom_classification_metrics['neual network regressor']={
#     'mse': mean_squared_error(y_test, neural_network_regressor.predict(X_test)),
#     'r2_score': r2_score(y_test, neural_network_regressor.predict(X_test))
# }
# custom_classification_metrics['neural network classifier']={
#     'accuracy': accuracy_score(y_test, neural_network_classifier.predict(X_test)),
#     'precision': precision_score(y_test, neural_network_classifier.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, neural_network_classifier.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, neural_network_classifier.predict(X_test), average='macro')
# }
# \nNN regressor: {} \nNN classfier: {}
print("\nCustom Classification Metrics:\
    \nLinear Regression: {}\nLogistic Regression: {}\nKNN: {}\nNaive Bayes: {}\nDecision tree classifier: {}\nDecision tree regressor: {}\nRandom forest classifer: {}\nRandom forest regressor: {}".format(
    custom_classification_metrics['linear_regression_metrics'],
    custom_classification_metrics['logistic_regression_metrics'],
    custom_classification_metrics['knn_metrics'],
    custom_classification_metrics['naive_bayes_metrics'],
    custom_classification_metrics['decision_tree_metrics_classifier'],
    custom_classification_metrics['decision_tree_metrics_regressor'],
    custom_classification_metrics['random_forest_classifier'],
    custom_classification_metrics['random_forest_regressor']
    # custom_classification_metrics['neual network regressor'],
    # custom_classification_metrics['neural network classifier']

))



sklearn_classification_metrics = {}



sklearn_classification_metrics['Linear Regression'] = {
    'mse': mean_squared_error(y_test, sklearn_linear_regression.predict(X_test)),
    'r2_score': r2_score(y_test, sklearn_linear_regression.predict(X_test))
}

sklearn_classification_metrics['Logistic Regression'] = {
    'accuracy': accuracy_score(y_test, sklearn_logistic_regression.predict(X_test)),
    'precision': precision_score(y_test, sklearn_logistic_regression.predict(X_test)),
    'recall': recall_score(y_test, sklearn_logistic_regression.predict(X_test)),
    'f1_score': f1_score(y_test, sklearn_logistic_regression.predict(X_test) )
}
sklearn_classification_metrics['KNN'] = {
    'accuracy': accuracy_score(y_test, sklearn_knn.predict(X_test)),
    'precision': precision_score(y_test, sklearn_knn.predict(X_test)),
    'recall': recall_score(y_test, sklearn_knn.predict(X_test), ),
    'f1_score': f1_score(y_test, sklearn_knn.predict(X_test), )
}
sklearn_classification_metrics['Naive Bayes'] = {
    'accuracy': accuracy_score(y_test, sklearn_naive_bayes.predict(X_test)),
    'precision': precision_score(y_test, sklearn_naive_bayes.predict(X_test)),
    'recall': recall_score(y_test, sklearn_naive_bayes.predict(X_test)),
    'f1_score': f1_score(y_test, sklearn_naive_bayes.predict(X_test))
}
sklearn_classification_metrics['Decision Tree classifier'] = {
    'accuracy': accuracy_score(y_test, sklearn_decision_tree_classifier.predict(X_test)),
    'precision': precision_score(y_test, sklearn_decision_tree_classifier.predict(X_test)),
    'recall': recall_score(y_test, sklearn_decision_tree_classifier.predict(X_test)),
    'f1_score': f1_score(y_test, sklearn_decision_tree_classifier.predict(X_test))
}
sklearn_classification_metrics['Decision Tree regressor'] = {
    'mse': mean_squared_error(y_test, sklearn_decision_tree_regressor.predict(X_test)),
    'r2_score': r2_score(y_test, sklearn_decision_tree_regressor.predict(X_test))
}

sklearn_classification_metrics['Random Forest classifier'] = {
    'accuracy': accuracy_score(y_test, sklearn_random_forest_classifier.predict(X_test)),
    'precision': precision_score(y_test, sklearn_random_forest_classifier.predict(X_test)),
    'recall': recall_score(y_test, sklearn_random_forest_classifier.predict(X_test)),
    'f1_score': f1_score(y_test, sklearn_random_forest_classifier.predict(X_test))
}
sklearn_classification_metrics['Random Forest regressor'] = {
    'mse': mean_squared_error(y_test, sklearn_random_forest_regressor.predict(X_test)),
    'r2_score': r2_score(y_test, sklearn_random_forest_regressor.predict(X_test))
}



# sklearn_classification_metrics['Linear Regression'] = {
#     'mse': mean_squared_error(y_test, sklearn_linear_regression.predict(X_test)),
#     'r2_score': r2_score(y_test, sklearn_linear_regression.predict(X_test))
# }

# sklearn_classification_metrics['Logistic Regression'] = {
#     'accuracy': accuracy_score(y_test, sklearn_logistic_regression.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_logistic_regression.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, sklearn_logistic_regression.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, sklearn_logistic_regression.predict(X_test), average='macro')
# }
# sklearn_classification_metrics['KNN'] = {
#     'accuracy': accuracy_score(y_test, sklearn_knn.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_knn.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, sklearn_knn.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, sklearn_knn.predict(X_test), average='macro')
# }
# sklearn_classification_metrics['Naive Bayes'] = {
#     'accuracy': accuracy_score(y_test, sklearn_naive_bayes.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_naive_bayes.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, sklearn_naive_bayes.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, sklearn_naive_bayes.predict(X_test), average='macro')
# }
# sklearn_classification_metrics['Decision Tree classifier'] = {
#     'accuracy': accuracy_score(y_test, sklearn_decision_tree_classifier.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_decision_tree_classifier.predict(X_test), average='macro'),
#     'recall': recall_score(y_test, sklearn_decision_tree_classifier.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, sklearn_decision_tree_classifier.predict(X_test), average='macro')
# }
# sklearn_classification_metrics['Decision Tree regressor'] = {
#     'mse': mean_squared_error(y_test, sklearn_decision_tree_regressor.predict(X_test)),
#     'r2_score': r2_score(y_test, sklearn_decision_tree_regressor.predict(X_test))
# }

# sklearn_classification_metrics['Random Forest classifier'] = {
#     'accuracy': accuracy_score(y_test, sklearn_random_forest_classifier.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_random_forest_classifier.predict(X_test), average='macro'),
#     'recall': recall_score(y_test, sklearn_random_forest_classifier.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, sklearn_random_forest_classifier.predict(X_test), average='macro')
# }
# sklearn_classification_metrics['Random Forest regressor'] = {
#     'mse': mean_squared_error(y_test, sklearn_random_forest_regressor.predict(X_test)),
#     'r2_score': r2_score(y_test, sklearn_random_forest_regressor.predict(X_test))
# }




# sklearn_classification_metrics['Neural Network Regressor'] = {
#     'mse': mean_squared_error(y_test, sklearn_neural_network_regressor.predict(X_test)),
#     'r2_score': r2_score(y_test, sklearn_neural_network_regressor.predict(X_test))
# }

# sklearn_classification_metrics['Neural Network Classifier'] = {
#     'accuracy': accuracy_score(y_test, sklearn_neural_network_classifier.predict(X_test)),
#     'precision': precision_score(y_test, sklearn_neural_network_classifier.predict(X_test), average='macro', zero_division=1),
#     'recall': recall_score(y_test, sklearn_neural_network_classifier.predict(X_test), average='macro'),
#     'f1_score': f1_score(y_test, sklearn_neural_network_classifier.predict(X_test), average='macro')
# }
# \nNN regressor: {} \nNN classfier: {}
print("\nSklearn Classification Metrics with Macro Average:\
    \nLinear Regression: {} \nLogistic Regression: {}\nKNN: {}\nNaive Bayes: {}\nDecision Tree classifier: {}\nDecision Tree regressor: {}\nRandom forest classifier: {}\nRandom forest regressor: {}".format(
    sklearn_classification_metrics['Linear Regression'],
    sklearn_classification_metrics['Logistic Regression'],
    sklearn_classification_metrics['KNN'],
    sklearn_classification_metrics['Naive Bayes'],
    sklearn_classification_metrics['Decision Tree classifier'],
    sklearn_classification_metrics['Decision Tree regressor'],
    sklearn_classification_metrics['Random Forest classifier'],
    sklearn_classification_metrics['Random Forest regressor']
    # sklearn_classification_metrics['Neural Network Regressor'],
    # sklearn_classification_metrics['Neural Network Classifier']
))