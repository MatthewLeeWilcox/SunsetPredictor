import pandas as pd


df = pd.read_csv('src/Weather/data/golden_co/weather_data_interpolated.csv')

df['date'] = pd.to_datetime(df['date'])

df.set_index('date', inplace=True)

df.interpolate(method='linear', inplace=True)
df.reset_index(inplace=True)

df.to_csv('src/Weather/data/golden_co/weather_data_interpolated.csv', index=True)