import pandas as pd
import numpy as np
from IPython.display import display
from ..utils.logger import Logger


class ShowInfoMixin:

    def get_schema(self) -> dict:
        return self.data.dtypes.apply(lambda x: x.name).to_dict()

    def update_schema(self, new_schema: dict) -> None:
        self.data = self.data.astype(new_schema)
        return self.data

    def show_info(self, num_rows: int = None, **kwargs) -> None:
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
        display(self.data.describe(datetime_is_numeric=True), **kwargs)
        print(f"\n{decor_section}\nINFO:\n")
        print(f"{decor_title}\n{self.data.info()}\n{decor_section}")
        for col in self.data.select_dtypes(exclude=np.number).columns:
            if pd.api.types.is_categorical_dtype(self.data[col]):
                display(self.data[col].value_counts())
