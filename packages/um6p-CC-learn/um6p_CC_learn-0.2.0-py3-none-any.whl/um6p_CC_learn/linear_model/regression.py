import numpy as np
from scipy.linalg import lstsq
from base.base import RegressorMixin, BaseEstimator

class LinearRegression(RegressorMixin, BaseEstimator):
    """
    Linear Regression model that uses the normal equation to fit and predict.

    Attributes:
        coef_ (np.ndarray): Coefficients of the linear regression model.
        intercept_ (float): Intercept of the linear regression model.
    """

    def fit(self, X, y):
        """
        Fit the linear regression model using the training data.

        Parameters:
            X (np.ndarray): Training data of shape (n_samples, n_features).
            y (np.ndarray): Target values of shape (n_samples,).

        Returns:
            self (LinearRegression): Returns the instance itself.
        """
        # Add a column of ones to X to account for the intercept
        X_with_intercept = np.hstack((np.ones((X.shape[0], 1)), X))
        
        # Solve the normal equation
        coef, _, _, _ = lstsq(X_with_intercept, y)
        
        # Store the coefficients and intercept
        self.intercept_ = coef[0]
        self.coef_ = coef[1:]

        self._is_fitted = True
        return self

    def predict(self, X):
        """
        Predict target values using the linear regression model.

        Parameters:
            X (np.ndarray): Input data of shape (n_samples, n_features).

        Returns:
            y_pred (np.ndarray): Predicted values of shape (n_samples,).
        """
        self.check_is_fitted()

        y_pred = np.dot(X, self.coef_) + self.intercept_
        
        return y_pred



