import warnings
warnings.filterwarnings("ignore")

from sklearn.datasets import load_breast_cancer, load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier as skDecisionTreeClassifier
from tree.decision_tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

criterion = 'gini'
max_depth = None

# Training my decision tree classifier
my_clf = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth).fit(X_train, y_train)

# Training sklearn's decision tree classifier
sk_clf = skDecisionTreeClassifier(random_state=0, criterion=criterion, max_depth=max_depth).fit(X_train, y_train)

# Calculating accuracy scores
accuracy_score_your_model = accuracy_score(y_test, my_clf.predict(X_test))
accuracy_score_sklearn_model = accuracy_score(y_test, sk_clf.predict(X_test))

# Printing the accuracy scores
print("Accuracy score of my decision tree classifier:", accuracy_score_your_model)
print("Depth of my decision tree classifier:", my_clf.depth)

print("Accuracy score of sklearn's decision tree classifier:", accuracy_score_sklearn_model)
print("Depth of sklearn's decision tree classifier:", sk_clf.get_depth())

print("--------------------------------------------------------------------------------")

from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor as skDecisionTreeRegressor
from tree.decision_tree import DecisionTreeRegressor

# Load the Boston housing dataset
X, y = fetch_california_housing(return_X_y=True)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

# Setting parameters
criterion = 'mse'
max_depth = None

# Training your decision tree regressor
my_reg = DecisionTreeRegressor(criterion=criterion, max_depth=max_depth).fit(X_train, y_train)

# Training scikit-learn's decision tree regressor
sk_reg = skDecisionTreeRegressor(random_state=0, criterion=criterion, max_depth=max_depth).fit(X_train, y_train)

# Calculating mean squared error
mse_your_model = mean_squared_error(y_test, my_reg.predict(X_test))
mse_sklearn_model = mean_squared_error(y_test, sk_reg.predict(X_test))

# Printing the mean squared error
print("Mean Squared Error of my decision tree regressor:", mse_your_model)
print("Depth of my decision tree regressor:", my_reg.depth)

print("Mean Squared Error of scikit-learn's decision tree regressor:", mse_sklearn_model)
print("Depth of scikit-learn's decision tree regressor:", sk_reg.get_depth())
