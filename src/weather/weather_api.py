import requests
import json
import os

# Load API keys
config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'keys.json')
with open(config_path, 'r') as file:
    keys = json.load(file)

api_key = keys['weather_api_key']
url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Specify location and time
location = "Golden, CO"
specific_time = "2024-04-23T17:53:00"

# API request
full_url = f"{url}/{location}/{specific_time}?key={api_key}&include=current"
response = requests.get(full_url)

if response.status_code == 200:
    try:
        data = response.json()
        print(f"Weather data for {location} at {specific_time}:")
        print(data)
    except json.JSONDecodeError:
        print("Failed to decode JSON from response")
else:
    print(f"Failed to fetch data: HTTP {response.status_code} - {response.text}")
