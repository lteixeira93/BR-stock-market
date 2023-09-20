from datetime import date

import pandas as pd

from FileManager import FileManager


class FileManagerXLSX(FileManager):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileManagerXLSX, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__filename = str(date.today())+'-most_valuables_BR_stocks.xlsx'

    def store_on_disk(self, stocks_data_frame: pd.DataFrame):
        writer = pd.ExcelWriter(self.__filename, engine='xlsxwriter')
        stocks_data_frame.to_excel(writer, sheet_name='Most_valuable_stocks', startrow=1)

        writer.close()
