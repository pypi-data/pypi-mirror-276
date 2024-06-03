import pandas as pd
import json
from .base_loader import BaseLoader
from typing import Dict, Any


class JSONLoader(BaseLoader):

    def __init__(self, filepath: str):
        """
        Initialize a JSONLoader object.

        Parameters:
        filepath (str): Path to the JSON file.
        """
        self.filepath = filepath

    def load_json_pandas(self, **kwargs) -> pd.DataFrame:
        """
        Load data from a JSON file into a pandas DataFrame.

        Parameters:
        **kwargs: Arbitrary keyword arguments to pass to the pandas read_json function.

        Returns:
        pd.DataFrame: Data from the JSON file.
        """
        return pd.read_json(self.filepath, **kwargs)

    def load_json_file(self, **kwargs) -> Dict[str, Any]:
        """
        Load raw data from a JSON file.

        Parameters:
        **kwargs: Arbitrary keyword arguments to pass to the json load function.

        Returns:
        dict: Raw data from the JSON file.
        """
        with open(self.filepath, "r", **kwargs) as f:
            data = json.load(f)
        return data

    def load_json_string(self, **kwargs) -> str:
        """
        Read a JSON file as a string.

        Parameters:
        **kwargs: Arbitrary keyword arguments to pass to the file read function.

        Returns:
        str: Contents of the JSON file.
        """
        with open(self.filepath, "r", **kwargs) as f:
            data = f.read()
        return data
