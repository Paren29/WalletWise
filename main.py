import glob, os
import pandas as pd
import configparser
import re
from CBA import CommBank
from NAB import nab

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


def write_to_excel(df, excel_file, sheet_name):
    """
    Writes a DataFrame to an Excel file, creating a new sheet for each unique dataframe.

    Parameters:
    - df: pandas DataFrame to be written
    - excel_file: Name of the Excel file
    - sheet_name: Name of the sheet in Excel
    """
    # Check if the Excel file exists

    # TODO - Sheet 'Dec' already exists and if_sheet_exists is set to 'error'.
    if not os.path.isfile(excel_file):
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def main():
    
    file_path = config['DEFAULT']['FILE_PATH']
    filename = readfiles(file_path)
    
    date_pattern = r'(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|Sept|September|Oct|October|Nov|November|Dec|December)(\d{2,4})'

    for file in filename:
        # file = '/Users/parenkansara/Desktop/Explorer/Personal Project/HomeProject/Phase1/to_process/CBASept2023.pdf'
        if 'CBA' in file:
            commbank_files = CommBank(file)
            print(f"Currently processing {file}")
            temp_df = commbank_files.main()
        elif 'NAB' in file:
            nab_files = nab(file)
            temp_df = nab_files.main()
    
        # book name - 'year'.xlsx
        # sheet name - 'month'.xlsx
        year_book = f'{re.search(date_pattern, file).group(2)}.xlsx'
        book_address = f"{config['DEFAULT']['BOOK_ADDRESS']}/{year_book}"
        sheet_name = f'{re.search(date_pattern, file).group(1)}'
        
        write_to_excel(temp_df, book_address, sheet_name)
        print(f"Data added to a file {year_book} and created/modified the workbook {sheet_name}")

if __name__ == "__main__":
    main()