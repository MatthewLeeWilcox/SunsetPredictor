import requests
import pickle
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

# Set the working directory for program
current_directory = os.getcwd()
target_directory = os.path.dirname(current_directory)
os.chdir(target_directory)

# Function to download files
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:  # Check if the request was successful
        with open(filename, 'wb') as file:
            file.write(response.content)
        # print(f"Downloaded {filename} successfully.")
    else:
        print("Failed to download the file.")


# Import Pickle
pickle_file_path = 'SkyImageCollection/url_scraped_files.pickle'

with open(pickle_file_path, "rb") as f:
    # Load the data from the pickle file
    url_data = pickle.load(f)

# Check for Data Folder
if not os.path.exists('Data'):
    os.makedirs('Data')

# Set Counter
counter = 0

# Download Files
for url in tqdm(url_data):
    file_path = 'Data/' + url.rsplit('/', 1)[-1]
    download_file(url, file_path)
    counter += 1
    if counter % 10 == 0:
        with open('Crash_RemainingList.pickle', 'wb') as f:
            pickle.dump(url_data[counter:], f)