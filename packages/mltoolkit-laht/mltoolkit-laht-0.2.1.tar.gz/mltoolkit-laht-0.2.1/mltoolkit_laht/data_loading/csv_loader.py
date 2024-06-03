import os
import pandas as pd
import numpy as np
from IPython.display import display
from .base_loader import BaseLoader


class CSVLoader(BaseLoader):
    def __init__(
        self,
        file_path: str = None,
        data: pd.DataFrame = None,
    ) -> None:
        super().__init__(file_path)
        self.data = data

        if not isinstance(self.data, pd.DataFrame) and self.file_path is None:
            msg = "Please provide either a DataFrame or a file path."
            self.logger.error(msg)
            raise ValueError(msg)

    def load_data(self, **kwargs) -> pd.DataFrame:
        """
        Load data from a CSV file.

        Parameters:
        **kwargs: specific parameters for the read_csv or read_pickle method.

        Returns:
        None
        """
        if self.file_path:
            _, file_extension = os.path.splitext(self.file_path)
            file_extension = file_extension[1:]  # remove the leading dot

        if isinstance(self.data, pd.DataFrame):
            self.logger.info("Loading data from DataFrame.")
            return self.data
        else:
            if file_extension == "csv":
                self.logger.info("Reading data from a CSV file.")
                self.data = pd.read_csv(self.file_path, **kwargs)
            elif file_extension in ["pkl", "pickle"]:
                self.logger.info("Reading data from a pickle file.")
                self.data = pd.read_pickle(self.file_path, **kwargs)
            else:
                msg = f"Unsupported file type: {self.file_path}. Only read .pkl, .pickle, and .csv files."
                self.logger.error(msg)
                raise ValueError(msg)
            return self.data

    def get_schema(self) -> dict:
        return self.data.dtypes.apply(lambda x: x.name).to_dict()

    def update_schema(self, new_schema: dict) -> None:
        self.data = self.data.astype(new_schema)
        return self.data

    def show_info(self, num_rows: int = None, describe_all: str = "all") -> None:
        """
        Show data information, including the first few rows, schema, shape, NANs, duplicates, and statistics.

        Parameters:
        - num_rows (int): The number of rows to display. If None, all rows will be displayed.
        - describe_all (str): The option to include all columns in the describe method.
          Possible values: "all", "None", "number", "category", "datetime", "timedelta".
          Default is "all".

        Returns:
        None
        """
        if num_rows:
            pd.set_option("display.max_rows", num_rows)

        decor_title = "-" * 10
        decor_section = "=" * 100
        data = self.data  # load data once

        def print_section(name, content):
            print(f"{decor_section}\n{name}:\n{decor_section}")
            print(content)

        print(f"{decor_section}\nINFO:\n{decor_section}")
        display(data.head())
        print_section("SCHEMA", data.dtypes)
        print_section("DATAFRAME SHAPE", data.shape)
        print_section("NANs", data.isna().sum())
        print_section("GENERAL DUPLICATED", data.duplicated().sum())
        print(f"{decor_section}\nSTATISTICS:\n{decor_section}")
        display(data.describe(include=describe_all))

        print(f"{decor_section}\nINFO:\n{decor_section}")
        data.info(verbose=True)

        categorical_columns = data.select_dtypes(exclude=np.number).columns
        categorical_value_counts = [
            data[col].value_counts()
            for col in categorical_columns
            if pd.api.types.is_categorical_dtype(data[col])
        ]

        for value_counts in categorical_value_counts:
            display(value_counts)
