import time
from threading import Thread

from DroneController import DroneController
from Arena import Arena
from Renderer import drawBoard
from RoutePlanner import RoutePlanner


class Crazyflie:
    def __init__(self):
        arena = Arena("../../../bin/arena.json")
        drone = DroneController(run)
        start_pos = drone.get_position()
        route = RoutePlanner(arena.segments, start_pos).find_route()
        print('route', route)

        drawBoard(arena.get_mapped_arena())

        self.cf = drone

        self.cf.droneInterface.takeoff()
        self.cf.move_to([1, 0, 1], self.cf.save_positions, 1)

if __name__ == "__main__":
    cf = Crazyflie()

def run(self):
    print("Running")
    # self.cf.droneInterface.takeoff()
    # print("Takeoff")
    self.send_target([1.0,1.0, 1.0])
    # print(self.cf.droneInterface.getRange(), self.cf.droneInterface.get_position())
    # for i in range(3):
    #     print(self.cf.droneInterface.getRange(), self.cf.droneInterface.get_position())
    #     time.sleep(1)
    time.sleep(10)
    # self.cf.droneInterface.send_target([0,0,0])