import numpy as np
from base.base import BaseEstimator, TransformerMixin

class OrdinalEncoder(TransformerMixin, BaseEstimator):
    def fit(self, X):
        """
        Fit OrdinalEncoder to X.

        Parameters:
        X (np.ndarray): The input array of shape (n_samples, n_features).
        """
        self.categories_ = [np.unique(column) for column in X.T]
        return self
    
    def transform(self, X):
        """
        Transform X using ordinal encoding.

        Parameters:
        X (np.ndarray): The input array of shape (n_samples, n_features).
        
        Returns:
        np.ndarray: Transformed array of shape (n_samples, n_features).
        """
        encoded_columns = []
        for i, column in enumerate(X.T):
            category_indices = {category: idx for idx, category in enumerate(self.categories_[i])}
            encoded_column = np.array([category_indices[value] for value in column])
            encoded_columns.append(encoded_column[:, np.newaxis])
        
        return np.hstack(encoded_columns)
    
    def fit_transform(self, X):
        """
        Fit to data, then transform it.

        Parameters:
        X (np.ndarray): The input array of shape (n_samples, n_features).
        
        Returns:
        np.ndarray: Transformed array of shape (n_samples, n_features).
        """
        return self.fit(X).transform(X)

# Example usage:
if __name__ == "__main__":
    X = np.array([['cat', 'A'], ['dog', 'B'], ['cat', 'A'], ['bird', 'B']])
    ordinal_encoder = OrdinalEncoder()
    X_encoded = ordinal_encoder.fit_transform(X)
    print(X_encoded)
