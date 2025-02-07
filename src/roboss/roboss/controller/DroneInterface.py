from typing import List

from abc import ABC, abstractmethod


class DroneInterface(ABC):
    @abstractmethod
    def takeoff(self) -> None:
        """
        Issues a take-off command to the drone.
        """
        pass

    @abstractmethod
    def land(self) -> None:
        """
        Issues a landing command to the drone.
        """
        pass

    @abstractmethod
    def send_target(self, position: List[float]) -> None:
        """
        Sends a target position to the drone.
        :param position: The target position (x, y, z).
        :return:
        """
        pass

    @abstractmethod
    def get_range(self) -> float:
        """
        Returns the range sensor value.
        :return: The height.
        """
        pass

    @abstractmethod
    def get_position(self) -> List[float]:
        """
        Returns the position of the drone.
        :return: The current position (x, y, z).
        """
        pass

    @abstractmethod
    def get_time(self) -> float:
        """
        Returns the current timestamp in seconds.
        :return: Seconds.
        """
        pass
