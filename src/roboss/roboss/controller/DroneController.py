from typing import Dict, Callable, Optional, List

import numpy as np

from . import DroneInterface
from ..config import Config


class DroneController:
    def __init__(self, interface):
        self.controller: DroneInterface = interface
        self.range_map: Dict[tuple[float], float] = {}

    def save_range(self, position: tuple[float], range: float) -> bool:
        """
        Saves the current range at the specified position, if it doesn't exist already.

        :param position: The position (x, y, z).
        :return: True if the position was saved, False otherwise.
        """
        if position in self.range_map:
            return False

        self.range_map[position] = position[2] * 1000 - range

        return True

    def move_to(self,
                target_pos: List[float],
                callback: Optional[Callable[[List[float]], None]] = None,
                callback_time: Optional[float] = 0.1) -> None:
        """
        Moves the drone to the specified position.

        Note: The callback function, if specified, will be called at least once when the position is reached.

        :param target_pos: The target position (x, y, z).
        :param callback: An optional callback function to be called during the movement.
        :param callback_time: The time interval between callback calls, defaults to 0.1.
        """
        self.controller.send_target(target_pos)
        last_time = self.controller.get_time()
        current_pos = self.controller.get_position()

        # Repeat while current position is not equal to target position by 0.1 absolute tolerance
        while not np.allclose(current_pos, target_pos, atol=Config.Drone.A_TOL):
            self.controller.sleep(0.1)
            current_time = self.controller.get_time()
            delta_time = current_time - last_time

            if callback is not None and callback_time is not None and delta_time >= callback_time:
                callback(current_pos)
                last_time = current_time
            
            current_pos = self.controller.get_position()

        if callback is not None:
            callback(current_pos)
