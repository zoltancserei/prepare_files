# Import neccessary modules
import os
import sys
import time
import shutil
import gzip
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# Set the path for chromedriver
PATH = r'D:\zoltancs\python_stuff\chromedriver.exe'

# Set up the download directory to be the current working directory in Chrome
chrome_options = webdriver.ChromeOptions()
directory = os.getcwd()
prefs = {'download.default_directory' : directory}
chrome_options.add_experimental_option('prefs', prefs)

# Define the parameters we are interested in downloading
params = ['batiments', 'parcelles', 'communes']

# Create a variable to store the insee of the communes we couldn't downlaod
not_found = []

def download_cadastre(number):
    # Set up selenium
    driver = webdriver.Chrome(PATH, options=chrome_options)

    # Check the cadastre number
    if number[:2] == '97': 
        # In this case the prefix is made of 3 digits
        prefix = number[:3]
        download_special(number, prefix, driver, params, not_found)
    else:
        prefix = number[:2]
        # In this case the prefix is made of 2 digits
        download_regular(number, prefix, driver, params, not_found)


def download_regular(number, prefix, driver, params, not_found):
    # Check if the page exists
    r = requests.get(f'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/{prefix}/{number}/')
    # If the page exists download the wanted files
    if r:
        driver.get(f'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/{prefix}/{number}/')
        
        for param in params:
            try:
                element = driver.find_element_by_xpath(f"//a[text()[contains(.,'{param}')]]")
                element.click()
            except NoSuchElementException:
                pass
    else:
        not_found.append(number)
        print(f' --- Download unsuccessful for cadastre {number}, because of the following error code: {r.status_code}. ---')
    time.sleep(1) # Waiting for the downloads to complete.
    driver.close()


def download_special(number, prefix, driver, params, not_found):
    # Check if the page exists    
    r = requests.get(f'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/{prefix}/{number}/')
    # Download the wanted files if the insee starts with 97
    if r:
        driver.get(f'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/{prefix}/{number}/')

        for param in params:
            try:
                element = driver.find_element_by_xpath(f"//a[text()[contains(.,'{param}')]]")
                element.click()
            except NoSuchElementException:
                pass     
    else:
        not_found.append(number)
        print(f' --- Download unsuccessful for cadastre {number}, because of the following error code: {r.status_code}. ---')
    time.sleep(1) # Waiting for the downloads to complete.
    driver.close()


# Unzip the downloaded files
def unzip():
    #Define the current working directory and the file extension
    directory = os.getcwd()
    extension = '.gz'
    
    # Loop through the items in the directory, check for '.gz' extension and extract them
    for item in os.listdir(directory):
        if item.endswith(extension): 
            filename = os.path.join(directory, item)
            extracted_filename = filename.replace(extension, '') # Remove the '.gz' extension from the filename
            with gzip.open(filename, 'r') as f_in, open(extracted_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.remove(filename)

    # Create the folders
    new_folders = ['Batiments', 'Communes', 'Parcelles', 'Deliverable']
    for folder in new_folders:
        new_folder = fr"{directory}\{folder}"
        os.makedirs(new_folder, exist_ok=True)

    # Move the files to their folders
    files = [file for file in os.listdir(directory) if file.endswith('.json')]
    for file in files:
        cadastre = file.split('-')[-1] # Extract the cadastre type (ex.: batiments.json) from the name
        file_name = os.path.join(directory, file)
        folder_name = os.path.join(directory, cadastre.split('.')[0].title()) # Generate the folder name (ex.: Batiments)
        new_file = os.path.join(folder_name, file)
        if os.path.exists(new_file): # If the file already exists, overwrite it
            os.remove(new_file)
        shutil.move(file_name, folder_name)

def download_multiple():
    for item in os.listdir(directory):
        if item.endswith('.txt'):
            file_name = item
    with open (file_name,'r') as f:
        insee_list = f.read().split('\n')
    for insee in insee_list:
        download_cadastre(insee.strip())

def main():
    assert len(sys.argv[1]) == 5 or sys.argv[1] == "insee", " --- The input must be a number of 5 digits or 'insee' if you are trying to download multiple municipalities (communes)! ---"

    if sys.argv[1] == 'insee':
        # Get the insee numbers from a text file
        download_multiple()
        unzip()
    else:
        # Get the cadastre number from the command line
        number = sys.argv[1]
        download_cadastre(number)
        unzip()

    if not_found:
        print(f" --- Could not download the commune(s) for the following insee: {(', '.join(not_found))}. ---")
    else:
        print(" --- Successfully downloaded the requested files. ---")

if __name__ == "__main__":
    main()
