import numpy as np
import copy
from um6p_CC_learn.base.base import TransformerMixin, BaseEstimator

class RFE(TransformerMixin, BaseEstimator):
    """Feature ranking with recursive feature elimination (RFE).

    This transformer recursively removes features, building a model on the
    remaining features at each step until the desired number of features is
    reached.

    Parameters:
    estimator : object
        An estimator with a `fit` method that provides feature importances
        or coefficients.

    Attributes:
    estimator_ : object
        The fitted estimator.
    support_ : ndarray of shape (n_features,)
        The mask of selected features.
    ranking_ : ndarray of shape (n_features,)
        The feature ranking, with the selected features assigned rank 1.
    """

    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y):
        """Fit the RFE meta-transformer.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.

        Returns:
        self : RFE
            The fitted RFE instance.
        """
        n_features_to_select = X.shape[1] // 2
        support = np.ones(X.shape[1], dtype=np.bool)
        ranking = np.ones(X.shape[1], dtype=np.int)
        
        while np.sum(support) > n_features_to_select:
            est = copy.deepcopy(self.estimator)
            est.fit(X[:, support], y)
            
            if hasattr(est, "feature_importances_"):
                importances = est.feature_importances_
            elif hasattr(est, "coef_"):
                if est.coef_.ndim == 1:
                    importances = np.abs(est.coef_)
                else:
                    importances = np.linalg.norm(est.coef_, ord=1, axis=0)
            
            cur_feature = np.arange(X.shape[1])[support][np.argmin(importances)]
            support[cur_feature] = False
            ranking[~support] += 1
        
        self.support_ = support
        self.ranking_ = ranking
        self.estimator_ = copy.deepcopy(self.estimator)
        self.estimator_.fit(X[:, support], y)
        return self

    def transform(self, X):
        """Transform the input data based on selected features.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Data to transform.

        Returns:
        X_transformed : array-like of shape (n_samples, n_selected_features)
            Transformed data with selected features.
        """
        return X[:, self.support_]