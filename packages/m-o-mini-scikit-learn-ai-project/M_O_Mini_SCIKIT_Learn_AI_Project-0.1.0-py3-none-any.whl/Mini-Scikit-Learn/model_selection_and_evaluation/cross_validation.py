# crossvalidation.py
import numpy as np

def cross_val_predict(estimator, X, y, cv=5, method='predict'):
    """
    Generates cross-validated predictions for each input sample.

    Parameters
    ----------
    estimator : object
        The estimator object implementing the 'fit' and 'predict' methods.
    X : array-like, shape (n_samples, n_features)
        The input samples.
    y : array-like, shape (n_samples,)
        The target values.
    cv : int or cross-validation generator, optional (default=5)
        Determines the cross-validation splitting strategy.
        If an integer, specifies the number of folds.
        If a cross-validation generator, provides the cross-validation iterator.
    method : {'predict', 'predict_proba'}, optional (default='predict')
        The method used for generating predictions.
        - 'predict': Returns class labels.
        - 'predict_proba': Returns class probabilities.

    Returns
    -------
    array-like, shape (n_samples,)
        Cross-validated predictions for each input sample.
    """
    n_samples = X.shape[0]
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    fold_sizes = np.full(cv, n_samples // cv, dtype=int)
    fold_sizes[:n_samples % cv] += 1
    
    current = 0
    predictions = np.zeros(n_samples)
    
    for fold_size in fold_sizes:
        start, stop = current, current + fold_size
        test_indices = indices[start:stop]
        train_indices = np.concatenate((indices[:start], indices[stop:]))
        
        X_train, y_train = X[train_indices], y[train_indices]
        X_test = X[test_indices]
        
        estimator.fit(X_train, y_train)
        if method == 'predict':
            predictions[test_indices] = estimator.predict(X_test)
        elif method == 'predict_proba':
            predictions[test_indices] = estimator.predict_proba(X_test)[:, 1]  # Assuming binary classification
        
        current = stop
    
    return predictions

class KFold:
    """
    KFold: A class for K-Fold cross-validation.

    This class splits a dataset into K consecutive folds, where each fold is then used as a validation set
    once while the K - 1 remaining folds form the training set.

    Attributes
    ----------
    n_splits : int, optional (default=5)
        The number of folds. Must be at least 2.
    shuffle : bool, optional (default=False)
        Whether to shuffle the data before splitting.
    random_state : int or None, optional (default=42)
        Controls the random seed for shuffling.

    Methods
    -------
    split(self, X)
        Generate indices to split data into training and test set.

    """

    def _init_(self, n_splits=5, shuffle=False, random_state=42):
        """
        Initializes the KFold cross-validator.

        Parameters
        ----------
        n_splits : int, optional (default=5)
            The number of folds. Must be at least 2.
        shuffle : bool, optional (default=False)
            Whether to shuffle the data before splitting.
        random_state : int or None, optional (default=42)
            Controls the random seed for shuffling.
        """
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

    def split(self, X):
        """
        Generate indices to split data into training and test set.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Yields
        ------
        train : ndarray
            The training set indices for that split.
        test : ndarray
            The testing set indices for that split.
        """
        n_samples = len(X)
        indices = np.arange(n_samples)

        if self.shuffle:
            if self.random_state is not None:
                np.random.seed(self.random_state)
            np.random.shuffle(indices)

        fold_sizes = np.full(self.n_splits, n_samples // self.n_splits, dtype=int)
        fold_sizes[:n_samples % self.n_splits] += 1

        current = 0
        for fold_size in fold_sizes:
            start, stop = current, current + fold_size
            test_indices = indices[start:stop]
            train_indices = np.concatenate((indices[:start], indices[stop:]))
            yield train_indices, test_indices
            current = stop
