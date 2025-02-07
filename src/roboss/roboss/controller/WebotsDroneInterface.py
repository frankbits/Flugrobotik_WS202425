from typing import List

from threading import Thread

from controller.DroneInterface import DroneInterface
from config import Config
from webots import Supervisor


class WebotsDroneInterface(DroneInterface, Supervisor):
    def __init__(self):
        super().__init__()
        print("WebotsDroneInterface started.")

        self.wb_node = super().getSelf().getParentNode()

        self.target_field = self.wb_node.getField(Config.Field.TARGET)
        self.position_field = self.wb_node.getField(Config.Field.TRANSLATION)
        self.range_finder = self.wb_node.getField(Config.Field.ZRANGE)

        thread = Thread(target=self.run)
        thread.start()

    def run(self):
        timestep = int(self.getBasicTimeStep())

        while self.step(timestep) != -1:
            # Triggering robot steps to keep the webots simulation running
            pass

    def takeoff(self) -> None:
        pos = self.get_position()
        self.target_field.setSFVec3f([pos[0], pos[1], 1.0])

    def land(self) -> None:
        pos = self.get_position()
        self.target_field.setSFVec3f([pos[0], pos[1], 0.0])

    def send_target(self, position) -> None:
        self.target_field.setSFVec3f(position)

    def get_range(self) -> float:
        return self.range_finder.getSFFloat()

    def get_position(self) -> List[float]:
        return self.position_field.getSFVec3f()

    def get_time(self) -> float:
        return self.getTime()
