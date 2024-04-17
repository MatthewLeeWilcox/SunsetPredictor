import requests
import pytz
import pandas as pd
from datetime import datetime, timedelta


def generate_dates(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

    return date_list

def convert_utc_to_edt(utc_time_str, timezone):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%S+00:00')

    utc_zone = pytz.timezone('UTC')
    local_zone = pytz.timezone(timezone)

    # Localize the UTC time
    utc_dt = utc_zone.localize(utc_time)

    eastern_dt = utc_dt.astimezone(local_zone)

    # Return the converted time as a string
    return eastern_dt.strftime('%H:%M:%S')


def get_sunset_time(latitude, longitude, date):
    # Build the API request URL
    url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={date}&formatted=0"


    # Make the API request
    response = requests.get(url)
    data = response.json()

    # Extract the sunset time
    sunset = data['results']['sunset']
    
    return sunset


locations = {"Bondville, IL": [40.1134, -88.3695],
             "Desert Rock, NV": [36.621, -116.029],
             "Fort Peck, MT": [], 
             "Goodwin Creek, MS": [],
             "Sioux Falls, SD": [],
             "State College, PA": [],
             "Boulder, CO": []}

for year in range(2006, 2025, 1):
    dates = generate_dates(year)

    columns = ['Date', 'Sunset Time']
    df_sunset_times = pd.DataFrame(columns=columns)

    for date in dates:
        sunset_time = get_sunset_time(locations["Desert Rock, NV"][0], locations["Desert Rock, NV"][1], date)
        
        local_time = convert_utc_to_edt(sunset_time, 'America/Los_Angeles')

        date_time = {'Date': date, 'Sunset Time': local_time} 
        df_sunset_times.loc[len(df_sunset_times)] = date_time
        print(date)

    df_sunset_times.to_csv(f'data/desert_rock/{year}.csv')


