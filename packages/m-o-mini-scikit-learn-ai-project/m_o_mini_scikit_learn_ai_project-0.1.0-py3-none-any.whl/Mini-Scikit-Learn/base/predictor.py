"""
base/predictor.py

This module contains the Predictor class, which is a base class for predictive models.
It inherits from the Estimator class and adds methods specific to prediction tasks.

Classes:
    Predictor: A base class for creating custom predictive models.
"""

from base.estimator import Estimator

class Predictor(Estimator):
    """
    A base class for creating custom predictive models.

    Inherits from the Estimator class and provides additional methods for 
    prediction tasks such as `predict`, `fit_predict`, and `score`.

    Methods
    -------
    __init__():
        Initializes the predictor.
        
    fit(X, y):
        Fits the predictor to the data. This method must be implemented by subclasses.
        
    predict(X):
        Predicts the target values for given input data. This method must be implemented by subclasses.
        
    fit_predict(X, y):
        Fits the predictor to the data and then predicts the target values.
        
    score(X, y):
        Evaluates the performance of the predictor on the given test data and labels.
    """

    def __init__(self):
        """
        Initializes the Predictor object.

        The constructor method for the Predictor class, which calls the constructor
        of the base Estimator class.
        """
        super().__init__()

    def fit(self, X, y):
        """
        Fits the predictor to the data.

        This method must be implemented by subclasses to provide the fitting logic.

        Parameters
        ----------
        X : array-like
            The training input samples.
        y : array-like
            The target values (class labels in classification, real numbers in regression).

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """
        raise NotImplementedError("fit method is not implemented")

    def predict(self, X):
        """
        Predicts the target values for given input data.

        This method must be implemented by subclasses to provide the prediction logic.

        Parameters
        ----------
        X : array-like
            The input samples for which to predict the target values.

        Returns
        -------
        array-like
            The predicted target values.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """
        raise NotImplementedError("predict method is not implemented")

    def fit_predict(self, X, y):
        """
        Fits the predictor to the data and then predicts the target values.

        Combines the `fit` and `predict` methods for convenience.

        Parameters
        ----------
        X : array-like
            The input samples.
        y : array-like
            The target values.

        Returns
        -------
        array-like
            The predicted target values after fitting the model.

        Example
        -------
        predictor = MyPredictor()
        predictions = predictor.fit_predict(X_train, y_train)
        """
        self.fit(X, y)
        return self.predict(X)

    def score(self, X, y):
        """
        Evaluates the performance of the predictor on the given test data and labels.

        This method should be implemented by subclasses to provide the evaluation logic.

        Parameters
        ----------
        X : array-like
            The test input samples.
        y : array-like
            The true target values for the test samples.

        Returns
        -------
        float
            The evaluation score (e.g., accuracy for classification, mean squared error for regression).

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """
        predictions = self.predict(X)
        # Implement scoring method based on your requirements
        # For example, if it's regression, you can use mean squared error
        # For classification, you can use accuracy, etc.
        raise NotImplementedError("score method is not implemented")
