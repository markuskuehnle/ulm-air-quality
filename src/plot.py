from typing import Optional
import plotly.express as px
import pandas as pd

def plot_one_sample(features: pd.DataFrame, target: pd.DataFrame, example_pollutant: str, predictions: Optional[pd.Series] = None):
    """Plots historical features, target, and predictions for a specified pollutant using Plotly Express.

    Args:
        features (pd.DataFrame): DataFrame containing the features.
        target (pd.DataFrame): DataFrame containing the target values.
        example_pollutant (str): The name of the pollutant column to plot.
        predictions (Optional[pd.Series], optional): Series containing the predictions. Defaults to None.
    """
    # Ensure 'date' is in the index and in datetime format
    if 'date' not in features.index.names:
        features = features.set_index('date')
    if 'date' not in target.index.names:
        target = target.set_index('date')
        
    features.index = pd.to_datetime(features.index)
    target.index = pd.to_datetime(target.index)

    # Filter the features and target for the specified pollutant
    features_filtered = features[[example_pollutant]]
    target_filtered = target[[example_pollutant]]

    # Create the initial plot with historical features
    fig = px.line(features_filtered, x=features_filtered.index, y=example_pollutant, labels={'x': 'Date', 'y': example_pollutant}, title=f'Historical Features, Target, and Predictions for {example_pollutant}')
    fig.update_traces(name='Historical Features')

    # Add the target values to the plot
    fig.add_scatter(x=target_filtered.index, y=target_filtered[example_pollutant], mode='lines', name='Target', line=dict(color='black'))

    # Add the predictions to the plot if provided
    if predictions is not None:
        # Ensure the predictions use the same dates as the target period
        fig.add_scatter(x=target_filtered.index, y=predictions, mode='lines+markers', name='Predictions', line=dict(color='red'), marker=dict(symbol='x', size=5))

    # Ensure the legend is complete
    fig.update_layout(legend_title_text='Legend')

    fig.show()
