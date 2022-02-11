# prepare_files

This script is used to download cadastre files (communes, parcelles, batiments) to the specified insee code. 
The downloaded files will be unarchived and placed in individual folders.

To run the script you will need to have the Selenium framework installed and the a WebDriver depending on your browser.

With this script is possible to download the cadastre files for a single commune or for multiple commues. 
To download the files for multiple communes, a .txt file is required in the same directory where the .py file is.
In the text file each insee number should be in a new row and without any punctuation mark.

To run the script, simply run the command prompt from the directory where the .py file is located and all the files will be downloaded in that directory.

For a single commune type in command prompt: python prepare_files.py 00000

For multiple communes type in command prompt: python prepare_files.py insee. 
