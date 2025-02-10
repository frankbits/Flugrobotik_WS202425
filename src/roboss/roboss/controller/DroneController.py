"""
Module: DroneController
Provides high-level control functionality for a drone using the DroneInterface.

This class serves as an abstraction for controlling a drone, handling movement
commands, range data storage, and optional callback execution during movement.
"""

from typing import Dict, Callable, Optional, List, Tuple

import numpy as np

from . import DroneInterface
from ..config import Config


class DroneController:
    """
    High-level controller for a drone using a DroneInterface implementation.

    This class provides movement commands, handles range data mapping, and allows
    optional callback functions to be executed during drone movement.

    Attributes:
        controller (DroneInterface): The drone interface used to send commands.
        range_map (Dict[Tuple[float, float, float], float]): Stores range sensor values mapped to specific positions.
    """

    def __init__(self, interface: DroneInterface) -> None:
        """
        Initializes the DroneController with a given drone interface.

        Parameters:
            interface (DroneInterface): The drone interface used for communication.
        """
        self.controller: DroneInterface = interface
        self.range_map: Dict[Tuple[float, float, float], float] = {}

    def save_range(self, position: Tuple[float, float, float], range_value: float) -> bool:
        """
        Saves the current range sensor value at a given position.

        The position must be unique in the range map; if it already exists, the function
        returns False without overwriting existing data.

        Parameters:
            position (Tuple[float, float, float]): The (x, y, z) coordinates where the range value is measured.
            range_value (float): The measured range value.

        Returns:
            bool: True if the position was saved, False if it already existed in the map.
        """
        if position in self.range_map:
            return False

        self.range_map[position] = position[2] * 1000 - range_value
        return True

    def move_to(self, target_pos: List[float], callback: Optional[Callable[[List[float]], None]] = None,
                callback_time: Optional[float] = 0.1) -> None:
        """
        Moves the drone to the specified target position.

        The drone moves towards the target while checking if the current position is within
        an absolute tolerance defined in the Config.Drone.A_TOL constant. If a callback is
        provided, it is executed at the specified time interval during movement.

        Parameters:
            target_pos (List[float]): The target position [x, y, z] the drone should move to.
            callback (Optional[Callable[[List[float]], None]]): A function to be called at
                intervals during movement. The function should accept a List[float] representing
                the drone's current position.
            callback_time (Optional[float]): The time interval (in seconds) between callback
                executions. Defaults to 0.1 seconds.
        """
        self.controller.send_target(target_pos)
        last_time = self.controller.get_time()
        current_pos = self.controller.get_position()

        # Repeat until the drone is within the absolute tolerance of the target position
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
