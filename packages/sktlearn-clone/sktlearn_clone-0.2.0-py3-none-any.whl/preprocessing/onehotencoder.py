from Transformer import Transformer
import numpy as np

class OneHotEncoder(Transformer):
    def __init__(self, feature_name_combiner=None):
        """
        Initialize the OneHotEncoder.

        Parameters:
        - handle_unknown: How to handle unknown categories ('error', 'ignore', 'impute').
        - drop: Whether to drop a category for each feature ('first', 'if_binary', None).
        - max_categories: Maximum number of categories to encode.
        - min_frequency: Minimum frequency for categories to be considered frequent.
        - feature_name_combiner: Custom function to combine feature names.
        """
        super().__init__()
        # TODO: include the commented attributes in the implementation
        # self.handle_unknown = handle_unknown
        # self.drop = drop
        # self.max_categories = max_categories
        # self.min_frequency = min_frequency
        self.feature_name_combiner = feature_name_combiner if feature_name_combiner is not None else self.default_feature_name_combiner

        self.categories_ = None
        # self.infrequent_categories_ = None
        self.feature_names_out_ = None

    def fit(self, X):
        """
        Fit the encoder to the data.

        Parameters:
        - X: Input data to fit.

        Returns:
        - self: Fitted encoder.
        """
        # Initialize categories_ and feature_names_out_ attributes
        self.categories_ = [np.unique(column) for column in X.T]
        self.feature_names_out_ = self.get_feature_names_out()

        return self

    def transform(self, X):
        """
        Transform input data into one-hot encoded format.

        Parameters:
        - X: Input data to transform.

        Returns:
        - X_encoded: Transformed data in one-hot encoded format.
        """
        # Initialize an empty array to store the encoded data
        X_encoded = np.zeros((X.shape[0], sum(len(categories) for categories in self.categories_)))

        # Iterate over each feature and encode it using one-hot encoding
        offset = 0
        for i, (column, categories) in enumerate(zip(X.T, self.categories_)):
            encoded = np.eye(len(categories))[np.searchsorted(categories, column)]
            X_encoded[:, offset:offset+len(categories)] = encoded
            offset += len(categories)

        return X_encoded

    def inverse_transform(self, X):
        """
        Convert one-hot encoded data back to its original form.

        Parameters:
        - X: One-hot encoded data to convert.

        Returns:
        - X_original: Original data before encoding.
        """
        # TODO: Implement inverse transformation logic here
        pass

    def get_feature_names_out(self):
        """
        Retrieve the feature names after encoding.

        Returns:
        - feature_names: Feature names after encoding.

        """
        feature_names = []
        for i, categories in enumerate(self.categories_):
            for category in categories:
                feature_names.append(self.feature_name_combiner(i, category))
        return feature_names

    def feature_name_combiner(self, feature, category):
        """
        Custom function to combine feature names.

        Parameters:
        - feature: Name of the feature.
        - category: Category of the feature.

        Returns:
        - combined_name: Combined feature name.
        """
        if self.feature_name_combiner:
            return self.feature_name_combiner(feature, category)
        else:
            return f'x{feature}_{category}'
        
    def default_feature_name_combiner(self, feature, category):
        return f'x{feature}_{category}'