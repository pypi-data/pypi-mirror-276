from utils.__clone import clone

from um6p_CC_learn.model_selection.__validation import cross_val_predict

from um6p_CC_learn.base.base import RegressorMixin, BaseEstimator

import numpy as np

class StackingClassifier(RegressorMixin, BaseEstimator):
    def __init__(self, estimators, final_estimator):
        self.estimators = estimators
        self.final_estimator = final_estimator

    def fit(self, X, y):
        self.estimators_ = []
        for est in self.estimators:
            self.estimators_.append(clone(est).fit(X, y))
        predictions = []
        for est in self.estimators:
            cur_prediction = cross_val_predict(est, X, y, method="predict_proba")
            if cur_prediction.shape[1] == 2:
                predictions.append(cur_prediction[:, [1]])
            else:
                predictions.append(cur_prediction)
        X_meta = np.hstack(predictions)
        self.final_estimator_ = clone(self.final_estimator)
        self.final_estimator_.fit(X_meta, y)
        self._is_fitted = True
        return self

    def transform(self, X):
        predictions = []
        for est in self.estimators_:
            cur_prediction = est.predict_proba(X)
            if cur_prediction.shape[1] == 2:
                predictions.append(cur_prediction[:, [1]])
            else:
                predictions.append(cur_prediction)
        return np.hstack(predictions)

    def predict(self, X):
        return self.final_estimator_.predict(self.transform(X))

    def predict_proba(self, X):
        return self.final_estimator_.predict_proba(self.transform(X))
    

class StackingRegressor(RegressorMixin, BaseEstimator):
    def __init__(self, estimators, final_estimator):
        self.estimators = estimators
        self.final_estimator = final_estimator

    def fit(self, X, y):
        self.estimators_ = [clone(est).fit(X, y) for est in self.estimators]
        predictions = [
            cross_val_predict(est, X, y, method='predict').reshape(-1, 1)
            for est in self.estimators_
        ]
        X_meta = np.hstack(predictions)
        self.final_estimator_ = clone(self.final_estimator).fit(X_meta, y)
        self._is_fitted = True
        return self

    def transform(self, X):
        predictions = [
            est.predict(X).reshape(-1, 1) for est in self.estimators_
        ]
        return np.hstack(predictions)

    def predict(self, X):
        return self.final_estimator_.predict(self.transform(X))