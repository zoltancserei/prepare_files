# Import neccessary modules
import os
import sys
import time
import shutil
import gzip
from selenium import webdriver

def download_cadastre():
    # Set up the download directory to be the current working directory in Chrome
    chrome_options = webdriver.ChromeOptions()
    directory = os.getcwd()
    prefs = {'download.default_directory' : directory}
    chrome_options.add_experimental_option('prefs', prefs)

    # Enter the cadastre number
    number = sys.argv[1]
    prefix = number[:2]

    # Check if the input has correct format
    if len(number) != 5:
        print('The number must have 5 digits!')
        sys.exit()

    # Set up selenium
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH, options=chrome_options)
    driver.get(f'https://cadastre.data.gouv.fr/data/etalab-cadastre/2021-02-01/geojson/communes/{prefix}/{number}/')

    # Download the wanted files
    params = ['batiments', 'parcelles', 'communes']
    for param in params:
        element = driver.find_element_by_xpath(f"//a[text()[contains(.,'{param}')]]")
        element.click()

    time.sleep(2)
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


def main():
    download_cadastre()
    unzip()

if __name__ == "__main__":
    main()
