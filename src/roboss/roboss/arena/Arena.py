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
    robots: List

    def __init__(self, src):
        # get arena-data from JSON-file
        parsed_data = json.load(open(src))
        # Map JSON data
        self.size = parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SIZE_KEY]

        for row in parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SEGMENTS_KEY]:
            row_segments = []

            for segment in row:
                if segment[Config.Arena.OBSTACLE_KEY]:
                    segment = Obstacle()
                else:
                    segment = Field()
                row_segments.append(segment)

            self.segments.append(row_segments)

    def get_mapped_arena(self):
        return list(
            map(
                lambda x:
                list(
                    map(lambda y: Config.Render.OBSTACLE if isinstance(y, Obstacle) else Config.Render.EMPTY, x)
                ),
                self.segments
            )
        )
