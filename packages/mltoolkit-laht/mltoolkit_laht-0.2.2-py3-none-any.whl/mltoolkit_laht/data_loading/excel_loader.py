import pandas as pd
from .base_loader import BaseLoader


class ExcelLoader(BaseLoader):
    """
    A class to load data from an Excel file using pandas.
    """

    def __init__(self, file_path, sheet_name=0):
        super().__init__(file_path)
        self.sheet_name = sheet_name
        self.data = None

    def load_data(self) -> pd.DataFrame:
        """
        Loads data from the specified Excel file and sheet.

        Returns:
        --------
        pd.DataFrame
            The loaded data as a pandas DataFrame.

        Raises:
        -------
        ValueError
            If there is an error loading the Excel file.
        """
        self.logger.debug(f"Attempting to load data from Excel file: {self.file_path}, sheet: {self.sheet_name}")
        try:
            self.data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            self.logger.info(f"Data loaded successfully from {self.file_path}, sheet: {self.sheet_name}")
            return self.data
        except Exception as e:
            self.logger.error(f"Failed to load data from {self.file_path}, sheet: {self.sheet_name}. Error: {e}", exc_info=True)
            raise ValueError(f"Failed to load data from {self.file_path}, sheet: {self.sheet_name}") from e
