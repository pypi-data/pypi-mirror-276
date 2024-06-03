import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def plot_histogram(data, feature_name):
    """
    Plot a histogram of the specified feature in the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.
    - feature_name (str): The name of the feature to plot.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    sns.histplot(data[feature_name], kde=True)
    plt.title(f'Histogram of {feature_name}')
    plt.xlabel(feature_name)
    plt.ylabel('Frequency')
    plt.show()

def plot_scatter(data, x_feature, y_feature):
    """
    Plot a scatter plot of two features in the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.
    - x_feature (str): The name of the feature to plot on the x-axis.
    - y_feature (str): The name of the feature to plot on the y-axis.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(data[x_feature], data[y_feature])
    plt.title(f'Scatter Plot of {x_feature} vs {y_feature}')
    plt.xlabel(x_feature)
    plt.ylabel(y_feature)
    plt.show()

def plot_pairplot(data):
    """
    Plot pairwise relationships in the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.

    Returns:
    - None
    """
    sns.pairplot(data)
    plt.show()

def plot_boxplot(data, feature_name):
    """
    Plot a box plot of the specified feature in the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.
    - feature_name (str): The name of the feature to plot.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, x=feature_name)
    plt.title(f'Box Plot of {feature_name}')
    plt.xlabel(feature_name)
    plt.show()

def plot_heatmap(data):
    """
    Plot a heatmap of the correlation matrix of the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.

    Returns:
    - None
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.show()

def plot_null_values(data):
    """
    Plot a heatmap to visualize null values in the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.

    Returns:
    - None
    """
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
    plt.title('Null Values Heatmap')
    plt.show()

def plot_outliers(data, feature_name):
    """
    Plot a box plot to visualize outliers in a numerical feature.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.
    - feature_name (str): The name of the numerical feature to analyze.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, x=feature_name)
    plt.title(f'Outliers in {feature_name}')
    plt.xlabel(feature_name)
    plt.show()


def plot_null_values_per_column(data):
    """
    Plot the count of null values in each column of the dataset.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.

    Returns:
    - None
    """
    null_counts = data.isnull().sum()
    plt.figure(figsize=(10, 6))
    null_counts.plot(kind='bar', color='skyblue')
    plt.title('Null Values Count per Column')
    plt.xlabel('Columns')
    plt.ylabel('Null Values Count')
    plt.xticks(rotation=45, ha='right')
    plt.show()


    
def plot_target_distribution(data, target_feature):
    """
    Plot the distribution of the target variable in the dataset using a count plot.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.
    - target_feature (str): The name of the target variable to visualize.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    sns.countplot(data[target_feature])
    plt.title(f'Distribution of {target_feature}')
    plt.xlabel(target_feature)
    plt.ylabel('Count')
    plt.show()

def plot_target_distribution_pie(data, target_feature):
    """
    Plot the distribution of the target variable in the dataset using a pie chart.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.
    - target_feature (str): The name of the target variable to visualize.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    data[target_feature].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
    plt.title(f'Distribution of {target_feature}')
    plt.ylabel('')
    plt.show()



import seaborn as sns
import matplotlib.pyplot as plt

def visualize_categorical(data, categorical_columns):
    """
    Visualize the distribution of categorical fields in a DataFrame using countplot.

    Parameters:
    - data (DataFrame): The pandas DataFrame containing the dataset.
    - categorical_columns (list): List of column names containing categorical variables.

    Returns:
    - None
    """
    for column in categorical_columns:
        plt.figure(figsize=(8, 6))
        sns.countplot(data=data, x=column)  # Specify x=column to fix the ValueError
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.show()



def plot_covariance_matrix(data):
    """
    Plot the covariance matrix of the dataset.

    Parameters:
    - data (DataFrame or array-like): The dataset containing numerical features.

    Returns:
    - None
    """
    if isinstance(data, pd.DataFrame):
        data = data.values

    covariance_matrix = np.cov(data, rowvar=False)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(covariance_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Covariance Matrix')
    plt.show()

