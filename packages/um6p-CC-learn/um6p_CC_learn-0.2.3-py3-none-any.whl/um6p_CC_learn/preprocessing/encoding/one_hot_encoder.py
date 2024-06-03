import numpy as np
from um6p_CC_learn.base.base import BaseEstimator, TransformerMixin

class OneHotEncoder(TransformerMixin, BaseEstimator):
    def fit(self, X):
        """
        Fit OneHotEncoder to X.

        Parameters:
        X (np.ndarray): The input array of shape (n_samples, n_features).
        """
        self.categories_ = [np.unique(column) for column in X.T]
        return self
    
    def transform(self, X):
        """
        Transform X using one-hot encoding.

        Parameters:
        X (np.ndarray): The input array of shape (n_samples, n_features).
        
        Returns:
        np.ndarray: Transformed array of shape (n_samples, n_encoded_features).
        """
        encoded_columns = []
        for i, column in enumerate(X.T):
            categories = self.categories_[i]
            encoded_column = np.zeros((X.shape[0], len(categories)))
            for j, value in enumerate(column):
                encoded_column[j, categories == value] = 1
            encoded_columns.append(encoded_column)
        
        return np.hstack(encoded_columns)
    
    def fit_transform(self, X):
        """
        Fit to data, then transform it.

        Parameters:
        X (np.ndarray): The input array of shape (n_samples, n_features).
        
        Returns:
        np.ndarray: Transformed array of shape (n_samples, n_encoded_features).
        """
        return self.fit(X).transform(X)

# Example usage
if __name__ == "__main__":
    X = np.array([['cat', 'A'], ['dog', 'B'], ['cat', 'A'], ['bird', 'B']])
    one_hot_encoder = OneHotEncoder()
    X_encoded = one_hot_encoder.fit_transform(X)
    print(X_encoded)
