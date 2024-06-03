# utilities/data_loading.py

import pandas as pd

def load_csv(file_path):
    """
    Load data from a CSV file.

    Parameters:
    - file_path: str, path to the CSV file.

    Returns:
    - pandas DataFrame containing the loaded data.
    """
    return pd.read_csv(file_path)

def load_excel(file_path):
    """
    Load data from an Excel file.

    Parameters:
    - file_path: str, path to the Excel file.

    Returns:
    - pandas DataFrame containing the loaded data.
    """
    return pd.read_excel(file_path)

def load_txt(file_path):
    """
    Load data from a text file.

    Parameters:
    - file_path: str, path to the text file.

    Returns:
    - pandas DataFrame containing the loaded data.
    """
    return pd.read_csv(file_path, delimiter='\t') 
