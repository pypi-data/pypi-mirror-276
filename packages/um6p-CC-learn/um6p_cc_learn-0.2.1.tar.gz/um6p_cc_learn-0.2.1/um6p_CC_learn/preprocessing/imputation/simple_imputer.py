import numpy as np
from scipy.stats import mode

from base.base import TransformerMixin, BaseEstimator

class SimpleImputer(TransformerMixin, BaseEstimator):
    def __init__(self, strategy='mean', fill_value=None):
        self.strategy = strategy
        self.fill_value = fill_value  # only used when strategy == 'constant'

    def fit(self, X):
        if self.strategy not in ["mean", "median", "most_frequent", "constant"]:
            raise ValueError("Invalid strategy: %s. Strategy must be one of 'mean', 'median', 'most_frequent', or 'constant'." % self.strategy)
        
        if self.strategy == "constant" and self.fill_value is None:
            raise ValueError("Strategy is 'constant' but no fill value provided.")
        
        if self.strategy == "mean":
            self.statistics_ = np.nanmean(X, axis=0)
        elif self.strategy == "median":
            self.statistics_ = np.nanmedian(X, axis=0)
        elif self.strategy == "most_frequent":
            self.statistics_ = mode(X, axis=0, nan_policy='omit')[0].squeeze()
        elif self.strategy == "constant":
            self.statistics_ = np.full(X.shape[1], self.fill_value)
        self._is_fitted = True
        
        return self

    def transform(self, X):
        Xt = X.copy()
        missing_mask = np.isnan(Xt)
        if self.strategy != "constant":
            for i in range(Xt.shape[1]):
                missing = missing_mask[:, i]
                if np.any(missing):
                    Xt[missing, i] = self.statistics_[i]
        else:
            Xt[missing_mask] = self.fill_value
        
        return Xt
