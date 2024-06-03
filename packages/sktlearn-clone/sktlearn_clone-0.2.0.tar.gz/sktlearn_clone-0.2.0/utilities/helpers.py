class HelperFunctions:
    @staticmethod
    def split_features_labels(data, target_column):
        """
        Split the DataFrame into features and labels.
        """
        X = data.drop(columns=[target_column])
        y = data[target_column]
        return X, y