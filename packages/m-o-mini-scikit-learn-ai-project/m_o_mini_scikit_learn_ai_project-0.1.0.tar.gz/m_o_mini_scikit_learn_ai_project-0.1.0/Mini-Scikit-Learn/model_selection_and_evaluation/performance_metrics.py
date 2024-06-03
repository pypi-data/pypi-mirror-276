import numpy as np

# Classification Metrics

def accuracy(y_true, y_pred):
    """
    Calculate the accuracy of the model predictions.

    Parameters:
    - y_true (array-like): The true labels.
    - y_pred (array-like): The predicted labels.

    Returns:
    - float: The accuracy score.
    """
    assert len(y_true) == len(y_pred), "Lengths of y_true and y_pred must be the same"
    correct_predictions = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    total_predictions = len(y_true)
    accuracy_score = correct_predictions / total_predictions
    return accuracy_score


def precision(y_true, y_pred):
    """
    Calculate precision score.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: Precision score.
    """
    TP = sum((true == 1 and pred == 1) for true, pred in zip(y_true, y_pred))
    FP = sum((true == 0 and pred == 1) for true, pred in zip(y_true, y_pred))
    if TP + FP == 0:
        return 0
    else:
        return TP / (TP + FP)
    

def recall(y_true, y_pred):
    """
    Calculate recall score.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: Recall score.
    """
    TP = sum((true == 1 and pred == 1) for true, pred in zip(y_true, y_pred))
    FN = sum((true == 1 and pred == 0) for true, pred in zip(y_true, y_pred))
    if TP + FN == 0:
        return 0
    else:
        return TP / (TP + FN)


def f1_score(y_true, y_pred):
    """
    Calculate F1-score.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: F1-score.
    """
    precision_score = precision(y_true, y_pred)
    recall_score = recall(y_true, y_pred)
    if precision_score + recall_score == 0:
        return 0
    else:
        return 2 * (precision_score * recall_score) / (precision_score + recall_score)


def classification_report(y_true, y_pred):
    """
    Generate a classification report with accuracy, precision, recall, and F1-score.

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - dict: A dictionary containing the classification report.
    """
    unique_labels = np.unique(y_true)
    report = {}

    for label in unique_labels:
        TP = sum((true == label and pred == label) for true, pred in zip(y_true, y_pred))
        FP = sum((true != label and pred == label) for true, pred in zip(y_true, y_pred))
        FN = sum((true == label and pred != label) for true, pred in zip(y_true, y_pred))
        TN = sum((true != label and pred != label) for true, pred in zip(y_true, y_pred))

        precision_score = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall_score = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1 = (2 * precision_score * recall_score) / (precision_score + recall_score) if (precision_score + recall_score) > 0 else 0

        report[label] = {
            'precision': precision_score,
            'recall': recall_score,
            'f1-score': f1,
            'support': TP + FN
        }

    accuracy_score = accuracy(y_true, y_pred)
    report['accuracy'] = accuracy_score

    return report


# Regression Metrics

def mean_squared_error(y_true, y_pred):
    """
    Calculate mean squared error (MSE).

    Parameters:
    - y_true (array-like): True labels.
    - y_pred (array-like): Predicted labels.

    Returns:
    - float: MSE.
    """
    mse = np.mean((np.array(y_true) - np.array(y_pred))**2)
    return mse
