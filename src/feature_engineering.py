import pandas as pd


def extract_date_features(df):
    """Extracts date-related features from the index of the DataFrame."""
    df.index = pd.to_datetime(df.index)
    df['day_of_week'] = df.index.dayofweek
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['season'] = df.index.month % 12 // 3 + 1  # 1: Winter, 2: Spring, 3: Summer, 4: Autumn
    return df


def create_interaction_features(df):
    """Creates interaction features between pollutants and weather conditions."""
    df['temp_pm10_interaction'] = df['mean_temp'] * df['pm10']
    df['windspeed_pm25_interaction'] = df['max_wind_gust'] * df['pm25']
    df['sunshine_pm10_interaction'] = df['sunshine'] * df['pm10']
    df['temp_windspeed_interaction'] = df['mean_temp'] * df['max_wind_gust']
    df['temp_sunshine_interaction'] = df['mean_temp'] * df['sunshine']
    df['windspeed_sunshine_interaction'] = df['max_wind_gust'] * df['sunshine']
    return df


def create_polynomial_features(df):
    """Creates polynomial features of the weather conditions."""
    df['temp_squared'] = df['mean_temp'] ** 2
    df['windspeed_squared'] = df['max_wind_gust'] ** 2
    df['sunshine_squared'] = df['sunshine'] ** 2
    df['temp_cubed'] = df['mean_temp'] ** 3
    df['windspeed_cubed'] = df['max_wind_gust'] ** 3
    df['sunshine_cubed'] = df['sunshine'] ** 3
    return df


def create_ratio_features(df):
    """Creates ratio features involving temperature and other weather conditions."""
    df['temp_precipitation_ratio'] = df['mean_temp'] / (df['precipitation'] + 1)
    df['windspeed_temp_ratio'] = df['max_wind_gust'] / (df['mean_temp'] + 1)
    return df


def create_cross_features(df):
    """Creates cross features from date-related features."""
    df['day_of_week_month'] = df['day_of_week'] * df['month']
    df['month_year'] = df['month'] * df['year']
    return df


def perform_feature_engineering(df):
    """Combines all feature engineering steps."""
    df = extract_date_features(df)
    df = create_interaction_features(df)
    df = create_polynomial_features(df)
    df = create_ratio_features(df)
    df = create_cross_features(df)
    return df


def merge_data(pollutants_df, weather_df):
    """Merges pollutant and weather data on common dates."""
    # Ensure both DataFrames have DatetimeIndex
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    weather_df = weather_df.set_index('date')

    # Inspect date ranges
    first_date_pollutants = pollutants_df.index.min()
    last_date_pollutants = pollutants_df.index.max()
    first_date_weather = weather_df.index.min()
    last_date_weather = weather_df.index.max()

    print(f"Pollutant DataFrame date range: {first_date_pollutants} to {last_date_pollutants}")
    print(f"Weather DataFrame date range: {first_date_weather} to {last_date_weather}")

    # Determine the overlapping date range
    overlap_start_date = max(first_date_pollutants, first_date_weather)
    overlap_end_date = min(last_date_pollutants, last_date_weather)

    if overlap_start_date > overlap_end_date:
        raise ValueError("No overlapping dates between pollutant and weather data.")

    # Filter DataFrames to the overlapping date range
    pollutants_df_filtered = pollutants_df.loc[overlap_start_date:overlap_end_date]
    weather_df_filtered = weather_df.loc[overlap_start_date:overlap_end_date]

    # Forward fill and backward fill to handle missing dates in the weather data
    weather_df_filtered = weather_df_filtered.reindex(pollutants_df_filtered.index).ffill().bfill()

    # Merge the DataFrames on the index (date)
    merged_df = pd.merge(pollutants_df_filtered, weather_df_filtered, left_index=True, right_index=True, how='inner')

    return merged_df
