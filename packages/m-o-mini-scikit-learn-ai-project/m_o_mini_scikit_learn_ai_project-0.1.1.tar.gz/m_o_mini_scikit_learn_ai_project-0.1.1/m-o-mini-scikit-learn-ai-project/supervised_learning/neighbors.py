import numpy as np

from base.predictor import Predictor


class KNeighbors(Predictor):
    def __init__(self, n_neighbors=5, mode='classification'):
        """
        K Nearest Neighbors classifier/regressor.

        Parameters
        ----------
        n_neighbors : int, optional (default=5)
            Number of neighbors to consider.
        mode : {'classification', 'regression'}, optional (default='classification')
            Mode of the K Nearest Neighbors algorithm.

        Attributes
        ----------
        X_train : array-like of shape (n_samples, n_features)
            The training input samples.
        y_train : array-like of shape (n_samples,)
            The target values.

        Raises
        ------
        ValueError
            If an invalid mode is provided.

        Notes
        -----
        Supported modes:
            - 'classification' for classification tasks.
            - 'regression' for regression tasks.
        """
        super().__init__()
        self.n_neighbors = n_neighbors
        self.mode = mode
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        """
        Fit the K Nearest Neighbors model to the training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        self : KNeighbors
            The fitted estimator.
        """
        self.X_train = X
        self.y_train = y
        return self

    def predict(self, X):
        """
        Perform classification/regression on samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y_pred : array-like
            Predicted target values.
        """
        predictions = []
        for sample in X:
            distances = np.sqrt(np.sum((self.X_train - sample) ** 2, axis=1))
            nearest_neighbors_indices = np.argsort(distances)[:self.n_neighbors]
            nearest_neighbors_labels = self.y_train[nearest_neighbors_indices]

            if self.mode == 'classification':
                predictions.append(self._predict_classification(nearest_neighbors_labels))
            elif self.mode == 'regression':
                predictions.append(self._predict_regression(nearest_neighbors_labels))
            else:
                raise ValueError("Invalid mode. Supported modes: 'classification', 'regression'")

        return np.array(predictions)

    def _predict_classification(self, nearest_neighbors_labels):
        """
        Perform classification based on the nearest neighbors' labels.

        Parameters
        ----------
        nearest_neighbors_labels : array-like of shape (n_neighbors,)
            The labels of the nearest neighbors.

        Returns
        -------
        label : array-like
            Predicted class label.
        """
        unique_labels, label_counts = np.unique(nearest_neighbors_labels, return_counts=True)
        return unique_labels[np.argmax(label_counts)]

    def _predict_regression(self, nearest_neighbors_labels):
        """
        Perform regression based on the nearest neighbors' labels.

        Parameters
        ----------
        nearest_neighbors_labels : array-like of shape (n_neighbors,)
            The labels of the nearest neighbors.

        Returns
        -------
        mean_label : float
            Predicted target value.
        """
        return np.mean(nearest_neighbors_labels)


class KNeighborsClassifier(KNeighbors):
    def __init__(self, n_neighbors=5):
        """
        K Nearest Neighbors classifier.

        Parameters
        ----------
        n_neighbors : int, optional (default=5)
            Number of neighbors to consider.
        """
        super().__init__(n_neighbors=n_neighbors, mode='classification')


class KNeighborsRegressor(KNeighbors):
    def __init__(self, n_neighbors=5):
        """
        K Nearest Neighbors regressor.

        Parameters
        ----------
        n_neighbors : int, optional (default=5)
            Number of neighbors to consider.
        """
        super().__init__(n_neighbors=n_neighbors, mode='regression')
