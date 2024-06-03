
from Transformer import Transformer
import numpy as np

class LabelEncoder(Transformer):
    def __init__(self):
        super().__init__()
        self.classes_ = None

    def fit(self, y):
        """
        Fit the encoder to the target labels.

        Parameters:
        - y: Target labels to fit.

        Returns:
        - self: Fitted encoder.
        """
        self.classes_ = np.unique(y)
        return self


    def transform(self, y):
        """
        Transform target labels into encoded format.

        Parameters:
        - y: Target labels to transform.

        Returns:
        - y_encoded: Transformed labels.
        """
        if self.classes_ is None:
            raise ValueError("fit method must be called before transform")

        # Sort unique classes and use np.searchsorted to map labels to their indices
        sorted_classes = np.sort(self.classes_)
        y_encoded = np.searchsorted(sorted_classes, y)
        return y_encoded
    

    def inverse_transform(self, y):
        """
        Convert encoded labels back to original format.

        Parameters:
        - y: Encoded labels to convert.

        Returns:
        - y_original: Original labels before encoding.
        """
        if self.classes_ is None:
            raise ValueError("fit method must be called before inverse_transform")

        # Inverse transform using the original classes
        y_original = self.classes_[y]
        return y_original
