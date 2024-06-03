import numpy as np
import pandas as pd
from collections import defaultdict

class Transformer:
    """Base class for all transformers."""
    def fit(self, X, y=None):
        """
        Fits the transformer on the data.

        Parameters:
            X (array-like): Input data.
            y (array-like, optional): Target data.

        Returns:
            self: Returns the instance itself.
        """
        raise NotImplementedError
    
    def transform(self, X):
        """
        Transforms the data.

        Parameters:
            X (array-like): Input data.

        Returns:
            array-like: Transformed data.
        """
        raise NotImplementedError
    
    def fit_transform(self, X, y=None):
        """
        Fits the transformer and then transforms the data.

        Parameters:
            X (array-like): Input data.
            y (array-like, optional): Target data.

        Returns:
            array-like: Transformed data.
        """
        self.fit(X, y)
        return self.transform(X)

class Encoder(Transformer):
    """Base class for encoders."""
    pass

class OrdinalEncoder(Encoder):
    """Simple ordinal encoder."""
    def __init__(self):
        """
        Initializes the OrdinalEncoder.
        """
        super().__init__()
        self.mapping = {}

    def fit(self, X, y=None, strategy=None, ignore_na=True):
        """
        Fits the encoder on the data.

        Parameters:
            X (array-like): Input data.
            y (array-like, optional): Target data.
            strategy (optional): Strategy for encoding.
            ignore_na (bool): Whether to ignore NaN values.

        Returns:
            self: Returns the instance itself.
        """
        unique_values = pd.Series(X).unique()
        if ignore_na:
            unique_values = [val for val in unique_values if pd.notna(val)]
        self.mapping = {val: idx for idx, val in enumerate(unique_values)}
        if ignore_na:
            self.mapping[np.nan] = -1  # Assign a special value for NaNs if ignoring them
        return self
    
    def transform(self, X):
        """
        Transforms the data using the fitted encoder.

        Parameters:
            X (array-like): Input data.

        Returns:
            array-like: Transformed data.
        """
        return np.array([self.mapping.get(item, -1) for item in X])

class OneHotEncoder(Encoder):
    """One hot encoder."""
    def __init__(self):
        """
        Initializes the OneHotEncoder.
        """
        super().__init__()
        self.categories = []

    def fit(self, X, y=None):
        """
        Fits the encoder on the data.

        Parameters:
            X (array-like): Input data.
            y (array-like, optional): Target data.

        Returns:
            self: Returns the instance itself.
        """
        self.categories = pd.Series(X).unique()
        return self
    
    def transform(self, X):
        """
        Transforms the data using the fitted encoder.

        Parameters:
            X (array-like): Input data.

        Returns:
            array-like: Transformed data.
        """
        result = np.zeros((len(X), len(self.categories)))
        category_to_index = {cat: idx for idx, cat in enumerate(self.categories)}
        for i, item in enumerate(X):
            if item in category_to_index:
                result[i, category_to_index[item]] = 1
        return result

class LabelEncoder(Encoder):
    """Label encoder."""
    def __init__(self):
        """
        Initializes the LabelEncoder.
        """
        super().__init__()
        self.classes_ = []

    def fit(self, X, y=None):
        """
        Fits the encoder on the data.

        Parameters:
            X (array-like): Input data.
            y (array-like, optional): Target data.

        Returns:
            self: Returns the instance itself.
        """
        self.classes_ = pd.Series(X).unique()
        self.class_to_index = {cls: idx for idx, cls in enumerate(self.classes_)}
        return self
    
    def transform(self, X):
        """
        Transforms the data using the fitted encoder.

        Parameters:
            X (array-like): Input data.

        Returns:
            array-like: Transformed data.
        """
        return np.array([self.class_to_index[item] for item in X])

