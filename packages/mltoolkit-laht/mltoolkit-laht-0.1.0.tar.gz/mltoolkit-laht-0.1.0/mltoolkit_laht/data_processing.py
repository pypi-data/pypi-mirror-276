import pandas as pd

from typing import Any, TypeVar
import pandas as pd

T = TypeVar('T', bound='pd.DataFrame')

class DataSource:
    @staticmethod
    def load_data(file_path: str, **kwargs) -> T:
        """
        Load data from a CSV file.

        Parameters:
        file_path (str): Path to the CSV file.

        Returns:
        DataFrame: Loaded data.
        """
        file_extension = file_path.split('.')[-1]
        if file_extension == 'csv':
            return pd.read_csv(file_path, **kwargs)
        elif file_extension == 'pkl' or file_extension == 'pickle':
            return pd.read_pickle(file_path, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {file_path}. Only read pkl, pickle, and csv files.")

    @staticmethod
    def show_info(title: str, to_show: Any) -> None:
        """
        Print the title and the content to show.

        Parameters:
        title (str): The title to print.
        to_show (Any): The content to print.

        Returns:
        None
        """
        print(f"{title}:\n{'-'*10}\n{to_show}\n{'_'*100}\n")

    @staticmethod
    def clean_data(df: T) -> T:
        """
        Clean the input DataFrame.

        Parameters:
        df (DataFrame): Input data.

        Returns:
        DataFrame: Cleaned data.
        """
        raise NotImplementedError("This method needs to be implemented")

    @staticmethod
    def transform_data(df: T) -> T:
        """
        Transform the input DataFrame.

        Parameters:
        df (DataFrame): Input data.

        Returns:
        DataFrame: Transformed data.
        """
        # Implement your data transformation logic here
        raise NotImplementedError("This method needs to be implemented")