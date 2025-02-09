import rclpy
from .arena.Arena import Arena
from .config import Config
from .controller.DroneController import DroneController
from .controller.ROSDroneInterface import ROSDroneInterface
from .render.Renderer import Renderer
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

    rclpy.init()

    route = plan_route(arena, (0, 0))
    print('ROUTE', route)

    # animate route on board
    mappedArena = arena.get_mapped_arena()
    framesFile = Renderer.drawBoardToFile(mappedArena, "route", colors=Renderer.defaultColors, clear=True)
    for pos in route:
        mappedArena[pos[0]][pos[1]] = 'v'
        Renderer.drawBoardToFile(mappedArena, "route", colors=Renderer.defaultColors)
        mappedArena[pos[0]][pos[1]] = 'X'
    Renderer.animate_frames(framesFile)

    interface = ROSDroneInterface()
    drone = DroneController(interface)

    print("Takeoff")
    drone.controller.sleep(4)
    drone.controller.takeoff()
    drone.controller.sleep(4)
    print("Sending target (1,1,1)")
    drone.move_to([1.0, 1.0, 1.0])
    drone.controller.sleep(2)
    print("Getting range and position")
    print(drone.controller.get_range(), drone.controller.get_position())
    print("Sending target (2,2,2)")
    drone.move_to([2.0, 2.0, 2.0])
    drone.controller.sleep(2)
    print("Landing")
    drone.controller.land()
    drone.controller.sleep(4)
    
    try:
        while rclpy.ok():
            rclpy.spin_once(interface, timeout_sec=0)
        interface.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
