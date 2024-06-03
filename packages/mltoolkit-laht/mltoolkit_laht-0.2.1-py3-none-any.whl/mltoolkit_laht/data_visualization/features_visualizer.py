from .base_visualizer import BaseVisualizer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Union, List


class FeaturesVisualizer(BaseVisualizer):
    def __init__(
        self,
        figsize: Tuple[int, int] = (10, 6),
        title: str = "Plot",
        x_label: str = "X-axis",
        y_label: str = "Y-axis",
    ) -> None:
        super().__init__(figsize, title, x_label, y_label)

    def plot_features(
        self,
        data: Union[pd.DataFrame, pd.Series],
        show_kde: bool = True,
        combine_plots: bool = False,
        standardize: bool = False,
        rotate_xticks: int = 0,
        extend_numerical_plots: bool = False,
        features_to_combine: List[str] = None,
    ) -> None:
        if isinstance(data, pd.Series):
            features = [(data.name, data)]
        elif isinstance(data, pd.DataFrame):
            features = [(name, series) for name, series in data.items()]
        else:
            msg = "Unsupported data type. Only support pandas Series or DataFrame."
            self.logger.error(msg)
            raise ValueError(msg)

        numerical_features = [
            (name, series)
            for name, series in features
            if pd.api.types.is_numeric_dtype(series)
        ]
        categorical_features = [
            (name, series)
            for name, series in features
            if pd.api.types.is_categorical_dtype(series)
        ]

        # Plot numerical data
        if numerical_features:
            self._plot_features(
                data=numerical_features,
                show_kde=show_kde,
                combine_plots=combine_plots,
                standardize=standardize,
                extend_plots=extend_numerical_plots,
                features_to_combine=features_to_combine,
                plot_type="Numerical",
            )
        else:
            self.logger.info("No numerical data to plot.")

        # Plot categorical data
        if categorical_features:
            self._plot_features(
                data=categorical_features,
                combine_plots=combine_plots,
                rotate_xticks=rotate_xticks,
                features_to_combine=features_to_combine,
                plot_type="Categorical",
            )
        else:
            self.logger.info("No categorical data to plot.")

    def _plot_features(
        self,
        data,
        combine_plots,
        features_to_combine,
        plot_type,
        show_kde=None,
        standardize=None,
        extend_plots=None,
        rotate_xticks=None,
    ):
        if combine_plots:
            if not features_to_combine:
                msg = "A list of features to combine must be provided."
                self.logger.error(msg)
                raise ValueError(msg)
            plt.figure(figsize=self.figsize)
            for name, series in data:
                if name in features_to_combine:
                    if standardize:
                        series = (series - series.mean()) / series.std()
                    if plot_type == "Numerical":
                        sns.histplot(series, kde=show_kde, label=name, multiple="stack")
                    else:
                        sns.countplot(x=series, label=name)
            plt.title(self.title + f" - {plot_type} Data")
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)
            if plot_type == "Categorical":
                plt.xticks(rotation=rotate_xticks)
            plt.legend()
            plt.show()
        else:
            for name, series in data:
                plt.figure(figsize=self.figsize)
                if plot_type == "Numerical":
                    if extend_plots:
                        fig, axes = plt.subplots(1, 3, figsize=self.figsize)
                        sns.histplot(series, kde=show_kde, ax=axes[0])
                        sns.boxplot(x=series, ax=axes[1])
                        sns.violinplot(x=series, ax=axes[2])
                    else:
                        sns.histplot(series, kde=show_kde)
                else:
                    sns.countplot(x=series, dodge=False)
                    plt.xticks(rotation=rotate_xticks)
                plt.title(f"{self.title} - {name}")
                plt.xlabel(self.x_label)
                plt.ylabel(self.y_label)
                plt.show()
