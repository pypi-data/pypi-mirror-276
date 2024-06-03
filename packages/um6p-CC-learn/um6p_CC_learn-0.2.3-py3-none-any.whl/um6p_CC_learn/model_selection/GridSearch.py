import numpy as np
from um6p_CC_learn.base.base import BaseEstimator
from um6p_CC_learn.utils.__clone import clone
from um6p_CC_learn.model_selection.__split import KFold, StratifiedKFold
from itertools import product

class GridSearchCVBase(BaseEstimator):
    def __init__(self, estimator, param_grid):
        self.estimator = estimator
        self.param_grid = param_grid

    def generate_grid(self):
        items = sorted(self.param_grid.items())
        keys, values = zip(*items)
        for v in product(*values):
            params = dict(zip(keys, v))
            yield params

    def fit(self, X, y):
        cv = self.get_cv(y)
        train_scores, test_scores  = [], []
        params = []
        for i, cur_param in enumerate(self.generate_grid()):
            cur_train_score, cur_test_score = [], []
            for j, (train, test) in enumerate(cv.split(X, y)):
                est = clone(self.estimator)
                est.set_params(**cur_param)
                est.fit(X[train], y[train])
                cur_train_score.append(est.score(X[train], y[train]))
                cur_test_score.append(est.score(X[test], y[test]))
            params.append(cur_param)
            train_scores.append(cur_train_score)
            test_scores.append(cur_test_score)
        train_scores = np.array(train_scores)
        test_scores = np.array(test_scores)
        cv_results = {}
        for i in range(cv.n_splits):
            cv_results["split" + str(i) + "_train_score"] = train_scores[:, i]
            cv_results["split" + str(i) + "_test_score"] = test_scores[:, i]
        cv_results["mean_train_score"] = np.mean(train_scores, axis=1)
        cv_results["std_train_score"] = np.std(train_scores, axis=1)
        cv_results["mean_test_score"] = np.mean(test_scores, axis=1)
        cv_results["std_test_score"] = np.std(test_scores, axis=1)
        cv_results['params'] = params
        self.cv_results_ = cv_results
        self.best_params_ = cv_results['params'][np.argmax(cv_results['mean_test_score'])]
        self.best_estimator_ = clone(self.estimator)
        self.best_estimator_.set_params(**self.best_params_)
        self.best_estimator_.fit(X, y)
        return self

    def get_cv(self, y):
        raise NotImplementedError

    def decision_function(self, X):
        return self.best_estimator_.decision_function(X)

    def predict(self, X):
        return self.best_estimator_.predict(X)


class GridSearchCVClassifier(GridSearchCVBase):
    def get_cv(self, y):
        return StratifiedKFold()


class GridSearchCVRegressor(GridSearchCVBase):
    def get_cv(self, y):
        return KFold()