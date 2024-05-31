import numpy as np
import pandas as pd

def mean_squared_error(col1, col2):
    """
    Calculate the Mean Squared Error between two columns in a DataFrame.

    Parameters:
    col1 (str): The name of the first column (actual values).
    col2 (str): The name of the second column (predicted values).

    Returns:
    float: The Mean Squared Error between the two columns.
    """
    squared_errors = (col1 - col2) ** 2
    mse = squared_errors.mean()
    return mse


def mean_absolute_error(col1, col2):
    """
    Calculate the Mean Absolute Error between two columns in a DataFrame.

    Parameters:
    col1 (str): The name of the first column (actual values).
    col2 (str): The name of the second column (predicted values).

    Returns:
    float: The Mean Absolute Error between the two columns.
    """
    absolute_errors = abs(col1 - col2)
    mae = absolute_errors.mean()
    return mae


def compute_rmse(df, col1, col2):
    return np.sqrt(mean_squared_error(df[col1], df[col2]))

def compute_mae(df, col1, col2):
    return mean_absolute_error(df[col1], df[col2])

def compute_metrics(df, col1, col2):
    rmse = compute_rmse(df, col1, col2)
    mae = compute_mae(df, col1, col2)
    correlation = df[col1].corr(df[col2])
    r_squared = correlation ** 2
    bias = (df[col1] - df[col2]).mean()
    return rmse, mae, correlation, r_squared, bias
