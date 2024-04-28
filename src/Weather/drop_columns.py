import pandas as pd


df = pd.read_csv('src/Weather/data/golden_co/weather_data.csv')

df['preciptype'] = df['preciptype'].fillna(0)

columns_to_drop = ['snow', 'snowdepth', 'windgust', 'solarradiation', 'solarenergy', 'uvindex', 'severerisk']

df.drop(columns=columns_to_drop, inplace=True)

df.to_csv('src/Weather/data/golden_co/weather_data_interpolated.csv', index=False)