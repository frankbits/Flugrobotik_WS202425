"""
Module: Plotter
Provides utilities for creating 2D and 3D plots using Matplotlib.

This class abstracts common plotting operations, including:
- 3D surface plots
- 3D bar plots
- 2D heatmaps
- Scatter plots

It allows users to dynamically add subplots and visualize data in an intuitive way.
"""

from typing import Iterable

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.image import AxesImage
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Plotter:
    """
    A helper class for creating 2D and 3D plots using Matplotlib.

    Attributes:
        fig (plt.Figure): The Matplotlib figure.
        nrows (int): Number of rows in the subplot grid.
        ncols (int): Number of columns in the subplot grid.
        sub_plot_index (int): Keeps track of the subplot position.
    """

    def __init__(self, nrows: int = 1, ncols: int = 1) -> None:
        """
        Initializes the Plotter with a given number of subplots.

        Parameters:
            nrows (int): Number of rows in the subplot grid.
            ncols (int): Number of columns in the subplot grid.
        """
        self.fig = plt.figure()
        self.nrows = nrows
        self.ncols = ncols
        self.sub_plot_index = 0

    def add_subplot(self, index: int = None, is3d: bool = False) -> Axes:
        """
        Adds a subplot to the figure.

        Parameters:
            index (int, optional): The position of the subplot. If None, it auto-increments.
            is3d (bool): True to create a 3D plot, False for a 2D plot.

        Returns:
            Axes: The created subplot Axes object.
        """
        self.sub_plot_index += 1
        self.sub_plot_index = index if index is not None and index > 0 else self.sub_plot_index
        return self.fig.add_subplot(self.nrows, self.ncols, self.sub_plot_index, projection='3d' if is3d else None)

    def add_plot_range_3d(self, xx: np.ndarray, yy: np.ndarray, zz: np.ndarray,
                          title: str = "3D-Höhenprofil") -> Poly3DCollection:
        """
        Adds a 3D surface plot.

        Parameters:
            xx (np.ndarray): The x values of the 3D data.
            yy (np.ndarray): The y values of the 3D data.
            zz (np.ndarray): The z values of the 3D data.
            title (str): The title of the plot.

        Returns:
            Poly3DCollection: The plotted surface.
        """
        ax = self.add_subplot(None, is3d=True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)
        return ax.plot_surface(xx, yy, zz, cmap='viridis', edgecolor='k')

    def add_plot_range_3d_bar(self, xx: np.ndarray, yy: np.ndarray, zz: np.ndarray,
                              title: str = "3D-Höhenprofil") -> Poly3DCollection:
        """
        Adds a 3D bar plot.

        Parameters:
            xx (np.ndarray): The x values of the 3D data.
            yy (np.ndarray): The y values of the 3D data.
            zz (np.ndarray): The z values of the 3D data.
            title (str): The title of the plot.

        Returns:
            Poly3DCollection: The plotted bars.
        """
        ax = self.add_subplot(None, is3d=True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        colors = plt.cm.get_cmap('viridis')(zz.flatten() / float(zz.max()))
        return ax.bar3d(xx, yy, 0, 1, 1, zz, shade=True, color=colors)

    def add_plot_range_2d(self, xx: np.ndarray, yy: np.ndarray, zz: np.ndarray,
                          title: str = "2D-Höhenprofil") -> AxesImage:
        """
        Adds a 2D heatmap plot.

        Parameters:
            xx (np.ndarray): The x values defining the x-axis range.
            yy (np.ndarray): The y values defining the y-axis range.
            zz (np.ndarray): The 2D data to plot.
            title (str): The title of the plot.

        Returns:
            AxesImage: The plotted heatmap.
        """
        ax = self.add_subplot()
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        extent = [np.min(xx), np.max(xx), np.min(yy), np.max(yy)]
        return ax.imshow(zz, cmap='viridis', origin='lower', extent=extent)

    def plot(self) -> None:
        """
        Displays the figure with all added subplots.
        """
        plt.show()
