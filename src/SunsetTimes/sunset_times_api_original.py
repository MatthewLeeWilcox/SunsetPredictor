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


locations = {"Golden, CO": [39.7555, -105.2211, 'America/Denver']}

columns = ['Date', 'Sunset Time']
df_sunset_times = pd.DataFrame(columns=columns)

for year in range(2005, 2021, 1):
    dates = generate_dates(year)

    for date in dates:
        sunset_time = get_sunset_time(locations["Golden, CO"][0], locations["Golden, CO"][1], date)
        
        local_time = convert_utc_to_edt(sunset_time, 'America/Denver')

        date_time = {'Date': date, 'Sunset Time': local_time} 
        df_sunset_times.loc[len(df_sunset_times)] = date_time
        print(date)


    df_sunset_times.to_csv(f'data/golden_co/sunset_times.csv')

