import numpy as np
from um6p_CC_learn.base.base import TransformerMixin, BaseEstimator

class MissingIndicator(TransformerMixin, BaseEstimator):
    def __init__(self, missing_values=np.nan, features='missing-only', sparse=False):
        self.missing_values = missing_values
        self.features = features
        self.sparse = sparse

    def fit(self, X, y=None):
        X = np.asarray(X)
        if self.features not in ['missing-only', 'all']:
            raise ValueError("Invalid value for 'features': {}. Allowed values are 'missing-only' or 'all'.".format(self.features))

        if self.missing_values is np.nan:
            mask = np.isnan(X)
        else:
            mask = (X == self.missing_values)

        if self.features == 'missing-only':
            n_missing = np.sum(mask, axis=0)
            self.features_ = np.flatnonzero(n_missing)
        else:
            self.features_ = np.arange(X.shape[1])

        return self

    def transform(self, X):
        X = np.asarray(X)
        if self.missing_values is np.nan:
            mask = np.isnan(X)
        else:
            mask = (X == self.missing_values)

        if self.features == 'missing-only':
            mask = mask[:, self.features_]
        elif self.features == 'all':
            mask = mask

        if self.sparse:
            from scipy.sparse import csr_matrix
            mask = csr_matrix(mask)

        return mask

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


