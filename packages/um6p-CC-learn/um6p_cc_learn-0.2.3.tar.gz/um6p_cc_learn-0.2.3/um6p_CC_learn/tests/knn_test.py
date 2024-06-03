import numpy as np
import time
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier as skKNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from um6p_CC_learn.neighbors.KNeighborsClassifier import KNeighborsClassifier

X, y = load_breast_cancer(return_X_y=True)

X = StandardScaler().fit_transform(X)

start_time = time.time()
clf1 = KNeighborsClassifier().fit(X, y)
end_time = time.time()
my_fit_time = end_time - start_time

start_time = time.time()
clf2 = skKNeighborsClassifier().fit(X, y)
end_time = time.time()
sk_fit_time = end_time - start_time

prob1 = clf1.predict_proba(X)

# Predict probabilities using scikit-learn's KNeighborsClassifier
prob2 = clf2.predict_proba(X)

# Check if probabilities are almost equal
assert np.allclose(prob1, prob2), "Probability predictions do not match."

# Predict classes using my KNeighborsClassifier
pred1 = clf1.predict(X)

# Predict classes using scikit-learn's KNeighborsClassifier
pred2 = clf2.predict(X)

# Check if class predictions are equal
assert np.array_equal(pred1, pred2), "Class predictions do not match."

# Calculate evaluation metrics
accuracy_my = accuracy_score(y, pred1)
precision_my = precision_score(y, pred1)
recall_my = recall_score(y, pred1)
f1_my = f1_score(y, pred1)

accuracy_sk = accuracy_score(y, pred2)
precision_sk = precision_score(y, pred2)
recall_sk = recall_score(y, pred2)
f1_sk = f1_score(y, pred2)

# Printing the results
print("My KNeighborsClassifier")
print("Accuracy:", accuracy_my)
print("Precision:", precision_my)
print("Recall:", recall_my)
print("F1-score:", f1_my)
print("Time taken to fit:", my_fit_time)

print("\nScikit-learn's KNeighborsClassifier")
print("Accuracy:", accuracy_sk)
print("Precision:", precision_sk)
print("Recall:", recall_sk)
print("F1-score:", f1_sk)
print("Time taken to fit:", sk_fit_time)
