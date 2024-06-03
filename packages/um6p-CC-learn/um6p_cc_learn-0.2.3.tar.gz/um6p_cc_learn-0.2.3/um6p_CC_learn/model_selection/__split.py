#TODO : revise the code 

import numpy as np

from abc import ABC, abstractmethod


class BaseKFold(ABC):
    def __init__(self, n_splits=5, shuffle=False, random_state=0) -> None:
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

    def split(self, X, y):
        indices = np.arange(X.shape[0])
        for test_index in self._iter_test_masks(X, y):
            yield indices[~test_index], indices[test_index]

    @abstractmethod
    def _iter_test_masks(self, X, y):
        pass 

class KFold(BaseKFold):

    def __init__(self, n_splits=5, shuffle=False, random_state=0) -> None:
        super().__init__(n_splits, shuffle, random_state)

    def _iter_test_indices(self, X, y):
        indices = np.arange(X.shape[0])
        if self.shuffle:
            rng = np.random.RandomState(self.random_state)
            rng.shuffle(indices)
        fold_sizes = np.full(self.n_splits, X.shape[0] // self.n_splits)
        fold_sizes[:X.shape[0] % self.n_splits] += 1
        current = 0
        for fold_size in fold_sizes:
            yield indices[current:current + fold_size]
            current += fold_size

    def _iter_test_masks(self, X, y):
        for test_index in self._iter_test_indices(X, y):
            test_mask = np.zeros(X.shape[0], dtype=bool)
            test_mask[test_index] = True
            yield test_mask

    def split(self, X, y):
        return super().split(X, y)


class StratifiedKFold(BaseKFold):

    def __init__(self, n_splits=5, shuffle=False, random_state=0) -> None:
        super().__init__(n_splits, shuffle, random_state)

    def _kfold(self, count, rng):
        indices = np.arange(count)
        if self.shuffle:
            rng.shuffle(indices)
        fold_sizes = np.full(self.n_splits, count // self.n_splits)
        fold_sizes[:count % self.n_splits] += 1
        current = 0
        for fold_size in fold_sizes:
            test_mask = np.zeros(count, dtype=bool)
            test_mask[current:current + fold_size] = True
            yield indices[test_mask]
            current += fold_size

    def _make_test_folds(self, X, y):
        rng = np.random.RandomState(self.random_state)
        unique_y, y_inversed = np.unique(y, return_inverse=True)
        y_counts = np.bincount(y_inversed)
        test_folds = np.zeros(X.shape[0])
        per_cls_cvs = [self._kfold(count, rng) for count in y_counts]
        test_folds = np.zeros(X.shape[0])
        for test_fold_indices, per_cls_splits in enumerate(zip(*per_cls_cvs)):
            for cls, test_split in zip(unique_y, per_cls_splits):
                cls_test_folds = test_folds[y == cls]
                cls_test_folds[test_split] = test_fold_indices
                test_folds[y == cls] = cls_test_folds
        return test_folds

    def _iter_test_masks(self, X, y):
        test_folds = self._make_test_folds(X, y)
        for i in range(self.n_splits):
            yield test_folds == i

    def split(self, X, y):
        return super().split(X, y)
    

def train_test_split(*arrays, test_size=0.25, random_state=None, shuffle=True):
    """
    Split arrays or matrices into random train and test subsets.

    Parameters:
        *arrays : sequence of indexables with same length / shape[0]
            Allowed inputs are lists, numpy arrays, scipy-sparse
            matrices or pandas dataframes.
        test_size : float or int, default=0.25
            If float, should be between 0.0 and 1.0 and represent the
            proportion of the dataset to include in the test split. If
            int, represents the absolute number of test samples.
        random_state : int or None, default=None
            Controls the shuffling applied to the data before applying the split.
            Pass an int for reproducible output across multiple function calls.
        shuffle : bool, default=True
            Whether or not to shuffle the data before splitting. If shuffle=False
            then stratify must be None.

    Returns:
        splitting : list, length=2 * len(arrays)
            List containing train-test split of inputs.
    """
    n_samples = len(arrays[0])
    if random_state is not None:
        np.random.seed(random_state)

    indices = np.arange(n_samples)
    if shuffle:
        np.random.shuffle(indices)

    if isinstance(test_size, float):
        test_size = int(n_samples * test_size)

    test_indices = indices[:test_size]
    train_indices = indices[test_size:]

    train_arrays = [np.take(arr, train_indices, axis=0) for arr in arrays]
    test_arrays = [np.take(arr, test_indices, axis=0) for arr in arrays]

    return [*train_arrays, *test_arrays]