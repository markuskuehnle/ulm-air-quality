import numpy as np
import pandas as pd
from typing import Tuple, Optional, List


def get_ts(data):
    """
    Converts a long DataFrame into a 3D numpy array for time series,
    excluding the "date" column and tracking feature names.

    Args:
        data (pd.DataFrame): DataFrame containing the time series data.

    Returns:
        np.ndarray: 3D numpy array of shape (num_samples, num_timesteps, num_features).
        list: List of feature names in the order they appear in the time series.
    """
    # Exclude the "date" column
    feats = [feat for feat in data.columns if feat != 'date']

    # Initialize an empty list to store the time series data
    timeseries = []

    # Convert the DataFrame to a 3D numpy array
    for col in feats:
        timeseries.append(data[col].values)

    # Transpose the array to match the desired shape (num_samples, num_timesteps, num_features)
    timeseries = np.array(timeseries).T

    return timeseries, feats


def aggregate_ts(ts, idx, thresholds):
    """
    Aggregates the time series based on the given thresholds.

    Args:
        ts (np.ndarray): 2D array representing the time series data.
        idx (int): Index of the feature to aggregate.
        thresholds (list): List of aggregation windows to use.

    Returns:
        list: Aggregated values.
    """
    agg_values = []
    for threshold in thresholds:
        agg_values.append(np.mean(ts[-threshold:, idx]))
    return agg_values



def get_feats_and_label(timeseries: pd.DataFrame, offset: int, label_period: int, label_idx: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extracts features and labels from time series data.

    Args:
        timeseries (pd.DataFrame): DataFrame representing the time series data.
        offset (int): Time steps to offset the label.
        label_period (int): Number of time steps to predict.
        label_idx (int): Index of the label column in the time series.
        thresholds (list, optional): Aggregation windows to use.

    Returns:
        tuple: Tuple containing arrays for features (X) and labels (y).
    """
    assert offset % label_period == 0

    end_offset = -offset
    if offset == 0:
        end_offset = None

    # Set 'date' column as index if it exists
    if 'date' in timeseries.columns:
        timeseries = timeseries.set_index('date')

    # Extract the label
    y = timeseries.iloc[-label_period-offset:end_offset, [label_idx]]

    # Extract features, excluding the label column
    X = timeseries.iloc[:-label_period-offset, :]

    return X, y