from DroneController import DroneController
from Arena import Arena
from Renderer import Renderer
from route.ShortestPathRoutePlanner import ShortestPathRoutePlanner
from route.SpiralRoutePlanner import SpiralRoutePlanner


def plan_route(arena: Arena, start_pos: tuple):
    routePlanner = ShortestPathRoutePlanner(arena, start_pos) # SpiralRoutePlanner(arena, start_pos)
    route = routePlanner.plan_route()
    return route

if __name__ == "__main__":
    print("Running")

    arena = Arena("../../../bin/arena.json")
    print(Renderer.drawBoard(arena.get_mapped_arena()))

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

    # drone = DroneController()
    # start_pos = drone.get_position()


    # print("Takeoff")
    # drone.droneInterface.takeoff()
    # print("Sending target (1,1,1)")
    # drone.move_to([1.0, 1.0, 1.0])
    # print("Getting range and position")
    # print(drone.droneInterface.getRange(), drone.droneInterface.get_position())
    # print("Sending target (2,2,2)")
    # drone.move_to([2,2,2])
    # print("Landing")
    # drone.droneInterface.land()