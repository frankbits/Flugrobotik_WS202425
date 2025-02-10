"""
Module: DroneInterface
Defines an abstract interface for drone operations.

This interface enforces a contract for drone control implementations,
ensuring that any concrete drone class provides implementations for
basic operations such as takeoff, landing, movement, and telemetry retrieval.
"""

from abc import ABC, abstractmethod
from typing import List


class DroneInterface(ABC):
    """
    Abstract Base Class (ABC) for drone control.

    This interface defines essential drone operations that must be implemented
    by any concrete drone class. These methods enable basic flight control,
    movement commands, and telemetry access.
    """

    @abstractmethod
    def takeoff(self) -> None:
        """
        Commands the drone to take off.

        This method should implement the necessary logic to initiate a safe
        takeoff sequence, ensuring that the drone achieves a stable hover.
        """
        pass

    @abstractmethod
    def land(self) -> None:
        """
        Commands the drone to land.

        This method should implement a controlled descent and landing procedure.
        """
        pass

    @abstractmethod
    def send_target(self, position: List[float]) -> None:
        """
        Sends a target position (x, y, z) for the drone to navigate to.

        The implementation should ensure smooth movement toward the target.

        Parameters:
            position (List[float]): The target position as [x, y, z] coordinates.
        """
        pass

    @abstractmethod
    def get_range(self) -> float:
        """
        Retrieves the current range sensor value.

        Typically used to determine altitude or detect obstacles.

        Returns:
            float: The current height or range sensor measurement.
        """
        pass

    @abstractmethod
    def get_position(self) -> List[float]:
        """
        Retrieves the drone's current position.

        Returns:
            List[float]: The current position of the drone as [x, y, z].
        """
        pass

    @abstractmethod
    def get_time(self) -> float:
        """
        Retrieves the current system time or flight time.

        Returns:
            float: The current timestamp in seconds.
        """
        pass

    @abstractmethod
    def sleep(self, duration: float) -> None:
        """
        Pauses execution for a specified duration.

        This method allows controlled timing for flight operations.

        Parameters:
            duration (float): The duration to sleep, in seconds.
        """
        pass
