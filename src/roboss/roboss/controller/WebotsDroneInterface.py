"""
Module: WebotsDroneInterface
Provides an implementation of the DroneInterface using Webots.

This class acts as a bridge between the Webots simulation environment and the drone
control system. It extends both DroneInterface (for drone command structure) and
Supervisor (to interact with Webots' simulation framework).

The interface supports takeoff, landing, target movement, retrieving telemetry data,
and running the Webots simulation loop in a separate thread.
"""

import time
from threading import Thread
from typing import List

from .DroneInterface import DroneInterface
from ..config import Config
from ..webots import Supervisor


class WebotsDroneInterface(DroneInterface, Supervisor):
    """
    Webots-based implementation of the DroneInterface.

    This class provides an interface for controlling a simulated drone inside Webots.
    It manages communication with the Webots simulation environment through fields
    that define the drone's position, target position, and range sensor values.

    Attributes:
        wb_node: The Webots node representing the drone in the simulation.
        target_field: Webots field representing the drone's movement target.
        position_field: Webots field storing the drone's current position.
        range_finder: Webots field representing the altitude/range sensor.
    """

    def __init__(self) -> None:
        """
        Initializes the Webots drone interface.

        - Retrieves the drone's Webots node.
        - Initializes fields for position, target movement, and range sensing.
        - Starts a background thread to keep the Webots simulation running.
        """
        super().__init__()
        print("WebotsDroneInterface started.")

        self.wb_node = super().getSelf().getParentNode()

        self.target_field = self.wb_node.getField(Config.Field.TARGET)
        self.position_field = self.wb_node.getField(Config.Field.TRANSLATION)
        self.range_finder = self.wb_node.getField(Config.Field.ZRANGE)

        thread = Thread(target=self.run, daemon=True)
        thread.start()

    def run(self) -> None:
        """
        Runs the Webots simulation loop in a separate thread.

        This ensures that Webots continues to update its simulation state.
        """
        timestep = int(self.getBasicTimeStep())

        while self.step(timestep) != -1:
            # Triggering robot steps to keep the Webots simulation running
            pass

    def takeoff(self) -> None:
        """
        Commands the drone to take off by setting its target position to an altitude of 1.0 meters.
        """
        pos = self.get_position()
        self.target_field.setSFVec3f([pos[0], pos[1], 1.0])

    def land(self) -> None:
        """
        Commands the drone to land by setting its target position to an altitude of 0.0 meters.
        """
        pos = self.get_position()
        self.target_field.setSFVec3f([pos[0], pos[1], 0.0])

    def send_target(self, position: List[float]) -> None:
        """
        Sends a target position (x, y, z) to the drone.

        Parameters:
            position (List[float]): The target position as [x, y, z].
        """
        self.target_field.setSFVec3f(position)

    def get_range(self) -> float:
        """
        Retrieves the current range sensor value.

        Returns:
            float: The altitude measurement from the range finder sensor.
        """
        return self.range_finder.getSFFloat()

    def get_position(self) -> List[float]:
        """
        Retrieves the drone's current position from the Webots simulation.

        Returns:
            List[float]: The drone's current position as [x, y, z].
        """
        return self.position_field.getSFVec3f()

    def get_time(self) -> float:
        """
        Retrieves the current simulation time in Webots.

        Returns:
            float: The simulation time in seconds.
        """
        return self.getTime()

    def sleep(self, duration: float) -> None:
        """
        Sleeps for the specified duration in seconds.

        Uses Python's `time.sleep()` to pause execution while the Webots simulation continues.

        Parameters:
            duration (float): The duration in seconds.
        """
        time.sleep(duration)
