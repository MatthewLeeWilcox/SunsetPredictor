import os
import pickle
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import threading
import numpy as np
import pandas as pd
import multiprocessing
import time
import concurrent.futures
from datetime import datetime


# Set the working directory for program
current_directory = os.getcwd()
target_directory = os.path.dirname(current_directory)
os.chdir(target_directory)

#Error File data
current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# Define file name
error_file_name = f"{current_timestamp}_error.txt"
with open(error_file_name, "w") as file:
    file.write("Errors:\n")

# Function to download files
def download_file(url, heading):
    filename = heading + url.rsplit('/', 1)[-1]
    try:
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
            # print(f"Downloaded {filename} successfully.")
    except:
        print("Failed to download the file.")
        with open(error_file_name, 'a') as file:
            # Write or append content to the file
            file.write(f"{url}\n")

# def download_file(url, filename):
#     response = requests.get(url)
#     if response.status_code == 200:  # Check if the request was successful
#         with open(filename, 'wb') as file:
#             file.write(response.content)
#         # print(f"Downloaded {filename} successfully.")
#     else:
#         print("Failed to download the file.")
#         with open('error.txt', 'a') as file:
#             # Write or append content to the file
#             file.write("{filename}\n")

# Import Pickle
pickle_file_path = 'SkyImageCollection/url_scraped_files.pickle'

with open(pickle_file_path, "rb") as f:
    # Load the data from the pickle file
    url_data = pickle.load(f)

# Check for Data Folder
if not os.path.exists('Data'):
    os.makedirs('Data')


# data_file_paths = np.char.add('Data/',np.array([x.rsplit('/', 1)[-1] for x in url_data]))

# print(data_file_paths)
print("Begin Scrape")



def set_up_threads(urls):
    with ThreadPoolExecutor() as executor:
        # Create a tqdm instance with total number of URLs to track progress
        with tqdm(total=len(urls)) as pbar:
            # Use executor.map to parallelize the download_file function
            # and feed the tqdm progress bar with updates
            for _ in executor.map(download_file, urls, ["Data/"]*len(urls)):
                pbar.update(1)
# def set_up_threads(urls):
#     l = len(urls)
#     with tqdm(total=l) as pbar:
#         with ThreadPoolExecutor(max_workers=num_cores) as executor:
#             future = {executor.submit(download_file,urls): arg for arg in urls}
#             for future in concurrent.futures.as_completed(future):
#                 pbar.update(1)

# def set_up_threads(urls, file_path):
#     with ThreadPoolExecutor(max_workers=num_cores) as executor:
#         return tqdm(executor.map(download_file,
#                                 urls,
#                                 file_path,
#                                 timeout = 5))
#                                     #  total=len(urls))

if __name__ == "__main__":
    set_up_threads(url_data)
# print(len(url_data))

# Set Counter
# counter = 0

# Download Files
# for url in tqdm(url_data):
#     file_path = 'Data/' + url.rsplit('/', 1)[-1]
#     download_file(url, file_path)
#     counter += 1
#     if counter % 10 == 0:
#         with open('Crash_RemainingList.pickle', 'wb') as f:
#             pickle.dump(url_data[counter:], f)