from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any
import matplotlib.pyplot as plt


class BasePlot(ABC):
    @abstractmethod
    def __init__(
        self,
        figsize: Tuple[int, int] = (10, 6),
        title: str = "Plot",
        x_label: str = "X-axis",
        y_label: str = "Y-axis",
    ) -> None:
        self.figsize = figsize
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
