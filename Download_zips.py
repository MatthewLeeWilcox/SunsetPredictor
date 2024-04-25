from tqdm import tqdm
import pandas as pd
import numpy as np
import requests, zipfile, io
from concurrent.futures import ThreadPoolExecutor


date_range = pd.date_range(start="2005-07-18",end="2020-02-02").to_pydatetime().tolist()

url_array= np.array([])
for date in tqdm(date_range):
    # print(date)
    day = date.day
    if day < 10:
        day = str(0) + str(day)
    else:
        day = str(day)
    year = str(date.year)

    month = date.month
    if month < 10:
        month = str(0) + str(month)
    else:
        month = str(month)
    # print(type(day))
    url = "https://midcdmz.nrel.gov/tsi/SRRL/" + year + "/" + year + month + day + ".zip"
    url_array= np.append(url_array, url)
# print(url_array)

def download_zip(url):
    try:
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("F:/SunSetPhotos")
    except:
        print(url, "Error")
print("Begin Scrape")



def set_up_threads(urls):
    with ThreadPoolExecutor() as executor:
        # Create a tqdm instance with total number of URLs to track progress
        with tqdm(total=len(urls)) as pbar:
            # Use executor.map to parallelize the download_file function
            # and feed the tqdm progress bar with updates
            for _ in executor.map(download_zip, urls):
                pbar.update(1)


if __name__ == "__main__":
    set_up_threads(url_array)


