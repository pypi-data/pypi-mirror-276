from um6p_CC_learn.base.base import BaseEstimator, ClassifierMixin
import numpy as np
from scipy.special import logsumexp

class BaseNB(BaseEstimator, ClassifierMixin):
    def predict(self, X):
        self.check_is_fitted()

        joint_log_likelihood = self._joint_log_likelihood(X)
        return self.classes_[np.argmax(joint_log_likelihood, axis=1)]
    
    def predict_proba(self, X):
        self.check_is_fitted()

        joint_log_likelihood = self._joint_log_likelihood(X)
        log_prob = joint_log_likelihood - logsumexp(joint_log_likelihood, axis=1)[:, np.newaxis]
        return np.exp(log_prob)

    def _encode(self, y):
        classes = np.unique(y)
        y_train = np.zeros((y.shape[0], len(classes)))
        for i, c in enumerate(classes):
            y_train[y == c, i] = 1
        return classes, y_train

class GaussianNB(BaseNB):
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n_features = X.shape[1]
        n_classes = len(self.classes_)
        self.theta_ = np.zeros((n_classes, n_features))     # The means
        self.sigma_ = np.zeros((n_classes, n_features))     # The standard deviations
        self.class_count_ = np.zeros(n_classes)
        for i, c in enumerate(self.classes_):
            X_c = X[y == c]
            self.theta_[i] = np.mean(X_c, axis=0)
            self.sigma_[i] = np.var(X_c, axis=0)
            self.class_count_[i] = X_c.shape[0]
        self.class_prior_ = self.class_count_ / np.sum(self.class_count_)

        self._is_fitted = True
        return self

    def _joint_log_likelihood(self, X):
        self.check_is_fitted()

        joint_log_likelihood = np.zeros((X.shape[0], len(self.classes_)))
        for i in range(len(self.classes_)):
            p1 = np.log(self.class_prior_[i])
            p2 = -0.5 * np.log(2 * np.pi * self.sigma_[i]) - 0.5 * (X - self.theta_[i]) ** 2 / self.sigma_[i]
            joint_log_likelihood[:, i] = p1 + np.sum(p2, axis=1)
        return joint_log_likelihood


class BernoulliNB(BaseNB):
    def __init__(self, alpha=1.0):
        super().__init__()
        self.alpha = alpha

    def fit(self, X, y):        
        self.classes_, y_train = self._encode(y)
        self.feature_count_ = np.dot(y_train.T, X)
        self.class_count_ = y_train.sum(axis=0)
        smoothed_fc = self.feature_count_ + self.alpha
        smoothed_cc = self.class_count_ + 2 * self.alpha
        self.feature_log_prob_ = (np.log(smoothed_fc) -
                                  np.log(smoothed_cc.reshape(-1, 1)))
        self.class_log_prior_ = np.log(self.class_count_) - np.log(self.class_count_.sum())

        self._is_fitted = True
        return self
    
    def _joint_log_likelihood(self, X):
        self.check_is_fitted()

        return (np.dot(X, self.feature_log_prob_.T) +
                np.dot(1 - X, np.log(1 - np.exp(self.feature_log_prob_)).T) +
                self.class_log_prior_)
    

class MultinomialNB(BaseNB):
    def __init__(self, alpha=1.0):
        super().__init__()
        self.alpha = alpha

    def fit(self, X, y):
        self.classes_, y_train = self._encode(y)
        self.feature_count_ = np.dot(y_train.T, X)
        self.class_count_ = y_train.sum(axis=0)
        smoothed_fc = self.feature_count_ + self.alpha
        smoothed_cc = smoothed_fc.sum(axis=1)
        self.feature_log_prob_ = (np.log(smoothed_fc) -
                                  np.log(smoothed_cc.reshape(-1, 1)))
        self.class_log_prior_ = np.log(self.class_count_) - np.log(self.class_count_.sum())

        self._is_fitted = True
        return self

    def _joint_log_likelihood(self, X):
        self.check_is_fitted()

        return np.dot(X, self.feature_log_prob_.T) + self.class_log_prior_
