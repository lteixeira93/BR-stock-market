from datetime import date

import pandas as pd

import settings
from file_manager import FileManager


class FileManagerXLSX(FileManager):
    filename = str(date.today()) + settings.XLSX_FILENAME

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileManagerXLSX, cls).__new__(cls)
        return cls.instance
    # end def

    def store_on_disk(
            self,
            stocks_data_frame: pd.DataFrame
    ) -> None:
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        try:
            stocks_data_frame.to_excel(writer, sheet_name='Most_valuable_stocks', startrow=0)
        except PermissionError as e:
            input(f"{e} - Could not write the spreadsheet.")

        writer.close()
    # end def
