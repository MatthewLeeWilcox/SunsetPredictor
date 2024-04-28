import requests
import json
import os
import pandas as pd

# Load API keys
config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'keys.json')
with open(config_path, 'r') as file:
    keys = json.load(file)

api_key = keys['weather_api_key']
url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Specify location and time
location = "Golden, CO"

sunset_times = pd.read_csv('src/SunsetTimes/data/golden_co/sunset_times.csv')

elements_to_store = ['datetime', 
                     'temp', 
                     'feelslike', 
                     'humidity', 
                     'dew', 
                     'precip', 
                     'precipprob', 
                     'snow', 
                     'snowdepth', 
                     'preciptype', 
                     'windgust', 
                     'windspeed', 
                     'winddir', 
                     'pressure', 
                     'visibility', 
                     'cloudcover', 
                     'solarradiation', 
                     'solarenergy', 
                     'uvindex', 
                     'severerisk', 
                     'conditions', 
                     'icon', 
                     'moonphase']

columns = ['date', *elements_to_store]
df_weather = pd.DataFrame(columns=columns)

for index, row in sunset_times.iterrows():
    date = row['Date']
    time = row['Sunset Time'] 

    specific_time = f"{date}T{time}"

    full_url = f"{url}/{location}/{specific_time}?key={api_key}&include=current"
    response = requests.get(full_url)

    if response.status_code == 200:
        try:
            data = response.json()

            weather_data = {'date': date, **data['currentConditions']} 
            df_weather.loc[len(df_weather)] = weather_data

            df_weather.to_csv(f'src/Weather/data/golden_co/weather_data.csv')

        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
    else:
        print(f"Failed to fetch data: HTTP {response.status_code} - {response.text}")
