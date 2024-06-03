"""
base/estimator.py

This module contains the base class for estimators. Estimators are used to fit data and make predictions.

Classes:
    Estimator: A base class for creating custom estimators. It includes methods for setting and getting parameters.
"""

class Estimator:
    """
    A base class for creating custom estimators.

    Methods
    -------
    __init__():
        Initializes the estimator. This is the constructor method.
        
    fit(X, y):
        Fits the estimator to the data. This method must be implemented by subclasses.
        
    set_params(**params):
        Sets the parameters of the estimator.
        
    get_params(deep=True):
        Gets the parameters of the estimator.

    Usage
    -----
    To create a custom estimator, inherit from this class and implement the fit method:
    
    class MyEstimator(Estimator):
        def fit(self, X, y):
            # Implementation of fitting algorithm
            pass
    """

    def __init__(self):
        """
        Initializes the Estimator object.

        The constructor method for the Estimator class.
        """
        pass

    def fit(self, X, y):
        """
        Fits the estimator to the data. 

        This method must be implemented by subclasses.

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

    def set_params(self, **params):
        """
        Sets the parameters of the estimator.

        Parameters
        ----------
        **params : keyword arguments
            Estimator parameters.

        Example
        -------
        est = Estimator()
        est.set_params(param1=value1, param2=value2)
        """
        for param, value in params.items():
            setattr(self, param, value)

    def get_params(self, deep=True):
        """
        Gets the parameters of the estimator.

        Parameters
        ----------
        deep : bool, optional, default=True
            If True, will return the parameters for this estimator and contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Dictionary of parameter names mapped to their values.

        Example
        -------
        est = Estimator()
        params = est.get_params()
        """
        return {key: getattr(self, key) for key in self.__dict__}
