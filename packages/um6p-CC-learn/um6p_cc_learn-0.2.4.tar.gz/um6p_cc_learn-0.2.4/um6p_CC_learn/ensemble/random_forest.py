import numpy as np
from um6p_CC_learn.base.base import ClassifierMixin, RegressorMixin, BaseEstimator
from um6p_CC_learn.tree.decision_tree import DecisionTreeClassifier, DecisionTreeRegressor

class RandomForestClassifier(ClassifierMixin, BaseEstimator):
    def __init__(self, n_estimators=100, criterion='gini', max_depth=None, min_samples_split=2, max_features='auto', bootstrap=True, random_state=None):
        """
        Initialize a random forest classifier with specified parameters.

        Parameters:
            n_estimators (int): The number of trees in the forest.
            criterion (str): The function to measure the quality of a split.
            max_depth (int, optional): The maximum depth of the tree.
            min_samples_split (int): The minimum number of samples required to split an internal node.
            max_features (int, float, str or None): The number of features to consider when looking for the best split.
            bootstrap (bool): Whether bootstrap samples are used when building trees.
            random_state (int, optional): The random seed.
        """
        self.n_estimators = n_estimators
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.random_state = random_state
        self.estimators_ = []
        self._is_fitted = False
        self._estimator_type = "classifier"

    def fit(self, X, y):
        """
        Fit the random forest classifier to the training data.

        Parameters:
            X (np.ndarray): Training data.
            y (np.ndarray): Target values.

        Returns:
            self (RandomForestClassifier): Fitted estimator.
        """
        if self.random_state is not None:
            np.random.seed(self.random_state)
        
        self.n_samples_, self.n_features_ = X.shape
        self.classes_, y_train = np.unique(y, return_inverse=True)
        self.n_classes_ = len(self.classes_)
        
        for _ in range(self.n_estimators):
            tree = DecisionTreeClassifier(
                criterion=self.criterion,
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=self.max_features
            )
            if self.bootstrap:
                indices = np.random.choice(self.n_samples_, self.n_samples_, replace=True)
            else:
                indices = np.arange(self.n_samples_)
            tree.fit(X[indices], y_train[indices])
            self.estimators_.append(tree)

        self._is_fitted = True
        return self

    def predict_proba(self, X):
        """
        Predict class probabilities for X.

        Parameters:
            X (np.ndarray): Input data.

        Returns:
            np.ndarray: Predicted class probabilities.
        """
        self.check_is_fitted()

        all_probas = np.zeros((X.shape[0], self.n_classes_))
        for tree in self.estimators_:
            all_probas += tree.predict_proba(X)
        all_probas /= self.n_estimators
        return all_probas

    def predict(self, X):
        """
        Predict class labels for X.

        Parameters:
            X (np.ndarray): Input data.

        Returns:
            np.ndarray: Predicted class labels.
        """
        self.check_is_fitted()

        proba = self.predict_proba(X)
        return self.classes_[np.argmax(proba, axis=1)]

    @property
    def feature_importances_(self):
        """
        Feature importances for the random forest.

        Returns:
            np.ndarray: Normalized feature importances.
        """
        self.check_is_fitted()
        all_importances = np.zeros(self.n_features_)
        
        for est in self.estimators_:
            all_importances += est.feature_importances_()
        
        all_importances /= self.n_estimators
        return all_importances / np.sum(all_importances)
    

class RandomForestRegressor(RegressorMixin, BaseEstimator):
    def __init__(self, n_estimators=100, criterion='mse', max_depth=None, min_samples_split=2, max_features='auto', bootstrap=True, random_state=None):
        """
        Initialize a random forest regressor with specified parameters.

        Parameters:
            n_estimators (int): The number of trees in the forest.
            criterion (str): The function to measure the quality of a split.
            max_depth (int, optional): The maximum depth of the tree.
            min_samples_split (int): The minimum number of samples required to split an internal node.
            max_features (int, float, str or None): The number of features to consider when looking for the best split.
            bootstrap (bool): Whether bootstrap samples are used when building trees.
            random_state (int, optional): The random seed.
        """
        self.n_estimators = n_estimators
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.random_state = random_state
        self.estimators_ = []
        self._is_fitted = False
        self._estimator_type = "regressor"

    def fit(self, X, y):
        """
        Fit the random forest regressor to the training data.

        Parameters:
            X (np.ndarray): Training data.
            y (np.ndarray): Target values.

        Returns:
            self (RandomForestRegressor): Fitted estimator.
        """
        if self.random_state is not None:
            np.random.seed(self.random_state)

        self.n_samples_, self.n_features_ = X.shape
        
        for _ in range(self.n_estimators):
            tree = DecisionTreeRegressor(
                criterion=self.criterion,
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=self.max_features
            )
            if self.bootstrap:
                indices = np.random.choice(self.n_samples_, self.n_samples_, replace=True)
            else:
                indices = np.arange(self.n_samples_)
            tree.fit(X[indices], y[indices])
            self.estimators_.append(tree)

        self._is_fitted = True
        return self

    def predict(self, X):
        """
        Predict regression target for X.

        Parameters:
            X (np.ndarray): Input data.

        Returns:
            np.ndarray: Predicted target values.
        """
        self.check_is_fitted()

        all_preds = np.zeros(X.shape[0])
        for tree in self.estimators_:
            all_preds += tree.predict(X)
        return all_preds / self.n_estimators
    
    @property
    def feature_importances_(self):
        """
        Feature importances for the random forest.

        Returns:
            np.ndarray: Normalized feature importances.
        """
        self.check_is_fitted()
        all_importances = np.zeros(self.n_features_)
        
        for est in self.estimators_:
            all_importances += est.feature_importances_()
        
        all_importances /= self.n_estimators
        return all_importances / np.sum(all_importances)