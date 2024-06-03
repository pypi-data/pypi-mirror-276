"""
base/transformer.py

This module contains the Transformer class, which is a base class for data transformation models.
It inherits from the Estimator class and adds methods specific to data transformation tasks.

Classes:
    Transformer: A base class for creating custom data transformation models.
"""

from base.estimator import Estimator

class Transformer(Estimator):
    """
    A base class for creating custom data transformation models.

    Inherits from the Estimator class and provides additional methods for 
    transformation tasks such as `transform` and `fit_transform`.

    Methods
    -------
    __init__():
        Initializes the transformer.
        
    fit(X, y=None):
        Fits the transformer to the data. This method must be implemented by subclasses.
        
    transform(X, y=None):
        Transforms the input data. This method must be implemented by subclasses.
        
    fit_transform(X, y=None):
        Fits the transformer to the data and then transforms the input data.
    """

    def __init__(self):
        """
        Initializes the Transformer object.

        The constructor method for the Transformer class, which calls the constructor
        of the base Estimator class.
        """
        super().__init__()

    def fit(self, X, y=None):
        """
        Fits the transformer to the data.

        This method must be implemented by subclasses to provide the fitting logic.

        Parameters
        ----------
        X : array-like
            The training input samples.
        y : array-like, optional
            The target values. Default is None.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """
        raise NotImplementedError("fit method is not implemented")

    def transform(self, X, y=None):
        """
        Transforms the input data.

        This method must be implemented by subclasses to provide the transformation logic.

        Parameters
        ----------
        X : array-like
            The input samples to transform.
        y : array-like, optional
            The target values. Default is None.

        Returns
        -------
        array-like
            The transformed input samples.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """
        raise NotImplementedError("transform method is not implemented")

    def fit_transform(self, X, y=None):
        """
        Fits the transformer to the data and then transforms the input data.

        Combines the `fit` and `transform` methods for convenience.

        Parameters
        ----------
        X : array-like
            The input samples.
        y : array-like, optional
            The target values. Default is None.

        Returns
        -------
        array-like
            The transformed input samples after fitting the model.

        Example
        -------
        transformer = MyTransformer()
        transformed_data = transformer.fit_transform(X_train)
        """
        self.fit(X, y)
        return self.transform(X, y)
