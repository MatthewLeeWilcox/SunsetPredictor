import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import shutil


def list_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    return files

folder_path = "F:\SunSetPhotos"
files_list = np.array(list_files_in_folder(folder_path))


rawImageList = files_list[np.char.endswith(files_list,"raw.jpg")]

sunsetDF  = pd.read_csv('F:\SunsetPredictor\src\SunSetTimes\data\golden_co\sunset_times.csv')

print(type(sunsetDF["Sunset Time"][1]))
print(len(files_list))
print(len(rawImageList))

dateTimeArray = np.array(sunsetDF["Date"] +" " + sunsetDF["Sunset Time"])

dateTimeArray = np.array(list(map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), dateTimeArray)))

print(dateTimeArray[0])

test_time = datetime.strptime("2020-12-29 4:43:32", '%Y-%m-%d %H:%M:%S')

def round_10min(datet):
    dt = datet
    minutes = dt.minute
    seconds = dt.second
    minutes_10 = minutes % 10
    total_seconds = minutes*60 + seconds
    if minutes_10 < 5:
        dt = dt.replace(minute = (minutes//10 *10), second = 0)
    else:
        if (minutes // 10 +1) *10 >= 60:
            dt = dt.replace(hour = dt.hour + 1, minute = 0, second = 0)
        else:
            dt = dt.replace(minute = ((minutes // 10 +1) *10), second = 0)    
    return dt

dateTimeArray = np.array(list(map(lambda x: round_10min(x), dateTimeArray)))

def giveImagecode(date):
    year = str(date.year)
    month = str(date.month) if date.month >= 10 else "0" + str(date.month)
    day = str(date.day) if date.day >= 10 else "0" + str(date.day)
    hour = str(date.hour) if date.hour >= 10 else "0" + str(date.hour)
    minute = str(date.minute) if date.minute >= 10 else "0" + str(date.minute)
    imagecode = year+ month + day + hour + minute + "00" + ".raw.jpg"
    return imagecode

def deviate_time(date, dev):
    # print("start-----")
    df = pd.DataFrame(columns = ['OGDate', 'TimeDif', 'imgCode'])
    for i in range(0,dev+1):
        # print("###", i, "###")
        if i == 0:
            new_row = np.array([date, 0+10*i, giveImagecode(date - timedelta(minutes=10*i))]) 
            new_df = pd.DataFrame([new_row], columns= df.columns)
            df = pd.concat([df, new_df], ignore_index=True)        
        else:
            new_row1 = np.array([date, 0+10*i, giveImagecode(date + timedelta(minutes=10*i))]) 
            new_row2 = np.array([date, 0-10*i, giveImagecode(date - timedelta(minutes=10*i))]) 
            new_df = pd.DataFrame([new_row1, new_row2], columns= df.columns)
            df = pd.concat([df, new_df], ignore_index=True)
    # print("----End----")
    return df

print(deviate_time(test_time, 5))
testdates = dateTimeArray[0:365]
counter = 1

df = pd.DataFrame(columns = ['OGDate', 'TimeDif', 'imgCode'])

print(testdates)
error = np.array([])
for date in tqdm(dateTimeArray):
    destination_folder = "F:/SunsetPredictor/Data/SunSetImg"
    temp_cp_files = deviate_time(date,3)
    # df = pd.concat([df, temp_cp_files], ignore_index=True)
    # print(df)
    for row in temp_cp_files.itertuples():
        source_file = "F:/SunSetPhotos/" + row[3]
       
        try:    
            shutil.copy2(source_file, destination_folder)
            temp_row = pd.DataFrame(data={'OGDate' : [row[1]], 'TimeDif' : [row[2]], 'imgCode' : [row[3]]})
            df = pd.concat([df, temp_row])
        except:
            # error = np.append(error, np.array([source_file]))
            counter += 1
print(df)
error = np.array([])
df.to_csv('test.csv')