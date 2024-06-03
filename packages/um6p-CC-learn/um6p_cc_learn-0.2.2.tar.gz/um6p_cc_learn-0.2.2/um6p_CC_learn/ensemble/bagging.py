import numpy as np
import copy
from base.base import BaseEstimator, ClassifierMixin, RegressorMixin
from tree.decision_tree import DecisionTreeClassifier, DecisionTreeRegressor

class BaggingClassifier(ClassifierMixin, BaseEstimator):
    def __init__(self, base_estimator=None, n_estimators=10, max_samples=1.0, bootstrap=True, random_state=None):
        self.base_estimator = base_estimator if base_estimator is not None else DecisionTreeClassifier()
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.bootstrap = bootstrap
        self.random_state = random_state
        self.estimators_ = []

    def fit(self, X, y):
        np.random.seed(self.random_state)
        self.estimators_ = []

        for _ in range(self.n_estimators):
            estimator = copy.deepcopy(self.base_estimator)
            n_samples = int(self.max_samples * X.shape[0])

            if self.bootstrap:
                indices = np.random.choice(X.shape[0], n_samples, replace=True)
            else:
                indices = np.random.choice(X.shape[0], n_samples, replace=False)

            estimator.fit(X[indices], y[indices])
            self.estimators_.append(estimator)

        return self

    def predict(self, X):
        predictions = np.array([estimator.predict(X) for estimator in self.estimators_])
        return np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=predictions)


class BaggingRegressor(RegressorMixin, BaseEstimator):
    def __init__(self, base_estimator=None, n_estimators=10, max_samples=1.0, bootstrap=True, random_state=None):
        self.base_estimator = base_estimator if base_estimator is not None else DecisionTreeRegressor()
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.bootstrap = bootstrap
        self.random_state = random_state
        self.estimators_ = []

    def fit(self, X, y):
        np.random.seed(self.random_state)
        self.estimators_ = []

        for _ in range(self.n_estimators):
            estimator = copy.deepcopy(self.base_estimator)
            n_samples = int(self.max_samples * X.shape[0])

            if self.bootstrap:
                indices = np.random.choice(X.shape[0], n_samples, replace=True)
            else:
                indices = np.random.choice(X.shape[0], n_samples, replace=False)

            estimator.fit(X[indices], y[indices])
            self.estimators_.append(estimator)

        return self

    def predict(self, X):
        predictions = np.array([estimator.predict(X) for estimator in self.estimators_])
        return np.mean(predictions, axis=0)
