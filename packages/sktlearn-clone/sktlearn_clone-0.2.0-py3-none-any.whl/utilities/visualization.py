import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Visualization:
    @staticmethod
    def plot_histogram(data, column, bins=30, title=None, xlabel=None, ylabel='Frequency'):
        """
        Plot a histogram for a specified column in the data.
        """
        plt.figure(figsize=(10, 6))
        plt.hist(data[column], bins=bins, edgecolor='k', alpha=0.7)
        plt.title(title if title else f'Histogram of {column}')
        plt.xlabel(xlabel if xlabel else column)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def plot_scatter(data, x_col, y_col, hue_col=None, title=None, xlabel=None, ylabel=None):
        """
        Plot a scatter plot for specified columns in the data.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=data[x_col], y=data[y_col], hue=data[hue_col] if hue_col else None)
        plt.title(title if title else f'Scatter plot of {x_col} vs {y_col}')
        plt.xlabel(xlabel if xlabel else x_col)
        plt.ylabel(ylabel if ylabel else y_col)
        plt.show()

    @staticmethod
    def plot_correlation_matrix(data, title='Correlation Matrix', cmap='coolwarm', annot=True):
        """
        Plot a correlation matrix for the data.
        """
        plt.figure(figsize=(12, 8))
        corr_matrix = data.corr()
        sns.heatmap(corr_matrix, annot=annot, cmap=cmap, center=0)
        plt.title(title)
        plt.show()

    @staticmethod
    def plot_boxplot(data, column, by=None, title=None, xlabel=None, ylabel=None):
        """
        Plot a boxplot for a specified column in the data.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=data[by] if by else None, y=data[column])
        plt.title(title if title else f'Boxplot of {column}')
        plt.xlabel(xlabel if xlabel else by if by else '')
        plt.ylabel(ylabel if ylabel else column)
        plt.show()

    @staticmethod
    def plot_line(data, x_col, y_col, title=None, xlabel=None, ylabel=None):
        """
        Plot a line chart for specified columns in the data.
        """
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=data[x_col], y=data[y_col])
        plt.title(title if title else f'Line plot of {x_col} vs {y_col}')
        plt.xlabel(xlabel if xlabel else x_col)
        plt.ylabel(ylabel if ylabel else y_col)
        plt.show()

    @staticmethod
    def plot_pairplot(data, hue=None, title=None):
        """
        Plot a pairplot for the data.
        """
        pairplot = sns.pairplot(data, hue=hue)
        plt.title(title if title else 'Pairplot')
        pairplot.fig.suptitle(title if title else 'Pairplot', y=1.02)  # Adjust the title position
        plt.show()
