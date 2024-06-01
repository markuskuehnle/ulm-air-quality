import pandas as pd


def extract_date_features(df):
    """Extracts date-related features from the 'date' column of the DataFrame."""
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['season'] = (df['date'].dt.month % 12 // 3) + 1  # 1: Winter, 2: Spring, 3: Summer, 4: Autumn
    return df


def create_interaction_features(df):
    """Creates interaction features between pollutants and weather conditions."""
    df['temp_pm10_interaction'] = df['mean_temp'] * df['pm10']
    df['windspeed_pm25_interaction'] = df['max_wind_gust'] * df['pm2.5']
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
    # Ensure both DataFrames have 'date' column formatted as dd.mm.YYYY
    pollutants_df = pollutants_df.reset_index()
    weather_df = weather_df.reset_index()

    pollutants_df['date'] = pd.to_datetime(pollutants_df['date'], format='%Y-%m-%d').dt.strftime('%d.%m.%Y')
    weather_df['date'] = pd.to_datetime(weather_df['date'], format='%Y-%m-%d').dt.strftime('%d.%m.%Y')

    # Merge the DataFrames on the 'date' column
    merged_df = pd.merge(pollutants_df, weather_df, on='date', how='inner')
    
    # Drop unnecessary index columns if they exist
    merged_df = merged_df.reset_index(drop=True)
    if 'index' in merged_df.columns:
        merged_df = merged_df.drop(columns=['index'])
    if 'level_0' in merged_df.columns:
        merged_df = merged_df.drop(columns=['level_0'])

    df = merged_df.reset_index(drop=True)
    return df