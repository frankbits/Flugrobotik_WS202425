from abc import ABC, abstractmethod
from typing import Any


class RoutePlanner(ABC):
    """
    Abstract base class for planning routes.

    This class serves as a blueprint for creating specific route planning
    implementations. It ensures that any subclass provides an implementation
    for the `plan_route` method.

    Methods:
        plan_route() -> Any
            This method should be overridden by subclasses to implement specific
            route planning logic.
    """

    @abstractmethod
    def plan_route(self) -> Any:
        """
        Plan a route based on the specific logic implemented in the subclass.

        This is an abstract method and must be implemented by subclasses.

        Returns
        -------
        Any
            The planned route, which can vary depending on the implementation.
        """
        pass
