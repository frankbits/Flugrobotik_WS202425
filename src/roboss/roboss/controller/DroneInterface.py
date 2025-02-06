from abc import ABC, abstractmethod


class DroneInterface(ABC):
    @abstractmethod
    def takeoff(self):
        pass

    @abstractmethod
    def land(self):
        pass

    @abstractmethod
    def send_target(self, position) -> None:
        pass

    @abstractmethod
    def get_range(self) -> float:
        pass

    @abstractmethod
    def get_position(self) -> tuple[float, float, float]:
        pass

    @abstractmethod
    def get_time(self) -> float:
        pass
