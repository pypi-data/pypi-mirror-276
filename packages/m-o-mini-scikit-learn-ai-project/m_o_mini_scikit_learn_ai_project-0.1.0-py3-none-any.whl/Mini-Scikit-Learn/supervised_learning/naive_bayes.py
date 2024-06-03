import numpy as np

from base.predictor import Predictor


class NaiveBayesClassifier(Predictor):
    def __init__(self):
        """
        Initialize the Naive Bayes classifier.
        """
        super().__init__()
        self.class_prior_ = None
        self.class_count_ = None
        self.feature_log_prob_ = None

    def fit(self, X, y):
        """
        Fit the Naive Bayes classifier to the training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input training data.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        self : NaiveBayesClassifier
            The fitted classifier.
        """
        self.classes_ = np.unique(y)
        self.class_prior_ = np.zeros(len(self.classes_))
        self.class_count_ = np.zeros(len(self.classes_))
        self.feature_log_prob_ = []

        for i, c in enumerate(self.classes_):
            X_class = X[y == c]
            self.class_prior_[i] = len(X_class) / len(X)
            self.class_count_[i] = len(X_class)
            feature_prob = np.mean(X_class, axis=0)
            self.feature_log_prob_.append(np.log(feature_prob + 1e-10))

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
            Predicted target values.
        """
        scores = np.zeros((X.shape[0], len(self.classes_)))
        for i, c in enumerate(self.classes_):
            log_prior = np.log(self.class_prior_[i])
            log_likelihood = self._predict_proba_log(X, i)  # No need to sum here
            scores[:, i] = log_prior + log_likelihood
        return self.classes_[np.argmax(scores, axis=1)]

    def _predict_proba_log(self, X, class_idx):
        """
        Compute the log probability estimates for the test data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.
        class_idx : int
            Index of the class.

        Returns
        -------
        log_proba : array-like of shape (n_samples,)
            Log probability estimates.
        """
        return np.dot(X, self.feature_log_prob_[class_idx])
