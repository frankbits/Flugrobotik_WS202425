from DroneInterface import DroneInterface
from crazyflie_extern import CrazyflieExternController


class SimDroneInterface(DroneInterface, CrazyflieExternController):
    def __init__(self):
        super().__init__()
        print("SimDroneInterface started.")

    def takeoff(self) -> None:
        pos = self.get_position()
        self.setTarget([pos[0], pos[1], 1.0])

    def land(self) -> None:
        pos = self.get_position()
        self.setTarget([pos[0], pos[1], 0.0])

    def send_target(self, position) -> None:
        self.setTarget(position)

    def get_range(self) -> float:
        return self.getRange()

    def get_position(self) -> list[float]:
        return self.getPosition()

    def get_time(self) -> float:
        return self.getTime()