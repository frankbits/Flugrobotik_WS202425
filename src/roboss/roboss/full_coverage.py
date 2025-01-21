from DroneController import DroneController
from Arena import Arena
from Renderer import drawBoard
from RoutePlanner import RoutePlanner

if __name__ == "__main__":
    print("Running")

    arena = Arena("../../../bin/arena.json")
    drawBoard(arena.get_mapped_arena())

    drone = DroneController()
    start_pos = drone.get_position()

    route = RoutePlanner(arena.segments, start_pos).find_route()
    print('route', route)

    print("Takeoff")
    drone.droneInterface.takeoff()
    print("Sending target (1,1,1)")
    drone.move_to([1.0, 1.0, 1.0])
    print("Getting range and position")
    print(drone.droneInterface.getRange(), drone.droneInterface.get_position())
    print("Sending target (2,2,2)")
    drone.move_to([2,2,2])
    print("Landing")
    drone.droneInterface.land()