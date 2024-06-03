import numpy as np
import itertools
from sklearn.model_selection import KFold
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

class GridSearch:
    """
    GridSearch: A class for performing grid search with cross-validation.

    This class performs an exhaustive search over a specified parameter grid for an estimator,
    evaluating each combination using cross-validation and selecting the parameters that yield
    the best mean cross-validated score.

    Attributes
    ----------
    estimator : estimator object
        The estimator to be tuned.
    param_grid : dict
        Dictionary with parameters names as keys and lists of parameter settings to try as values.
    cv : int, cross-validation generator or an iterable, optional (default=5)
        Determines the cross-validation splitting strategy.
        - None, to use the default 5-fold cross-validation.
        - Integer, to specify the number of folds.
        - An object to be used as a cross-validation generator.
    random_state : int or None, optional (default=None)
        Controls the random seed for shuffling.

    Methods
    -------
    fit(self, X, y)
        Fit the grid search with the specified training data and labels.
    """

    def _init_(self, estimator, param_grid, cv=5, random_state=None):
        """
        Initializes the GridSearch object.

        Parameters
        ----------
        estimator : estimator object
            The estimator to be tuned.
        param_grid : dict
            Dictionary with parameters names as keys and lists of parameter settings to try as values.
        cv : int, cross-validation generator or an iterable, optional (default=5)
            Determines the cross-validation splitting strategy.
            - None, to use the default 5-fold cross-validation.
            - Integer, to specify the number of folds.
            - An object to be used as a cross-validation generator.
        random_state : int or None, optional (default=None)
            Controls the random seed for shuffling.
        """
        self.estimator = estimator
        self.param_grid = param_grid
        self.cv = cv
        self.random_state = random_state

    def fit(self, X, y):
        """
        Fit the grid search with the specified training data and labels.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values (class labels).
        """
        best_score = float("-inf")
        best_params = None

        # Create KFold instance with random_state for reproducibility
        kf = KFold(n_splits=self.cv, shuffle=True, random_state=self.random_state)

        for params in self._generate_param_combinations():
            fold_scores = []

            for train_index, test_index in kf.split(X):
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]

                estimator = self.estimator(**params)
                estimator.fit(X_train, y_train)

                score = estimator.score(X_test, y_test)
                fold_scores.append(score)

                # Debug: Print fold scores
                print(f"Params: {params}, Fold Score: {score}")

            mean_score = np.mean(fold_scores)
            print(f"Params: {params}, Mean CV Score: {mean_score}")  # Debug: Print mean CV score

            if mean_score > best_score:
                best_score = mean_score
                best_params = params

        # Fit the best estimator using the entire dataset
        self.best_estimator_ = self.estimator(**best_params)
        self.best_estimator_.fit(X, y)
        self.best_params_ = best_params  # Store the best parameters

    def _generate_param_combinations(self):
        """
        Generates all possible combinations of parameters from the parameter grid.

        Yields
        ------
        dict
            Dictionary containing parameter names and their corresponding values for each combination.
        """
        param_names = list(self.param_grid.keys())
        param_values = list(self.param_grid.values())

        for combination in itertools.product(*param_values):
            yield dict(zip(param_names, combination))
