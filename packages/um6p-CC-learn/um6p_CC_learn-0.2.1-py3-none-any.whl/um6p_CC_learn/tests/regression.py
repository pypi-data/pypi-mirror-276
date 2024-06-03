import warnings
warnings.filterwarnings("ignore")

import numpy as np
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.linear_model import LinearRegression as skLinearRegression
from sklearn.linear_model import LogisticRegression as skLogisticRegression

from linear_model.regression import LinearRegression
from linear_model.logistic_regression import LogisticRegression

# --- Linear Regression Test ---

# Load the diabetes dataset for regression
X, y = load_diabetes(return_X_y=True)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

# Training my linear regression model
my_linear_reg = LinearRegression().fit(X_train, y_train)

# Training sklearn's linear regression model
sk_linear_reg = skLinearRegression().fit(X_train, y_train)

# Calculating mean squared error
mse_my_model = mean_squared_error(y_test, my_linear_reg.predict(X_test))
mse_sk_model = mean_squared_error(y_test, sk_linear_reg.predict(X_test))

# Printing the mean squared error
print("Mean Squared Error of my linear regression model:", mse_my_model)
print("Mean Squared Error of sklearn's linear regression model:", mse_sk_model)

print("--------------------------------------------------------------------------------")

# --- Logistic Regression Test ---

# Load the breast cancer dataset for classification
X, y = load_breast_cancer(return_X_y=True)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

# Training my logistic regression model
my_logistic_reg = LogisticRegression().fit(X_train, y_train)

# Training sklearn's logistic regression model
sk_logistic_reg = skLogisticRegression().fit(X_train, y_train)

# Calculating accuracy scores
accuracy_my_model = accuracy_score(y_test, my_logistic_reg.predict(X_test))
accuracy_sk_model = accuracy_score(y_test, sk_logistic_reg.predict(X_test))

# Printing the accuracy scores
print("Accuracy score of my logistic regression model:", accuracy_my_model)
print("Accuracy score of sklearn's logistic regression model:", accuracy_sk_model)