import numpy as np

class Perceptron:
    """
    Perceptron: A class for implementing a Perceptron classifier.

    This class implements a simple Perceptron classifier for binary classification.

    Attributes
    ----------
    input_dim : int
        The dimensionality of the input data.
    learning_rate : float, optional (default=0.01)
        The learning rate for updating the weights during training.
    weights : array-like, shape (input_dim,)
        The weights associated with each feature.
    bias : float
        The bias term of the Perceptron.

    Methods
    -------
    __init__(self, input_dim, learning_rate=0.01)
        Initializes the Perceptron object with the specified parameters.
    _activation(self, x)
        Computes the activation function for a given input.
    fit(self, X, y, epochs=100)
        Trains the Perceptron on the given training data.
    predict(self, X)
        Predicts target values for the input data.
    """

    def __init__(self, input_dim, learning_rate=0.01):
        """
        Initializes the Perceptron object with the specified parameters.

        Parameters
        ----------
        input_dim : int
            The dimensionality of the input data.
        learning_rate : float, optional (default=0.01)
            The learning rate for updating the weights during training.
        """
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.weights = np.zeros(input_dim)
        self.bias = 0

    def _activation(self, x):
        """
        Computes the activation function for a given input.

        Parameters
        ----------
        x : float
            The input value.

        Returns
        -------
        int
            The binary output of the activation function.
        """
        return 1 if x >= 0 else 0

    def fit(self, X, y, epochs=100):
        """
        Trains the Perceptron on the given training data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values (class labels).
        epochs : int, optional (default=100)
            The number of training epochs.
        """
        for _ in range(epochs):
            for xi, target in zip(X, y):
                linear_output = np.dot(xi, self.weights) + self.bias
                prediction = self._activation(linear_output)
                update = self.learning_rate * (target - prediction)
                self.weights += update * xi
                self.bias += update

    def predict(self, X):
        """
        Predicts target values for the input data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        array-like, shape (n_samples,)
            The predicted class labels.
        """
        linear_output = np.dot(X, self.weights) + self.bias
        return np.array([self._activation(x) for x in linear_output])
