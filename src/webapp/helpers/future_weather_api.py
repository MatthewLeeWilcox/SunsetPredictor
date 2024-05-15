import requests
import json
import os
import pandas as pd
from datetime import datetime


def convert_date_format(date_string):
    date_object = datetime.strptime(date_string, '%m/%d/%Y')
    new_date_format = date_object.strftime('%Y-%m-%d')
    return new_date_format

def get_future_weather(date):
    # Load API keys
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'configs', 'keys.json')
    with open(config_path, 'r') as file:
        keys = json.load(file)

    api_key = keys['weather_api_key']
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    # Define elements to fetch and their new key names
    key_mapping = {
        'datetime': 'Date',
        'temp': 'Temperature',
        'feelslike': 'Feels Like',
        'humidity': 'Humidity',
        'dew': 'Dew Point',
        'precip': 'Precipitation',
        'precipprob': 'Precipitation Probability',
        'windspeed': 'Wind Speed',
        'winddir': 'Wind Direction',
        'pressure': 'Pressure',
        'visibility': 'Visibility',
        'cloudcover': 'Cloud Cover',
        'conditions': 'Weather Conditions',
        'icon': 'Weather Icon',
        'moonphase': 'Moon Phase'
    }

    elements_to_store = list(key_mapping.keys())

    date = convert_date_format(date)
    time = '17:00:00'
    specific_time = f"{date}T{time}"
    location = "Golden, CO"

    full_url = f"{url}/{location}/{specific_time}?key={api_key}&include=current"
    response = requests.get(full_url)

    if response.status_code == 200:
        try:
            data = response.json()
            weather_data = {key_mapping[key]: data['currentConditions'][key] for key in elements_to_store}
            weather_data['Date'] = date  # Overwrite date if necessary or reformat
            df_weather = pd.DataFrame([weather_data])
            return df_weather
        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
    else:
        print(f"Failed to fetch data: HTTP {response.status_code} - {response.text}")

