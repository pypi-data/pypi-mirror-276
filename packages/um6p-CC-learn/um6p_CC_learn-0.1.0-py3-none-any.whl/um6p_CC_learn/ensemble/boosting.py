import numpy as np
from base.base import BaseEstimator, ClassifierMixin
from tree.decision_tree import DecisionTreeClassifier, DecisionTreeRegressor
from scipy.special import expit, logsumexp


class AdaBoostClassifier(ClassifierMixin, BaseEstimator):
    def __init__(self, n_estimators=50, random_state=0):
        self.n_estimators = n_estimators
        self.random_state = random_state

    def fit(self, X, y):
        self.classes_, y_train = np.unique(y, return_inverse=True)
        self.n_classes_ = len(self.classes_)
        sample_weight = np.full(X.shape[0], 1 / X.shape[0])
        self.estimators_ = []
        self.estimator_weights_ = np.zeros(self.n_estimators)
        self.estimator_errors_ = np.ones(self.n_estimators)
        MAX_INT = np.iinfo(np.int32).max
        rng = np.random.RandomState(self.random_state)
        for i in range(self.n_estimators):
            est = DecisionTreeClassifier(max_depth=1)
            est.fit(X, y_train)
            y_predict = est.predict(X)
            incorrect = y_predict != y_train
            estimator_error = np.average(incorrect, weights=sample_weight)
            estimator_weight = (np.log((1 - estimator_error) / estimator_error) +
                                np.log(self.n_classes_ - 1))
            sample_weight *= np.exp(estimator_weight * incorrect)
            sample_weight /= np.sum(sample_weight)
            self.estimators_.append(est)
            self.estimator_errors_[i] = estimator_error
            self.estimator_weights_[i] = estimator_weight
        return self

    def decision_function(self, X):
        pred = np.zeros((X.shape[0], self.n_classes_))
        for i in range(self.n_estimators):
            pred[np.arange(X.shape[0]), self.estimators_[i].predict(X)] += self.estimator_weights_[i]
        pred /= np.sum(self.estimator_weights_)
        if self.n_classes_ == 2:
            return pred[:, 1] - pred[:, 0]
        return pred

    def predict(self, X):
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = np.argmax(scores, axis=1)
        return self.classes_[indices]
    


class GradientBoostingClassifier(ClassifierMixin, BaseEstimator):
    def __init__(self, learning_rate=0.1, n_estimators=100, max_depth=3, random_state=0):
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state

    def fit(self, X, y):
        self.n_features_ = X.shape[1]
        self.classes_, y = np.unique(y, return_inverse=True)
        self.n_classes_ = len(self.classes_)
        if self.n_classes_ == 2:
            n_effective_classes = 1
        else:
            n_effective_classes = self.n_classes_
        self.estimators_ = np.empty((self.n_estimators, n_effective_classes), dtype=object)
        raw_predictions = np.zeros((X.shape[0], n_effective_classes))
        for i in range(self.n_estimators):
            raw_predictions_copy = raw_predictions.copy()
            for j in range(n_effective_classes):
                # binary classification
                if n_effective_classes == 1:
                    y_enc = y
                    residual = y_enc - expit(raw_predictions_copy.ravel())
                # multiclass classification
                else:
                    y_enc = (y == j).astype(np.int)
                    residual = y_enc - np.nan_to_num(np.exp(raw_predictions_copy[:, j] 
                                                            - logsumexp(raw_predictions_copy, axis=1)))
                tree = DecisionTreeRegressor(criterion="mse", max_depth=self.max_depth)
                tree.fit(X, residual)
                raw_predictions[:, j] += self.learning_rate * tree.predict(X)
                self.estimators_[i, j] = tree
        self._is_fitted = True
        return self

    def _predict(self, X):
        raw_predictions = np.zeros((X.shape[0], self.estimators_.shape[1]))
        for i in range(self.estimators_.shape[0]):
            for j in range(self.estimators_.shape[1]):
                raw_predictions[:, j] += self.learning_rate * self.estimators_[i, j].predict(X)
        return raw_predictions

    def decision_function(self, X):
        prob = self._predict(X)
        if self.n_classes_ == 2:
            return prob.ravel()
        else:
            return prob

    def predict_proba(self, X):
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            prob = expit(scores)
            prob = np.vstack((1 - prob, prob)).T
        else:
            prob = np.nan_to_num(np.exp(scores - logsumexp(scores, axis=1)[:, np.newaxis]))
        return prob

    def predict(self, X):
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = np.argmax(scores, axis=1)
        return self.classes_[indices]

    @property
    def feature_importances_(self):
        all_importances = np.zeros(self.n_features_)
        for i in range(self.estimators_.shape[0]):
            for j in range(self.estimators_.shape[1]):
                all_importances += self.estimators_[i, j].tree_.compute_feature_importances(normalize=False)
        return all_importances / np.sum(all_importances)


