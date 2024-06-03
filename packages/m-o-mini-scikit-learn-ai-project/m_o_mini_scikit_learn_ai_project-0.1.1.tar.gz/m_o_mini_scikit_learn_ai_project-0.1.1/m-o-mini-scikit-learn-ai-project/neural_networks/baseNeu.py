class BaseNeuralNetwork:
    """
    BaseNeuralNetwork: Abstract base class for neural network models.

    This class defines the interface for neural network models, including methods for fitting,
    predicting, and evaluating the model.

    Methods
    -------
    __init__()
        Initializes the BaseNeuralNetwork object.
    fit(self, X, y)
        Fits the neural network model to the training data.
    predict(self, X)
        Predicts target values for the input data.
    evaluate(self, X, y)
        Evaluates the performance of the model on the given test data.
    """

    def __init__(self):
        """
        Initializes the BaseNeuralNetwork object.
        """
        pass

    def fit(self, X, y):
        """
        Fits the neural network model to the training data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass.
        """
        raise NotImplementedError("fit method must be implemented in subclass")

    def predict(self, X):
        """
        Predicts target values for the input data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass.
        """
        raise NotImplementedError("predict method must be implemented in subclass")

    def evaluate(self, X, y):
        """
        Evaluates the performance of the model on the given test data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.
        y : array-like, shape (n_samples,)
            The true target values.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass.
        """
        raise NotImplementedError("evaluate method must be implemented in subclass")
