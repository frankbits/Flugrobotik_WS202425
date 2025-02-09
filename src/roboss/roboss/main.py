import rclpy
from .arena.Arena import Arena
from .config import Config
from .controller.DroneController import DroneController
from .controller.ROSDroneInterface import ROSDroneInterface
from .render.Renderer import Renderer
from .route.F2CRoute import F2CRoute
from route.ShortestPathRoutePlanner import ShortestPathRoutePlanner
from route.SpiralRoutePlanner import SpiralRoutePlanner


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

    for state in path.getStates():
        drone.move_to([state.point.X(), state.point.Y(), 1.0])

    print("Resetting and landing")

    drone.move_to([0.0, 0.0, 0.0])
    drone.controller.land()
    drone.controller.sleep(4)

    print("Finished")

    try:
        while rclpy.ok():
            rclpy.spin_once(interface, timeout_sec=0)
        interface.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
