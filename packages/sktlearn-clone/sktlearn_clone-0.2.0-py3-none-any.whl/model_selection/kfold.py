import numpy as np

class KFold:
    def __init__(self, n_splits=5, shuffle=False, random_state=None):
        """
        K-Fold cross-validator.

        Parameters
        ----------
        n_splits : int, default=5
            Number of folds. Must be at least 2.

        shuffle : bool, default=False
            Whether to shuffle the data before splitting into batches.
            Note that the samples within each split will not be shuffled.

        random_state : int, RandomState instance or None, default=None
            When `shuffle` is True, `random_state` affects the ordering of the
            indices, which controls the randomness of each fold. Otherwise, this
            parameter has no effect.
            Pass an int for reproducible output across multiple function calls.
        """
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

    def split(self, X, y=None, groups=None):
        """
        Generate indices to split data into training and test sets.

        Parameters
        ----------
        X : array-like
            The data to split.

        y : array-like, default=None
            Ignored. Exists only for compatibility.

        groups : array-like, default=None
            Ignored. Exists only for compatibility.

        Yields
        ------
        train_index : ndarray
            The training set indices for that split.

        test_index : ndarray
            The testing set indices for that split.
        """
        n_samples = len(X)
        indices = np.arange(n_samples)
        if self.shuffle:
            rng = np.random.RandomState(self.random_state)
            rng.shuffle(indices)

        fold_sizes = np.full(self.n_splits, n_samples // self.n_splits, dtype=int)
        fold_sizes[: n_samples % self.n_splits] += 1

        current = 0
        for fold_size in fold_sizes:
            start, stop = current, current + fold_size
            test_index = indices[start:stop]
            train_index = np.concatenate((indices[:start], indices[stop:]))
            yield train_index, test_index
            current = stop
            