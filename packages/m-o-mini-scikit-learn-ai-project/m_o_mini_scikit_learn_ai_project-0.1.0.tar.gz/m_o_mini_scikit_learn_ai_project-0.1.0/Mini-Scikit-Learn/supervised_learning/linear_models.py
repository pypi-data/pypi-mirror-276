import sys
sys.path.append(r'c:\Users\mahah\OneDrive\Desktop\Mini-Scikit-Learn')
from base.predictor import Predictor
import numpy as np

class LinearRegression(Predictor):
    def __init__(self):
        """
        Initialize linear regression model parameters.
        """
        super().__init__()
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """
        Fit the linear regression model to the training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input training data.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        self : LinearRegression
            The fitted model.
        """
        X = np.insert(X, 0, 1, axis=1)  
        self.weights = np.linalg.inv(X.T @ X) @ X.T @ y
        self.bias = self.weights[0]
        self.weights = self.weights[1:]
        return self

    def predict(self, X):
        """
        Predict target values for samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y_pred : array-like of shape (n_samples,)
            Predicted target values.
        """
        if self.weights is None or self.bias is None:
            print("Warning: This LinearRegression instance is not fitted yet. Returning zeros as predictions.")
            return np.zeros(X.shape[0])
        else:
            return X @ self.weights + self.bias



class LogisticRegression(Predictor):
    def __init__(self, learning_rate=0.01, max_iter=1000, tol=1e-4):
        """
        Initialize logistic regression model parameters.

        Parameters
        ----------
        learning_rate : float, default=0.01
            The learning rate used in gradient descent optimization.
        max_iter : int, default=1000
            The maximum number of iterations for gradient descent optimization.
        tol : float, default=1e-4
            The tolerance for the change in model parameters to determine convergence.
        """
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        """
        Fit the logistic regression model to the training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input training data.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        self : LogisticRegression
            The fitted model.
        """
        # Initialize parameters
        self.coef_ = np.zeros(X.shape[1])
        self.intercept_ = 0

        # Gradient descent
        for _ in range(self.max_iter):
            prev_coef = np.copy(self.coef_)
            prev_intercept = self.intercept_

            # Compute predictions
            z = np.dot(X, self.coef_) + self.intercept_
            y_pred = self._sigmoid(z)

            # Compute gradients
            gradient_coef = np.dot(X.T, (y_pred - y)) / len(y)
            gradient_intercept = np.mean(y_pred - y)

            # Update parameters
            self.coef_ -= self.learning_rate * gradient_coef
            self.intercept_ -= self.learning_rate * gradient_intercept

            # Check for convergence
            if np.linalg.norm(prev_coef - self.coef_) < self.tol and abs(prev_intercept - self.intercept_) < self.tol:
                break

        return self

    def predict(self, X):
        """
        Predict class labels for samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y_pred : array-like of shape (n_samples,)
            Predicted class labels.
        """
        if self.coef_ is None or self.intercept_ is None:
            raise RuntimeError("The model has not been fitted yet.")
        z = np.dot(X, self.coef_) + self.intercept_
        y_pred = self._sigmoid(z)
        return (y_pred >= 0.5).astype(int)

    def _sigmoid(self, z):
        """
        Compute the sigmoid function.

        Parameters
        ----------
        z : array-like
            The input values.

        Returns
        -------
        sigmoid : array-like
            The output of the sigmoid function.
        """
        return 1 / (1 + np.exp(-z))
