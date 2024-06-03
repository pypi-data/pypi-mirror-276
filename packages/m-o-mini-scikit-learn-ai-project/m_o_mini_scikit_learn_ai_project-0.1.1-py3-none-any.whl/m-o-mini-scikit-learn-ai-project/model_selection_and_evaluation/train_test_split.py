import numpy as np

def train_test_split(X, y, test_size=0.2, random_state=None):
    """
    Split the dataset into train and test sets.

    Parameters:
    - X: array-like, feature matrix
    - y: array-like, target vector
    - test_size: float, optional (default=0.2), proportion of the dataset to include in the test split
    - random_state: int or None, optional (default=None), seed for random number generation

    Returns:
    - X_train: array-like, training features
    - X_test: array-like, testing features
    - y_train: array-like, training targets
    - y_test: array-like, testing targets
    """
    if random_state:
        np.random.seed(random_state)
    
    num_samples = X.shape[0]
    num_test_samples = int(test_size * num_samples)

    indices = np.arange(num_samples)
    np.random.shuffle(indices)

    test_indices = indices[:num_test_samples]
    train_indices = indices[num_test_samples:]

    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]

    return X_train, X_test, y_train, y_test
