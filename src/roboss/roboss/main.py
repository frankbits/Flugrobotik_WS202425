import rclpy
from .util import plot_range
from .arena.Arena import Arena, Obstacle
from .config import Config
from .controller.DroneController import DroneController
from .controller.ROSDroneInterface import ROSDroneInterface
from .render.Renderer import draw_board
from .route.F2CRoute import F2CRoute
from .render.Plotter import Plotter

def plot_heights(arena: Arena):
    import matplotlib.pyplot as plt
    import numpy as np

    plotter = Plotter()

    # Create a grid of x and y values.
    xs = np.linspace(0, arena.size, arena.size)
    ys = np.linspace(0, arena.size, arena.size)
    X, Y = np.meshgrid(xs, ys)
    x, y = X.ravel(), Y.ravel()

    # Initialize Z values to NaN. (NaN-values will be interpolated)
    Z = np.full(X.shape, np.nan)

    # Populate Z values with max-height for obstacles and 0 for fields.
    for i in range(arena.size):
        for j in range(arena.size):
            if isinstance(arena.segments[i][j], Obstacle):
                Z[i][j] = 10
            else:
                Z[i][j] = arena.segments[i][j].height

    z = Z.ravel()

    axes_image = plotter.add_plot_range_3d_bar(x, y, z, "3D-Höhenprofil")

    # show colorbar
    plt.colorbar(axes_image)

    # Show the figure
    plotter.plot()

def main():
    print("Running")

    arena = Arena(Config.Arena.PATH)
    draw_board(arena.get_mapped_arena())

    print("Calculating path")

    path = F2CRoute.test()

    rclpy.init()

    interface = ROSDroneInterface()
    drone = DroneController(interface)

    print("Takeoff")

    drone.controller.takeoff()
    drone.controller.sleep(4)

    print("Flying path")

    drone.controller.set_range_callback(lambda x: drone.save_range(drone.controller.get_position(), x[0]))

    for state in path.getStates():
        drone.move_to([state.point.X(), state.point.Y(), 1.0], lambda pos: drone.controller.get_range())

    drone.controller.stop_range_callback()

    print("Resetting and landing")

    drone.move_to([0.0, 0.0, 0.0])
    drone.controller.land()
    drone.controller.sleep(4)

    print("Finished")

    print("Plotting Ranges")
    
    print(drone.range_map)
    plot_heights(arena)
    plot_range(2, list(drone.range_map.keys()), list(drone.range_map.values()))

    try:
        while rclpy.ok():
            rclpy.spin_once(interface, timeout_sec=0)
        interface.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
