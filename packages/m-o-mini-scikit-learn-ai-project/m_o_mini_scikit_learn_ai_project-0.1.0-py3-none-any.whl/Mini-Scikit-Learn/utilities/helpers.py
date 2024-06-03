import numpy as np

def extract_categorical_features(data):
    """
    Extract categorical features from the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.

    Returns:
    - DataFrame: A DataFrame containing only the categorical features.
    """
    categorical_features = data.select_dtypes(include=['object', 'category'])
    return categorical_features


def extract_numerical_features(data):
    """
    Extract numerical features from the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.

    Returns:
    - DataFrame: A DataFrame containing only the numerical features.
    """
    numerical_features = data.select_dtypes(include=[np.number])
    return numerical_features


