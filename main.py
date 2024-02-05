import glob, os
import pandas as pd
import configparser
import re
from CBA import CommBank
from NAB import nab
from file_processing import Process_Files
from openpyxl import load_workbook

config = configparser.ConfigParser()
config.read('secrets.txt')

def readfiles(path):
    """Reads all the files with .pdf extension present in the folder

    Args:
        path (str): Absolute path to the folder

    Returns:
        list: List of pdf files 
    """
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
        pdfs.append(file)
    return pdfs


def main():
    file_path = config['DEFAULT']['FILE_PATH']
    filename = readfiles(file_path)
    date_pattern = r'(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|Sept|September|Oct|October|Nov|November|Dec|December)(\d{2,4})'
    new_files = Process_Files(filename, date_pattern)
    new_files.file_processing()

if __name__ == "__main__":
    main()