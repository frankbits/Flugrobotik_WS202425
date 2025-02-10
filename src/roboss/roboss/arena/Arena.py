"""
Module: Arena
This module defines data structures to represent an arena divided into segments,
where each segment is either a Field or an Obstacle. It also provides functionality
to load arena data from a JSON file and to compute mappings of obstacles and renderable
representations of the arena.
"""

import json
from dataclasses import dataclass
from typing import List

from ..config import Config


@dataclass
class Segment:
    """
    Abstract base class for segments in the arena.
    This class is extended by specific segment types such as Field and Obstacle.
    """
    pass


@dataclass
class Field(Segment):
    """
    Represents a field segment in the arena.

    Attributes:
        height (int): The height of the field segment.
        visited (bool): Flag indicating if the segment has been visited.
    """
    height: int = 0
    visited: bool = False


@dataclass
class Obstacle(Segment):
    """
    Represents an obstacle segment in the arena.
    """
    pass


class Arena:
    """
    Represents the arena for the drone, composed of a grid of segments.

    Attributes:
        size (int): The number of segments along one dimension of the arena.
        segments (List[List[Segment]]): A 2D list representing the arena grid, where each
            element is either a Field or an Obstacle.
        n_fields (int): The total number of field segments in the arena.
    """
    size: int
    segments: List[List[Segment]]
    n_fields: int

    def __init__(self, src: str) -> None:
        """
        Initializes the arena by loading data from a JSON file.

        The JSON file is expected to have a structure defined by the Config module,
        containing keys for the arena size and segments. Each segment is determined
        to be an Obstacle or a Field based on the value of Config.Arena.OBSTACLE_KEY.

        Parameters:
            src (str): The path to the JSON file containing arena data.
        """
        # Load arena data from JSON file
        with open(src, 'r') as f:
            parsed_data = json.load(f)

        # Retrieve arena size from the parsed data
        self.size = parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SIZE_KEY]
        self.n_fields = 0
        self.segments = []  # Initialize segments as an empty list

        # Build the arena grid from the segments data in the JSON file.
        for row in parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SEGMENTS_KEY]:
            row_segments: List[Segment] = []
            for segment in row:
                if segment[Config.Arena.OBSTACLE_KEY]:
                    seg_obj: Segment = Obstacle()
                else:
                    seg_obj = Field()
                    self.n_fields += 1
                row_segments.append(seg_obj)
            self.segments.append(row_segments)

    def get_obstacles(self) -> List[List[float]]:
        """
        Returns the Cartesian coordinates of all obstacles in the arena.

        Each obstacle is represented by its [x, y] coordinate, which is computed from
        the segment's row and column indices using the map_to_cartesian method.

        Returns:
            List[List[float]]: A list of coordinates for obstacles.
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
        Maps the arena segments to their corresponding character representations.

        For each segment:
          - If it is an Obstacle, it is mapped to the character defined by Config.Render.OBSTACLE.
          - If it is a Field, it is mapped to Config.Render.EMPTY_VISITED if visited is True;
            otherwise, it is mapped to Config.Render.EMPTY.

        Returns:
            List[List[str]]: A 2D list containing the character representation of the arena.
        """
        mapped_arena = [[Config.Render.OBSTACLE if isinstance(seg, Obstacle) else (
            Config.Render.ROUTE if seg.visited else Config.Render.EMPTY) for seg in row] for row in
            self.segments]
        return mapped_arena

    def map_to_cartesian(self, index: int) -> float:
        """
        Converts a segment index to a Cartesian coordinate.

        The conversion maps the index in the arena grid to a real-world coordinate,
        based on the arena size defined in Config.Arena.SIZE. The coordinate system is
        assumed to be centered at zero.

        Parameters:
            index (int): The segment index (row or column index).

        Returns:
            float: The corresponding Cartesian coordinate.
        """
        # The formula maps index [0, size-1] to [-SIZE, SIZE]
        return -Config.Arena.SIZE + (index / float(self.size - 1) * (Config.Arena.SIZE * 2))
