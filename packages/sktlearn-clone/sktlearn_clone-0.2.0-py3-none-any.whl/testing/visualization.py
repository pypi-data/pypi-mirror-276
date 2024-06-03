import pandas as pd
from sklearn.datasets import load_iris
import sys
sys.path.append('C:\\Users\\Pc\\Downloads\\scikit-learn-clone')
# Load sample data
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['species'] = iris.target
from utilities.visualization import Visualization

# Visualization
viz = Visualization()

# Histogram
viz.plot_histogram(data, column='sepal length (cm)', bins=20, title='Sepal Length Distribution')

# Scatter Plot
viz.plot_scatter(data, x_col='sepal length (cm)', y_col='sepal width (cm)', hue_col='species', title='Sepal Length vs Width')

# Correlation Matrix
viz.plot_correlation_matrix(data.drop(columns=['species']), title='Correlation Matrix of Iris Features')

# Boxplot
viz.plot_boxplot(data, column='sepal length (cm)', by='species', title='Sepal Length by Species')

# Line Plot (just an example, not meaningful for iris dataset)
viz.plot_line(data, x_col='sepal length (cm)', y_col='sepal width (cm)', title='Sepal Length vs Width Line Plot')

# Pairplot
viz.plot_pairplot(data, hue='species', title='Pairplot of Iris Dataset')
