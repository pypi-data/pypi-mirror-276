import numpy as np
import copy
from base.base import BaseEstimator, TransformerMixin

class SelectFromModel(TransformerMixin, BaseEstimator):
    """Meta-transformer for selecting features based on importance weights.

    This transformer selects features based on the importance weights
    provided by an estimator. Features whose importance exceeds a given
    threshold are retained, while others are discarded.

    Parameters:
    estimator : object
        An estimator with a `fit` method that provides feature importances
        or coefficients.

    Attributes:
    estimator_ : object
        The fitted estimator.
    importances_ : array of shape (n_features,)
        The feature importances or coefficients provided by the estimator.
    threshold_ : float
        The threshold used for feature selection.
    """

    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y):
        """Fit the SelectFromModel meta-transformer.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.

        Returns:
        self : SelectFromModel
            The fitted SelectFromModel instance.
        """
        self.estimator_ = copy.deepcopy(self.estimator)
        self.estimator_.fit(X, y)
        
        if hasattr(self.estimator_, "feature_importances_"):
            self.importances_ = self.estimator_.feature_importances_
        elif hasattr(self.estimator_, "coef_"):
            if self.estimator_.coef_.ndim == 1:
                self.importances_ = np.abs(self.estimator_.coef_)
            else:
                self.importances_ = np.linalg.norm(self.estimator_.coef_, ord=1, axis=0)
        
        self.threshold_ = np.mean(self.importances_)
        return self

    def transform(self, X):
        """Transform the input data based on the feature importances.

        Parameters:
        X : array-like of shape (n_samples, n_features)
            Data to transform.

        Returns:
        X_transformed : array-like of shape (n_samples, n_selected_features)
            Transformed data with selected features.
        """
        return X[:, self.importances_ >= self.threshold_]
