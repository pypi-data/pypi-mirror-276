import pandas as pd
import numpy as np
from IPython.display import display


class DataSource:

    SCHEMA_UPDATED = False

    def __init__(self, data: pd.DataFrame = None, file_path: str = None) -> None:
        self.file_path = file_path
        self.data = data

        if not isinstance(self.data, pd.DataFrame) and self.file_path is None:
            raise ValueError("Please provide either a DataFrame or a file path.")

    def load_data(self, **kwargs) -> pd.DataFrame:
        """
        Load data from a CSV file.

        Parameters:
        **kwargs: specific parameters for the read_csv or read_pickle method.

        Returns:
        None
        """
        if isinstance(self.data, pd.DataFrame):
            print("Loading data from DataFrame...")
            return self.data
        else:
            print("Loading data from a file...")
            file_extension = self.file_path.split(".")[-1]
            if file_extension == "csv":
                self.data = pd.read_csv(self.file_path, **kwargs)
            elif file_extension == "pkl" or file_extension == "pickle":
                self.data = pd.read_pickle(self.file_path, **kwargs)
            else:
                raise ValueError(
                    f"Unsupported file type: {self.file_path}. Only read pkl, pickle, and csv files."
                )
            return self.data

    def get_schema(self) -> dict:
        return self.data.dtypes.apply(lambda x: x.name).to_dict()

    def update_schema(self, new_schema: dict) -> None:
        self.data = self.data.astype(new_schema)
        SCHEMA_UPDATED = True
        return self.data

    def show_df_info(self, num_rows: int = None, describe_all: str = "all") -> None:
        """
        Print the title and the content to show.

        Parameters:
        title (str): The title to print.
        to_show (Any): The content to print.

        Returns:
        None
        """
        if num_rows:
            pd.set_option("display.max_rows", num_rows)

        decor_title = "-" * 10
        decor_section = "=" * 100

        print(f"{decor_section}")
        print(f"SAMPLE:\n{decor_title}")
        display(self.data.head())
        print(f"\n{decor_section}\n")
        print(f"SCHEMA:\n{decor_title}\n{self.data.dtypes}\n{decor_section}\n")
        print(f"DATAFRAME SHAPE:\n{decor_title}\n{self.data.shape}\n{decor_section}\n")
        print(f"NANs:\n{decor_title}\n{self.data.isna().sum()}\n{decor_section}\n")
        print(
            f"GENERAL DUPLICATED:\n{decor_title}\n{self.data.duplicated().sum()}\n{decor_section}\n"
        )
        print(f"STATISTICS:\n{decor_title}")
        display(self.data.describe(include=describe_all, datetime_is_numeric=True))
        print(f"\n{decor_section}\nINFO:\n")
        print(f"{decor_title}\n{self.data.info()}\n{decor_section}")
        for col in self.data.select_dtypes(exclude=np.number).columns:
            if pd.api.types.is_categorical_dtype(self.data[col]):
                display(self.data[col].value_counts())

    @staticmethod
    def clean_data(df: pd.DataFrame) -> None:
        """
        Clean the input DataFrame.

        Parameters:
        df (DataFrame): Input data.

        Returns:
        DataFrame: Cleaned data.
        """
        raise NotImplementedError("This method needs to be implemented")

    @staticmethod
    def transform_data(df: pd.DataFrame) -> None:
        """
        Transform the input DataFrame.

        Parameters:
        df (DataFrame): Input data.

        Returns:
        DataFrame: Transformed data.
        """
        # Implement your data transformation logic here
        raise NotImplementedError("This method needs to be implemented")
