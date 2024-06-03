import numpy as np
from baseNeu import BaseNeuralNetwork

class FeedforwardNeuralNetwork(BaseNeuralNetwork):
    """
    FeedforwardNeuralNetwork: A class for implementing a feedforward neural network.

    This class implements a feedforward neural network with customizable architecture,
    including the number of input and output neurons, and the number of hidden layers
    and neurons in each hidden layer.

    Attributes
    ----------
    input_dim : int
        The dimensionality of the input data.
    hidden_layers : list
        A list containing the number of neurons in each hidden layer.
    output_dim : int
        The dimensionality of the output data.
    weights : list
        A list containing weight matrices for each layer.
    biases : list
        A list containing bias vectors for each layer.
    activation_functions : list
        A list containing activation functions for each layer.
    loss_history : list
        A list containing the loss value at each epoch during training.
    accuracy_history : list
        A list containing the accuracy value at each epoch during training.

    Methods
    -------
    __init__(self, input_dim, hidden_layers, output_dim)
        Initializes the FeedforwardNeuralNetwork object with the specified architecture.
    fit(self, X, y, epochs=100, learning_rate=0.01)
        Trains the neural network on the given training data.
    predict(self, X)
        Predicts target values for the input data.
    evaluate(self, X, y)
        Evaluates the performance of the model on the given test data.
    """

    def __init__(self, input_dim, hidden_layers, output_dim):
        """
        Initializes the FeedforwardNeuralNetwork object with the specified architecture.

        Parameters
        ----------
        input_dim : int
            The dimensionality of the input data.
        hidden_layers : list
            A list containing the number of neurons in each hidden layer.
        output_dim : int
            The dimensionality of the output data.
        """
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.output_dim = output_dim
        self.weights = []
        self.biases = []
        self.activation_functions = []
        self.loss_history = []
        self.accuracy_history = []

    def _initialize_parameters(self):
        # Code omitted for brevity
        pass

    def _sigmoid(self, x):
        """
        Computes the sigmoid activation function.

        Parameters
        ----------
        x : array-like
            The input data.

        Returns
        -------
        array-like
            The output of the sigmoid function applied to the input data.
        """
        return 1 / (1 + np.exp(-x))

    def _sigmoid_derivative(self, x):
        """
        Computes the derivative of the sigmoid activation function.

        Parameters
        ----------
        x : array-like
            The input data.

        Returns
        -------
        array-like
            The derivative of the sigmoid function applied to the input data.
        """
        return x * (1 - x)

    def _forward_propagation(self, X):
        """
        Performs forward propagation through the neural network.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input data.

        Returns
        -------
        array-like
            The output of the neural network after forward propagation.
        """
        layer_output = X
        self.layer_outputs = [layer_output]
        for i in range(len(self.hidden_layers) + 1):
            layer_input = np.dot(layer_output, self.weights[i]) + self.biases[i]
            layer_output = self.activation_functions[i](layer_input)
            self.layer_outputs.append(layer_output)
        return layer_output

    def _backward_propagation(self, X, y, learning_rate):
        """
        Performs backward propagation through the neural network.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input data.
        y : array-like, shape (n_samples,)
            The target values (class labels).
        learning_rate : float
            The learning rate for updating the weights during backpropagation.
        """
        error = y - self.layer_outputs[-1]
        delta = error * self._sigmoid_derivative(self.layer_outputs[-1])
        for i in range(len(self.hidden_layers), -1, -1):
            self.weights[i] += np.dot(self.layer_outputs[i].T, delta) * learning_rate
            self.biases[i] += np.sum(delta, axis=0) * learning_rate
            error = np.dot(delta, self.weights[i].T)
            delta = error * self._sigmoid_derivative(self.layer_outputs[i])

    def fit(self, X, y, epochs=100, learning_rate=0.01):
        """
        Trains the neural network on the given training data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values (class labels).
        epochs : int, optional (default=100)
            The number of training epochs.
        learning_rate : float, optional (default=0.01)
            The learning rate for updating the weights during training.
        """
        self._initialize_parameters()
        for _ in range(epochs):
            output = self._forward_propagation(X)
            self._backward_propagation(X, y, learning_rate)
            self.loss_history.append(np.mean(np.abs(y - output)))
            predictions = (output > 0.5).astype(int)
            accuracy = np.mean(predictions == y)
            self.accuracy_history.append(accuracy)

    def predict(self, X):
        """
        Predicts target values for the input data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        array-like
            The predicted class labels.
        """
        return self._forward_propagation(X)

    def evaluate(self, X, y):
        """
        Evaluates the performance of the model on the given test data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.
        y : array-like, shape (n_samples,)
            The true target values.

        Returns
        -------
        float
            The accuracy of the model on the test data.
        """
        predictions = (self.predict(X) > 0.5).astype(int)
        accuracy = np.mean(predictions == y)
        return accuracy
