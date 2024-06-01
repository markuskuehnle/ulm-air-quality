import pandas as pd
import plotly.express as px
from typing import Optional

def plot_one_sample(features: pd.DataFrame, target: pd.DataFrame, example_pollutant: str, predictions: Optional[pd.Series] = None):
    """Plots historical features, target, and predictions for a specified pollutant using Plotly Express.

    Args:
        features (pd.DataFrame): DataFrame containing the features.
        target (pd.DataFrame): DataFrame containing the target values.
        example_pollutant (str): The name of the pollutant column to plot.
        predictions (Optional[pd.Series], optional): Series containing the predictions. Defaults to None.
    """
    # Filter the features and target for the specified pollutant
    features_filtered = features[['date', example_pollutant]].set_index('date')
    target_filtered = target[['date', example_pollutant]].set_index('date')

    # Ensure 'date' is in datetime format
    features_filtered.index = pd.to_datetime(features_filtered.index)
    target_filtered.index = pd.to_datetime(target_filtered.index)
    
    # Create the initial plot with historical features
    fig = px.line(features_filtered, x=features_filtered.index, y=example_pollutant, labels={'x': 'Date', 'y': example_pollutant}, title=f'Historical Features, Target, and Predictions for {example_pollutant}')
    fig.update_traces(name='Historical Features')

    # Add the target values to the plot
    fig.add_scatter(x=target_filtered.index, y=target_filtered[example_pollutant], mode='lines', name='Target', line=dict(color='black'))

    # Add the predictions to the plot if provided
    if predictions is not None:
        predictions = predictions.loc[target_filtered.index]
        fig.add_scatter(x=target_filtered.index, y=predictions, mode='lines+markers', name='Predictions', line=dict(color='red'), marker=dict(symbol='x', size=10))

    # Ensure the legend is complete
    fig.update_layout(legend_title_text='Legend')

    fig.show()
    