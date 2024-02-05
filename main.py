import glob, os
import pandas as pd
import configparser
import re
from CBA import CommBank
from NAB import nab
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


def process_files(filename, date_pattern):

    monthly_files = {}
    for file in filename:
        year = f'{re.search(date_pattern, file).group(2)}'
        month = f'{re.search(date_pattern, file).group(1)}'

        if year not in monthly_files:
            monthly_files[year] = {}
        if month not in monthly_files[year]:
            monthly_files[year][month] = []

        # check if different files belong to same month
        if 'CBA' in file or 'TransactionSummary' in file:
            commbank_files = CommBank(file)
            temp_df = commbank_files.main()
            monthly_files[year][month].append(temp_df)
            # monthly_files.setdefault(temp_keys, []).append(temp_df)

        elif 'NAB' in file or 'nab' in file:
            nab_files = nab(file)
            temp_df = nab_files.main()
            monthly_files[year][month].append(temp_df)
            # monthly_files.setdefault(temp_keys, []).append(temp_df)

    # check if same month has multiple files
    for years in monthly_files:
        for months in monthly_files[years]:
            transactions = monthly_files[years][months]
            monthly_df = pd.concat(transactions, ignore_index=True)
            monthly_files[years][months] = monthly_df
            del transactions
    
    for year in monthly_files:
        file_name = f'{year}.xlsx'
        file_address = f"{config['DEFAULT']['BOOK_ADDRESS']}/{file_name}"
        for month in monthly_files[year]:
            sheet_name = f'{month}'
            if not os.path.isfile(file_address):
                with pd.ExcelWriter(file_address, engine='openpyxl', mode='w') as writer:
                    monthly_files[year][month].to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                with pd.ExcelWriter(file_address, engine='openpyxl', mode='a') as writer:
                    monthly_files[year][month].to_excel(writer, sheet_name=sheet_name, index=False)
    return monthly_files


def main():
    file_path = config['DEFAULT']['FILE_PATH']
    filename = readfiles(file_path)
    date_pattern = r'(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|Sept|September|Oct|October|Nov|November|Dec|December)(\d{2,4})'
    process_files(filename, date_pattern)

if __name__ == "__main__":
    main()