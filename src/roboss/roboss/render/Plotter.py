from typing import Any, Iterable

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.image import AxesImage
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Plotter:
    def __init__(self, nrows: int = 1, ncols: int = 1):
        self.fig = plt.figure()
        self.nrows = nrows
        self.ncols = ncols
        self.sub_plot_index = 0

    def add_subplot(self, index: int = None, is3d: bool = False) -> Axes:
        """
        Add a subplot to the figure.

        :param index: The position of the subplot.
        :param is3d: True if the subplot should be a 3D plot, False otherwise.
        :return: The created subplot-Axes.
        """
        self.sub_plot_index += 1
        # index is sub_plot_index if index is None or < 1
        self.sub_plot_index = index if index is not None and index > 0 else self.sub_plot_index
        return self.fig.add_subplot(self.nrows, self.ncols, self.sub_plot_index, projection='3d' if is3d else None)

    def add_plot_range_3d(self, xx: np.ndarray[Any, np.dtype], yy: np.ndarray[Any, np.dtype],
                          zz: np.ndarray[Any, np.dtype], title: str = "3D-Höhenprofil") -> Poly3DCollection:
        """
        Add a 3D plot to the given axis-position.

        :param xx: The x values of the 3D data.
        :param yy: The y values of the 3D data.
        :param zz: The z values of the 3D data.
        :param title: The title of the plot.
        :return: Poly3DCollection object.
        """

        # Create a subplot.
        ax = self.add_subplot(None, is3d=True)

        # Set z-axis limits
        # ax.set_zlim(0, 1)

        # Set labels and title
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        # Create 3D plot
        return ax.plot_surface(xx, yy, zz, cmap='viridis', edgecolor='k')

    def add_plot_range_3d_bar(self, xx: np.ndarray[Any, np.dtype], yy: np.ndarray[Any, np.dtype], zz: np.ndarray[Any, np.dtype], title: str = "3D-Höhenprofil") -> Poly3DCollection:
        """
        Add a 3D bar plot to the given axis-position.

        :param xx: The x values of the 3D data.
        :param yy: The y values of the 3D data.
        :param zz: The z values of the 3D data.
        :param title: The title of the plot.
        :return: Poly3DCollection object.
        """

        # Create a subplot.
        ax = self.add_subplot(None, is3d=True)

        # Set z-axis limits
        # ax.set_zlim(0, 1)

        # Set labels and title
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        # Create 3D plot with different colors based on z-values.
        colors = plt.cm.get_cmap('viridis')(zz.flatten()/float(zz.max()))
        return ax.bar3d(xx, yy, 0, 1, 1, zz, shade=True, color=colors)

    def add_plot_range_2d(self, xx: np.ndarray[Any, np.dtype], yy: np.ndarray[Any, np.dtype], zz: np.ndarray[Any, np.dtype], title: str = "2D-Höhenprofil") -> AxesImage:
        """
        Add a 2D plot to the given axis.

        :param xx: The x values of the 2D data, defining the x-axis-range.
        :param yy: The y values of the 2D data, defining the y-axis-range.
        :param zz: The 2D data to plot.
        :param title: The title of the plot.
        :return: AxesImage object.
        """

        # Create a subplot.
        ax = self.add_subplot()

        # Set labels and title
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        # Create 2D plot
        extent = [np.min(xx), np.max(xx), np.min(yy), np.max(yy)]
        return ax.imshow(zz, cmap='viridis', origin='lower', extent=extent)

    def add_plot_range_scatter(self, positions: Iterable, ranges: Iterable,
                               title: str = "Scatter-2D-Höhenprofil") -> PathCollection:
        """
        Plots a scatter plot of positions with varying sizes and colors based on ranges.

        Args:
            :param positions: List of [x: float, y: float] positions.
            :param ranges: List of range values (float) corresponding to the positions.
            :param title: The title of the plot.

            :return: PathCollection object.
        """

        # Create a subplot.
        ax = self.add_subplot()
        ax.set_title(title)

        # Extract x and y positions and calculate sizes and colors for the scatter plot.
        x_positions = [row[0] for row in positions]
        y_positions = [row[1] for row in positions]
        sizes = list(map(lambda range1: range1 / 10, ranges))
        colors = list(map(lambda range1: range1 * 100, ranges))

        # Plot some data on the Axes.
        return ax.scatter(x_positions, y_positions, s=sizes, c=colors, cmap='viridis')

    def plot(self):
        # Show the figure
        plt.show()