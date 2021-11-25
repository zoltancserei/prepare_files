# Import neccessary modules
import os
import sys
import time
import shutil
import gzip
from selenium import webdriver

# Set the path for chromedriver
PATH = '\chromedriver.exe'

# Set up the download directory to be the current working directory in Chrome
chrome_options = webdriver.ChromeOptions()
directory = os.getcwd()
prefs = {'download.default_directory' : directory}
chrome_options.add_experimental_option('prefs', prefs)


def download_cadastre(number):
    # Set up selenium
    driver = webdriver.Chrome(PATH, options=chrome_options)
    # Check if the input has correct format
    if len(number) != 5:
        print('The number must have 5 digits!')
        sys.exit()

    # Check the cadastre number
    if number[:2] == '97':
        prefix = number[:3]
        download_special(number, prefix, driver)
    else:
        prefix = number[:2]
        download_regular(number, prefix, driver)


def download_regular(number, prefix, driver):
    # Download the wanted files
    driver.get(f'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/{prefix}/{number}/')
    params = ['batiments', 'parcelles', 'communes']
    for param in params:
        element = driver.find_element_by_xpath(f"//a[text()[contains(.,'{param}')]]")
        element.click()

    time.sleep(1)
    driver.close()


def download_special(number, prefix, driver):
    # Download the wanted files if the insee starts with 97
    driver.get(f'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/{prefix}/{number}/')
    params = ['batiments', 'parcelles', 'communes']
    for param in params:
        element = driver.find_element_by_xpath(f"//a[text()[contains(.,'{param}')]]")
        element.click()

    time.sleep(1)
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
        cadastre = file.split('-')[-1]
        file_name = fr"{directory}\{file}"
        folder_name = fr"{directory}\{cadastre.split('.')[0].title()}"
        shutil.move(os.path.join(directory, file), folder_name)


def download_multiple():
    file_name = 'insee.txt'
    with open (file_name,'r') as f:
        insee_list = f.read().split('\n')
    for insee in insee_list:
        download_cadastre(insee.strip())

def main():
    if sys.argv[1] == 'insee':
        # Get the insee numbers from a text file
        download_multiple()
        unzip()
    else:
        # Get the cadastre number from the command line
        number = sys.argv[1]
        download_cadastre(number)
        unzip()


if __name__ == "__main__":
    main()
