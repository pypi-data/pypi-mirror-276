from .base_plotter import BasePlot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Union


class DistributionPlot(BasePlot):
    def __init__(
        self,
        figsize: Tuple[int, int] = (10, 6),
        title: str = "Plot",
        x_label: str = "X-axis",
        y_label: str = "Y-axis",
    ) -> None:
        super().__init__(figsize, title, x_label, y_label)

    def plot_distributions(
        self,
        data: Union[pd.DataFrame, pd.Series],
        show_kde: bool = True,
        combine_plots: bool = False,
        standardize: bool = False,
    ) -> None:
        """
        Plot the distribution of one or more pandas series. If combine_plots is True, combine all plots of the same type into a single graph.

        NOTE: It is important to define the dtype of the columns in the DataFrame before using this method.

        Parameters:
        data (pd.DataFrame or pd.Series): Dataframe or Series.
        show_kde (bool): If True, show the KDE plot for numerical variables.
        combine_plots (bool): If True, combine all plots of the same type into a single graph.
        standardize (bool): If True and combine_plots is True, standardize numerical variables.
        """
        if isinstance(data, pd.Series):
            numerical_data = (
                [(data.name, data)] if pd.api.types.is_numeric_dtype(data) else []
            )
            categorical_data = (
                [(data.name, data)] if pd.api.types.is_categorical_dtype(data) else []
            )
        elif isinstance(data, pd.DataFrame):
            numerical_data = [
                (name, series)
                for name, series in data.items()
                if pd.api.types.is_numeric_dtype(series)
            ]
            categorical_data = [
                (name, series)
                for name, series in data.items()
                if pd.api.types.is_categorical_dtype(series)
            ]
        else:
            raise ValueError(
                "Unsupported data type. Only support pandas Series or DataFrame."
            )

        # Plot numerical data
        if numerical_data:
            self._plot_data(
                data=numerical_data,
                title="Numerical Data",
                show_kde=show_kde,
                combine_plots=combine_plots,
                standardize=standardize,
            )
        else:
            print("No numerical data to plot.")

        # Plot categorical data
        if categorical_data:
            self._plot_data(
                data=categorical_data,
                title="Categorical Data",
                show_kde=False,
                combine_plots=combine_plots,
                standardize=False,
            )
        else:
            print("No categorical data to plot.")

    def _plot_data(self, data, title, show_kde, combine_plots, standardize=False):
        if combine_plots:
            plt.figure(figsize=self.figsize)
            for name, series in data:
                if standardize:
                    series = (series - series.mean()) / series.std()
                sns.histplot(series, kde=show_kde, label=name)
            plt.title(self.title + " - " + title)
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)
            plt.legend()
            plt.show()
        else:
            for name, series in data:
                plt.figure(figsize=self.figsize)
                if show_kde:
                    sns.histplot(series, kde=show_kde)
                else:
                    sns.countplot(x=series)
                plt.title(f"{self.title} - {name}")
                plt.xlabel(self.x_label)
                plt.ylabel(self.y_label)
                plt.show()
