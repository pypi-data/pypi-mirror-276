import numpy as np
from scipy.optimize import minimize
from um6p_CC_learn.base.base import BaseEstimator, ClassifierMixin

class LogisticRegression(ClassifierMixin, BaseEstimator):
    """
    Logistic Regression classifier using maximum likelihood estimation.

    Attributes:
        coef_ (np.ndarray): Coefficients of the logistic regression model.
        intercept_ (float): Intercept of the logistic regression model.
    """

    def sigmoid(self, z):
        """
        Compute the sigmoid function.

        Parameters:
            z (np.ndarray): Input array.

        Returns:
            np.ndarray: Sigmoid of the input array.
        """
        return 1 / (1 + np.exp(-z))

    def log_likelihood(self, coef, X, y):
        """
        Compute the log-likelihood of the logistic regression model.

        Parameters:
            coef (np.ndarray): Coefficients of the model including intercept.
            X (np.ndarray): Training data.
            y (np.ndarray): Target values.

        Returns:
            float: Log-likelihood value.
        """
        z = np.dot(X, coef)
        ll = np.sum(y * z - np.log(1 + np.exp(z)))
        return -ll  # Negative log-likelihood for minimization

    def fit(self, X, y):
        """
        Fit the logistic regression model using the training data.

        Parameters:
            X (np.ndarray): Training data of shape (n_samples, n_features).
            y (np.ndarray): Target values of shape (n_samples,).

        Returns:
            self (LogisticRegression): Returns the instance itself.
        """
        # Add a column of ones to X to account for the intercept
        X_with_intercept = np.hstack((np.ones((X.shape[0], 1)), X))
        
        # Initial guess for the coefficients
        initial_coef = np.zeros(X_with_intercept.shape[1])
        
        # Minimize the negative log-likelihood
        result = minimize(self.log_likelihood, initial_coef, args=(X_with_intercept, y), method='BFGS')
        
        # Store the coefficients and intercept
        self.intercept_ = result.x[0]
        self.coef_ = result.x[1:]

        self._is_fitted = True
        return self

    def predict_proba(self, X):
        """
        Predict probability estimates for the input data.

        Parameters:
            X (np.ndarray): Input data of shape (n_samples, n_features).

        Returns:
            np.ndarray: Predicted probabilities of shape (n_samples, 2).
        """
        self.check_is_fitted()

        # Add a column of ones to X to account for the intercept
        X_with_intercept = np.hstack((np.ones((X.shape[0], 1)), X))
        
        # Compute the probability estimates
        prob = self.sigmoid(np.dot(X_with_intercept, np.hstack(([self.intercept_], self.coef_))))
        
        return np.vstack((1 - prob, prob)).T

    def predict(self, X):
        """
        Predict class labels for the input data.

        Parameters:
            X (np.ndarray): Input data of shape (n_samples, n_features).

        Returns:
            np.ndarray: Predicted class labels of shape (n_samples,).
        """
        self.check_is_fitted()

        # Predict probabilities
        prob = self.predict_proba(X)[:, 1]
        
        # Predict class labels based on probability threshold of 0.5
        return (prob >= 0.5).astype(int)
    def get_params(self, deep=True):
        """
        Get parameters for this estimator.

        Parameters:
            deep (bool, optional): If True, will return the parameters for this estimator and contained subobjects that are estimators.

        Returns:
            dict: Parameter names mapped to their values.
        """
        return {}