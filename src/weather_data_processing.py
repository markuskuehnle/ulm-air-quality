import time
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from typing import List

def configure_webdriver() -> webdriver.Chrome:
    """Configures and returns a Chrome WebDriver instance."""
    return webdriver.Chrome()

def accept_cookies(driver: webdriver.Chrome) -> None:
    """Accepts the cookies on the webpage if the cookie banner is present."""
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[id^="sp_message_iframe_"]'))
        )
        driver.switch_to.frame(iframe)

        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Zustimmen"]'))
        )
        accept_button.click()
        driver.switch_to.default_content()
        time.sleep(2)
    except TimeoutException:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")

def set_date(driver: webdriver.Chrome, date: datetime) -> None:
    """Sets the date in the date input field and clicks the "Ansicht aktualisieren" button."""
    try:
        date_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'datum'))
        )
        date_input.clear()
        time.sleep(1)
        date_input.send_keys(date.strftime('%d.%m.%Y'))

        update_button_div = driver.find_element(By.CSS_SELECTOR, 'div.uk-panel.uk-panel-box.uk-margin')
        update_button = update_button_div.find_element(By.CSS_SELECTOR, 'button.uk-button.uk-button-success')
        update_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while setting the date: {e}")

def scrape_table(driver: webdriver.Chrome) -> List[List[str]]:
    """Scrapes the weather data table from the webpage."""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "extremwerte")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'id': 'extremwerte'})
        rows = table.find('tbody').find_all('tr')

        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)
        
        return data
    except Exception as e:
        print(f"An error occurred while scraping the table: {e}")
        return []

def build_dynamic_url() -> str:
    """Builds the dynamic URL based on the current date."""
    today = datetime.today()
    end_date = today
    start_date = end_date - timedelta(weeks=8)
    
    return f"https://www.wetterkontor.de/de/wetter/deutschland/rueckblick.asp?id=203&datum0={start_date.strftime('%d.%m.%Y')}&datum1={end_date.strftime('%d.%m.%Y')}&jr={end_date.year}&mo={end_date.month}&datum={end_date.strftime('%d.%m.%Y')}&t=8&part=2"

def fetch_weather_data() -> pd.DataFrame:
    """Fetches weather data from the dynamically generated URL."""
    url = build_dynamic_url()
    driver = configure_webdriver()
    driver.get(url)

    accept_cookies(driver)

    end_date = datetime.strptime(url.split('datum1=')[1].split('&')[0], '%d.%m.%Y')
    start_date = datetime.strptime(url.split('datum0=')[1].split('&')[0], '%d.%m.%Y')

    all_data = []

    while end_date > start_date:
        set_date(driver, end_date)
        data = scrape_table(driver)
        all_data.extend(data)
        end_date -= timedelta(weeks=8)

    driver.quit()

    # Convert the scraped data to a DataFrame
    columns = ['Datum', 'Minimum Temp [°C]', 'Maximum Temp [°C]', 'Mittel Temp [°C]', 'Niederschlag [l/m2]', 'Sonnenschein [h]', 'Max Windböe', 'Schneehöhe [cm]']
    df = pd.DataFrame(all_data, columns=columns)

    # Split 'Max Windböe' into 'Max Windböe [Bft]' and 'Max Windböe [km/h]'
    df[['Max Windböe [Bft]', 'Max Windböe [km/h]']] = df['Max Windböe'].str.extract(r'(\d)(\d+)')
    df['Max Windböe [Bft]'] = df['Max Windböe [Bft]'].astype(float)
    df['Max Windböe [km/h]'] = df['Max Windböe [km/h]'].astype(float)
    df = df.drop(columns=['Max Windböe'])

    return df

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the weather data DataFrame."""
    # Drop 'Max Windböe [Bft]' column 
    df = df.drop(columns=['Max Windböe [Bft]'])
    
    # Rename columns to English
    df.columns = [
        'date', 'min_temp', 'max_temp', 'mean_temp', 'precipitation', 
        'sunshine', 'snow_depth', 'max_wind_gust'
    ]
    
    # Replace commas with periods in relevant columns and convert to numeric
    columns_to_convert = [
        'min_temp', 'max_temp', 'mean_temp', 'precipitation', 
        'sunshine', 'snow_depth'
    ]
    
    for column in columns_to_convert:
        df[column] = df[column].replace('-', np.nan)
        df[column] = df[column].str.replace(',', '.').astype(float)
    
    # Convert 'Date' column to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    
    return df

def validate_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validates and interpolates missing values in the weather data DataFrame."""
    df['snow_depth'] = df['snow_depth'].interpolate(method='linear')
    
    return df
