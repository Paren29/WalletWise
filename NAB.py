from pdf2image import convert_from_path
from dateutil.parser import parse
from pytesseract import pytesseract
import pandas as pd
import re
import configparser

config = configparser.ConfigParser()
config.read('secrets.txt')

class nab:

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


    def extract_text_from_image(self, page):
        """Extracting text from image. Uses Python wrapper for Tesseract OCR engine from Google.
        Returns the extracted text from the image in datatype string.
        
        The reason behind converting pdf files to image was to avoid hassle of reading pdf files and
        implementing data manipulation techniques for several use-cases. Although it sounds counter-intuitive,
        the implementation makes more sense from the development perspective.

        Args:
            pages (PPM): Document pages in the form of Image

        Returns:
            list: A list containing elements equal to the number of pages in the document. Each element will contain extracted text from the page.
        """
        pytesseract.tesseract_cmd = config['DEFAULT']['PYTESSERACT_PATH']
        text = pytesseract.image_to_string(page, config=pytesseract.tesseract_cmd) # if it fails, use config=' --psm 3'
        return text


    def filter_transactions(self, pages):
        """This function extracts text(everything written in the page) from image.
        Data cleaning methods are applied to filter out unnecessary details.
        Since each page contains information besides financial transactions, we create a start-stop pattern that directs algorithm to start/stop scanning the text.

        Args:
            pages (list): List of PIL element equal to the number of pages in the document.

        Returns:
            dict: A dictionary with keys indicating the text of a particular page number and its values containing text as string of the scanned transactions.
        """
        text = []
        transactions = []

        for content in pages[1:]:
            text = self.extract_text_from_image(content)
            
            temp_text = text.splitlines()
            temp_text = list(filter(None, temp_text))

            for words in temp_text:
                if self.is_date(words.split(' ')[0]) and self.is_date(words.split(' ')[1]) and not 'INTERNET ' in words:
                    transactions.append(words)
        
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
        transaction_dict = {'Date processed': [], 'Date of transaction': [], 'Details': [], 'Amount': []}

        for element in data:
            transaction_dict['Date processed'].append(' '.join(element.split()[:1]))
            transaction_dict['Date of transaction'].append(' '.join(element.split()[1:2]))

            """ Breakdown of regex expression
            (\d{2}\/\d{2}\/\d{2}\s\d{2}\/\d{2}\/\d{2}\s)+:  This part matches a sequence of date strings in the format DD/MM/YY followed by spaces. The + at the end ensures that this sequence can occur one or more times.
            (7202 |V7202 ):                                 This part matches either "7202 " or "V7202 ". The space after the options ensures that it is not part of a longer number.
            (.*?):                                          This part is a non-greedy capture group that matches any characters (except for a newline) zero or more times. The non-greedy operator ? ensures that it captures the shortest possible match.
            (\d{1,3}(?:,\d{3})*(?:\.\d{1,3})):              This part captures a numerical value that may include commas as thousand separators and a dot as a decimal separator.
            """
            
            transaction_dict['Details'].append(re.search(r'(\d{2}\/\d{2}\/\d{2}\s\d{2}\/\d{2}\/\d{2}\s)+(7202 |V7202 )(.*?)(\d{1,3}(?:,\d{3})*(?:\.\d{1,3}))', element).group(3))
            transaction_dict['Amount'].append(''.join(element.split()[-1]))

        NAB_data = pd.DataFrame(transaction_dict)
        return NAB_data    


    def main(self):

        pages = convert_from_path(self.file, poppler_path=config['DEFAULT']['POPPLER_PATH'])
        transactions_list = self.filter_transactions(pages)
        NAB_data = self.data_cleaning(transactions_list)

        # forward data to main file
        return NAB_data