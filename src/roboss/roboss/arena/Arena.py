import json
from dataclasses import dataclass
from typing import List

from ..config import Config


@dataclass
class Segment:
    pass


@dataclass
class Field(Segment):
    height: int = 0
    visited: bool = False


@dataclass
class Obstacle(Segment):
    pass


class Arena:
    size: int
    segments: List[List[Segment]] = []

    def __init__(self, src):
        # get arena-data from JSON-file
        parsed_data = json.load(open(src))

        # Mapping für das Fremdmodell
        self.size = parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SIZE_KEY]
        self.n_fields = 0
        for row in parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SEGMENTS_KEY]:
            row_segments = []
            for segment in row:
                if segment[Config.Arena.OBSTACLE_KEY]:
                    segment = Obstacle()
                else:
                    segment = Field()
                    self.n_fields += 1
                row_segments.append(segment)
            self.segments.append(row_segments)

    def get_obstacles(self) -> List[List[float]]:
        """
        Returns the cartesian coordinates of all the obstacles in the arena.

        :return: All obstacle coordinates
        """
        obstacles: List[List[float]] = []

        for row_index, row in enumerate(self.segments):
            for column_index, segment in enumerate(row):
                if isinstance(segment, Obstacle):
                    y: float = self.map_to_cartesian(row_index)
                    x: float = self.map_to_cartesian(column_index)
                    obstacles.append([x, y])

        return obstacles

    def get_mapped_arena(self) -> List[List[str]]:
        """
        Maps the current arena segments to their character representations.

        :return: The character representation of the arena.
        """
        return list(
            map(
                lambda x: list(
                    map(
                        lambda y: (
                            Config.Render.OBSTACLE
                            if isinstance(y, Obstacle)
                            else (Config.Render.ROUTE if y.visited else Config.Render.EMPTY)
                        ),
                        x,
                    )
                ),
                self.segments,
            )
        )

    def map_to_cartesian(self, index) -> float:
        """
        Maps the given segment index to real cartesian coordinate.

        :param index: The segment index
        :return: Cartesian coordinate
        """
        return -Config.Arena.SIZE + (
            index / float(self.size - 1) * (Config.Arena.SIZE * 2)
        )
