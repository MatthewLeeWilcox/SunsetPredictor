import requests
import pytz
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def generate_dates(start_year, end_year=2020):
    start_date = datetime(start_year, 7, 18)
    end_date = datetime(end_year, 2, 2)

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


def get_sunset_time(date, latitude, longitude, timezone):
    # Build the API request URL
    # print("Begin_apiPull")
    try:
        url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={date}&formatted=0"

        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Extract the sunset time
        sunset = data['results']['sunset']
        # print(convert_utc_to_edt(sunset, timezone))
        return convert_utc_to_edt(sunset, timezone)
    except:
        print("Failed")
        return(date,"NA")

from tqdm import tqdm

location = {"Golden, CO": [39.7555, -105.2211, 'America/Denver']}
latitude = location["Golden, CO"][0]
longitude = location["Golden, CO"][1]
timezone = location["Golden, CO"][2]

# for year in range(2005, 2021, 1):
#     dates = generate_dates(year)
#     # print(dates)
#     columns = ['Date', 'Sunset Time']
#     df_sunset_times = pd.DataFrame(columns=columns)

#     for date in tqdm(dates):
#         try:
#             sunset_time = get_sunset_time(date,location["Golden, CO"][0], location["Golden, CO"][1],timezone )

#             # local_time = convert_utc_to_edt(sunset_time, location["Golden, CO"][2])

#             date_time = {'Date': date, 'Sunset Time': sunset_time}
#             df_sunset_times.loc[len(df_sunset_times)] = date_time
#             # print(date)

#     df_sunset_times.to_csv(f'data/golden_co/year_{year}.csv')


date_range = pd.date_range(start="2005-07-18",end="2020-02-02")#.to_pydatetime()
date_list = np.array(date_range.strftime('%Y-%m-%d').tolist())
sunset_times = np.array([])
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

sunset_times = pd.DataFrame(columns = ['Date', 'Time'])
# 
def set_up_threads(dates, latitude, longitude, timezone):
    sunset_times = np.array([])
    date_list = np.array([])
    with ThreadPoolExecutor() as executor:
        # Create a tqdm instance with total number of URLs to track progress
        with tqdm(total=len(dates)) as pbar:
            # Use executor.map to parallelize the download_file function
            # and feed the tqdm progress bar with updates
            for _ in executor.map(get_sunset_time, dates, [latitude]*len(dates), [longitude]*len(dates), [timezone]*len(dates)):
                print(_)
                sunset_times = np.append(sunset_times, np.array([_[0]]))
                date_list = np.append(date_list, np.array([_[0]]))
                pbar.update(1)
    sunset_df = pd.DataFrame({'Dates': date_list, "Time": sunset_times})
    return sunset_df


if __name__ == "__main__":
    df = set_up_threads(date_list, latitude, longitude, timezone)
    df.to_csv('sunset_times.csv')