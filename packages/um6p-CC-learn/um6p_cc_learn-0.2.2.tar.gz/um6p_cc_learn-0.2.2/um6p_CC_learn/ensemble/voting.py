import numpy as np
from copy import deepcopy

from base.base import BaseEstimator, ClassifierMixin, RegressorMixin


# TODO : revise the code
class VotingClassifier(ClassifierMixin, BaseEstimator):
    def __init__(self, estimators, voting='hard'):
        self.estimators = estimators
        self.voting = voting

    def fit(self, X, y):
        self.classes_, y_train = np.unique(y, return_inverse=True)
        self.estimators_ = [deepcopy(est).fit(X, y_train) for _, est in self.estimators]
        self._is_fitted = True
        return self

    def transform(self, X):
        if self.voting == 'hard':
            prob = np.array([est.predict(X) for est in self.estimators_]).T
        elif self.voting == 'soft':
            prob = np.array([est.predict_proba(X) for est in self.estimators_])
        return prob

    def predict(self, X):
        prob = self.transform(X)
        if self.voting == 'hard':
            pred = np.apply_along_axis(lambda x:np.argmax(np.bincount(x)), axis=1, arr=prob)
        elif self.voting == 'soft':
            pred = np.argmax(np.mean(prob, axis=0), axis=1)
        return self.classes_[pred]

    def predict_proba(self, X):
        if self.voting == 'hard':
            raise AttributeError
        return np.mean(self.transform(X), axis=0)
    

class VotingRegressor(RegressorMixin, BaseEstimator):
    
    def __init__(self, estimators):
        self.estimators = estimators

    def fit(self, X, y):
        self.estimators_ = [deepcopy(est).fit(X, y) for _, est in self.estimators]
        self._is_fitted = True
        return self

    def transform(self, X):
        prob = np.array([est.predict(X) for est in self.estimators_]).T
        return prob

    def predict(self, X):
        prob = self.transform(X)
        return np.mean(prob, axis=1)
    

