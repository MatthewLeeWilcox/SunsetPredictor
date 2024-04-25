# Import Packages
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pickle
#Intial Url Selection
url = "https://gml.noaa.gov/aftp/data/radiation/surfrad/TSI/Daily/"


#ignore Performed finding the source list in a ipynb
data = requests.get(url).text

soup = BeautifulSoup(data,'html.parser')


# Source optained from ipynb
Image_source_list =np.array( [ 'BND-Images/', 'DRA-Images/', 'FPK-Images/',
       'GWN-Images/', 'PSU-Images/', 'RUT-Images/', 'SLV-Images/',
       'SXF-Images/', 'TMT-Images/', 'WAS-Images/'])
#Combine the Intial URL with locations
image_source_url = np.char.add(url, Image_source_list)


#Function to scrape all list values inside the year. 
def scrape_table_urls(input_url_array, mask_val =False):
    loc_year_url_list = np.array([])
    for source in tqdm(input_url_array):
        # print(source)
        dataLoc = requests.get(source).text
        soupLocation = BeautifulSoup(dataLoc, 'html.parser')

        tableLocation = soupLocation.find('table')

        rowsLoc = []
        for row in tableLocation.find_all('tr'):
            cols = [col.get_text(strip=True) for col in row.find_all('td')]
            rowsLoc.append(cols)
        rowsLoc = rowsLoc[3:]
        rowsLoc = np.array(rowsLoc[:-1])
        rowsLoc = rowsLoc[:,1]
        if mask_val == True:
            mask = np.char.endswith(rowsLoc, '/')
            rowsLoc = rowsLoc[mask]
        return_year_array = np.char.add(source, rowsLoc)
        loc_year_url_list = np.append(loc_year_url_list, return_year_array)
    return loc_year_url_list

print("Scrape Location")
scraped_loc = scrape_table_urls(image_source_url, True)
print("Scrape Years")
year_scraped = scrape_table_urls(scraped_loc, False)
print("Completed!")
with open('url_scraped_files.pickle', 'wb') as f:
    pickle.dump(year_scraped, f)