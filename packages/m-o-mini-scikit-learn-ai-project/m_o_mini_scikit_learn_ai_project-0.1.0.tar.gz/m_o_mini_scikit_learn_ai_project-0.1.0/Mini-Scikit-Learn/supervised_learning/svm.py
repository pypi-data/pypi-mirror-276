import numpy as np
from base.predictor import Predictor

class SVMClassifier(Predictor):
    def __init__(self, C=1.0, max_iter=1000, tol=1e-3):
        """
        Support Vector Machine (SVM) classifier.

        Parameters
        ----------
        C : float, optional (default=1.0)
            Regularization parameter.
        max_iter : int, optional (default=1000)
            Maximum number of iterations for optimization.
        tol : float, optional (default=1e-3)
            Tolerance for stopping criteria.

        Attributes
        ----------
        w : array-like of shape (n_features,)
            Coefficients of the support vector.
        b : float
            Intercept of the decision boundary.

        Notes
        -----
        The class labels should be in the form of {-1, 1}.

        References
        ----------
        - Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine learning, 20(3), 273-297.
        """
        super().__init__()
        self.C = C
        self.max_iter = max_iter
        self.tol = tol
        self.w = None
        self.b = None

    def fit(self, X, y):
        """
        Fit the SVM classifier to the training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        self : SVMClassifier
            The fitted estimator.
        """
        # Ensure y is in the form of {-1, 1}
        y = np.where(y == 0, -1, 1)
        n_samples, n_features = X.shape

        # Initialize weights and bias
        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.max_iter):
            for idx, x_i in enumerate(X):
                condition = y[idx] * (np.dot(x_i, self.w) + self.b) >= 1
                if condition:
                    self.w -= self.tol * (2 * self.w / self.max_iter)
                else:
                    self.w -= self.tol * (2 * self.w / self.max_iter - np.dot(x_i, y[idx]))
                    self.b -= self.tol * y[idx]

        return self

    def predict(self, X):
        """
        Perform classification on samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y_pred : array-like of shape (n_samples,)
            Predicted class labels.
        """
        linear_output = np.dot(X, self.w) + self.b
        return np.where(linear_output >= 0, 1, 0)
