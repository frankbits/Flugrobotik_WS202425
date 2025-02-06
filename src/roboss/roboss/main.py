from arena.Arena import Arena
from config import Config
from controller.DroneController import DroneController
from render.Renderer import draw_board
from route.RoutePlanner import RoutePlanner

if __name__ == "__main__":
    print("Running")

    arena = Arena(Config.Arena.PATH)
    draw_board(arena.get_mapped_arena())

    drone = DroneController()
    start_pos = drone.get_position()

    route = RoutePlanner(arena.segments, start_pos).find_route()
    print('route', route)

    print("Takeoff")
    drone.controller.takeoff()
    print("Sending target (1,1,1)")
    drone.move_to([1.0, 1.0, 1.0])
    print("Getting range and position")
    print(drone.controller.getRange(), drone.controller.get_position())
    print("Sending target (2,2,2)")
    drone.move_to([2, 2, 2])
    print("Landing")
    drone.controller.land()
