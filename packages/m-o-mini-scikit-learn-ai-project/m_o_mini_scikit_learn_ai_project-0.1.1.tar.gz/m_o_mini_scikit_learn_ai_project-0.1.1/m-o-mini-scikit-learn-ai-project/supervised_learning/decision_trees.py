import sys
sys.path.append(r'c:\Users\mahah\OneDrive\Desktop\Mini-Scikit-Learn')
import numpy as np
from base.predictor import Predictor

class DecisionTreeClassifier(Predictor):
    """
    DecisionTreeClassifier: A class for implementing a decision tree classifier.

    This class implements a decision tree classifier, which is a predictive model
    that maps input features to predicted target labels. It recursively splits the
    input space into regions and assigns labels to each region based on the majority
    class of the training samples in that region.

    Attributes
    ----------
    max_depth : int or None, default=None
        The maximum depth of the tree. If None, the tree is grown until all leaves
        are pure or until all leaves contain less than the minimum samples required
        to split.
    tree_ : dict or None
        The constructed decision tree represented as a dictionary.

    Methods
    -------
    __init__(self, max_depth=None)
        Initializes the DecisionTreeClassifier object.
    fit(self, X, y)
        Fits the decision tree classifier to the training data.
    predict(self, X)
        Predicts the target labels for the input data.
    _build_tree(self, X, y, depth)
        Recursively builds the decision tree.
    _find_best_split(self, X, y)
        Finds the best feature and threshold for splitting the data.
    _calculate_score(self, left_labels, right_labels)
        Calculates the score for splitting the data.
    _predict(self, x, tree)
        Recursively predicts the target label for a single sample.
    """

    def __init__(self, max_depth=None):
        """
        Initializes the DecisionTreeClassifier object.

        Parameters
        ----------
        max_depth : int or None, default=None
            The maximum depth of the tree. If None, the tree is grown until all leaves
            are pure or until all leaves contain less than the minimum samples required
            to split.
        """
        super().__init__()
        self.max_depth = max_depth
        self.tree_ = None

    def fit(self, X, y):
        """
        Fits the decision tree classifier to the training data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target labels.

        Returns
        -------
        self : object
            Returns self.
        """
        self.tree_ = self._build_tree(X, y, depth=0)
        return self

    def predict(self, X):
        """
        Predicts the target labels for the input data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y_pred : array-like, shape (n_samples,)
            The predicted target labels.
        """
        if self.tree_ is None:
            raise RuntimeError("The model has not been fitted yet.")
        return np.array([self._predict(x, self.tree_) for x in X])

    def _build_tree(self, X, y, depth):
        """
        Recursively builds the decision tree.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.
        y : array-like, shape (n_samples,)
            The target labels.
        depth : int
            The current depth of the tree.

        Returns
        -------
        tree : dict
            The constructed decision tree represented as a dictionary.
        """
        if depth == self.max_depth or len(np.unique(y)) == 1:
            return {'leaf': True, 'value': np.mean(y)}

        best_split = self._find_best_split(X, y)
        if best_split is None:
            return {'leaf': True, 'value': np.mean(y)}

        left_indices = X[:, best_split['feature']] <= best_split['threshold']
        right_indices = ~left_indices

        left_tree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_tree = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return {'leaf': False,
                'feature': best_split['feature'],
                'threshold': best_split['threshold'],
                'left': left_tree,
                'right': right_tree}

    def _find_best_split(self, X, y):
        """
        Finds the best feature and threshold for splitting the data.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.
        y : array-like, shape (n_samples,)
            The target labels.

        Returns
        -------
        best_split : dict or None
            A dictionary containing the best feature and threshold for splitting
            the data, or None if no suitable split is found.
        """
        best_split = None
        best_score = -float('inf')

        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_indices = X[:, feature] <= threshold
                right_indices = ~left_indices

                score = self._calculate_score(y[left_indices], y[right_indices])
                if score > best_score:
                    best_split = {'feature': feature, 'threshold': threshold}
                    best_score = score

        return best_split

    def _calculate_score(self, left_labels, right_labels):
        """
        Calculates the score for splitting the data.

        Parameters
        ----------
        left_labels : array-like
            The target labels of the left child node.
        right_labels : array-like
            The target labels of the right child node.

        Returns
        -------
        score : float
            The score for splitting the data.
        """
        if len(left_labels) == 0 or len(right_labels) == 0:
            return -float('inf')

        # Calculate variance reduction
        total_var = np.var(np.concatenate((left_labels, right_labels)))
        left_var = np.var(left_labels) * len(left_labels)
        right_var = np.var(right_labels) * len(right_labels)
        return total_var - (left_var + right_var) / len(np.concatenate((left_labels, right_labels)))
    
    
    def _predict(self, x, tree):
        """
        Recursively predicts the target label for a given sample.

        This method traverses the decision tree recursively to predict the target
        label for a given input sample.

        Parameters
        ----------
        x : array-like, shape (n_features,)
            The input sample for which the target label is to be predicted.
        tree : dict
            The subtree of the decision tree to be traversed.

        Returns
        -------
        value : float
            The predicted target label.
        """
        if tree['leaf']:
            return tree['value']
        else:
            if x[tree['feature']] <= tree['threshold']:
                return self._predict(x, tree['left'])
            else:
                return self._predict(x, tree['right'])
