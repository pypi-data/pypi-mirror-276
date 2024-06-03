import numpy as np
from numpy.linalg import svd
from um6p_CC_learn.base.base import BaseEstimator, TransformerMixin

class PCA(BaseEstimator, TransformerMixin):
    def __init__(self, n_components=2):
        self.n_components = n_components

    def fit(self, X, y=None):
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_
        U, S, Vt = svd(X_centered, full_matrices=False)
        self.components_ = Vt[:self.n_components]
        self.explained_variance_ = (S[:self.n_components] ** 2) / (X.shape[0] - 1)
        self.explained_variance_ratio_ = self.explained_variance_ / np.sum(S ** 2 / (X.shape[0] - 1))
        self._is_fitted = True
        return self

    def transform(self, X):
        X_centered = X - self.mean_
        return np.dot(X_centered, self.components_.T)

    def inverse_transform(self, X):
        return np.dot(X, self.components_) + self.mean_