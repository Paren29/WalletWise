from PIL import Image
from pdf2image import convert_from_path
from dateutil.parser import parse
from pytesseract import pytesseract
# import cv2
# import numpy as np
import pandas as pd
import re
import configparser

config = configparser.ConfigParser()
config.read('secrets.txt')

class CommBank:

    def __init__(self, file):
        self.file = file

    def is_date(self, text, fuzzy=False):
        """Checks whether string is a date or not

        Args:
            text (string): Text of datatype string
            fuzzy (bool, optional): Defaults to False.

        Returns:
            bool: True/False
        """
        try:
            parse(text, fuzzy=fuzzy)
            return True
        except ValueError:
            return False


    def extract_text_from_image(self, pages):
        """Extracting text from image. Uses Python wrapper for Tesseract OCR engine from Google.
        Returns the extracted text from the image in datatype string.
        
        The reason behind converting pdf files to image has been to avoid hassle of reading pdf files and
        implementing data manipulation techniques for several use-cases. Although it sounds counter-intuitive,
        the implementation makes more sense from the development perspective.

        Args:
            pages (PPM): Document pages in the form of Image

        Returns:
            list: A list containing elements equal to the number of pages in the document. Each element will contain extracted text from the page.
        """
        pytesseract.tesseract_cmd = config['DEFAULT']['PYTESSERACT_PATH']
        text = pytesseract.image_to_string(pages, config=pytesseract.tesseract_cmd) #  config=' --psm 3'
        return text


    def filter_transactions(self, pages):
        """This function extracts text(everything written in the page) from image.
        Data cleaning methods are applied to filter out unnecessary details.
        Since each page contains information besides financial transactions, we create a start-stop pattern that directs algorithm to start/stop scanning the text. 
        For each page, this will be unique.
        e.g.    Start indicator for each page will be unique. It will be the date of the first transaction e.g. '03 Feb 2023'
        Stop indicator for each page will vary as per page number.
        e.g.    Indicator for algorithm to stop scanning will be the word 'Created' if its not the last page of the document,
        else, it will be 'Any pending transactions' 

        Args:
            pages (list): List of PIL element equal to the number of pages in the document.

        Returns:
            dict: A dictionary with keys indicating the text of a particular page number and its values containing text as string of the scanned transactions.
        """
        extracted_text = []
        name = []
        for page_number, page_content in enumerate(pages):
            text = self.extract_text_from_image(page_content)
            # check if the page is blank (empty text)
            if text == '':
                continue
            extracted_text.append(text)
            name.append('page'+f'{page_number}'+'text')
            name.append('page'+f'{page_number}'+'start')
            name.append('page'+f'{page_number}'+'stop')
        
        text_details = dict()
        # regex pattern to scan dates in the format DD MM YYYY. e.g. '03 Feb 2023'
        date_pattern = r"^\b\d{2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b"
        
        start_words = []
        stop_words = []

        for page_count in range(len(extracted_text)):
            text = extracted_text[page_count]
            text_list = text.splitlines()
            
            for element in text_list:
                # Scans the transactions and scans for date_pattern in an element. If selected, appends to start_words list
                if re.findall(date_pattern, element):
                    date = re.search(date_pattern, element)
                    start_words.append(element[date.regs[0][0] : date.regs[0][1]])
                    break

        # populates stop_words list    
        i = 0
        while i < len(start_words):
            if 'Any pending transactions ' in extracted_text[i]:
                stop_words.append('Any pending transactions')
            else:
                stop_words.append('Created')
            i += 1
            
        page_index = 0
        normal_counter = 0
        
        while normal_counter < len(start_words):
            # splitting lines and removing blank elements from the list 
            text_details[name[page_index]] = list(filter(None, extracted_text[normal_counter].splitlines()))

            # filtering transactions
            text_details[name[page_index+1]] = [j for j, element in enumerate(text_details[name[page_index]]) if start_words[normal_counter] in element][0]
            text_details[name[page_index+2]] = [k for k, element in enumerate(text_details[name[page_index]]) if stop_words[normal_counter] in element][0]
            
            text_details[name[page_index]] = text_details[name[page_index]][text_details[name[page_index+1]]: text_details[name[page_index+2]]] # +1:
        
            # remove key-value pairs that contains start-stop details of a page
            del text_details[name[page_index+1]]
            del text_details[name[page_index+2]]

            page_index += 3
            normal_counter += 1
            
        return text_details
    

    def data_preprocessing(self, transaction_details):
        """This function is responsible for stiching elements present in the value of a dictionary to a string and return as a
        human readable transaction. 
        e.g. DD MM YYYY Monthly Allowance to myself $xxxx.xx $xxxx.xx

        Args:
            transaction_details (dict): A key-value pair containing elements same as number of pages. 
            Keys suggest the text for a particular page number and its value contains the actual text in form of string elements.

        Returns:
            list: String stichted together to form a human readable transaction.
            Number of elements in the list equal to the number of transactions in the scanned document.
        """
        transactions = []

        # for each element in the value of dict
        for _, value in transaction_details.items():
            count = 0
            # while the counter does not reach the last element of the dict values
            while count < len(value):
                i = 1
                # if the first three elements of the dict values is a date 
                if count+i < len(value) and self.is_date(' '.join(value[count].split()[:3])):                    # 'count + i < ...' check is to avoid end of list error
                    # then select all the elements until a similar condition is not met and append them
                    # e.g. | start | 03 Feb 2023 xxx xxx $xxx.xx $xxx.xx | stop | start |10 Feb 2023
                    while count+i < len(value) and not self.is_date(' '.join(value[count+i].split()[:3])):
                        i += 1
                    transactions.append(' '.join(value[count: count + i]))
                count += i

        return transactions


    def data_cleaning(self, data):
        """Providing appropriate headers to each transaction and creating a dataframe.
        This dataframe will be passed onto the main file where similar dataframes will be then merged and a csv or xlsx file
        will be created from it.

        Args:
            data (list): A list containing all individual transactions as elements.
            Total number of elements same as transactions scanned.

        Returns:
            DataFrame: A Pandas DataFrame containing the same details in a structured manner.
        """

        # It is not advisable to create a dataframe first and then expand it.
        # List of headers for pandas dataframe.
        transaction_dict = {'Date processed' : [], 'Date of transaction': [], 'Details': [], 'Amount': []}

        # for each transaction
        for element in data:
            # Split the first three elements of string i.e. dates to the first header
            transaction_dict['Date processed'].append(' '.join(element.split()[:3]))
            
            # if a string of interest is found then add successive strings to the second header else copy it from the above
            if 'Value Date:' in element:
                transaction_dict['Date of transaction'].append(element.split('Value Date: ')[1].split()[0])
            else:
                transaction_dict['Date of transaction'].append(' '.join(element.split()[:3]))
            
            # everything except the date and the strings after '$' sign goes to this header. Contains transaction details
            transaction_dict['Details'].append(re.search(r'\d{1,2} [A-Za-z]+ \d{4}(?:\.\s+)?(.+?)(?:\$|\-\$)', element).group(1))

            # add everything after the first '$' sign here.
            # If the transaction details contains the sign '$', this will fail
            if element.count("$") == 2:
                count = 0
                temp_amount = []
                for word in element.split():
                    if '$' in word:
                        count += 1
                        temp_amount.append(word)
                if count % 2 == 0:
                        transaction_dict['Amount'].append(temp_amount[0])

            elif element.count("$") < 2:
                transaction_dict['Amount'].append(None)

        CBA_data = pd.DataFrame(transaction_dict)
        return CBA_data


    def main(self):
        
        pages = convert_from_path(self.file, poppler_path=config['DEFAULT']['POPPLER_PATH'])
        file_details = self.filter_transactions(pages)
        transaction_list = self.data_preprocessing(file_details)
        CBA_data = self.data_cleaning(transaction_list)

        # forward data to main file
        return CBA_data