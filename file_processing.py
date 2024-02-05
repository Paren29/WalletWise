import glob, os
import pandas as pd
import configparser
import re
from CBA import CommBank
from NAB import nab
from openpyxl import load_workbook

config = configparser.ConfigParser()
config.read('secrets.txt')

class Process_Files:

    def __init__(self, filename, date_pattern):
        self.date_pattern = date_pattern
        self.filename = filename
        
    
    def file_processing(self):
        """Merges data frames collected from different classes
        Args:
            filename (string): File Name with absolute location
            date_pattern (string): Regex expression to filter Month and Year

        Returns:
            None: Resultant dataframe is written as an excel file and thus returned nowhere
        """

        """
        Visualisation of nested dictionary
        monthly_files = 
        {
            '2023' : 
                    {
                        'Oct' : dataframe,
                        'Nov' : dataframe,
                        'Dec' : dataframe
                    },
            '2024' :
                    {
                        ...
                    }
        }
        """
        monthly_files = {}
        
        for file in self.filename:
            year = f'{re.search(self.date_pattern, file).group(2)}'
            month = f'{re.search(self.date_pattern, file).group(1)}'

            if year not in monthly_files:
                # create a key (year) if it does not exist
                monthly_files[year] = {}

            if month not in monthly_files[year]:
                # create a nested key (month) if it does not exist
                monthly_files[year][month] = []

            # process files as per its nominated bank
            if 'CBA' in file or 'TransactionSummary' in file:
                commbank_files = CommBank(file)
                temp_df = commbank_files.main()
                monthly_files[year][month].append(temp_df)

            elif 'NAB' in file or 'nab' in file:
                nab_files = nab(file)
                temp_df = nab_files.main()
                monthly_files[year][month].append(temp_df)

        # concat files if a single month has transactions in more than one bank
        for years in monthly_files:
            for months in monthly_files[years]:
                transactions = monthly_files[years][months]
                monthly_df = pd.concat(transactions, ignore_index=True)
                monthly_files[years][months] = monthly_df
                del transactions
        
        # create an excel file if it does not exist, else append to it
        # Sheet name - {year}.xlsx
        # Workbook name - {month}
                    
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
        return None