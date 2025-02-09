import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import griddata

from .render.Plotter import Plotter


def interpolate(data):
    # Meshgrid für die Positionen der Daten erstellen
    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])
    xx, yy = np.meshgrid(x, y)

    # Nur die Positionen und Werte der gültigen Daten extrahieren
    valid_points = ~np.isnan(data)
    points = np.column_stack((xx[valid_points], yy[valid_points]))
    values = data[valid_points]

    # Zielkoordinaten für die Interpolation
    grid_x, grid_y = np.meshgrid(x, y)

    # Interpolation durchführen
    interpolated_data = griddata(points, values, (grid_x, grid_y), method='linear')

    # NaN-Werte außerhalb des Interpolationsbereichs auf 0 oder einen anderen Wert setzen
    return np.nan_to_num(interpolated_data)

def plot_range(area_len, positions, ranges, step_count=40):
    """
    Plots a 3D surface plot of positions with heights based on ranges.

    :param area_len: Length of a side of the area.
    :param positions: List of [x, y] positions.
    :param ranges: List of range values corresponding to the positions.
    :param step_count: Number of steps in the x and y direction.
    """
    ranges_count = len(ranges)

    factor = round(step_count / np.sqrt(ranges_count)) or 1

    # Create a grid of x and y values.
    xs = np.linspace(0, area_len, round(np.sqrt(ranges_count)) * factor + 1)
    ys = np.linspace(0, area_len, round(np.sqrt(ranges_count)) * factor + 1)
    X, Y = np.meshgrid(xs, ys)

    # Initialize Z values to NaN. (NaN-values will be interpolated)
    Z = np.full(X.shape, np.nan)

    # Initialize Z count values to zero.
    z_count = np.zeros(X.shape)

    # Populate Z values based on positions and ranges.
    for i, pos in enumerate(positions):
        x_index = int(pos[1] / area_len * np.sqrt(ranges_count) * factor)
        y_index = int(pos[0] / area_len * np.sqrt(ranges_count) * factor)

        # Add the range value to the Z value or set it to the range value if it is NaN.
        Z[x_index, y_index] = (0 if np.isnan(Z[x_index, y_index]) else Z[x_index, y_index]) + ranges[i] / 1000
        z_count[x_index, y_index] += 1

    # Calculate average Z values.
    # Z = np.divide(Z, z_count, out=Z, where=z_count != 0)
    np.divide(Z, z_count, out=Z, where=z_count != 0)
    # Z = np.true_divide(Z, z_count, where=z_count != 0)

    # print which values are NaN with 🟥 and 🟩
    # for row in np.array(Z):
    #     print('\u2009'.join(np.where(np.isnan(row), "🟥", "🟩")))

    # plot_range_2d(Z)
    zz_interpolated = interpolate(Z)

    # Create a plotter object with 1 row and 2 columns.
    # plotter = Plotter(2, 2)
    plotter = Plotter(1, 2)

    # Add 2D, 2D-Scatter and 3D plots
    # plotter.add_plot_range_3d(X, Y, Z)
    plotter.add_plot_range_3d(X, Y, zz_interpolated, "Interpoliertes 3D-Höhenprofil")

    # plotter.add_plot_range_2d(X, Y, Z)
    axes_image = plotter.add_plot_range_2d(X, Y, zz_interpolated, "Interpoliertes 2D-Höhenprofil")

    # plotter.add_plot_range_scatter(positions, ranges)

    # show colorbar
    plt.colorbar(axes_image)

    # Show the figure
    plt.show()