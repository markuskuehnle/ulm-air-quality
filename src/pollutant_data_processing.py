import urllib.request
import json
import pandas as pd
from paths import RAW_DATA_DIR, TRANSFORMED_DATA_DIR 

def fetch_data(url, limit=300000) -> pd.DataFrame:
    """
    Fetches data from the specified URL with pagination if the response returns the limit number of rows.
    
    Args:
        url (str): The base URL for the API request.
        limit (int): The maximum number of rows per request. Default is 300000.
        
    Returns:
        pd.DataFrame: A DataFrame containing the concatenated results from all requests.
    """
    all_data = []
    offset = 0
    while True:
        paginated_url = f"{url}&limit={limit}&offset={offset}"
        response = urllib.request.urlopen(paginated_url)
        assert response.code == 200

        # Convert HTTP Response to JSON
        string = response.read().decode("utf-8")
        response_dict = json.loads(string)
        assert response_dict["success"] is True

        # Convert JSON object to DataFrame
        created_package = response_dict["result"]
        df_raw = pd.DataFrame.from_dict(created_package["records"])

        # Remove \r\n from string conversion
        df_raw = df_raw.replace({r"\r\n": ""}, regex=True)

        all_data.append(df_raw)
        
        # If less than limit rows returned, we are done
        if len(df_raw) < limit:
            break
        
        # Update offset for next request
        offset += limit

    # Concatenate all DataFrames
    final_df = pd.concat(all_data, ignore_index=True)
    
    return final_df

def validate_data(df) -> pd.DataFrame:
    """
    Validate the data by filling gaps and ensuring no values are below 0.
    
    Args:
        df (pd.DataFrame): The input DataFrame to validate.
        
    Returns:
        pd.DataFrame: The validated DataFrame with gaps filled and no negative values.
    """
    df = df.rename(columns={'_id': 'id', 'timestamp': 'date', 'schadstoff': 'pollutant', 'wert': 'concentration'})
    df = df.drop(columns={"id", "station"})
    df = df.sort_values(by='date')

    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # Remove duplicate timestamps by aggregating (e.g., taking the mean)
    df = df.groupby(['date', 'pollutant']).mean().reset_index()
    df = df.set_index('date')

    # Resample the data to hourly frequency and identify any missing timestamps
    df_resampled = df.groupby('pollutant').resample('h').asfreq().drop(columns="pollutant").reset_index()

    # Fill missing values
    def fill_gaps(group):
        # Interpolate remaining gaps
        group['concentration'] = group['concentration'].interpolate(method='linear')
        # Fill forward
        group['concentration'] = group['concentration'].ffill()
        # Fill backward only where forward fill did not fill
        group['concentration'] = group['concentration'].bfill()
        return group

    # Apply fill_gaps function to each group
    df_filled = df_resampled.groupby('pollutant', group_keys=True).apply(fill_gaps).drop(columns="pollutant")

    # Remove any negative values
    df_filled['concentration'] = df_filled['concentration'].apply(lambda x: max(x, 0))

    # Reset index for further operations
    df_filled = df_filled.reset_index()
    df_filled = df_filled.drop(columns="level_1", errors='ignore')
    return df_filled

def clean_data(df) -> pd.DataFrame:
    """
    Clean the data by renaming columns, filtering for a specific station, 
    and removing unnecessary columns and index.
    
    Args:
        df (pd.DataFrame): The input DataFrame to clean.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Ensure the index is a DatetimeIndex
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # Pivot the DataFrame to have separate columns for each pollutant
    df_pivot = df.pivot_table(values='concentration', index='date', columns='pollutant')

    return df_pivot

def resample_data(df) -> pd.DataFrame:
    # Resample to daily averages and handle missing values
    df = df.resample('D').mean().dropna()
    return df