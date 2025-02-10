import rclpy
from .util import plot_range
from .arena.Arena import Arena, Obstacle
from .config import Config
from .controller.DroneController import DroneController
from .controller.ROSDroneInterface import ROSDroneInterface
from .render.Renderer import Renderer
from .route.F2CRoute import F2CRoute
from .render.Plotter import Plotter
from route.ShortestPathRoutePlanner import ShortestPathRoutePlanner
from route.SpiralRoutePlanner import SpiralRoutePlanner

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

def plan_route(arena: Arena, start_pos: tuple):
    routePlanner = ShortestPathRoutePlanner(arena, start_pos) # SpiralRoutePlanner(arena, start_pos)
    route = routePlanner.plan_route()
    return route

def main():
    print("Running")

    arena = Arena(Config.Arena.PATH)
    print(Renderer.drawBoard(arena.get_mapped_arena()))

    print("Calculating path")

    path = F2CRoute.getRoute(arena.get_obstacles())

    rclpy.init()
    
    #route = plan_route(arena, (0, 0))
    #print('ROUTE', route)

    # animate route on board
    #mappedArena = arena.get_mapped_arena()
    #framesFile = Renderer.drawBoardToFile(mappedArena, "route", colors=Renderer.defaultColors, clear=True)
    #for pos in route:
    #    mappedArena[pos[0]][pos[1]] = 'v'
    #    Renderer.drawBoardToFile(mappedArena, "route", colors=Renderer.defaultColors)
    #    mappedArena[pos[0]][pos[1]] = 'X'
    #Renderer.animate_frames(framesFile)

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
    # plot_heights(arena) # only showing obstacles with full height 
    # TODO: use plot_heights() with Plotter.add_plot_range_3d_bar() (bar3d) instead of add_plot_range_3d() (plot_surface)
    # TODO: better calculation of rangeValues: more measurePoints (ROSDroneInterface l62), are 10 interpolate-steps in plot_range() correct?
    plot_range(2, list(drone.range_map.keys()), list(drone.range_map.values()), 10)

    try:
        while rclpy.ok():
            rclpy.spin_once(interface, timeout_sec=0)
        interface.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
