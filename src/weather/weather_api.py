import requests
from datetime import datetime
import json
import os


config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'keys.json')

with open(config_path, 'r') as file:
    keys = json.load(file)

# API key
api_key = keys['api_key'] 

# API endpoint
url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


# Locations
locations = ["Bondville, IL"]
             
# locations = ["Bondville, IL", 
#              "Desert Rock, NV", 
#              "Fort Peck, MT", 
#              "Goodwin Creek, MS",
#              "Sioux Falls, SD",
#              "State College, PA",
#              "Boulder, CO"]  

# Set the start and end dates
start_date = "2024-04-16"
end_date = datetime.now().strftime("%Y-%m-%d")  # Today's date

headers = {
    "accept": "application/json"
}
params = {
    "key": api_key,
    "contentType": "json"
}

# Loop through each location and make the API request
for location in locations:
    full_url = f"{url}/{location}/{start_date}/{end_date}"
    response = requests.get(full_url, headers=headers, params=params)
    data = response.json()
    
    print(f"Weather data for {location}:")
    print(data)
