import warnings
warnings.filterwarnings("ignore")

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB as skGaussianNB, BernoulliNB as skBernoulliNB, MultinomialNB as skMultinomialNB
from um6p_CC_learn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

# Load the iris dataset
X, y = load_breast_cancer(return_X_y=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

# Initialize the models
my_gnb = GaussianNB()
my_bnb = BernoulliNB()
my_mnb = MultinomialNB()

sk_gnb = skGaussianNB()
sk_bnb = skBernoulliNB()
sk_mnb = skMultinomialNB()

# Train the models
my_gnb.fit(X_train, y_train)
my_bnb.fit(X_train, y_train)
my_mnb.fit(X_train, y_train)

sk_gnb.fit(X_train, y_train)
sk_bnb.fit(X_train, y_train)
sk_mnb.fit(X_train, y_train)

# Calculate accuracy scores
accuracy_my_gnb = accuracy_score(y_test, my_gnb.predict(X_test))
accuracy_my_bnb = accuracy_score(y_test, my_bnb.predict(X_test))
accuracy_my_mnb = accuracy_score(y_test, my_mnb.predict(X_test))

accuracy_sk_gnb = accuracy_score(y_test, sk_gnb.predict(X_test))
accuracy_sk_bnb = accuracy_score(y_test, sk_bnb.predict(X_test))
accuracy_sk_mnb = accuracy_score(y_test, sk_mnb.predict(X_test))

# Print the accuracy scores
print("My Gaussian Naive Bayes Accuracy:", accuracy_my_gnb)
print("My Bernoulli Naive Bayes Accuracy:", accuracy_my_bnb)
print("My Multinomial Naive Bayes Accuracy:", accuracy_my_mnb)

print("Scikit-learn Gaussian Naive Bayes Accuracy:", accuracy_sk_gnb)
print("Scikit-learn Bernoulli Naive Bayes Accuracy:", accuracy_sk_bnb)
print("Scikit-learn Multinomial Naive Bayes Accuracy:", accuracy_sk_mnb)
