import pandas as pd

class ColumnClassifier:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.numerical_columns = self.get_numerical_columns()
        self.categorical_columns = self.get_categorical_columns()

    def get_numerical_columns(self):
        return self.dataframe.select_dtypes(include=['number']).columns.tolist()

    def get_categorical_columns(self):
        return self.dataframe.select_dtypes(include=['object']).columns.tolist()