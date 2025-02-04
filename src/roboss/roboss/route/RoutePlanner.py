from abc import ABC, abstractmethod


class RoutePlanner(ABC):
    @abstractmethod
    def plan_route(self):
        pass