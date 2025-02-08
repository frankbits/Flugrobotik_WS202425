from arena.Arena import Arena
from config import Config
from controller.DroneController import DroneController
from controller.WebotsDroneInterface import WebotsDroneInterface
from render.Renderer import draw_board
from route.RoutePlanner import RoutePlanner

def main():
    print("Running")

    arena = Arena(Config.Arena.PATH)
    draw_board(arena.get_mapped_arena())
    
    interface = WebotsDroneInterface()
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

if __name__ == "__main__":
    main()